from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.reviews import ReviewCreate, ReviewResponse
from api.crud.reviews import create_review, get_reviews_by_user, get_review_by_id, get_reviews_by_product

router = APIRouter()

@router.post("/add", response_model=ReviewResponse)
def add_reviews(review: ReviewCreate, db: Session = Depends(get_db)):
    """Adds a review for a product."""
    return create_review(db, review)

def get_all_reviews(db: Session):
    """Fetch all reviews."""
    return db.query(Review).all()

@router.get("/review/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    """Fetch a specific review by its ID."""
    review = get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.get("/product/{product_id}", response_model=list[ReviewResponse])
def get_reviews_for_product(product_id: int, db: Session = Depends(get_db)):
    """Fetch all reviews for a specific product."""
    reviews = get_reviews_by_product(db, product_id)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this product")
    return reviews

@router.get("/user/{user_id}", response_model=list[ReviewResponse])
def get_reviews_for_user(user_id: int, db: Session = Depends(get_db)):
    """Fetch all reviews made by a specific user."""
    reviews = get_reviews_by_user(db, user_id)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this user")
    return reviews
