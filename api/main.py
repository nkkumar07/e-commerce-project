from fastapi import FastAPI
from api.routes import address, auth, carts, users, products, categories, orders, reviews,analytics
from api.database.connection import engine
from api.database.base import Base

# Create all database tables if they don't already exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Include authentication-related routes (Login, Signup, Token handling, etc.)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Include user-related routes (Profile management, User details, etc.)
app.include_router(users.router, prefix="/users", tags=["Users"])

# Include product-related routes (CRUD operations for products)
app.include_router(products.router, prefix="/products", tags=["Products"])

# Include category-related routes (Manage product categories)
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

# Include address-related routes (User address management)
app.include_router(address.router, prefix="/addresses", tags=["Addresses"])

# Include cart-related routes (Manage shopping cart)
app.include_router(carts.router, prefix="/carts", tags=["Carts"])

# Include order-related routes (Order placement, tracking, history, etc.)
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

# Include review-related routes (Product reviews & ratings)
app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])

# Change from "dashboard" to "analytics"
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])