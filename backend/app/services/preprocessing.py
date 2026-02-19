"""
Image Preprocessing Service
Handles image validation, loading, resizing, and normalization
"""
import numpy as np
from PIL import Image
import cv2
import io
import logging
from pathlib import Path
from ..core.config import settings

logger = logging.getLogger(__name__)


class ImagePreprocessor:
    """Handles all image preprocessing operations"""
    
    def __init__(self):
        self.target_size = settings.IMAGE_SIZE
        self.max_size_bytes = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
    
    def validate_image(self, file_data: bytes, filename: str) -> tuple[bool, str]:
        """
        Validate uploaded image file
        
        Args:
            file_data: Raw file bytes
            filename: Original filename
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file size
        if len(file_data) > self.max_size_bytes:
            return False, f"File size exceeds {settings.MAX_IMAGE_SIZE_MB}MB limit"
        
        # Check file extension
        file_ext = Path(filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            return False, f"Invalid file type. Allowed: {', '.join(self.allowed_extensions)}"
        
        # Try to open as image
        try:
            img = Image.open(io.BytesIO(file_data))
            img.verify()
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
        
        return True, ""
    
    def load_image_from_bytes(self, file_data: bytes) -> np.ndarray:
        """
        Load image from bytes and convert to numpy array
        
        Args:
            file_data: Raw file bytes
            
        Returns:
            Image as numpy array (H, W, C)
        """
        img = Image.open(io.BytesIO(file_data))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(img)
        
        return img_array
    
    def preprocess_for_segmentation(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for lung segmentation model
        
        Args:
            image: RGB image array (H, W, 3)
            
        Returns:
            Preprocessed grayscale image (256, 256, 1), normalized [0, 1]
        """
        # Convert to grayscale
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Resize to 256x256 for U-Net model
        resized = cv2.resize(gray, (256, 256), interpolation=cv2.INTER_AREA)
        
        # Normalize to [0, 1]
        normalized = resized.astype(np.float32) / 255.0
        
        # Add channel dimension
        preprocessed = np.expand_dims(normalized, axis=-1)
        
        return preprocessed
    
    def preprocess_for_classification(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for classification models
        
        Args:
            image: RGB image array (H, W, 3)
            
        Returns:
            Preprocessed grayscale image (224, 224, 1), normalized [0, 1]
        """
        # Convert to grayscale
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Resize to 224x224 for classification models
        resized = cv2.resize(gray, (224, 224), interpolation=cv2.INTER_AREA)
        
        # Normalize to [0, 1]
        normalized = resized.astype(np.float32) / 255.0
        
        # Add channel dimension
        preprocessed = np.expand_dims(normalized, axis=-1)
        
        return preprocessed
    
    def apply_clahe(self, image: np.ndarray) -> np.ndarray:
        """
        Apply Contrast Limited Adaptive Histogram Equalization
        
        Args:
            image: Grayscale image (H, W) or (H, W, 1)
            
        Returns:
            Enhanced image
        """
        if len(image.shape) == 3:
            image = image[:, :, 0]
        
        # Convert to uint8 for CLAHE
        if image.max() <= 1.0:
            image = (image * 255).astype(np.uint8)
        else:
            image = image.astype(np.uint8)
        
        # Apply CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
        
        # Convert back to float [0, 1]
        enhanced = enhanced.astype(np.float32) / 255.0
        
        return enhanced
    
    def postprocess_segmentation_mask(self, mask: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """
        Postprocess segmentation mask
        
        Args:
            mask: Raw segmentation output (256, 256, 1), values [0, 1]
            threshold: Binarization threshold
            
        Returns:
            Binary mask (256, 256, 1)
        """
        # Apply threshold
        binary_mask = (mask > threshold).astype(np.float32)
        
        # Optional: Apply morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        
        if len(binary_mask.shape) == 3:
            mask_2d = binary_mask[:, :, 0]
        else:
            mask_2d = binary_mask
        
        # Close small holes
        closed = cv2.morphologyEx(mask_2d, cv2.MORPH_CLOSE, kernel)
        
        # Open to remove noise
        cleaned = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
        
        # Add channel dimension back
        cleaned = np.expand_dims(cleaned, axis=-1)
        
        return cleaned
    
    def overlay_mask_on_image(self, image: np.ndarray, mask: np.ndarray, alpha: float = 0.5) -> np.ndarray:
        """
        Overlay segmentation mask on original image
        
        Args:
            image: Original grayscale image (256, 256, 1)
            mask: Binary segmentation mask (256, 256, 1)
            alpha: Transparency factor
            
        Returns:
            Overlayed image (256, 256, 3) for visualization
        """
        # Convert grayscale to RGB
        if len(image.shape) == 3 and image.shape[-1] == 1:
            image = image[:, :, 0]
        
        image_rgb = np.stack([image] * 3, axis=-1)
        
        # Remove mask channel dimension
        if len(mask.shape) == 3 and mask.shape[-1] == 1:
            mask = mask[:, :, 0]
        
        # Create colored mask (cyan)
        colored_mask = np.zeros_like(image_rgb)
        colored_mask[:, :, 1] = mask  # Green channel
        colored_mask[:, :, 2] = mask  # Blue channel
        
        # Blend
        overlay = cv2.addWeighted(image_rgb, 1 - alpha, colored_mask, alpha, 0)
        
        return overlay


# Global instance
preprocessor = ImagePreprocessor()
