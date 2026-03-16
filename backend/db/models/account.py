from sqlalchemy import Column, Integer, String, ForeignKey
from backend.db.session import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_type = Column(String)
    account_number = Column(String)
