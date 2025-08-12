from app.database import SessionLocal
from app import crud

def test_crud_operations():
    """Test CRUD operations"""
    db = SessionLocal()
    try:
        # Test database stats
        stats = crud.get_database_stats(db)
        print("Database Stats:", stats)
        
        # Test user search
        users = crud.search_users(db, first_name="John", limit=5)
        print(f"Found {len(users)} users with first name containing John")
        
        if len(users) > 0:
            print("Sample user:", users[0].first_name, users[0].last_name, users[0].email)
        
        # Test order operations
        if len(users) > 0:
            user_orders = crud.get_user_orders(db, users[0].id, limit=3)
            print(f"User {users[0].id} has {len(user_orders)} orders")
        
        print("? All CRUD functions loaded successfully!")
        return True
        
    except Exception as e:
        print(f"? Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_crud_operations()

