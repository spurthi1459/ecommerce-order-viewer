from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

# Distribution Center Schemas
class DistributionCenterBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class DistributionCenter(DistributionCenterBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

# User Schemas
class UserBase(BaseModel):
    email: str = Field(..., description="User email address")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    phone: Optional[str] = Field(None, description="Phone number")
    address: Optional[str] = Field(None, description="Address")
    city: Optional[str] = Field(None, description="City")
    country: Optional[str] = Field(None, description="Country")

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class UserSearch(BaseModel):
    email: Optional[str] = Field(None, description="Search by email (partial match)")
    first_name: Optional[str] = Field(None, description="Search by first name (partial match)")
    last_name: Optional[str] = Field(None, description="Search by last name (partial match)")
    city: Optional[str] = Field(None, description="Search by city (partial match)")
    phone: Optional[str] = Field(None, description="Search by phone (partial match)")

# Product Schemas
class ProductBase(BaseModel):
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., description="Product price")
    category: Optional[str] = Field(None, description="Product category")
    sku: str = Field(..., description="Stock keeping unit")

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

# Order Item Schemas
class OrderItemBase(BaseModel):
    quantity: int = Field(..., description="Quantity ordered")
    price: float = Field(..., description="Price per unit at time of order")

class OrderItem(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    order_id: int
    product_id: int
    product: Product

class OrderItemSummary(BaseModel):
    order_id: int
    items: List[OrderItem]
    summary: dict = Field(..., description="Summary with totals and counts")

# Order Schemas
class OrderBase(BaseModel):
    order_number: str = Field(..., description="Unique order number")
    status: str = Field(..., description="Order status (pending, completed, shipped, etc.)")
    total_amount: float = Field(..., description="Total order amount")
    order_date: datetime = Field(..., description="Order date and time")

class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    distribution_center_id: Optional[int]
    distribution_center: Optional[DistributionCenter]

class OrderWithItems(Order):
    order_items: List[OrderItem]

class OrderWithUser(Order):
    user: User

# Response Schemas
class UserOrderSummary(BaseModel):
    user_id: int
    total_orders: int
    total_spent: float
    orders: List[Order]
    latest_order_date: Optional[datetime]

class DatabaseStats(BaseModel):
    users_count: int
    orders_count: int
    products_count: int
    order_items_count: int
    distribution_centers_count: int

class SearchResult(BaseModel):
    results: List[User]
    total_count: int
    page: int
    limit: int

# Health Check Schema
class HealthCheck(BaseModel):
    status: str = Field(..., description="API status")
    message: str = Field(..., description="Status message")
    timestamp: datetime = Field(..., description="Current timestamp")
    database_stats: Optional[DatabaseStats] = Field(None, description="Database statistics")

