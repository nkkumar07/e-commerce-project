from sqlalchemy.orm import Session
from fastapi import HTTPException

from api.database.models.categories import Category
from api.database.schemas.categories import CategoryCreate, CategoryUpdate


def create_category(db: Session, category: CategoryCreate):
    """Create a new category."""
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session):
    """Retrieve all categories."""
    categories = db.query(Category).all()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return categories


# delete_category function
def delete_category(db: Session, category_id: int):
    """Delete a category by ID."""
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")  # Raise exception for better API response

    db.delete(category)
    db.commit()

    return {"success": True, "message": "Category deleted successfully"}


# update_category function
def update_category(db: Session, category_id: int, category_data: CategoryUpdate):
    """Update an existing category."""
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")  # Handle case where category doesn't exist

    if category_data.name:
        category.name = category_data.name

    db.commit()
    db.refresh(category)

    return category
