from fastapi import Request, HTTPException
from backend.security.jwt import decode_token

async def auth_guard(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(401, "Missing token")
    try:
        decode_token(token.replace("Bearer ", ""))
    except:
        raise HTTPException(401, "Invalid token")
