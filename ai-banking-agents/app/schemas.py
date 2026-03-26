from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AgentNext(BaseModel):
    session_id: str
    state: dict

class ToolCall(BaseModel):
    tool: str
    params: dict
