from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from api.database.models.products import Product, ProductStatus
from api.database.schemas.products import ProductCreate, ProductUpdate

# Function for validation
def validate_product_data(mrp: float, net_price: float, stock: int):
    """Ensures that net price and stock have valid values."""
    if net_price > mrp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Net price cannot be higher than MRP."
        )

    if stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock cannot be negative."
        )

# Create Product
def create_product(db: Session, product: ProductCreate):
    """
    Adds a new product to the database.
    """
    # Check if a product with the same name already exists
    if db.query(Product).filter_by(name=product.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists."
        )

    # Validate product data
    validate_product_data(product.mrp, product.net_price, product.stock)

    # Create a new product entry
    db_product = Product(
        category_id=product.category_id,
        name=product.name,
        description=product.description,
        mrp=product.mrp,
        net_price=product.net_price,
        stock=product.stock,
        status=ProductStatus.AVAILABLE if product.stock > 0 else ProductStatus.NOT_AVAILABLE,
        image=product.image if product.image else None,
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

# Delete Product
def delete_product(db: Session, product_id: int):
    """
    Deletes a product by ID.
    """
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )

    db.delete(product)
    db.commit()

    return {"success": True, "message": "Product deleted successfully."}

# Update Product
def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    """
    Updates an existing product.
    """
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )

    # Update only provided fields
    validate_product_data(
        product_data.mrp if product_data.mrp is not None else product.mrp,
        product_data.net_price if product_data.net_price is not None else product.net_price,
        product_data.stock if product_data.stock is not None else product.stock,
    )

    for attr, value in product_data.dict(exclude_unset=True).items():
        setattr(product, attr, value)

    # Automatically update status based on stock
    product.update_status_based_on_stock()

    db.commit()
    db.refresh(product)

    return product

def get_active_products(db: Session):
    """
    Fetches all products with an active status.
    """
    active_products = db.query(Product).filter(Product.status == ProductStatus.AVAILABLE).all()
    return active_products


