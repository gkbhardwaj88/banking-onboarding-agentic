from backend.db.session import SessionLocal
from backend.db.models.user import User

class UserRepo:
    def create(self, name, email, pwd):
        db = SessionLocal()
        user = User(name=name, email=email, password_hash=pwd)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
