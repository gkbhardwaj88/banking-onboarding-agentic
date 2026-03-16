import streamlit as st
from services.api_client import KYCClient

def upload_kyc_docs():
    aadhaar = st.file_uploader("Upload Aadhaar", type=["jpg","jpeg","png"])
    pan = st.file_uploader("Upload PAN", type=["jpg","jpeg","png"])

    if st.button("Submit"):
        client = KYCClient()
        res = client.send_kyc(aadhaar, pan)
        st.session_state['kyc_data'] = res
        st.session_state['step'] = 2
        st.rerun()
