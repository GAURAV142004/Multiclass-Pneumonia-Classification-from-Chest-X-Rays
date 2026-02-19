"""
Response Formatting Utilities
Standardizes API responses
"""
from typing import Any, Optional
from datetime import datetime


def success_response(data: Any, message: str = "Success") -> dict:
    """
    Format successful API response
    
    Args:
        data: Response data
        message: Success message
        
    Returns:
        Formatted response dictionary
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }


def error_response(message: str, error_code: Optional[str] = None, details: Optional[dict] = None) -> dict:
    """
    Format error API response
    
    Args:
        message: Error message
        error_code: Optional error code
        details: Optional additional error details
        
    Returns:
        Formatted error response
    """
    response = {
        "success": False,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if error_code:
        response["error_code"] = error_code
    
    if details:
        response["details"] = details
    
    return response


def prediction_response(
    prediction_label: str,
    confidence: float,
    original_image: str,
    segmented_image: str,
    additional_data: Optional[dict] = None
) -> dict:
    """
    Format prediction response
    
    Args:
        prediction_label: Predicted class label
        confidence: Prediction confidence
        original_image: Base64 encoded original image
        segmented_image: Base64 encoded segmented image
        additional_data: Optional additional prediction data
        
    Returns:
        Formatted prediction response
    """
    from ..core.config import settings
    
    response = {
        "prediction": {
            "label": prediction_label,
            "confidence": round(confidence * 100, 2)  # Convert to percentage
        },
        "images": {
            "original": original_image,
            "segmented": segmented_image
        },
        "disclaimer": settings.MEDICAL_DISCLAIMER,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if additional_data:
        response["prediction"].update(additional_data)
    
    return response
