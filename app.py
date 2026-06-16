# =====================================================================
# APPEND THIS TO THE ABSOLUTE BOTTOM OF YOUR EXISTING app.py FILE
# =====================================================================
import streamlit as st

# Custom CSS to float a button in the bottom-right corner
st.markdown(
    """
    <style>
    div.stActionButton {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 999999;
    }
    .stActionButton button {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        font-size: 28px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
        border: none !important;
        cursor: pointer !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Container rendering the floating chat icon
with st.container():
    st.markdown('<div class="stActionButton">', unsafe_allow_html=True)
    if st.button("💬", key="home_floating_chat_action"):
        st.switch_page("pages/support_chatbot.py")
    st.markdown('</div>', unsafe_allow_html=True)
