"""
Authentication API Endpoints
Handles user registration, login, and token management
"""
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from bson import ObjectId
from ..db.schemas import UserCreate, UserLogin, Token, UserResponse
from ..db.mongodb import get_database
from ..core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    validate_password_strength
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db = Depends(get_database)):
    """
    Register a new user
    
    Args:
        user_data: User registration data
        db: Database connection
        
    Returns:
        JWT token and user information
    """
    try:
        # Validate password strength
        is_valid, error_msg = validate_password_strength(user_data.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user document
        user_doc = {
            "email": user_data.email,
            "hashed_password": hashed_password,
            "full_name": user_data.full_name,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        }
        
        # Insert into database
        result = await db.users.insert_one(user_doc)
        user_id = str(result.inserted_id)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user_id, "email": user_data.email}
        )
        
        # Prepare user response
        user_response = UserResponse(
            id=user_id,
            email=user_data.email,
            full_name=user_data.full_name,
            created_at=user_doc["created_at"]
        )
        
        logger.info(f"New user registered: {user_data.email}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db = Depends(get_database)):
    """
    Login user and return JWT token
    
    Args:
        credentials: User login credentials
        db: Database connection
        
    Returns:
        JWT token and user information
    """
    try:
        # Find user by email
        user = await db.users.find_one({"email": credentials.email})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(credentials.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if account is active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Create access token
        user_id = str(user["_id"])
        access_token = create_access_token(
            data={"sub": user_id, "email": user["email"]}
        )
        
        # Prepare user response
        user_response = UserResponse(
            id=user_id,
            email=user["email"],
            full_name=user["full_name"],
            created_at=user["created_at"]
        )
        
        logger.info(f"User logged in: {credentials.email}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.get("/verify", response_model=UserResponse)
async def verify_token(current_user: dict = Depends(lambda: None)):
    """
    Verify JWT token and return user information
    This is a placeholder - actual implementation in users.py
    """
    pass
