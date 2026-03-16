import streamlit as st

def review_form():
    data = st.session_state.get("kyc_data", {})
    st.json(data)
    if st.button("Proceed to Assistant"):
        st.session_state['step'] = 4
        st.rerun()
