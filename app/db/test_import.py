import sys
sys.path.append(".")

try:
    from app.db.models import User
    print("From app.db.models import User.")
except Exception as e:
    print(f"Failed to import User from app.db.models: {e}")


try:
    from models import User
    print("From models import User.")
except Exception as e:
    print(f"Failed to import User from models: {e}")