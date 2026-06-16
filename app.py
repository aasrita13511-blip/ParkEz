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

apply_corporate_theme()
render_brand_header("Smart Valet Logistics — Skip the Wait, Enjoy the Ride")

# --- FLOATING CHATBOT BUTTON ---
st.markdown("""
    <style>
    .floating-support-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #DC2626;
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
        background-color: #B91C1C;
    }
    </style>
    
    <a href="/support_chatbot" target="_self" class="floating-support-btn">
        💬 Live AI Support
    </a>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 SIGN UP"])

# ---------------- LOGIN ----------------
with tab1:
    role = st.selectbox("Login As", ["Customer", "Driver", "Manager"])
    phone = st.text_input("Enter Phone Number", key="login_phone")
    password = st.text_input("Enter Password", type="password", key="login_pass")

    if st.button("LOGIN"):
        if role == "Customer":
            user = customer_login(phone, password)
            if user:
                st.session_state["user_phone"] = phone
                st.session_state["user_name"] = user[0] if isinstance(user, (list, tuple)) else user
                st.session_state["role"] = "Customer"
                st.success("Welcome!")
                st.switch_page("pages/customer.py")
            else:
                st.error("Invalid Credentials")
        elif role == "Driver":
            if phone == "8888888888" and password == "1234":
                st.session_state["user_phone"] = phone
                st.session_state["role"] = "Driver"
                st.switch_page("pages/driver.py")
            else:
                st.error("Invalid Credentials")
        elif role == "Manager":
            if phone == "7777777777" and password == "1234":
                st.session_state["user_phone"] = phone
                st.session_state["role"] = "Manager"
                st.switch_page("pages/manager.py")
            else:
                st.error("Invalid Credentials")

# ---------------- SIGNUP ----------------
with tab2:
    st.subheader("Create Customer Account")
    name = st.text_input("Full Name", key="signup_name")
    phone_signup = st.text_input("Phone Number ", key="signup_phone")
    password_signup = st.text_input("Password ", type="password", key="signup_pass")

    if st.button("SIGN UP"):
        if name and phone_signup and password_signup:
            success = register_customer(name, phone_signup, password_signup)
            if success:
                st.success("Account Created Successfully! Go to LOGIN tab.")
            else:
                st.error("Phone Number Already Exists")
        else:
            st.warning("Please fill all fields")
