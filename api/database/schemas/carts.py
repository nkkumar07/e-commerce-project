from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CartCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class CartUpdate(BaseModel):
    
    product_id: Optional[int] = None
    quantity: Optional[int] = None

class CartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    created_at: datetime

    class Config:
        from_attributes = True


class CartUpdateResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    created_at: datetime

    class Config:
        from_attributes = True
