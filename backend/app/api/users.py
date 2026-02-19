"""
User Management API Endpoints
Handles user profile, settings, and scan history
"""
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from ..db.schemas import UserResponse, UserProfileUpdate, PasswordChange
from ..db.mongodb import get_database
from ..core.security import get_current_user, get_password_hash, verify_password
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Get current user's profile information
    
    Args:
        current_user: Authenticated user from JWT
        db: Database connection
        
    Returns:
        User profile information
    """
    try:
        user = await db.users.find_one({"_id": ObjectId(current_user["user_id"])})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=str(user["_id"]),
            email=user["email"],
            full_name=user["full_name"],
            created_at=user["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user profile"
        )


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Update current user's profile
    
    Args:
        profile_data: Updated profile data
        current_user: Authenticated user from JWT
        db: Database connection
        
    Returns:
        Updated user profile
    """
    try:
        update_fields = {}
        
        if profile_data.full_name is not None:
            update_fields["full_name"] = profile_data.full_name
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Update user
        result = await db.users.update_one(
            {"_id": ObjectId(current_user["user_id"])},
            {"$set": update_fields}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Fetch updated user
        user = await db.users.find_one({"_id": ObjectId(current_user["user_id"])})
        
        return UserResponse(
            id=str(user["_id"]),
            email=user["email"],
            full_name=user["full_name"],
            created_at=user["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Change user password
    
    Args:
        password_data: Current and new password
        current_user: Authenticated user from JWT
        db: Database connection
        
    Returns:
        Success message
    """
    try:
        # Get user
        user = await db.users.find_one({"_id": ObjectId(current_user["user_id"])})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify current password
        if not verify_password(password_data.current_password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect"
            )
        
        # Hash new password
        new_hashed_password = get_password_hash(password_data.new_password)
        
        # Update password
        await db.users.update_one(
            {"_id": ObjectId(current_user["user_id"])},
            {"$set": {"hashed_password": new_hashed_password}}
        )
        
        logger.info(f"Password changed for user: {current_user['email']}")
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )


@router.get("/history")
async def get_scan_history(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database),
    limit: int = 10
):
    """
    Get user's scan history
    
    Args:
        current_user: Authenticated user from JWT
        db: Database connection
        limit: Maximum number of records to return
        
    Returns:
        List of scan history records
    """
    try:
        cursor = db.scan_history.find(
            {"user_id": current_user["user_id"]}
        ).sort("created_at", -1).limit(limit)
        
        history = []
        async for record in cursor:
            history.append({
                "id": str(record["_id"]),
                "prediction_label": record["prediction_label"],
                "confidence": record["confidence"],
                "created_at": record["created_at"].isoformat()
            })
        
        return {"history": history, "count": len(history)}
        
    except Exception as e:
        logger.error(f"Error fetching scan history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch scan history"
        )
