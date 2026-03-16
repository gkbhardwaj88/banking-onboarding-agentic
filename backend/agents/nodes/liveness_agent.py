from backend.liveness.liveness_service import liveness_check

def liveness_agent(state):
    if state.selfie_frames and state.aadhaar_data.get("photo"):
        res = liveness_check(state.selfie_frames, state.aadhaar_data["photo"])
        state.liveness = res
    return state
