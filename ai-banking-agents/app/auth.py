import datetime
from jose import jwt
from passlib.context import CryptContext
from .config import JWT_SECRET, JWT_ALGO
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pw(pw): return pwd.hash(pw)

def verify_pw(pw, h): return pwd.verify(pw, h)

def create_token(sub, minutes=1440):
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    return jwt.encode({"sub": sub, "exp": exp}, JWT_SECRET, algorithm=JWT_ALGO)
