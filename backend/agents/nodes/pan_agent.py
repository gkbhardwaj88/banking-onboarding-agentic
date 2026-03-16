from backend.pan.pan_service import process_pan

def pan_agent(state):
    if state.ocr_text and state.ocr_text.get("error"):
        state.pan_data = {"error": state.ocr_text["error"], "details": state.ocr_text.get("details")}
        return state

    fields = process_pan(state.ocr_text.get("fallback_text",""))
    state.pan_data = fields
    return state
