from app.auth import get_password_hash
from app.db.session import SessionLocal
from app.db.db_models import User

db = SessionLocal()

user_passwords = {
    "user2.test2@email.com": "password2",
    "user3.test3@email.com": "password3",
    "user4.test4@email.com": "password4",
    "user5.test5@email.com": "password5"
}

for email, password in user_passwords.items():
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.password_hash = get_password_hash(password)
        print(f"Update password for {email}")

db.commit()
db.close()