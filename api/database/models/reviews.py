from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from api.database.connection import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # Rating should be an integer (1-5)
    review_text = Column(String(500), nullable=True)  # User's review text
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="reviews")
    order = relationship("Order", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
