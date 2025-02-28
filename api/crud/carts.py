from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.database.models.carts import Cart
from api.database.schemas.carts import CartCreate, CartUpdate

def add_to_cart(db: Session, cart: CartCreate):
    """Adds a product to the user's cart."""
    db_cart = Cart(
        user_id=cart.user_id,
        product_id=cart.product_id,
        quantity=cart.quantity
    )
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def get_cart_items(db: Session, user_id: int):
    """Fetch all cart items for a specific user."""
    return db.query(Cart).filter(Cart.user_id == user_id).all()

def update_cart_item(db: Session, cart_item_id: int, cart: CartUpdate):
    """Updates an existing cart item."""
    db_cart = db.query(Cart).filter(Cart.id == cart_item_id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart item not found")
    

    if cart.product_id is not None:
        db_cart.product_id = cart.product_id
    if cart.quantity is not None:
        db_cart.quantity = cart.quantity

    db.commit()
    db.refresh(db_cart)
    return db_cart
