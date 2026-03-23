import streamlit as st
import cv2
import numpy as np
from services.api_client import KYCClient

def capture_selfie():
    camera_input = st.camera_input("Take a selfie")
    if camera_input:
        selfie_bytes = camera_input.getvalue()
        client = KYCClient()
        res = client.send_selfie(selfie_bytes)
        st.session_state['selfie_result'] = res
        st.session_state['step'] = 4
        st.rerun()
