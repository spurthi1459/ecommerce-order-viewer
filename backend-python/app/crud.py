from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from . import models, schemas
from typing import List, Optional

# User CRUD Operations
def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """Get a single user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email address"""
    return db.query(models.User).filter(models.User.email == email).first()

def search_users(db: Session,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None,
                city: Optional[str] = None,
                phone: Optional[str] = None,
                skip: int = 0,
                limit: int = 100) -> List[models.User]:
    """Advanced user search with multiple criteria support"""
    query = db.query(models.User)
    filters = []

    if email:
        filters.append(models.User.email.ilike(f"%{email}%"))
    if first_name:
        filters.append(models.User.first_name.ilike(f"%{first_name}%"))
    if last_name:
        filters.append(models.User.last_name.ilike(f"%{last_name}%"))
    if city:
        filters.append(models.User.city.ilike(f"%{city}%"))
    if phone:
        filters.append(models.User.phone.ilike(f"%{phone}%"))

    if filters:
        query = query.filter(or_(*filters))

    return query.offset(skip).limit(limit).all()

def get_users_count(db: Session) -> int:
    """Get total count of users"""
    return db.query(models.User).count()

# Order CRUD Operations
def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[models.Order]:
    """Get all orders for a specific user with related data"""
    return db.query(models.Order).options(joinedload(models.Order.distribution_center)).filter(models.Order.user_id == user_id).order_by(models.Order.order_date.desc()).offset(skip).limit(limit).all()

def get_order_by_id(db: Session, order_id: int) -> Optional[models.Order]:
    """Get single order with all related data"""
    return db.query(models.Order).options(joinedload(models.Order.user), joinedload(models.Order.distribution_center), joinedload(models.Order.order_items).joinedload(models.OrderItem.product)).filter(models.Order.id == order_id).first()

def get_orders_by_status(db: Session, status: str, limit: int = 100) -> List[models.Order]:
    """Get orders by status"""
    return db.query(models.Order).filter(models.Order.status == status).order_by(models.Order.order_date.desc()).limit(limit).all()

# Order Items CRUD Operations
def get_order_items(db: Session, order_id: int) -> List[models.OrderItem]:
    """Get all items for a specific order with product details"""
    return db.query(models.OrderItem).options(joinedload(models.OrderItem.product)).filter(models.OrderItem.order_id == order_id).all()

def get_order_items_with_totals(db: Session, order_id: int):
    """Get order items with calculated totals"""
    items = get_order_items(db, order_id)
    total_items = sum(item.quantity for item in items)
    total_amount = sum(item.quantity * item.price for item in items)
    
    return {
        "order_id": order_id,
        "items": items,
        "summary": {
            "total_items": total_items,
            "total_amount": round(total_amount, 2),
            "item_count": len(items)
        }
    }

# Product CRUD Operations
def get_product_by_id(db: Session, product_id: int) -> Optional[models.Product]:
    """Get product by ID"""
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products_by_category(db: Session, category: str, limit: int = 50) -> List[models.Product]:
    """Get products by category"""
    return db.query(models.Product).filter(models.Product.category.ilike(f"%{category}%")).limit(limit).all()

def search_products(db: Session,
                   name: Optional[str] = None,
                   category: Optional[str] = None,
                   min_price: Optional[float] = None,
                   max_price: Optional[float] = None,
                   limit: int = 50) -> List[models.Product]:
    """Advanced product search"""
    query = db.query(models.Product)
    
    if name:
        query = query.filter(models.Product.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(models.Product.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    
    return query.limit(limit).all()

# Distribution Center CRUD Operations
def get_distribution_centers(db: Session) -> List[models.DistributionCenter]:
    """Get all distribution centers"""
    return db.query(models.DistributionCenter).all()

def get_distribution_center_by_id(db: Session, center_id: int) -> Optional[models.DistributionCenter]:
    """Get distribution center by ID"""
    return db.query(models.DistributionCenter).filter(models.DistributionCenter.id == center_id).first()

# Analytics and Summary Functions
def get_user_order_summary(db: Session, user_id: int):
    """Get comprehensive order summary for a user"""
    orders = get_user_orders(db, user_id)
    
    if not orders:
        return {
            "user_id": user_id,
            "total_orders": 0,
            "total_spent": 0,
            "orders": []
        }
    
    total_spent = sum(order.total_amount for order in orders)
    
    return {
        "user_id": user_id,
        "total_orders": len(orders),
        "total_spent": round(total_spent, 2),
        "orders": orders,
        "latest_order_date": orders[0].order_date if orders else None
    }

def get_database_stats(db: Session):
    """Get overall database statistics"""
    return {
        "users_count": db.query(models.User).count(),
        "orders_count": db.query(models.Order).count(),
        "products_count": db.query(models.Product).count(),
        "order_items_count": db.query(models.OrderItem).count(),
        "distribution_centers_count": db.query(models.DistributionCenter).count()
    }

