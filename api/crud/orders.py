from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from api.database.models.orders import Order
from api.database.schemas.orders import OrderCreate, OrderUpdate,OrderResponse

# Create a new order
def create_order(db: Session, order: OrderCreate):
    """Adds a new order to the database."""
    db_order = Order(
        user_id=order.user_id,
        subtotal=order.subtotal,
        discount=order.discount,
        total=order.total,
        status=order.status,
        shipping_address=order.shipping_address
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_all_orders(db: Session):
    """Fetch all orders from the database."""
    return db.query(Order).all()


# Get Order by ID
def get_order_by_id(db: Session, order_id: int):
    """Fetch an order by its ID."""
    return db.query(Order).filter(Order.id == order_id).first()

# Update Order by ID
def update_order(db: Session, order_id: int, order_data: OrderUpdate):
    """Update an existing order by ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None  # Order not found

    for attr, value in order_data.dict(exclude_unset=True).items():
        setattr(order, attr, value)

    db.commit()
    db.refresh(order)
    return order

# Get latest 5 orders
def get_latest_five_orders(db: Session):
    """Fetch the latest 5 orders."""
    return db.query(Order).order_by(Order.created_at.desc()).limit(5).all()

# Get last month's revenue
def get_last_month_revenue(db: Session):
    """Calculate revenue from last month's orders (sum of total column)."""
    today = datetime.today()
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_last_month = today.replace(day=1) - timedelta(days=1)

    revenue = db.query(func.sum(Order.total)).filter(
        Order.created_at >= first_day_last_month,
        Order.created_at <= last_day_last_month
    ).scalar()

    return revenue if revenue else 0

# Get last 3 months' revenue
def get_last_three_months_revenue(db: Session):
    """Calculate total revenue for the last 3 months."""
    today = datetime.today()
    first_day_three_months_ago = (today.replace(day=1) - timedelta(days=90)).replace(day=1)

    revenue = db.query(func.sum(Order.total)).filter(
        Order.created_at >= first_day_three_months_ago,
        Order.created_at <= today
    ).scalar()

    return revenue if revenue else 0

# Get orders delivered on a specific date
def get_orders_delivered_on_date(db: Session, delivery_date: datetime):
    """Fetch all orders that were delivered on a specific date."""
    return db.query(Order).filter(
        func.date(Order.created_at) == delivery_date.date(),
        Order.status == "delivered"
    ).all()

# Get current pending orders list
def get_pending_orders(db: Session):
    """Fetch all orders that are currently pending."""
    return db.query(Order).filter(Order.status == "pending").all()

# Get all delivered orders
def get_delivered_orders(db: Session):
    """Fetch all delivered orders."""
    return db.query(Order).filter(Order.status == "delivered").all()


