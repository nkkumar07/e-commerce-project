from pydantic import BaseModel
from typing import Optional

class AddressCreate(BaseModel):
    user_id: int
    state: str
    city: str
    address_line1: str
    address_line2: Optional[str] = None
    pincode: str

class AddressUpdate(BaseModel):
    state: Optional[str] = None
    city: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    pincode: Optional[str] = None

class AddressResponse(BaseModel):
    id: int
    user_id: int
    state: str
    city: str
    address_line1: str
    address_line2: Optional[str] = None
    pincode: str
    complete_address: str

    class Config:
        from_attributes = True
