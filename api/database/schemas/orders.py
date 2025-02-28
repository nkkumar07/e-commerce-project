from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional

class OrderCreate(BaseModel):
    user_id: int
    subtotal: float
    discount: float
    total: float
    status: Literal["pending", "shipped", "cancelled", "delivered"]
    shipping_address: str

class OrderUpdate(BaseModel):
    subtotal: Optional[float] = None
    discount: Optional[float] = None
    total: Optional[float] = None
    status: Optional[Literal["pending", "shipped", "cancelled", "delivered"]] = None
    shipping_address: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    subtotal: float
    discount: float
    total: float
    status: Literal["pending", "shipped", "cancelled", "delivered"]
    shipping_address: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  
