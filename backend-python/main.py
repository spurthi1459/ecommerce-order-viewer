from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from dotenv import load_dotenv

from app.database import SessionLocal, engine
from app import models, schemas, crud

load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Order Viewer API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "E-commerce Order Viewer API is running!"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "API is working properly"}

# User search endpoint
@app.get("/api/users/search", response_model=List[schemas.User])
def search_users(
    email: Optional[str] = Query(None),
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    users = crud.search_users(db, email=email, first_name=first_name, 
                            last_name=last_name, city=city)
    return users

# User orders endpoint
@app.get("/api/users/{user_id}/orders", response_model=List[schemas.Order])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    orders = crud.get_user_orders(db, user_id=user_id)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders

# Order items endpoint
@app.get("/api/orders/{order_id}/items", response_model=List[schemas.OrderItem])
def get_order_items(order_id: int, db: Session = Depends(get_db)):
    items = crud.get_order_items(db, order_id=order_id)
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this order")
    return items

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

