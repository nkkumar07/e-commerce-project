from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.schemas.user import UserResponse, UserProfileUpdate, UserPasswordUpdate
from api.token import get_current_user
from api.database.connection import get_db  
from api.crud.user import update_user_profile, get_user_by_email, update_user_password ,get_all_users,get_user_by_id 

# Creating an API router instance for handling user-related routes
router = APIRouter()

@router.get("/Profile", response_model=list[UserResponse])
def get_users_profile(db: Session = Depends(get_db)):
    """Endpoint to retrieve all user profiles."""
    return get_all_users(db)

@router.get("/profile/email/{email}", response_model=UserResponse)
def get_user_profile_by_email(email: str, db: Session = Depends(get_db)):
    """Endpoint to retrieve a user profile by email."""
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/profile/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Endpoint to retrieve a user profile by ID."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.put("/profile/update/", response_model=dict)
def update_profile(user_id: int, user_data: UserProfileUpdate, db: Session = Depends(get_db)):
    """Endpoint to update the current user's profile."""
    return update_user_profile(db, user_id, user_data)


@router.put("/users/update-password")
def update_password(
    email: str, 
    password_data: UserPasswordUpdate, 
    db: Session = Depends(get_db)
):
    """API endpoint to update a user's password."""
    user = get_user_by_email(db, email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(status_code=400, detail="New password and confirmation password do not match")

    # Update password directly
    update_user_password(db, user, password_data.new_password)
    
    return {"message": "Password updated successfully"}
