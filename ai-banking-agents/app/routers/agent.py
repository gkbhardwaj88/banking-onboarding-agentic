from fastapi import APIRouter
from pydantic import BaseModel
from .. import agent

router = APIRouter(prefix="/agent", tags=["Agent"])

class AgentReq(BaseModel):
    session_id: str
    state: dict

class ToolReq(BaseModel):
    tool: str
    params: dict

@router.post("/next")
def next_action(req: AgentReq):
    return agent.decide(req.state)

@router.post("/tool")
def call_tool(req: ToolReq):
    return agent.run_tool(req.tool, req.params)
