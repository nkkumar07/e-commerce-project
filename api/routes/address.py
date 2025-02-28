from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.address import AddressCreate, AddressUpdate,AddressResponse  
from api.crud.address import create_address ,get_address,delete_address,update_address,get_all_address


router = APIRouter()

@router.post("/add", response_model=AddressResponse)
def add_address(address: AddressCreate, db: Session = Depends(get_db)):
    
    return create_address(db, address)

# Get all Address (GET)
@router.get("/address", response_model=list[AddressResponse])
def fetch_all_address(db: Session = Depends(get_db)):
    return get_all_address(db)


# Get an address by ID
@router.get("/{address_id}", response_model=AddressResponse)
def get_address_by_id(address_id: int, db: Session = Depends(get_db)):
    address = get_address(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

# Delete an address
@router.delete("/delete/{address_id}", response_model=dict)
def delete_address_by_id(address_id: int, db: Session = Depends(get_db)):
    success = delete_address(db, address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}

# Update an existing address
@router.put("/update/{address_id}", response_model=AddressResponse)
def updated_address_by_id(address_id: int, address_data: AddressUpdate, db: Session = Depends(get_db)):
    updated_address = update_address(db, address_id, address_data)
    if not updated_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated_address