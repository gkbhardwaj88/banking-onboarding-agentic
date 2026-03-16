from sqlalchemy import Column, Integer, String, ForeignKey
from backend.db.session import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    amount = Column(Integer)
    method = Column(String)
