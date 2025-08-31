from app.db.session import SessionLocal
from app.db.db_models import User, Organization


def add_user():
    with SessionLocal() as db:
        organization = db.query(Organization).first()
        if not organization:
            print("Create an organization.")
            return
        
        users = [
            {"first_name": "User2", "last_name": "Test2", "email": "user2.test2@email.com"},
            {"first_name": "User3", "last_name": "Test3", "email": "user3.test3@email.com"},
            {"first_name": "User4", "last_name": "Test4", "email": "user4.test4@email.com"},
            {"first_name": "User5", "last_name": "Test5", "email": "user5.test5@email.com"},
            {"first_name": "User6", "last_name": "Test6", "email": "user6.test6@email.com"}
        ]

        user_count = 0

        for user in users:
            user = User(
                first_name = user["first_name"],
                last_name = user["last_name"],
                email = user["email"],
                organization_id = organization.id
            )

            db.add(user)
            user_count += 1

        print(f"Added {user_count} users")
        db.commit()


if __name__ == "__main__":
    add_user()