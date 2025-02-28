from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from api.database.models.products import ProductStatus  # Importing ProductStatus Enum

class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: str
    mrp: float = Field(..., gt=0, description="MRP must be greater than zero.")
    net_price: float = Field(..., gt=0, description="Net price must be greater than zero.")
    stock: int = Field(..., ge=0, description="Stock cannot be negative.")
    image: str | None = None 

    @field_validator("net_price")
    @classmethod
    def check_net_price(cls, net_price, values):
        """Ensure net_price is not greater than MRP."""
        mrp = values.data.get("mrp")  
        if mrp is not None and net_price > mrp:
            raise ValueError("Net price cannot be higher than MRP.")
        return net_price


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    mrp: float | None = Field(None, gt=0)
    net_price: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    image: str | None = None
    category_id: int | None = None

    @field_validator("net_price")
    @classmethod
    def check_net_price(cls, net_price, values):
        """Ensure net_price is not greater than MRP."""
        mrp = values.data.get("mrp")  
        if mrp is not None and net_price > mrp:
            raise ValueError("Net price cannot be higher than MRP.")
        return net_price


class ProductResponse(BaseModel):
    id: int
    category_id: int
    name: str
    description: str
    mrp: float
    net_price: float
    stock: int
    status: ProductStatus  
    image: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
