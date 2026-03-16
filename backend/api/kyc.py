from fastapi import APIRouter, UploadFile, File
from backend.agents.workflow import run_workflow

router = APIRouter(prefix="/kyc", tags=["KYC"])

@router.post("/process")
async def process(aadhaar: UploadFile = File(None), pan: UploadFile = File(None)):
    aadhaar_bytes = await aadhaar.read() if aadhaar else None
    pan_bytes = await pan.read() if pan else None
    state = run_workflow(aadhaar_bytes, pan_bytes, [], "SAVINGS")
    return state
