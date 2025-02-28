from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.crud.orders import (
    get_latest_five_orders,
    get_last_month_revenue,
    get_last_three_months_revenue,
    get_pending_orders,
    get_delivered_orders,
)

router = APIRouter()

@router.get("/dashboard/")
def fetch_dashboard_analytics(db: Session = Depends(get_db)):
    """
    Fetch dashboard analytics data in a single response.
    """
    return {
        "last_five_orders": get_latest_five_orders(db),
        "last_month_revenue": get_last_month_revenue(db),
        "last_three_months_revenue": get_last_three_months_revenue(db),
        "current_pending_orders": get_pending_orders(db),
        "delivered_products": get_delivered_orders(db),
    }
