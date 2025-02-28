from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.database.models.address import Address 
from api.database.schemas.address import AddressCreate,AddressUpdate

def create_address(db: Session, address: AddressCreate):
    
    db_address = Address(
        user_id=address.user_id,
        state=address.state,
        city=address.city,
        address_line1=address.address_line1,
        address_line2=address.address_line2,
        pincode=address.pincode,
        complete_address=f"{address.address_line1}, {address.address_line2}, {address.city}, {address.state} - {address.pincode}"
    )
    
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


#  GET Address by ID
def get_address(db: Session, address_id: int):
    
    return db.query(Address).filter(Address.id == address_id).first()


# Delete an address by ID
def delete_address(db: Session, address_id: int):
    address = db.query(Address).filter(Address.id == address_id).first()
    
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(address)
    db.commit()
    return {"message": "Address deleted successfully"}

def get_all_address(db: Session):
    """Fetch all address from the database."""
    return db.query(Address).all()


# Update an existing address
def update_address(db: Session, address_id: int, address_data: AddressUpdate):
    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    if address_data.state:
        address.state = address_data.state
    if address_data.city:
        address.city = address_data.city
    if address_data.address_line1:
        address.address_line1 = address_data.address_line1
    if address_data.address_line2 is not None:
        address.address_line2 = address_data.address_line2
    if address_data.pincode:
        address.pincode = address_data.pincode

    # Update the complete address
    address.complete_address = f"{address.address_line1}, {address.address_line2}, {address.city}, {address.state} - {address.pincode}"

    db.commit()
    db.refresh(address)
    
    return address