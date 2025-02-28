from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from api.database.connection import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationship with Product
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
