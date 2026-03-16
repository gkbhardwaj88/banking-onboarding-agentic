import streamlit as st

def init_state():
    if 'step' not in st.session_state:
        st.session_state['step'] = 1
