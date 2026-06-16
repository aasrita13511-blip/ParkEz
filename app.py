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
        ["Customer", "Driver", "Manager"]
    )

    phone = st.text_input("Enter Phone Number")
    password = st.text_input("Enter Password", type="password")

    if st.button("LOGIN"):
        if role == "Customer":
            user = customer_login(phone, password)
            if user:
                st.session_state["user_phone"] = phone
                st.session_state["user_name"] = user[1] # Fixed: Safely pulls just name string
                st.session_state["role"] = "Customer"
                
                # --- NEW INTERACTIVE NOTIFICATIONS ---
                st.toast(f"🔒 Authenticated securely as Customer: {st.session_state['user_name']}")
                st.success(f"Welcome {st.session_state['user_name']}!")
                st.switch_page("pages/customer.py")
            else:
                st.error("Invalid Credentials")

        elif role == "Driver":
            if phone == "8888888888" and password == "1234":
                st.session_state["user_phone"] = phone
                st.session_state["role"] = "Driver"
                
                st.toast("👨‍✈️ Driver Authentication Approved. Opening workload dispatch panel...")
                st.switch_page("pages/driver.py")
            else:
                st.error("Invalid Credentials")

        elif role == "Manager":
            if phone == "7777777777" and password == "1234":
                st.session_state["user_phone"] = phone
                st.session_state["role"] = "Manager"
                
                st.toast("📊 Manager Credentials Approved. Launching administrative matrix dashboard...")
                st.switch_page("pages/manager.py")
            else:
                st.error("Invalid Credentials")

# ---------------- SIGNUP ----------------
with tab2:
    st.subheader("Create Customer Account")
    name = st.text_input("Full Name")
    phone_signup = st.text_input("Phone Number ")
    password_signup = st.text_input("Password ", type="password")

    if st.button("SIGN UP"):
        success = register_customer(name, phone_signup, password_signup)
        if success:
            # --- NEW INTERACTIVE CELEBRATION ANIMATION ---
            st.balloons()
            st.success("Account Created Successfully! Please switch to the LOGIN tab to access your profile.")
        else:
            st.error("Phone Number Already Exists")
