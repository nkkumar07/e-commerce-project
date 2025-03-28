from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from api.database.models.categories import Category
from api.database.schemas.categories import CategoryCreate, CategoryUpdate


def get_category(db: Session, category_id: int) -> Category:
    """Helper function to fetch a category or raise 404."""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


def create_category(db: Session, category: CategoryCreate) -> Category:
    """Create a new category (with name uniqueness check)."""
    # Check if category name already exists
    existing_category = db.query(Category).filter(
        Category.name == category.name
    ).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )

    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(
    db: Session, 
    category_id: int, 
    category_data: CategoryUpdate
) -> Category:
    """Update an existing category."""
    category = get_category(db, category_id)  
    
    if category_data.name:
     
        conflicting_category = db.query(Category).filter(
            Category.name == category_data.name,
            Category.id != category_id
        ).first()
        if conflicting_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another category with this name already exists"
            )
        
        category.name = category_data.name

    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> dict:
    """Delete a category by ID."""
    category = get_category(db, category_id)  # Reuse helper
    db.delete(category)
    db.commit()
    return {
        "success": True,
        "message": "Category deleted successfully"
    }
