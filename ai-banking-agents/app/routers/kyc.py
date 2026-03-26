from fastapi import APIRouter, UploadFile, File
from ..services import ocr, pan, aadhaar
router = APIRouter(prefix="/kyc", tags=["KYC"])

@router.post("/pan/ocr")
async def pan_ocr(file: UploadFile = File(...)):
    data = await file.read()
    txt = ocr.pan_ocr(data)
    parsed = pan.parse_pan(txt.get("fallback_text",""))
    return {"ocr": txt, "parsed": parsed}

@router.post("/aadhaar/validate")
def aadhaar_validate(id_number: str):
    return aadhaar.validate(id_number)

@router.post("/aadhaar/generate-otp")
def aadhaar_generate(id_number: str):
    return aadhaar.generate_otp(id_number)

@router.post("/aadhaar/submit-otp")
def aadhaar_submit(client_id: str, otp: str):
    return aadhaar.submit_otp(client_id, otp)
