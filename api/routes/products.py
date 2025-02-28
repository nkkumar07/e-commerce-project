from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.products  import ProductCreate ,ProductUpdate,ProductResponse
from api.crud.products import create_product,delete_product,update_product,get_active_products

# Create a new API router for handling authentication-related endpoints
router = APIRouter()


@router.post("/add", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
        return create_product(db, product)


# Delete a category by its ID

@router.delete("/delete/{product_id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    
    return delete_product(db, product_id)

# Update an existing category
@router.put("/update/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data:  ProductUpdate, db: Session = Depends(get_db)):
    
    return update_product(db, product_id, product_data)

@router.get("/products/active", response_model=list[ProductResponse])
def active_products(db: Session = Depends(get_db)):
    return get_active_products(db)



