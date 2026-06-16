import streamlit as st
import random
import time

from database import (
    add_booking,
    get_available_driver,
    get_booking,
    update_status
)


st.set_page_config(
    page_title="Customer Portal",
    page_icon="🚗",
    layout="wide"
)


# ---------------- STYLE ----------------

st.markdown("""
<style>

.portal-title{
text-align:center;
font-size:40px;
font-weight:bold;
color:#0B3D91;
}

.card{
background:white;
padding:25px;
border-radius:20px;
box-shadow:0px 5px 15px #ddd;
}

/* --- ADDED THIS HERE TO KEEP THE SIDEBAR IN CAPITALS --- */
section[data-testid="stSidebar"] *, 
[data-testid="stSidebarNavItems"] *,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] a {
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    font-weight: 600 !important;
}

</style>

""", unsafe_allow_html=True)


st.markdown(
"""
<div class="portal-title">
👤 CUSTOMER PORTAL
</div>
""",
unsafe_allow_html=True
)


st.divider()


# ---------------- TABS ----------------

book, retrieve = st.tabs(
[
"🚗 REQUEST VALET",
"🔑 RETRIEVE VEHICLE"
]
)



# ================= BOOK VALET =================


with book:


    st.subheader(
        "Book Your Valet Driver"
    )


    name = st.text_input(
        "Customer Name"
    )


    phone = st.text_input(
        "Phone Number"
    )


    car_model = st.text_input(
        "Car Model"
    )


    vehicle_number = st.text_input(
        "Vehicle Number"
    )


    arrival = st.time_input(
        "Arrival Time"
    )


    if st.button(
        "REQUEST DRIVER"
    ):


        if (
            name
            and phone
            and car_model
            and vehicle_number
        ):


            ticket = (
                "VAL"
                +
                str(
                    random.randint(
                        1000,
                        9999
                    )
                )
            )


            driver = get_available_driver()


            add_booking(

                (
                ticket,
                name,
                phone,
                car_model,
                vehicle_number,
                str(arrival),
                driver,
                "Driver Assigned",
                "Just Now"
                )

            )


            st.success(
                "Valet Driver Assigned Successfully"
            )


            st.info(
                f"""
🎫 Ticket ID : {ticket}

🚘 Driver : {driver}

📍 Status : Driver Assigned
"""
            )


        else:

            st.warning(
                "Please fill all details"
            )




# ================= RETRIEVE VEHICLE =================



with retrieve:


    st.subheader(
        "Request Vehicle Retrieval"
    )


    ticket = st.text_input(
        "Enter Ticket ID"
    )


    leave_time = st.selectbox(
        "When are you leaving?",
        [
            "2 Minutes",
            "5 Minutes",
            "10 Minutes"
        ]
    )


    if st.button(
        "BRING MY CAR"
    ):


        booking = get_booking(ticket)


        if booking:


            update_status(
                ticket,
                "Vehicle Returning"
            )


            st.success(
                "Driver has been notified"
            )


            st.divider()


            st.subheader(
                "📍 LIVE TRACKING"
            )



            tracking = st.empty()



            steps = [

            "Driver Assigned 🚘",

            "Driver Going To Parking Area 📍",

            "Vehicle Located 🔎",

            "Vehicle Moving 🚗",

            "Arriving At Pickup Point ✅"

            ]



            progress = st.progress(0)



            for i,step in enumerate(steps):


                time.sleep(1)


                tracking.info(
                    step
                )


                progress.progress(
                    (i+1)/len(steps)
                )



            st.success(
                f"""
Vehicle Ready!

ETA : {leave_time}

Driver : {booking[7]}
"""
            )



        else:


            st.error(
                "Invalid Ticket ID"
            )


# =====================================================================
# CHATBOT NAVIGATION INTEGRATION (ADDED AT THE BOTTOM)
# =====================================================================
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
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stActionButton button:hover {
        background-color: #e04040 !important;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown('<div class="stActionButton">', unsafe_allow_html=True)
    if st.button("💬", key="customer_portal_floating_chat_action"):
        st.switch_page("pages/support_chatbot.py")
    st.markdown('</div>', unsafe_allow_html=True)
