from enum import Enum

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class ProductStatus(str, Enum):
    AVAILABLE = "Y"
    NOT_AVAILABLE = "N"