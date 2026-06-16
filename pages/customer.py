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
/* Global Canvas Background Adjustments */
.stApp {
    background-color: #F8F9FA !important; /* Soft Premium Off-White Canvas */
    font-family: 'Inter', -apple-system, sans-serif !important;
}

.portal-title{
text-align:center;
font-size:40px;
font-weight:bold;
color:#1A365D; /* Corporate Deep Blue Accent */
}

/* Card Styling Override */
.card{
background:white;
padding:25px;
border-radius:20px;
box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
border: 1px solid #E2E8F0;
}

/* Input Fields Cleanup */
.stTextInput input, .stSelectbox div[data-baseweb="select"], .stTimeInput input {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #1A202C !important;
}

/* Red and Blue Tab Accent Controls */
div[data-testid="stTabs"] button {
    font-size: 14px !important;
    font-weight: 700 !important;
    color: #718096 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #DE2910 !important; /* Active indicator brand red line */
    border-bottom: 3px solid #DE2910 !important;
}

/* Option 2 Premium Corporate Button Overrides */
div.stButton > button {
    background-color: #1A365D !important; /* Brand Deep Blue Call-to-Action */
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 12px 24px !important;
    border-radius: 30px !important; /* Elegant modern pill buttons */
    border: none !important;
    width: 100% !important; 
    box-shadow: 0 4px 6px -1px rgba(26, 54, 93, 0.1) !important;
}
div.stButton > button:hover {
    background-color: #122542 !important; /* Darker blue on hover event */
}

/* Light Grey Feature Bubble Squares (Uber Style Blocks) */
.benefit-card {
    background-color: #EEEEEE !important; /* Solid light grey bubble background */
    border-radius: 12px !important;
    padding: 24px !important;
    min-height: 160px !important;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-bottom: 15px;
}
.benefit-card h3 {
    color: #1A202C !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    margin: 0 0 8px 0 !important;
}
.benefit-card p {
    color: #718096 !important;
    font-size: 13px !important;
    line-height: 1.4 !important;
    margin: 0 !important;
}

/* --- ADDED THIS HERE TO KEEP THE SIDEBAR IN CAPITALS --- */
section[data-testid="stSidebar"], section[data-testid="stSidebar"] * {
    background-color: #212529 !important; /* High-Contrast Charcoal Dark Slate Sidebar */
    color: #FFFFFF !important; /* Pure White text on dark sidebar options */
}
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
# EXPLORE BENEFITS GRID INTEGRATION (ADDED AT THE BOTTOM)
# =====================================================================
st.write("")
st.write("---")
st.markdown("### Explore what you can do with ParkEz")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="benefit-card">
            <h3>Book Spot</h3>
            <p>Reserve parking in advance. Skip the long lines and park hassle-free.</p>
        </div>
    """, unsafe_allow_html=True)
    st.button("Details", key="grid_details_spot")
    
with col2:
    st.markdown("""
        <div class="benefit-card">
            <h3>Monthly Pass</h3>
            <p>Get unlimited access to your favorite parking zones with fixed rates.</p>
        </div>
    """, unsafe_allow_html=True)
    st.button("Details", key="grid_details_pass")
    
with col3:
    st.markdown("""
        <div class="benefit-card">
            <h3>EV Charging</h3>
            <p>Find and secure parking slots equipped with rapid electric charging docks.</p>
        </div>
    """, unsafe_allow_html=True)
    st.button("Details", key="grid_details_ev")


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
