from sqlalchemy.orm import Session
from api.database.models.user import User
from api.database.schemas.user import UserCreate, UserProfileUpdate  
from api.security import hash_password
from fastapi import HTTPException  

# Function to create a new user in the database
def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),  # Hash the password before storing
        mobile=user.mobile,
        role=user.role if hasattr(user, "role") else "customer",
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Function to retrieve a user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# Function to fetch all users
def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    """Fetch a user profile by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user_profile(db: Session, user_id: int, user_data: UserProfileUpdate):
    # Fetch user from the database (User is the SQLAlchemy model)
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only provided fields
    user_data_dict = user_data.model_dump(exclude_unset=True)  

    for key, value in user_data_dict.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return {"message": "User updated successfully"}

def update_user_password(db: Session, user: User, new_password: str):
    """Update user's password."""
    user.password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user
