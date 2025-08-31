#!/usr/bin/env python3
"""
Script to create the first admin user for the System Management application.
This script should be run once to set up the initial administrator account.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.db_models import User, Organization
from app.auth import get_password_hash

def create_admin_user():
    """Create the first admin user."""
    print("🔐 Creating First Admin User")
    print("=" * 40)
    
    # Get user input
    print("\nPlease provide the details for the admin user:")
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    email = input("Email Address: ").strip()
    
    while True:
        password = input("Password (min 8 characters): ").strip()
        if len(password) >= 8:
            confirm_password = input("Confirm Password: ").strip()
            if password == confirm_password:
                break
            else:
                print("❌ Passwords do not match. Please try again.")
        else:
            print("❌ Password must be at least 8 characters long.")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.is_admin == True).first()
        if existing_admin:
            print(f"\n⚠️  Admin user already exists: {existing_admin.email}")
            response = input("Do you want to create another admin user? (y/N): ").strip().lower()
            if response != 'y':
                print("Operation cancelled.")
                return
        
        # Check if user with this email already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"❌ User with email {email} already exists.")
            return
        
        # Get or create organization
        organization = db.query(Organization).first()
        if not organization:
            organization = Organization(name="Default Organization")
            db.add(organization)
            db.commit()
            db.refresh(organization)
            print(f"✓ Created organization: {organization.name}")
        
        # Hash the password
        hashed_password = get_password_hash(password)
        
        # Create admin user
        admin_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hashed_password,
            organization_id=organization.id,
            is_admin=True,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"\n✅ Admin user created successfully!")
        print(f"   Name: {first_name} {last_name}")
        print(f"   Email: {email}")
        print(f"   Admin: Yes")
        print(f"   Active: Yes")
        print(f"\nYou can now log in to the system using these credentials.")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main function."""
    print("System Management - Admin User Creation")
    print("=" * 50)
    print("This script will create the first administrator user for your system.")
    print("Only run this script once to set up the initial admin account.")
    print()
    
    response = input("Do you want to continue? (y/N): ").strip().lower()
    if response == 'y':
        create_admin_user()
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()
