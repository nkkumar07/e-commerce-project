from pydantic import BaseModel, EmailStr
from api.database.schemas.enums import UserRole  

# Schema for Creating a New User (Input)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    mobile: str
    role: UserRole = UserRole.CUSTOMER  # Restrict to valid roles

    def hash_user_password(self):
        """Hashes the password before storing it."""
        from api.security import hash_password  
        self.password = hash_password(self.password)

# Schema for User Response (Output)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    mobile: str
    role: UserRole

class UserProfileUpdate(BaseModel):

    name: str
    email: EmailStr
    mob_number: str
    

    # Pydantic schema for password update
class UserPasswordUpdate(BaseModel):
 
    new_password: str
    confirm_password: str


    class Config:
        from_attributes = True 

# Schema for User Login
class UserLogin(BaseModel):
    email: EmailStr  
    password: str  
