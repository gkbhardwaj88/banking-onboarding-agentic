from sqlalchemy import Column, Integer, String, ForeignKey
from backend.db.session import Base

class KYCSession(Base):
    __tablename__ = "kyc_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)
