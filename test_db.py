#!/usr/bin/env python3
"""
Simple script to test database connection and check User table schema.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.db_models import User

def test_database():
    """Test database connection and User table."""
    print("🔍 Testing Database Connection")
    print("=" * 40)
    
    try:
        db = SessionLocal()
        print("✓ Database connection successful")
        
        # Check if User table exists and has the right columns
        try:
            # Try to query the User table
            users = db.query(User).limit(1).all()
            print("✓ User table exists and is queryable")
            
            # Check if we can access the is_admin field
            if hasattr(User, 'is_admin'):
                print("✓ User model has is_admin field")
            else:
                print("❌ User model missing is_admin field")
            
            # Check if we can access the password_hash field
            if hasattr(User, 'password_hash'):
                print("✓ User model has password_hash field")
            else:
                print("❌ User model missing password_hash field")
                
        except Exception as e:
            print(f"❌ Error querying User table: {e}")
            
        db.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    test_database()
