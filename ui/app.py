import streamlit as st
from components.uploader import upload_kyc_docs
from components.webcam import capture_selfie
from components.chat_box import chat_ui
from components.review_form import review_form
from components.command_palette import command_palette
from components.agent_panel import agent_panel
from services.api_client import KYCClient
from utils.state import init_state

st.set_page_config(page_title="AI Banking Onboarding", layout="wide")

init_state()
client = KYCClient()

st.title("AI Banking Onboarding System")
command_palette()
agent_panel()

step = st.session_state.get("step", 1)

# Simple stepper
steps = {
    1: "Upload Documents",
    2: "Review Parsed Data",
    3: "Selfie / Liveness",
    4: "Final Review",
    5: "Assistant Chat"
}
st.progress((step - 1) / (len(steps) - 1))
st.caption(" -> ".join(f"{idx}. {label}" for idx, label in steps.items()))

if step == 1:
    st.header("Upload KYC Documents")
    upload_kyc_docs()
elif step == 2:
    st.header("Review Parsed Information (before selfie)")
    review_form(show_photos=False, advance_step=3, submit_label="Proceed to Selfie", show_payment=False, show_validation=True)
elif step == 3:
    st.header("Capture Selfie for Liveness")
    capture_selfie()
elif step == 4:
    st.header("Final Review")
    review_form(show_photos=True, advance_step=5, submit_label="Save Review", show_payment=True)
    # Account summary between Final Review and Assistant Chat
    account_type = st.session_state.get("account_type", "Savings")
    kyc_status = st.session_state.get("kyc_data", {}).get("validation_ok")
    deposit_order = st.session_state.get("deposit_order") or {}
    acc_num = st.session_state.get("account_number")
    if not acc_num and deposit_order.get("order_id"):
        import random
        acc_num = str(random.randint(10**11, 10**12 - 1))
        st.session_state["account_number"] = acc_num
    st.subheader("Account Summary")
    status_label = "Verified" if kyc_status else "Pending/Failed"
    amount_display = f"₹{(deposit_order.get('amount', 0) or 0)/100:.2f}" if deposit_order else "₹0.00"
    st.write(f"- Account Type: {account_type}")
    st.write(f"- Account Number: {acc_num or 'Pending assignment'}")
    st.write(f"- Opening Deposit: {amount_display}")
    st.write(f"- KYC Status: {status_label}")
    # Confirm & Continue button after summary, enabled only if deposit order exists and account type chosen
    if deposit_order.get("order_id") and account_type:
        if st.button("Confirm & Continue", key="confirm_after_summary"):
            st.session_state["step"] = 5
            st.rerun()
elif step == 5:
    st.header("Chat with Banking Assistant")
    chat_ui()
