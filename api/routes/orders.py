from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.orders import OrderCreate, OrderUpdate, OrderResponse
from api.crud.orders import create_order, update_order, get_order_by_id, get_all_orders

# Create API router
router = APIRouter()

# Create a new order (POST)
@router.post("/add", response_model=OrderResponse)
def add_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)

# Update an existing order (PUT)
@router.put("/update/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    updated_order = update_order(db, order_id, order_data)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

# Get all orders (GET)
@router.get("/orders", response_model=list[OrderResponse])
def fetch_all_orders(db: Session = Depends(get_db)):
    return get_all_orders(db)


# Get a specific order by ID (GET)
@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

