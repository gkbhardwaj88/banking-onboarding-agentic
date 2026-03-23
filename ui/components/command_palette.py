import streamlit as st

def command_palette():
    """
    Simple local command palette to trigger quick actions.
    """
    st.subheader("Command Palette")
    cmd = st.text_input("Type a command (e.g., 'go upload', 'go review', 'go selfie', 'reset')", key="cmd_palette")
    mapping = {
        "go upload": 1,
        "go review": 2,
        "go selfie": 3,
        "go final": 4,
        "go chat": 5,
    }
    if cmd:
        lower = cmd.strip().lower()
        if lower == "reset":
            st.session_state.clear()
            st.success("Session reset.")
            st.rerun()
        elif lower in mapping:
            st.session_state["step"] = mapping[lower]
            st.info(f"Jumped to step {mapping[lower]}")
            st.rerun()
        else:
            st.warning("Unknown command. Try: go upload, go review, go selfie, go final, go chat, or reset.")
