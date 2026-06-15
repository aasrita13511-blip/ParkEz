import streamlit as st

st.set_page_config(
    page_title="ParkEz",
    page_icon="🚗",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None


users = {
    "9999999999": {
        "password": "1234",
        "role": "Customer"
    },
    "8888888888": {
        "password": "1234",
        "role": "Driver"
    },
    "7777777777": {
        "password": "1234",
        "role": "Manager"
    }
}


if not st.session_state.logged_in:

    st.title("🚗 ParkEz")
    st.subheader("Skip the Wait, Enjoy the Ride")

    phone = st.text_input("Phone Number")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if phone in users:

            if users[phone]["password"] == password:

                st.session_state.logged_in = True
                st.session_state.role = users[phone]["role"]

                st.rerun()

            else:
                st.error("Wrong Password")

        else:
            st.error("Invalid Phone Number")

else:

    role = st.session_state.role

    st.sidebar.success(
        f"Logged in as {role}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.role = None

        st.rerun()

    if role == "Customer":
        st.switch_page("pages/customer.py")

    elif role == "Driver":
        st.switch_page("pages/driver.py")

    elif role == "Manager":
        st.switch_page("pages/manager.py")