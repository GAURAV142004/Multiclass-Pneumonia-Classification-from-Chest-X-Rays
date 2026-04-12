"""
Inference API Endpoint
Handles complete two-stage pneumonia detection pipeline:
1. Lung segmentation
2. Stage-1: Normal vs Pneumonia classification
3. Stage-2: Viral vs Bacterial classification (if pneumonia detected)
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from datetime import datetime
import logging
import numpy as np
import cv2

from ..services.preprocessing import preprocessor
from ..services.segmentation_service import segmentation_service
from ..services.stage1_classifier import stage1_classifier
from ..services.stage2_classifier import stage2_classifier
from ..utils.image_utils import numpy_to_base64
from ..utils.response_formatter import prediction_response, success_response, error_response
from ..core.security import get_current_user
from ..core.config import settings
from ..db.mongodb import get_database

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/inference", tags=["Inference"])


@router.post("/predict")
async def predict_pneumonia(
    file: UploadFile = File(...),
    run_stage2: bool = False,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Two-stage pneumonia detection pipeline with optional stage-2 execution
    
    Pipeline:
    1. Validate and preprocess uploaded X-ray image
    2. Perform lung segmentation using U-Net
    3. Stage-1 classification: Normal vs Pneumonia
    4. If Pneumonia detected and run_stage2=True → Stage-2: Viral vs Bacterial
    5. Return results with images and confidence scores
    
    Args:
        run_stage2: If True, automatically run stage-2 when pneumonia detected
        file: Uploaded chest X-ray image
        current_user: Authenticated user from JWT
        db: Database connection
        
    Returns:
        Prediction results with images and disclaimer
    """
    try:
        logger.info(f"Starting inference for user: {current_user['email']}")
        
        # ============= STEP 1: Validate and Load Image =============
        file_data = await file.read()
        
        # Validate image
        is_valid, error_msg = preprocessor.validate_image(file_data, file.filename)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        # Load image
        original_image_rgb = preprocessor.load_image_from_bytes(file_data)
        logger.info(f"Image loaded: {original_image_rgb.shape}")
        
        
        # ============= STEP 2: Preprocess for Models =============
        # Preprocess for segmentation (256x256 grayscale)
        preprocessed_seg = preprocessor.preprocess_for_segmentation(original_image_rgb)
        
        # Preprocess for classification (224x224 grayscale)
        preprocessed_cls = preprocessor.preprocess_for_classification(original_image_rgb)
        logger.info("Image preprocessed for models")
        
        
        # ============= STEP 3: Lung Segmentation =============
        logger.info("Running lung segmentation...")
        segmentation_mask = segmentation_service.predict(preprocessed_seg)
        
        # Postprocess mask
        cleaned_mask = preprocessor.postprocess_segmentation_mask(segmentation_mask)
        logger.info("Segmentation complete")
        
        # Apply mask to extract segmented lung region (256x256)
        segmented_lung_256 = preprocessed_seg * cleaned_mask
        
        # Resize segmented lung to 224x224 for classification
        segmented_lung_224 = cv2.resize(segmented_lung_256[:, :, 0], (224, 224), interpolation=cv2.INTER_AREA)
        segmented_lung_224 = np.expand_dims(segmented_lung_224, axis=-1)

        # Build Stage-2 segmented input using training-aligned pipeline.
        # This mirrors the notebook that generated segmented_extended_dataset:
        # threshold -> close/open (7x7, iterations 2/1) -> resize mask back to original
        # -> bitwise_and on original grayscale -> resize to 224 -> normalize [0,1].
        original_gray = cv2.cvtColor(original_image_rgb, cv2.COLOR_RGB2GRAY)
        stage2_mask = (segmentation_mask[:, :, 0] > 0.5).astype(np.uint8) * 255
        stage2_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        stage2_mask = cv2.morphologyEx(stage2_mask, cv2.MORPH_CLOSE, stage2_kernel, iterations=2)
        stage2_mask = cv2.morphologyEx(stage2_mask, cv2.MORPH_OPEN, stage2_kernel, iterations=1)
        stage2_mask = cv2.resize(
            stage2_mask,
            (original_gray.shape[1], original_gray.shape[0]),
            interpolation=cv2.INTER_LINEAR
        )
        segmented_fullres_for_stage2 = cv2.bitwise_and(original_gray, original_gray, mask=stage2_mask)
        segmented_stage2_224 = cv2.resize(
            segmented_fullres_for_stage2, (224, 224), interpolation=cv2.INTER_AREA
        ).astype(np.float32) / 255.0
        segmented_stage2_224 = np.expand_dims(segmented_stage2_224, axis=-1)
        
        
        # ============= STEP 4: Stage-1 Classification =============
        logger.info("Running Stage-1 classification (Normal vs Pneumonia)...")
        # Use SEGMENTED lung region, not raw X-ray
        stage1_result = stage1_classifier.predict(segmented_lung_224)
        
        logger.info(f"Stage-1 result: {stage1_result['predicted_class']} "
                   f"(confidence: {stage1_result['confidence']:.2%})")
        
        
       # ============= STEP 5: Stage-2 Classification (conditional) =============
        final_prediction = {
            "label": stage1_result["predicted_class"],
            "confidence": stage1_result["confidence"],
            "stage": 1,
            "normal_probability": 1 - stage1_result["pneumonia_probability"],
            "pneumonia_probability": stage1_result["pneumonia_probability"],
            "pending_stage2": False
        }
        
        if stage1_result["has_pneumonia"]:
            if run_stage2:
                logger.info("Pneumonia detected. Running Stage-2 classification...")
                
                # Stage-2: Viral vs Bacterial
                # Input 1: Original X-ray (224x224) - full context
                # Input 2: Segmented lung region (224x224) - focused lungs
                stage2_result = stage2_classifier.predict(preprocessed_cls, segmented_stage2_224)
                
                logger.info(f"Stage-2 result: {stage2_result['predicted_class']} "
                           f"(confidence: {stage2_result['confidence']:.2%})")
                
                # Update final prediction
                final_prediction = {
                    "label": stage2_result["predicted_class"],
                    "confidence": stage2_result["confidence"],
                    "stage": 2,
                    "viral_probability": stage2_result["viral_probability"],
                    "bacterial_probability": stage2_result["bacterial_probability"],
                    "pending_stage2": False
                }
            else:
                # Pneumonia detected but stage-2 not requested
                logger.info("Pneumonia detected. Awaiting user confirmation for Stage-2...")
                final_prediction["pending_stage2"] = True
        
        
        # ============= STEP 6: Prepare Response Images =============
        # Convert images to base64
        # Show original preprocessed image
        original_base64 = numpy_to_base64(preprocessed_seg)
        # Show SEGMENTED LUNG REGION (not just mask)
        segmented_base64 = numpy_to_base64(segmented_lung_256)
        
        
        # ============= STEP 7: Save to History (Optional) =============
        try:
            history_record = {
                "user_id": current_user["user_id"],
                "prediction_label": final_prediction["label"],
                "confidence": final_prediction["confidence"],
                "stage": final_prediction["stage"],
                "created_at": datetime.utcnow()
            }
            await db.scan_history.insert_one(history_record)
            logger.info("Scan saved to history")
        except Exception as e:
            logger.warning(f"Failed to save scan history: {str(e)}")
        
        
        response = prediction_response(
            prediction_label=final_prediction["label"],
            confidence=final_prediction["confidence"],
            original_image=original_base64,
            segmented_image=segmented_base64,
            additional_data={
                "stage": final_prediction["stage"],
                **{k: v for k, v in final_prediction.items() if k not in ["label", "confidence", "stage"]}
            }
        )
        
        logger.info(f"Inference complete: {final_prediction['label']}")
        
        return success_response(response, "Prediction completed successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Inference error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/models/status")
async def get_models_status(current_user: dict = Depends(get_current_user)):
    """
    Get status of all loaded models
    
    Args:
        current_user: Authenticated user from JWT
        
    Returns:
        Status information for all models
    """
    try:
        return success_response({
            "segmentation": segmentation_service.get_model_info(),
            "stage1_classifier": stage1_classifier.get_model_info(),
            "stage2_classifier": stage2_classifier.get_model_info()
        }, "Models status retrieved")
        
    except Exception as e:
        logger.error(f"Error getting model status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get model status"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint (no authentication required)
    
    Returns:
        API health status
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }
