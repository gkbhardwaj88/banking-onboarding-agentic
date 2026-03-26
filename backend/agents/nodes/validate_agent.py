def validate_agent(state):
    ok = True
    if state.aadhaar_data and state.aadhaar_data.get("error"):
        ok=True
    if state.pan_data and state.pan_data.get("error"):
        ok=True
    state.validation_ok = ok
    return state
