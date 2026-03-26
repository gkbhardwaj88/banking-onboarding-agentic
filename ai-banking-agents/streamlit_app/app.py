import os
import base64
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.set_page_config(page_title="AI Banking Agentic Onboarding", layout="wide")

if "kyc_state" not in st.session_state:
    st.session_state.kyc_state = {
        "pan_number": None,
        "aadhaar_number": None,
        "aadhaar_verified": False,
        "kyc_ok": False,
        "deposit_amount": 0,
        "account_type": "Savings",
    }

if "deposit_order" not in st.session_state:
    st.session_state.deposit_order = {}

# Utility calls

def call_agent_next():
    r = requests.post(f"{API_BASE}/agent/next", json={"session_id": "demo", "state": st.session_state.kyc_state})
    return r.json()

def call_tool(name, params):
    r = requests.post(f"{API_BASE}/agent/tool", json={"tool": name, "params": params})
    return r.json()

st.title("AI Banking Agentic Onboarding")
col_status, col_actions = st.columns([2,1])
with col_actions:
    if st.button("Agent Suggest"):
        st.session_state.agent_decision = call_agent_next()
    if st.button("Run Suggested Tool") and st.session_state.get("agent_decision", {}).get("tool"):
        tool = st.session_state.agent_decision["tool"]
        params = st.session_state.agent_decision.get("params", {})
        res = call_tool(tool, params)
        st.session_state.agent_tool_result = res
        # update state heuristics
        if res.get("parsed", {}).get("pan"):
            st.session_state.kyc_state["pan_number"] = res["parsed"]["pan"]
        if res.get("success"):
            st.session_state.kyc_state["aadhaar_verified"] = True
with col_status:
    st.caption("Agent decision")
    st.json(st.session_state.get("agent_decision", {}), expanded=True)
    st.caption("Last tool result")
    st.json(st.session_state.get("agent_tool_result", {}), expanded=True)

st.header("Step 2: Review Parsed Data")
pan_file = st.file_uploader("PAN Image", type=["png","jpg","jpeg"], key="pan_file")
colv = st.columns(2)
with colv[0]:
    if st.button("Validate PAN", key="val_pan_btn") and st.session_state.kyc_state.get("pan_number"):
        st.success("PAN format looks valid")
with colv[1]:
    aadhaar_num = st.text_input("Aadhaar Number", value=st.session_state.kyc_state.get("aadhaar_number") or "")
    if st.button("Validate Aadhaar", key="val_aad_btn"):
        res = requests.post(f"{API_BASE}/kyc/aadhaar/validate", params={"id_number": aadhaar_num}).json()
        st.json(res)
        st.session_state.kyc_state["aadhaar_verified"] = res.get("success", False)
        st.session_state.kyc_state["aadhaar_number"] = aadhaar_num

if st.button("Upload PAN & OCR") and pan_file:
    txt_bytes = pan_file.read()
    res = requests.post(f"{API_BASE}/kyc/pan/ocr", files={"file": txt_bytes}).json()
    st.session_state.pan_ocr = res
    st.session_state.kyc_state["pan_number"] = res.get("parsed", {}).get("pan")
    st.json(res)

st.header("Step 3: Selfie (placeholder)")
st.info("Selfie capture not implemented here; assume selfie_ok once uploaded in real flow.")

st.header("Step 4: Final Review & Payment")
account_type = st.selectbox("Account Type", ["Savings","Current","Salary"], index=["Savings","Current","Salary"].index(st.session_state.kyc_state.get("account_type","Savings")))
deposit_amt = st.number_input("Deposit Amount (INR)", min_value=0, value=1000, step=500)
if st.button("Pay Deposit (stub)"):
    res = requests.post(f"{API_BASE}/payment/order", params={"amount_paise": int(deposit_amt*100)}).json()
    st.session_state.deposit_order = res
    st.session_state.kyc_state["deposit_amount"] = res.get("amount",0)
    st.session_state.kyc_state["account_type"] = account_type
    st.success(f"Order created: {res.get('order_id')}")

order = st.session_state.get("deposit_order", {})
acc_num = st.session_state.get("account_number")
if not acc_num and order.get("order_id"):
    import random
    acc_num = str(random.randint(10**11, 10**12-1))
    st.session_state.account_number = acc_num

st.subheader("Account Summary")
st.markdown(f"**Account Type:** {st.session_state.kyc_state.get('account_type','Savings')}")
st.markdown(f"**Account Number:** {acc_num or 'Pending'}")
st.markdown(f"**Opening Deposit:** ?{(order.get('amount',0)/100):.2f}")
st.markdown(f"**KYC Status:** {'Verified' if st.session_state.kyc_state.get('aadhaar_verified') else 'Pending'}")
if order.get("order_id"):
    if st.button("Confirm & Continue"):
        st.success("Account confirmed. Proceed to chat.")

st.header("Step 5: Chat (placeholder)")
st.write("Connect this to your LLM/agent chat UI.")
