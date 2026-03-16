import streamlit as st
from components.uploader import upload_kyc_docs
from components.webcam import capture_selfie
from components.chat_box import chat_ui
from components.review_form import review_form
from services.api_client import KYCClient
from utils.state import init_state

st.set_page_config(page_title="AI Banking Onboarding", layout="wide")

init_state()
client = KYCClient()

st.title("AI Banking Onboarding System")

step = st.session_state.get("step", 1)

if step == 1:
    st.header("Upload KYC Documents")
    upload_kyc_docs()
elif step == 2:
    st.header("Capture Selfie for Liveness")
    capture_selfie()
elif step == 3:
    st.header("Review Extracted Information")
    review_form()
elif step == 4:
    st.header("Chat with Banking Assistant")
    chat_ui()
