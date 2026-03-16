from fastapi import APIRouter, HTTPException
from backend.security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

fake_users = {"test@example.com": "hashedpwd"}

@router.post("/login")
def login(email: str, password: str):
    if email not in fake_users:
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": email})
    return {"access_token": token}
