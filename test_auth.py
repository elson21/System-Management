#!/usr/bin/env python3
"""
Test script for the authentication system.
This script tests the core authentication functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token
)

def test_password_hashing():
    """Test password hashing and verification."""
    print("Testing password hashing...")
    
    # Test password
    test_password = "testpassword123"
    
    # Hash the password
    hashed = get_password_hash(test_password)
    print(f"✓ Password hashed successfully: {hashed[:20]}...")
    
    # Verify the password
    is_valid = verify_password(test_password, hashed)
    print(f"✓ Password verification: {'PASS' if is_valid else 'FAIL'}")
    
    # Test wrong password
    is_valid_wrong = verify_password("wrongpassword", hashed)
    print(f"✓ Wrong password rejection: {'PASS' if not is_valid_wrong else 'FAIL'}")
    
    return True

def test_jwt_tokens():
    """Test JWT token creation and verification."""
    print("\nTesting JWT tokens...")
    
    # Test data
    test_email = "test@example.com"
    
    # Create token
    token = create_access_token(data={"sub": test_email})
    print(f"✓ Token created successfully: {token[:20]}...")
    
    # Verify token
    verified_email = verify_token(token)
    print(f"✓ Token verification: {'PASS' if verified_email == test_email else 'FAIL'}")
    
    # Test invalid token
    invalid_email = verify_token("invalid.token.here")
    print(f"✓ Invalid token rejection: {'PASS' if invalid_email is None else 'FAIL'}")
    
    return True

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from app.db.session import SessionLocal
        print("✓ Database session imported successfully")
    except ImportError as e:
        print(f"✗ Database session import failed: {e}")
        return False
    
    try:
        from app.db.db_models.user import User
        print("✓ User model imported successfully")
    except ImportError as e:
        print(f"✗ User model import failed: {e}")
        return False
    
    try:
        from app.auth import authenticate_user, get_current_user
        print("✓ Authentication functions imported successfully")
    except ImportError as e:
        print(f"✗ Authentication functions import failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🔐 Authentication System Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Password Hashing Test", test_password_hashing),
        ("JWT Token Test", test_jwt_tokens),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Authentication system is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
