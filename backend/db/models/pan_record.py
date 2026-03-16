from sqlalchemy import Column, Integer, String, ForeignKey
from backend.db.session import Base

class PANRecord(Base):
    __tablename__ = "pan_records"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pan_number_enc = Column(String)
    name = Column(String)
