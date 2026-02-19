"""
Lung Segmentation Service using U-Net
Loads model from config.json and model.weights.h5
Performs inference-only lung segmentation on chest X-rays
"""
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import logging
from pathlib import Path
from ..core.config import settings

logger = logging.getLogger(__name__)


class LungSegmentationService:
    """Service for lung segmentation using pre-trained U-Net model"""
    
    def __init__(self):
        self.model = None
        self.input_shape = None
        self.model_version = None
        
    def _load_model_from_keras_config(self, config: dict) -> keras.Model:
        """
        Load model from full Keras config.json (generated from model.to_json())
        
        Args:
            config: Full Keras model configuration dictionary
            
        Returns:
            Keras Model (uncompiled)
        """
        # Use Model.from_config for Keras 3.x
        # Extract the actual config portion if it exists
        from tensorflow.keras.models import Model
        
        if 'config' in config:
            # This is a full model export, extract just the config portion
            model_config = config['config']
        else:
            # This is already just the config
            model_config = config
            
        model = Model.from_config(model_config)
        return model
    
    def load_model(self):
        """
        Load U-Net segmentation model from config and weights
        DOES NOT use load_model() - reconstructs architecture manually
        """
        try:
            logger.info("Loading lung segmentation model...")
            
            # Verify files exist
            config_path = Path(settings.SEGMENTATION_CONFIG)
            weights_path = Path(settings.SEGMENTATION_WEIGHTS)
            metadata_path = Path(settings.SEGMENTATION_METADATA)
            
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")
            if not weights_path.exists():
                raise FileNotFoundError(f"Weights file not found: {weights_path}")
            
            # Load configuration
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            logger.info(f"Model config loaded: {config.get('class_name', 'U-Net')}")
            
            # Extract input shape from config
            # Look for InputLayer in the layers list
            input_shape = [256, 256, 1]  # Default
            if 'config' in config and 'layers' in config['config']:
                for layer in config['config']['layers']:
                    if layer.get('class_name') == 'InputLayer':
                        batch_shape = layer['config'].get('batch_shape', [None, 256, 256, 1])
                        input_shape = batch_shape[1:]  # Remove batch dimension
                        break
            
            self.input_shape = tuple(input_shape)
            logger.info(f"Model input shape: {self.input_shape}")
            
            # Load metadata if exists
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    self.model_version = metadata.get("version", "unknown")
                    logger.info(f"Model version: {self.model_version}")
            else:
                self.model_version = "unknown"
            
            # Reconstruct model from full Keras config
            self.model = self._load_model_from_keras_config(config)
            
            # Load pre-trained weights
            self.model.load_weights(weights_path)
            
            logger.info(f"✓ Segmentation model loaded successfully")
            logger.info(f"  Input shape: {self.input_shape}")
            logger.info(f"  Total parameters: {self.model.count_params():,}")
            
        except Exception as e:
            logger.error(f"Failed to load segmentation model: {str(e)}")
            raise
    
    def predict(self, image: np.ndarray) -> np.ndarray:
        """
        Perform lung segmentation on preprocessed image
        
        Args:
            image: Preprocessed image array (224, 224, 1), normalized [0, 1]
            
        Returns:
            Segmentation mask (224, 224, 1), values [0, 1]
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Ensure correct shape
        if len(image.shape) == 2:
            image = np.expand_dims(image, axis=-1)
        
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        
        # Perform inference
        mask = self.model.predict(image, verbose=0)
        
        # Remove batch dimension
        mask = mask[0]
        
        return mask
    
    def get_model_info(self) -> dict:
        """Get model information"""
        return {
            "model_name": "U-Net Lung Segmentation",
            "version": self.model_version,
            "input_shape": self.input_shape,
            "loaded": self.model is not None
        }


# Global instance (loaded at startup)
segmentation_service = LungSegmentationService()
