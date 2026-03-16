def document_intake(state, aadhaar_bytes=None, pan_bytes=None):
    state.aadhaar_bytes=aadhaar_bytes
    state.pan_bytes=pan_bytes
    return state
