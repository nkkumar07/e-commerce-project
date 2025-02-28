from pydantic import BaseModel,Field
from datetime import datetime


class ReviewCreate(BaseModel):
    user_id: int
    order_id: int
    product_id: int
    rating: int = Field(..., ge=1, le=5)
    review_text: str
    created_at: datetime

 
class  ReviewResponse(BaseModel):
    id: int
    user_id: int
    order_id: int
    product_id: int
    rating: int
    review_text: str
    created_at: datetime


    class Config:
        from_attributes = True  


