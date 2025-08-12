from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    sku: str

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    order_number: str
    status: str
    total_amount: float
    order_date: datetime

class Order(OrderBase):
    id: int
    user_id: int
    user: User

    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    quantity: int
    price: float

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    product_id: int
    product: Product

    class Config:
        from_attributes = True

