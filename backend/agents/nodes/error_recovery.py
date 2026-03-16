def error_recovery(state):
    return {"error": "KYC failed", "details": state.to_response()}
