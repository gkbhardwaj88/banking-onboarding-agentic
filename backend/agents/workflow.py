from backend.agents.state import KYCState
from backend.agents.nodes.document_intake import document_intake
from backend.agents.nodes.ocr_agent import ocr_agent
from backend.agents.nodes.aadhaar_agent import aadhaar_agent
from backend.agents.nodes.pan_agent import pan_agent
from backend.agents.nodes.validate_agent import validate_agent
from backend.agents.nodes.liveness_agent import liveness_agent
from backend.agents.nodes.form_builder import form_builder
from backend.agents.nodes.account_agent import account_agent
from backend.agents.nodes.payment_agent import payment_agent
from backend.agents.nodes.error_recovery import error_recovery

def run_workflow(aadhaar_bytes=None, pan_bytes=None, selfie_frames=None, account_type='SAVINGS'):
    state = KYCState()
    state = document_intake(state, aadhaar_bytes, pan_bytes)
    state = ocr_agent(state)

    if aadhaar_bytes:
        state = aadhaar_agent(state)
    if pan_bytes:
        state = pan_agent(state)

    state.selfie_frames = selfie_frames or []
    state = validate_agent(state)
    if not state.validation_ok:
        return error_recovery(state)

    state = liveness_agent(state)
    state = form_builder(state)
    state = account_agent(state, account_type)
    state = payment_agent(state)
    return state.to_response()
