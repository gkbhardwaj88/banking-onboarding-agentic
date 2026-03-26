from fastapi import APIRouter, UploadFile, File
from backend.agents.workflow import run_workflow
from backend.aadhaar.aadhaar_service import validate_aadhaar_number, generate_aadhaar_otp, submit_aadhaar_otp

router = APIRouter(prefix="/kyc", tags=["KYC"])

@router.post("/process")
async def process(aadhaar: UploadFile = File(None), pan: UploadFile = File(None)):
    aadhaar_bytes = await aadhaar.read() if aadhaar else None
    pan_bytes = await pan.read() if pan else None
    state = run_workflow(aadhaar_bytes, pan_bytes, [], "SAVINGS")
    return state


@router.post("/aadhaar/validate")
def validate_aadhaar(id_number: str):
    return validate_aadhaar_number(id_number)


@router.post("/aadhaar/generate-otp")
def aadhaar_generate_otp(id_number: str):
    return generate_aadhaar_otp(id_number)


@router.post("/aadhaar/submit-otp")
def aadhaar_submit_otp(client_id: str, otp: str):
    return submit_aadhaar_otp(client_id, otp)
