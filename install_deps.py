#!/usr/bin/env python3
"""
Script to install authentication dependencies for the System Management application.
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def main():
    """Install required authentication packages."""
    print("Installing authentication dependencies...")
    
    packages = [
        "passlib[bcrypt]",
        "python-jose[cryptography]",
        "python-multipart"
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\nInstallation complete: {success_count}/{len(packages)} packages installed successfully.")
    
    if success_count == len(packages):
        print("✓ All dependencies installed successfully!")
        print("You can now run your application with authentication enabled.")
    else:
        print("⚠ Some packages failed to install. Please check the errors above.")
        print("You may need to install them manually or check your Python environment.")

if __name__ == "__main__":
    main()
