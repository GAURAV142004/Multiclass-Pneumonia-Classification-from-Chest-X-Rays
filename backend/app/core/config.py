"""
Core Configuration for Pneumonia Detection System
Handles environment variables, model paths, and application settings
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Application
    APP_NAME: str = "Pneumonia Detection System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "pneumonia_detection"
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # Model Paths (relative to backend root)
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")
    
    # Lung Segmentation Model (U-Net)
    SEGMENTATION_MODEL_DIR: str = os.path.join(MODELS_DIR, "lung_segmentation")
    SEGMENTATION_WEIGHTS: str = os.path.join(SEGMENTATION_MODEL_DIR, "model.weights.h5")
    SEGMENTATION_CONFIG: str = os.path.join(SEGMENTATION_MODEL_DIR, "config.json")
    SEGMENTATION_METADATA: str = os.path.join(SEGMENTATION_MODEL_DIR, "metadata.json")
    
    # Stage-1 Binary Classifier
    STAGE1_MODEL_PATH: str = os.path.join(MODELS_DIR, "stage1_convnext.keras")
    
    # Stage-2 Dual-Input Classifier
    STAGE2_MODEL_PATH: str = os.path.join(MODELS_DIR, "dual_input_stage2_final.keras")
    
    # Image Processing Settings
    IMAGE_SIZE: tuple = (224, 224)
    MAX_IMAGE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".dcm"}
    
    # Classification Thresholds
    STAGE1_THRESHOLD: float = 0.5  # Normal vs Pneumonia
    STAGE2_THRESHOLD: float = 0.5  # Viral vs Bacterial
    
    # Medical Disclaimer
    MEDICAL_DISCLAIMER: str = (
        "This system is intended for research and educational purposes only "
        "and must not be used for clinical diagnosis. Always consult a qualified "
        "healthcare professional for medical advice."
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
