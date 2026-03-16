from fastapi import APIRouter
from backend.agents.nodes.assistant_agent import assistant_agent

router = APIRouter(prefix="/assistant", tags=["Assistant"])

@router.post("/chat")
def chat(msg: str):
    return {"response": assistant_agent(msg)}
