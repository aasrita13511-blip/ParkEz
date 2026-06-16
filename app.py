import streamlit as st
import pandas as pd
from database import *
from styles import apply_corporate_theme, render_brand_header

create_tables()

st.set_page_config(
    page_title="ParkEz - Login",
    page_icon="🚗",
    layout="wide"
)

# Apply global red & white enterprise styles instantly
apply_corporate_theme()
render_brand_header("Smart Valet Logistics — Skip the Wait, Enjoy the Ride")

# --- FLOATING AI CHATBOT SUPPORT BUTTON HTML/CSS ---
st.markdown("""
    <style>
    .floating-support-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #DC2626; /* Dynamic Operational Red */
        color: white !important;
        padding: 15px 25px;
        border-radius: 50px;
        text-decoration: none !important;
        font-weight: 700;
        box-shadow: 0 10px 15px -3px rgba(220, 38, 38, 0.3);
        z-index: 999999;
        transition: transform 0.2s ease;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .floating-support-btn:hover {
        transform: translateY(-3px);
        background-color: #B91C1C; /* Hover Dark Red */
    }
    </style>
    
    <a href="/support_chatbot" target="_self" class="floating-support-btn">
        💬 Live AI Support
    </a>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(
    [
        "🔐 LOGIN",
        "📝 SIGN UP"
    ]
)

# ---------------- LOGIN ----------------

with tab1:

    role = st.selectbox(
        "Login As",
        [
            "Customer",
            "Driver",
            "Manager"
        ]
    )

    phone = st.text_input(
        "Enter Phone Number"
    )

    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("LOGIN"):

        if role == "Customer":

            user = customer_login(
                phone,
                password
            )

            if user:
                # Store user properties safely inside session memory arrays
                st.session_state["user_phone"] = phone
                st.session_state["user_name"] = user[1] if isinstance(user, (list, tuple)) else user
                st.session_state["role"] = "Customer"

                st.toast(f"🔒 Authenticated as Customer: {st.session_state['user_name']}")
                st.success(f"Welcome {st.session_state['user_name']}!")
                st.switch_page("pages/customer.py")

            else:
                st.error(
                    "Invalid Credentials"
                )

        elif role == "Driver":

            if (
                phone == "8888888888"
                and password == "1234"
            ):
                st.session_state["user_phone"] = phone
                st.session_state["role"] = "Driver"

                st.toast("👨‍✈️ Driver Authentication Approved. Opening active dispatch boards...")
                st.switch_page("pages/driver.py")

            else:
                st.error(
                    "Invalid Credentials"
                )

        elif role == "Manager":

            if (
                phone == "7777777777"
                and password == "1234"
            ):
                st.session_state["user_phone"] = phone
                st.session_state["role"] = "Manager"

                st.toast("📊 Manager Access Token Approved. Booting operational matrix charts...")
                st.switch_page("pages/manager.py")

            else:
                st.error(
                    "Invalid Credentials"
                )

# ---------------- SIGNUP ----------------

with tab2:

    st.subheader(
        "Create Customer Account"
    )

    name = st.text_input(
        "Full Name"
    )

    phone_signup = st.text_input(
        "Phone Number "
    )

    password_signup = st.text_input(
        "Password ",
        type="password"
    )

    if st.button("SIGN UP"):

        success = register_customer(
            name,
            phone_signup,
            password_signup
        )

        if success:
            # Interactive visual celebration popup on account registration completion
            st.balloons()
            st.success(
                "Account Created Successfully! Switch over to the LOGIN tab to access your panel."
            )

        else:
            st.error(
                "Phone Number Already Exists"
            )
