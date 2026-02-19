"""
Database Schemas and Models
Pydantic models for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ============= Authentication Schemas =============

class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user data in responses"""
    id: str
    email: EmailStr
    full_name: str
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ============= Prediction Schemas =============

class PredictionRequest(BaseModel):
    """Schema for prediction request (not used directly - file upload)"""
    pass


class PredictionResult(BaseModel):
    """Schema for prediction results"""
    label: str
    confidence: float
    stage: int  # 1 or 2
    additional_info: Optional[dict] = None


class PredictionResponse(BaseModel):
    """Schema for complete prediction response"""
    prediction: PredictionResult
    images: dict
    disclaimer: str
    timestamp: datetime


# ============= Scan History Schemas =============

class ScanHistoryCreate(BaseModel):
    """Schema for creating scan history record"""
    user_id: str
    prediction_label: str
    confidence: float
    original_image_url: Optional[str] = None
    segmented_image_url: Optional[str] = None


class ScanHistoryResponse(BaseModel):
    """Schema for scan history response"""
    id: str
    user_id: str
    prediction_label: str
    confidence: float
    created_at: datetime
    original_image_url: Optional[str] = None
    segmented_image_url: Optional[str] = None


# ============= User Profile Schemas =============

class UserProfileUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = None


class PasswordChange(BaseModel):
    """Schema for password change"""
    current_password: str
    new_password: str = Field(..., min_length=8)


# ============= Error Schemas =============

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
