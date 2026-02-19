"""
Stage-2 Dual-Input Classifier Service
Classifies pneumonia as Viral vs Bacterial using original + segmented images
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
import logging
from pathlib import Path
from ..core.config import settings

logger = logging.getLogger(__name__)


class Stage2ClassifierService:
    """Dual-input classifier: Viral vs Bacterial Pneumonia"""
    
    def __init__(self):
        self.model = None
        self.class_names = ["Bacterial Pneumonia", "Viral Pneumonia"]  # 0=Bacterial, 1=Viral
        self.threshold = settings.STAGE2_THRESHOLD
        
    def load_model(self):
        """Load Stage-2 dual-input classifier"""
        try:
            logger.info("Loading Stage-2 dual-input classifier...")
            
            model_path = Path(settings.STAGE2_MODEL_PATH)
            
            if not model_path.exists():
                raise FileNotFoundError(f"Stage-2 model not found: {model_path}")
            
            # Load model directly (single .keras file)
            self.model = keras.models.load_model(model_path, compile=False)
            
            logger.info(f"✓ Stage-2 classifier loaded successfully")
            logger.info(f"  Input 1: Original X-ray (224, 224, 1)")
            logger.info(f"  Input 2: Segmented lung (224, 224, 1)")
            logger.info(f"  Output: Viral vs Bacterial")
            logger.info(f"  Threshold: {self.threshold}")
            
        except Exception as e:
            logger.error(f"Failed to load Stage-2 classifier: {str(e)}")
            raise
    
    def preprocess_for_convnext(self, image: np.ndarray) -> np.ndarray:
        """
        Convert grayscale to RGB and apply ConvNeXt preprocessing
        
        Args:
            image: Grayscale image (224, 224, 1), normalized [0, 1]
            
        Returns:
            Preprocessed RGB image (224, 224, 3)
        """
        # Remove channel dimension if present
        if len(image.shape) == 3 and image.shape[-1] == 1:
            image = image[:, :, 0]
        
        # Convert grayscale to RGB
        image_rgb = np.stack([image] * 3, axis=-1)
        
        # Convert to 0-255 range
        if image_rgb.max() <= 1.0:
            image_rgb = image_rgb * 255.0
        
        # Apply ConvNeXt preprocessing
        image_rgb = tf.keras.applications.convnext.preprocess_input(image_rgb)
        
        return image_rgb
    
    def predict(self, original_image: np.ndarray, segmented_image: np.ndarray) -> dict:
        """
        Classify pneumonia type using both original and segmented images
        
        Args:
            original_image: Original X-ray (224, 224, 1), normalized [0, 1]
            segmented_image: Segmented lung mask (224, 224, 1), normalized [0, 1]
            
        Returns:
            Dictionary with prediction results:
            - predicted_class: "Viral Pneumonia" or "Bacterial Pneumonia"
            - confidence: float [0, 1]
            - viral_probability: float [0, 1]
            - bacterial_probability: float [0, 1]
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Try passing grayscale images directly (model may convert to RGB internally)
        # Add batch dimension
        original_batch = np.expand_dims(original_image, axis=0)
        segmented_batch = np.expand_dims(segmented_image, axis=0)
        
        # Perform inference with dual inputs
        prediction = self.model.predict([original_batch, segmented_batch], verbose=0)
        
        # Extract probability (sigmoid output = probability of class 1 = Viral)
        # Training used: classes = ["bacterial", "viral"] where 0=Bacterial, 1=Viral
        viral_prob = float(prediction[0][0])
        bacterial_prob = 1 - viral_prob
        
        # Determine predicted class (threshold comparison with viral_prob)
        is_viral = viral_prob >= self.threshold
        predicted_class = "Viral Pneumonia" if is_viral else "Bacterial Pneumonia"
        confidence = viral_prob if is_viral else bacterial_prob
        
        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "viral_probability": viral_prob,
            "bacterial_probability": bacterial_prob
        }
    
    def get_model_info(self) -> dict:
        """Get model information"""
        return {
            "model_name": "Stage-2 Dual-Input Classifier (ConvNeXt)",
            "classes": self.class_names,
            "inputs": ["Original X-ray", "Segmented Lung"],
            "threshold": self.threshold,
            "loaded": self.model is not None
        }


# Global instance (loaded at startup)
stage2_classifier = Stage2ClassifierService()
