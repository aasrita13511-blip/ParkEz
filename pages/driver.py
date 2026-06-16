import streamlit as st
from datetime import datetime

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

.title{
text-align:center;
font-size:42px;
font-weight:bold;
color:#0B3D91;
}


.driver-card{
background:white;
padding:25px;
border-radius:20px;
box-shadow:0px 5px 15px #ddd;
margin-bottom:20px;
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


                    update_status(

                        ticket,

                        "Picked Up"

                    )


                    st.success(

                        f"""
Status Updated

Picked Up

Time:

{datetime.now().strftime("%I:%M %p")}

"""
                    )




            with col2:


                if st.button(
                    "🅿️ PARKED VEHICLE",
                    key=ticket+"park"
                ):


                    update_status(

                        ticket,

                        "Parked Vehicle"

                    )


                    st.success(

                        f"""
Status Updated

Parked Vehicle

Time:

{datetime.now().strftime("%I:%M %p")}

"""
                    )




            with col3:


                if st.button(
                    "✅ DELIVERED VEHICLE",
                    key=ticket+"deliver"
                ):


                    update_status(

                        ticket,

                        "Delivered Vehicle"

                    )


                    st.success(

                        f"""
Status Updated

Delivered Vehicle

Time:

{datetime.now().strftime("%I:%M %p")}

"""
                    )



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
