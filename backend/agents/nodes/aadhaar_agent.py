from backend.aadhaar.aadhaar_service import process_aadhaar

def aadhaar_agent(state):
    out = process_aadhaar(state.aadhaar_bytes)
    state.aadhaar_data = out
    return state
