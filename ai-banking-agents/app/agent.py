from typing import Any, Dict
from .services import ocr, pan, aadhaar, payment

def decide(state: Dict[str, Any]) -> Dict[str, Any]:
    if not state:
        return {"action":"idle","message":"No state"}
    if not state.get("pan_number"):
        return {"action":"ocr_pan","tool":"ocr_pan","params":{}}
    if not state.get("aadhaar_verified") and state.get("aadhaar_number"):
        return {"action":"validate_aadhaar","tool":"validate_aadhaar","params":{"id_number":state["aadhaar_number"]}}
    if state.get("kyc_ok"):
        return {"action":"create_payment_order","tool":"create_payment_order","params":{"amount_paise": state.get("deposit_amount",100000)}}
    return {"action":"idle","tool":None,"params":{}}


def run_tool(name:str, params:Dict[str,Any]):
    if name == "ocr_pan":
        txt = ocr.pan_ocr(params.get("pan_bytes", b""))
        parsed = pan.parse_pan(txt.get("fallback_text",""))
        return {"ocr": txt, "parsed": parsed}
    if name == "validate_aadhaar":
        return aadhaar.validate(params["id_number"])
    if name == "generate_otp":
        return aadhaar.generate_otp(params["id_number"])
    if name == "submit_otp":
        return aadhaar.submit_otp(params["client_id"], params["otp"])
    if name == "create_payment_order":
        return payment.create_order(params.get("amount_paise",0))
    return {"error":"unknown_tool"}
