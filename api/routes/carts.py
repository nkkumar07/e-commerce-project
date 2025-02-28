from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.carts import CartCreate, CartUpdate, CartResponse, CartUpdateResponse
from api.crud.carts import add_to_cart, get_cart_items, update_cart_item

router = APIRouter()

@router.post("/add", response_model=CartResponse)
def add(cart: CartCreate, db: Session = Depends(get_db)):
    """Adds a product to the cart."""
    return add_to_cart(db, cart)

@router.get("/{user_id}", response_model=list[CartResponse])
def get_cart(user_id: int, db: Session = Depends(get_db)):
    """Fetch all cart items for a specific user."""
    cart_items = get_cart_items(db, user_id)
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")
    return cart_items

@router.put("/{cart_item_id}", response_model=CartUpdateResponse)
def update_cart(cart_item_id: int, cart: CartUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing cart item.
    This endpoint updates only the product_id and quantity of the cart item.
    The user_id will remain unchanged and will not be shown in the response.
    """
    updated_cart = update_cart_item(db, cart_item_id, cart)
    if not updated_cart:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_cart
