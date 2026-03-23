from backend.pan.pan_service import process_pan
from backend.ocr.smart_ocr_router import extract_text

def pan_agent(state):
    # Run OCR on the PAN image directly (don't rely on Aadhaar OCR)
    pan_ocr = extract_text(state.pan_bytes) if state.pan_bytes else {"error": "No PAN uploaded"}
    state.pan_ocr_text = pan_ocr

    if pan_ocr.get("error"):
        state.pan_data = {"error": pan_ocr.get("error"), "details": pan_ocr.get("details")}
        return state

    fields = process_pan(pan_ocr.get("fallback_text",""))
    state.pan_data = fields
    return state
