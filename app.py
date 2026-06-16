import streamlit as st
import pandas as pd  # Ready for any direct frontend manipulations
from database import *

create_tables()

st.set_page_config(
    page_title="ParkEz",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
background:#F5F9FF;
}

.big-title{
text-align:center;
font-size:65px;
font-weight:bold;
color:#0B3D91;
}

.tagline{
text-align:center;
font-size:25px;
color:#555;
margin-bottom:40px;
}

.block-container{
padding-top:2rem;
}

/* --- NEW SIDEBAR CAPITALIZATION STYLING --- */
[data-testid="stSidebarNavItems"] span {
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
"""
<div class='big-title'>
🚗 ParkEz
</div>

<div class='tagline'>
Skip the Wait, Enjoy the Ride
</div>
""",
unsafe_allow_html=True
)

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
                # Store user info in session memory so pages can filter booking data by phone
                st.session_state["user_phone"] = phone
                st.session_state["user_name"] = user[1]
                st.session_state["role"] = "Customer"

                st.success(f"Welcome {user[1]}")
                st.switch_page("pages/customer.py")

            else:
                st.error("Invalid Credentials")

        elif role == "Driver":

            if (
                phone == "8888888888"
                and password == "1234"
            ):
                st.session_state["user_phone"] = phone
                st.session_state["role"] = "Driver"
                
                st.switch_page("pages/driver.py")

            else:
                st.error("Invalid Credentials")

        elif role == "Manager":

            if (
                phone == "7777777777"
                and password == "1234"
            ):
                st.session_state["user_phone"] = phone
                st.session_state["role"] = "Manager"
                
                st.switch_page("pages/manager.py")

            else:
                st.error("Invalid Credentials")

# ---------------- SIGNUP ----------------

with tab2:

    st.subheader(
        "Create Customer Account"
    )

    name = st.text_input(
        "Full Name"
    )

    phone = st.text_input(
        "Phone Number "
    )

    password = st.text_input(
        "Password ",
        type="password"
    )

    if st.button("SIGN UP"):

        success = register_customer(
            name,
            phone,
            password
        )

        if success:
            st.success("Account Created Successfully")
        else:
            st.error("Phone Number Already Exists")
