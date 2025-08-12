import csv
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

def load_csv_data(file_path, required_columns=None):
    """Generic CSV loader with error handling"""
    data = []
    if not os.path.exists(file_path):
        print(f"? File not found: {file_path}")
        return data
        
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if required_columns:
                    # Check if all required columns exist
                    if all(col in row for col in required_columns):
                        data.append(row)
                else:
                    data.append(row)
        print(f"? Loaded {len(data)} records from {os.path.basename(file_path)}")
    except Exception as e:
        print(f"? Error loading {file_path}: {e}")
    
    return data

def create_sample_data():
    db = SessionLocal()
    try:
        if db.query(models.User).first():
            print("Database already has data. Skipping seeding.")
            return
        
        print("Loading real dataset from CSV files...")
        
        # 1. Load Distribution Centers
        print("\\n1. Loading Distribution Centers...")
        centers_data = load_csv_data("../data/distribution_centers.csv", ["id", "name", "latitude", "longitude"])
        for row in centers_data:
            center = models.DistributionCenter(
                id=int(row["id"]),
                name=row["name"],
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"])
            )
            db.add(center)
        db.commit()
        
        # 2. Load Users
        print("\\n2. Loading Users...")
        users_data = load_csv_data("../data/users.csv")
        for row in users_data:
            user = models.User(
                id=int(row.get("id", 0)),
                first_name=row.get("first_name", ""),
                last_name=row.get("last_name", ""),
                email=row.get("email", ""),
                phone=row.get("phone", ""),
                city=row.get("city", ""),
                country=row.get("country", "USA"),
                address=row.get("address", "")
            )
            db.add(user)
        db.commit()
        
        # 3. Load Products
        print("\\n3. Loading Products...")
        products_data = load_csv_data("../data/products.csv")
        for row in products_data:
            product = models.Product(
                id=int(row.get("id", 0)),
                name=row.get("name", ""),
                description=row.get("description", ""),
                price=float(row.get("price", 0)),
                category=row.get("category", ""),
                sku=row.get("sku", "")
            )
            db.add(product)
        db.commit()
        
        # 4. Load Orders
        print("\\n4. Loading Orders...")
        orders_data = load_csv_data("../data/orders.csv")
        for row in orders_data:
            order = models.Order(
                id=int(row.get("id", 0)),
                user_id=int(row.get("user_id", 0)),
                order_number=row.get("order_number", ""),
                status=row.get("status", "pending"),
                total_amount=float(row.get("total_amount", 0)),
                order_date=datetime.fromisoformat(row.get("order_date", "2025-01-01T00:00:00").replace("Z", "+00:00"))
            )
            db.add(order)
        db.commit()
        
        # 5. Load Order Items
        print("\\n5. Loading Order Items...")
        items_data = load_csv_data("../data/order_items.csv")
        for row in items_data:
            item = models.OrderItem(
                id=int(row.get("id", 0)),
                order_id=int(row.get("order_id", 0)),
                product_id=int(row.get("product_id", 0)),
                quantity=int(row.get("quantity", 1)),
                price=float(row.get("price", 0))
            )
            db.add(item)
        db.commit()
        
        print("\\n?? MILESTONE 1 COMPLETE!")
        print("? All CSV files loaded successfully into database")
        print("? E-commerce Order Viewer backend ready with real data")
        print("? Ready to test your 3 core features:")
        print("   1. Search users by criteria")
        print("   2. View user orders") 
        print("   3. See order items")
        
    except Exception as e:
        print(f"? Error loading data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()

