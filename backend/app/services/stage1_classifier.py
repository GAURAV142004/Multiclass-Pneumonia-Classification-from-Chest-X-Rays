"""
Stage-1 Binary Classifier Service
Classifies chest X-rays as Normal vs Pneumonia using ConvNeXt
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
import logging
from pathlib import Path
from ..core.config import settings

logger = logging.getLogger(__name__)


class Stage1ClassifierService:
    """Binary classifier: Normal vs Pneumonia"""
    
    def __init__(self):
        self.model = None
        self.class_names = ["Normal", "Pneumonia"]
        self.threshold = settings.STAGE1_THRESHOLD
        
    def load_model(self):
        """Load Stage-1 ConvNeXt binary classifier"""
        try:
            logger.info("Loading Stage-1 binary classifier...")
            
            model_path = Path(settings.STAGE1_MODEL_PATH)
            
            if not model_path.exists():
                raise FileNotFoundError(f"Stage-1 model not found: {model_path}")
            
            # Load model directly (single .keras file)
            self.model = keras.models.load_model(model_path, compile=False)
            
            logger.info(f"✓ Stage-1 classifier loaded successfully")
            logger.info(f"  Input shape: {self.model.input_shape}")
            logger.info(f"  Output: Sigmoid (Normal vs Pneumonia)")
            logger.info(f"  Threshold: {self.threshold}")
            
        except Exception as e:
            logger.error(f"Failed to load Stage-1 classifier: {str(e)}")
            raise
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image to match training (simple RGB conversion + [0,1] normalization)
        
        Args:
            image: Grayscale image (224, 224) or (224, 224, 1), normalized [0, 1]
            
        Returns:
            Preprocessed RGB image (1, 224, 224, 3)
        """
        # Convert grayscale to RGB (replicate channel 3 times)
        if len(image.shape) == 2:
            image = np.stack([image] * 3, axis=-1)
        elif image.shape[-1] == 1:
            image = np.concatenate([image] * 3, axis=-1)
        
        # Image is already normalized to [0, 1] - keep it as is
        # NO ConvNeXt preprocessing - training only used simple [0,1] normalization
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def predict(self, image: np.ndarray) -> dict:
        """
        Classify image as Normal or Pneumonia
        
        Args:
            image: Preprocessed image (224, 224, 1), normalized [0, 1]
            
        Returns:
            Dictionary with prediction results:
            - predicted_class: "Normal" or "Pneumonia"
            - confidence: float [0, 1]
            - pneumonia_probability: float [0, 1]
            - has_pneumonia: bool
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Preprocess for ConvNeXt
        preprocessed = self.preprocess_image(image)
        
        # Perform inference
        prediction = self.model.predict(preprocessed, verbose=0)
        
        # Extract probability (sigmoid output)
        pneumonia_prob = float(prediction[0][0])
        
        # Apply threshold
        has_pneumonia = pneumonia_prob >= self.threshold
        predicted_class = "Pneumonia" if has_pneumonia else "Normal"
        confidence = pneumonia_prob if has_pneumonia else (1 - pneumonia_prob)
        
        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "pneumonia_probability": pneumonia_prob,
            "has_pneumonia": has_pneumonia
        }
    
    def get_model_info(self) -> dict:
        """Get model information"""
        return {
            "model_name": "Stage-1 Binary Classifier (ConvNeXt)",
            "classes": self.class_names,
            "threshold": self.threshold,
            "loaded": self.model is not None
        }


# Global instance (loaded at startup)
stage1_classifier = Stage1ClassifierService()
