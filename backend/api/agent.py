from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.agent import agent_tools

router = APIRouter(prefix="/agent", tags=["Agent"])


class AgentRequest(BaseModel):
    session_id: str
    state: dict
    pan_bytes_present: bool = False
    aadhaar_number: str | None = None


@router.post("/next")
def agent_next(req: AgentRequest):
    decision = agent_tools.decide_next(req.state)
    decision["session_id"] = req.session_id
    agent_tools.log_event(req.session_id, {"type": "decision", "decision": decision})
    return decision


class PanOcrRequest(BaseModel):
    session_id: str
    pan_bytes_b64: str


@router.post("/ocr-pan")
def agent_ocr_pan(req: PanOcrRequest):
    import base64

    try:
        pan_bytes = base64.b64decode(req.pan_bytes_b64)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid base64: {exc}")
    result = agent_tools.tool_ocr_pan(pan_bytes)
    agent_tools.log_event(req.session_id, {"type": "tool", "tool": "ocr_pan", "result": result})
    return result
