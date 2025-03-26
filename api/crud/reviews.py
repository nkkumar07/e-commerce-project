from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from api.database.models.reviews import Review
from api.database.schemas.reviews import ReviewCreate

def create_review(db: Session, review: ReviewCreate):
    """
    Creates a new review.
    """

    # Validate if rating is within the range (should not be necessary due to Pydantic)
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )

    # Create the review
    db_review = Review(
        user_id=review.user_id,
        order_id=review.order_id,
        product_id=review.product_id,
        rating=review.rating,
        review_text=review.review_text,
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review

def get_all_reviews(db: Session):
    """Fetch all reviews."""
    return db.query(Review).all()


def get_review_by_id(db: Session, review_id: int):
    """Fetch a specific review by its ID."""
    return db.query(Review).filter(Review.id == review_id).first()


def get_reviews_by_user(db: Session, user_id: int):
    """
    Fetch all reviews made by a specific user.
    """
    return db.query(Review).filter(Review.user_id == user_id).all()


def get_reviews_by_product(db: Session, product_id: int):
    """Fetch all reviews for a specific product."""
    return db.query(Review).filter(Review.product_id == product_id).all()

