from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from . import models

def search_users(db: Session, email: Optional[str] = None, 
                first_name: Optional[str] = None, 
                last_name: Optional[str] = None, 
                city: Optional[str] = None) -> List[models.User]:
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
    
    if filters:
        query = query.filter(or_(*filters))
    
    return query.limit(50).all()

def get_user_orders(db: Session, user_id: int) -> List[models.Order]:
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()

def get_order_items(db: Session, order_id: int) -> List[models.OrderItem]:
    return db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()

