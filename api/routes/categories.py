from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.categories import CategoryCreate, CategoryUpdate, CategoryResponse
from api.crud.categories import create_category, delete_category, update_category
from api.database.models.categories import Category  

router = APIRouter()

# Add a new category
@router.post("/add", response_model=CategoryResponse)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category)
    
@router.get("/viewcategories", response_model=list[CategoryResponse])
def view_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

# Delete a category by its ID
@router.delete("/delete/{category_id}", response_model=dict)
def delete_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return delete_category(db, category_id)

# Update an existing category
@router.put("/update/{category_id}", response_model=CategoryResponse)
def update_category_by_id(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    return update_category(db, category_id, category_data)
