import streamlit as st
from datetime import datetime
import time

from database import (
    get_all_bookings,
    update_status
)


st.set_page_config(
    page_title="Driver Portal",
    page_icon="🚘",
    layout="wide"
)



# ---------- STYLE ----------

st.markdown("""
<style>
/* Global Canvas Background Adjustments */
.stApp {
    background-color: #F8F9FA !important; /* Soft Premium Off-White Canvas */
    font-family: 'Inter', -apple-system, sans-serif !important;
}

.title{
text-align:center;
font-size:42px;
font-weight:bold;
color:#1A365D; /* Corporate Deep Blue Accent */
}


.driver-card{
background:white;
padding:25px;
border-radius:20px;
box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
border: 1px solid #E2E8F0;
margin-bottom:20px;
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

/* High-Contrast Charcoal Dark Slate Sidebar Layout Adjustments */
section[data-testid="stSidebar"] {
    background-color: #212529 !important; 
    border-right: none !important;
}

/* Force all text elements, links, spans, and navigation text in the sidebar to Pure White */
section[data-testid="stSidebar"] *, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebarNavItems"] span,
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] span {
    color: #FFFFFF !important; /* Crisp white elements over dark background */
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    font-weight: 600 !important;
}

</style>

""", unsafe_allow_html=True)



st.markdown(
"""
<div class="title">

🚘 DRIVER PORTAL

</div>
""",

unsafe_allow_html=True
)



st.divider()



st.write(
"Manage customer vehicles and update valet status."
)



bookings = get_all_bookings()



if len(bookings)==0:


    st.info(
        "No active valet requests"
    )



else:



    for booking in bookings:


        # RE-ESTABLISHED CORRECT ROW EXTRACTION INDEX KEYS HERE
        ticket = booking[1]
        customer = booking[2]
        phone = booking[3]
        car = booking[4]
        number = booking[5]
        driver = booking[7]
        status = booking[8]
        updated = booking[9]



        with st.container():


            st.markdown(
            """
            <div class="driver-card">
            """,
            unsafe_allow_html=True
            )



            st.subheader(
                f"🎫 Ticket : {ticket}"
            )


            st.write(
            f"""

👤 Customer:

{customer}


📞 Phone:

{phone}


🚗 Car Model:

{car}


🔢 Vehicle Number:

{number}


👨‍✈️ Driver:

{driver}


📌 Current Status:

{status}


⏰ Last Updated:

{updated}

"""
            )



            st.markdown(
            "</div>",
            unsafe_allow_html=True
            )



            col1,col2,col3 = st.columns(3)




            with col1:


                if st.button(
                    "🚗 PICKED UP",
                    key=ticket+"pickup"
                ):

                    current_time_str = datetime.now().strftime("%I:%M %p")

                    # Commits status text and independent, real-time dynamic timestamp parameters
                    update_status(
                        ticket,
                        "Picked Up",
                        current_time_str
                    )


                    st.success(

                        f"""
Status Updated

Picked Up

Time:

{current_time_str}

"""
                    )
                    time.sleep(0.4)
                    st.rerun()




            with col2:


                if st.button(
                    "🅿️ PARKED VEHICLE",
                    key=ticket+"park"
                ):

                    current_time_str = datetime.now().strftime("%I:%M %p")

                    # Commits status text and independent, real-time dynamic timestamp parameters
                    update_status(
                        ticket,
                        "Parked Vehicle",
                        current_time_str
                    )


                    st.success(

                        f"""
Status Updated

Parked Vehicle

Time:

{current_time_str}

"""
                    )
                    time.sleep(0.4)
                    st.rerun()




            with col3:


                if st.button(
                    "✅ DELIVERED VEHICLE",
                    key=ticket+"deliver"
                ):

                    current_time_str = datetime.now().strftime("%I:%M %p")

                    # Commits status text and independent, real-time dynamic timestamp parameters
                    update_status(
                        ticket,
                        "Delivered Vehicle",
                        current_time_str
                    )


                    st.success(

                        f"""
Status Updated

Delivered Vehicle

Time:

{current_time_str}

"""
                    )
                    time.sleep(0.4)
                    st.rerun()



            st.divider()


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
    if st.button("💬", key="driver_floating_chat_action"):
        st.switch_page("pages/support_chatbot.py")
    st.markdown('</div>', unsafe_allow_html=True)
