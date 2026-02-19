"""
Image Utility Functions
Handles image encoding, decoding, and conversions
"""
import numpy as np
import base64
from PIL import Image
import io
import cv2


def numpy_to_base64(image: np.ndarray) -> str:
    """
    Convert numpy array to base64 string
    
    Args:
        image: Numpy array (H, W) or (H, W, C)
        
    Returns:
        Base64 encoded string
    """
    # Ensure image is in [0, 255] range
    if image.max() <= 1.0:
        image = (image * 255).astype(np.uint8)
    else:
        image = image.astype(np.uint8)
    
    # Remove channel dimension if grayscale
    if len(image.shape) == 3 and image.shape[-1] == 1:
        image = image[:, :, 0]
    
    # Convert to PIL Image
    pil_image = Image.fromarray(image)
    
    # Encode to base64
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def base64_to_numpy(base64_string: str) -> np.ndarray:
    """
    Convert base64 string to numpy array
    
    Args:
        base64_string: Base64 encoded image string
        
    Returns:
        Numpy array
    """
    # Remove data URI prefix if present
    if "base64," in base64_string:
        base64_string = base64_string.split("base64,")[1]
    
    # Decode
    img_bytes = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_bytes))
    
    return np.array(img)


def resize_image(image: np.ndarray, size: tuple) -> np.ndarray:
    """
    Resize image to specified size
    
    Args:
        image: Input image
        size: Target size (width, height)
        
    Returns:
        Resized image
    """
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize image to [0, 1] range
    
    Args:
        image: Input image
        
    Returns:
        Normalized image
    """
    if image.max() > 1.0:
        return image.astype(np.float32) / 255.0
    return image.astype(np.float32)


def create_thumbnail(image: np.ndarray, max_size: int = 300) -> str:
    """
    Create thumbnail of image
    
    Args:
        image: Input image
        max_size: Maximum dimension size
        
    Returns:
        Base64 encoded thumbnail
    """
    # Calculate new dimensions
    h, w = image.shape[:2]
    if h > w:
        new_h = max_size
        new_w = int(w * (max_size / h))
    else:
        new_w = max_size
        new_h = int(h * (max_size / w))
    
    # Resize
    thumbnail = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    return numpy_to_base64(thumbnail)
