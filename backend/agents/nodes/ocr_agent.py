from backend.ocr.smart_ocr_router import extract_text

def ocr_agent(state):
    if state.aadhaar_bytes:
        txt = extract_text(state.aadhaar_bytes)
    elif state.pan_bytes:
        txt = extract_text(state.pan_bytes)
    else:
        txt = {"error": "No documents uploaded"}
    state.ocr_text = txt
    return state
