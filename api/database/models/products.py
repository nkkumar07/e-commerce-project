from enum import Enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import relationship
from api.database.connection import Base

# Enum for Product Status
class ProductStatus(str, Enum):
    AVAILABLE = "Y"
    NOT_AVAILABLE = "N"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)  
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255), nullable=False)
    mrp = Column(Float, nullable=False)  
    net_price = Column(Float, nullable=False)  
    stock = Column(Integer, nullable=False)
    status = Column(SQLEnum(ProductStatus), default=ProductStatus.AVAILABLE, nullable=False)  
    image = Column(String(255), nullable=True)  
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship with Category
    category = relationship("Category", back_populates="products") 

    # Relationship with Cart
    cart_items = relationship("Cart", back_populates="product")  
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")

    # Automatically update status when stock is zero
    def update_status_based_on_stock(self):
        if self.stock <= 0:
            self.status = ProductStatus.NOT_AVAILABLE
        else:
            self.status = ProductStatus.AVAILABLE
