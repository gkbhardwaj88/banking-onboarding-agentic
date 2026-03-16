from sqlalchemy import Column, Integer, String, ForeignKey
from backend.db.session import Base

class AadhaarRecord(Base):
    __tablename__ = "aadhaar_records"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    aadhaar_number_enc = Column(String)
    name = Column(String)
    dob = Column(String)
    address = Column(String)
