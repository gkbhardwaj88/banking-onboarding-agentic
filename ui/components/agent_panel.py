import json
import streamlit as st
from services.api_client import KYCClient


def agent_panel():
    st.subheader("Agent Suggestions")
    state = st.session_state.get("kyc_data", {})
    session_id = st.session_state.get("session_id", "default-session")
    client = KYCClient()
    decision = client.agent_next(session_id, state)
    st.json(decision)
    if decision.get("message"):
        st.info(decision["message"])
    if decision.get("action") == "create_payment_order":
        st.session_state["agent_suggest_payment"] = True
    else:
        st.session_state["agent_suggest_payment"] = False
