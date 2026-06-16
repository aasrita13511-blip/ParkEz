import streamlit as st

from database import (
    total_cars,
    retrieved_cars,
    active_drivers,
    get_all_bookings
)



st.set_page_config(
    page_title="Manager Dashboard",
    page_icon="📊",
    layout="wide"
)



# ------------ STYLE ------------

st.markdown("""
<style>


.title{
text-align:center;
font-size:42px;
font-weight:bold;
color:#0B3D91;
}


.card{
background:white;
padding:20px;
border-radius:18px;
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

""",
unsafe_allow_html=True
)




st.markdown(
"""
<div class="title">

📊 VENUE MANAGER DASHBOARD

</div>
""",

unsafe_allow_html=True
)



st.write(
"Monitor valet operations in real time."
)



st.divider()



# ------------ ANALYTICS ------------



col1,col2,col3,col4 = st.columns(4)



with col1:

    st.metric(
        "🚗 TOTAL CARS",
        total_cars()
    )



with col2:

    st.metric(
        "✅ CARS RETRIEVED",
        retrieved_cars()
    )



with col3:

    st.metric(
        "👨‍✈️ ACTIVE DRIVERS",
        len(active_drivers())
    )



with col4:

    st.metric(
        "⏱ AVG WAIT TIME",
        "3 Minutes"
    )




st.divider()



# ------------ DRIVER DETAILS ------------



st.subheader(
"👨‍✈️ DRIVER AVAILABILITY"
)



drivers = active_drivers()



if drivers:


    for driver in drivers:


        st.markdown(
        f"""

<div class="card">


### 🚘 {driver[1]}


📞 Phone:

{driver[2]}


Status:

🟢 Available


</div>


        """,
        unsafe_allow_html=True
        )


        st.write("")



else:


    st.warning(
        "No drivers available"
    )





st.divider()



# ------------ VEHICLE ACTIVITY ------------



st.subheader(
"🚗 LIVE VEHICLE ACTIVITY"
)



bookings = get_all_bookings()



if bookings:


    for booking in bookings:



        st.info(

        f"""

🎫 Ticket:

{booking[1]}


👤 Customer:

{booking[2]}


🚗 Car Model:

{booking[4]}


👨‍✈️ Driver:

{booking[7]}


📌 Status:

{booking[8]}


⏰ Updated:

{booking[9]}

"""

        )



else:


    st.info(
        "No vehicle activity yet"
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
    if st.button("💬", key="manager_floating_chat_action"):
        st.switch_page("pages/support_chatbot.py")
    st.markdown('</div>', unsafe_allow_html=True)
