from sqlalchemy import Column, Integer, String, JSON, Boolean
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

class KYCState(Base):
    __tablename__ = "kyc_states"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), unique=True, index=True)
    aadhaar_number = Column(String(20))
    pan_number = Column(String(20))
    aadhaar_verified = Column(Boolean, default=False)
    kyc_ok = Column(Boolean, default=False)
    selfie_ok = Column(Boolean, default=False)
    account_type = Column(String(20))
    deposit_amount = Column(Integer)  # paise
    payment_order = Column(JSON)
    pan_ocr = Column(JSON)
    aadhaar_ocr = Column(JSON)
