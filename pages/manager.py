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


.card{
background:white;
padding:20px;
border-radius:18px;
box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
border: 1px solid #E2E8F0;
}

/* Metric Layout Polish */
div[data-testid="stMetricValue"] {
    color: #1A365D !important;
    font-weight: 800 !important;
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
# LIVE DRIVER CAR COUNT ACTIVITY TABLE (ADDED HERE)
# =====================================================================
st.divider()
st.subheader("📋 LIVE DRIVER WORKLOAD SUMMARY")

if bookings:
    # Calculate live active car tallies per assigned driver dynamically
    driver_tallies = {}
    for booking in bookings:
        assigned_driver = booking[7]
        current_status = booking[8]
        
        # Only count cars currently in active transit or parked states
        if current_status not in ["Delivered Vehicle", "Vehicle Ready!"]:
            driver_tallies[assigned_driver] = driver_tallies.get(assigned_driver, 0) + 1

    # Format data table arrays for streamlined Streamlit display framework
    table_records = []
    for driver in drivers:
        d_name = driver[1]
        d_phone = driver[2]
        active_count = driver_tallies.get(d_name, 0)
        
        table_records.append({
            "Driver Name": d_name,
            "Contact Number": d_phone,
            "Active Assigned Cars": f"📦 {active_count} Vehicles"
        })

    # Render a responsive, clean tabular layout on screen
    st.table(table_records)
else:
    st.info("No active workloads to display.")


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
