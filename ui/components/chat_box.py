import streamlit as st
from services.api_client import KYCClient

def chat_ui():
    client = KYCClient()
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_msg = st.text_input("Your message:")
    if st.button("Send"):
        res = client.chat(user_msg)
        st.session_state['chat_history'].append(("You", user_msg))
        st.session_state['chat_history'].append(("Assistant", res["response"]))

    for speaker, msg in st.session_state['chat_history']:
        st.write(f"**{speaker}:** {msg}")
