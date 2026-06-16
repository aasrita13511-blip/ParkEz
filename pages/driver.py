import streamlit as st
import pandas as pd  # <--- NEW: Integrated for dashboard data grid transformation
from datetime import datetime

from database import (
    get_bookings_df,  # <--- NEW: Using our fast Pandas query
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

/* --- SIDEBAR CAPITALIZATION STYLING --- */
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


# ================= NEW PANDAS QUICK-FILTER INTERFACE =================
try:
    df = get_bookings_df()
except Exception as e:
    st.error(f"Database error: {e}")
    df = pd.DataFrame()

if df.empty:
    st.info("No active valet requests")
else:
    # Dropdown menu to filter list views seamlessly via Pandas
    filter_status = st.selectbox(
        "🔍 Filter Active Workload By Status:",
        ["All Tasks", "Driver Assigned", "Picked Up", "Parked Vehicle", "Vehicle Returning", "Delivered Vehicle"]
    )
    
    if filter_status != "All Tasks":
        df = df[df['status'] == filter_status]
        
    st.divider()

    if df.empty:
        st.info(f"No vehicles currently match status: '{filter_status}'")
    else:
        # Loop through rows safely using Pandas iteration matrix instead of messy raw loops
        for index, row in df.iterrows():
            ticket = row['ticket']
            customer = row['customer']
            phone = row['phone']
            car = row['car_model']
            number = row['vehicle_number']
            driver = row['driver']
            status = row['status']
            updated = row['updated_time']

            with st.container():
                st.markdown('<div class="driver-card">', unsafe_allow_html=True)

                st.subheader(f"🎫 Ticket : {ticket}")
                st.write(
                f"""
                👤 **Customer:** {customer}  
                📞 **Phone:** {phone}  
                🚗 **Car Model:** {car}  
                🔢 **Vehicle Number:** {number}  
                👨‍✈️ **Driver Assigned:** {driver}  
                📌 **Current Status:** {status}  
                ⏰ **Last Tracked Event Time:** {updated}
                """
                )

                st.markdown("</div>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("🚗 PICKED UP", key=ticket+"pickup"):
                        update_status(ticket, "Picked Up")
                        st.success(f"Status changed to Picked Up!")
                        time_now = datetime.now().strftime("%I:%M %p")
                        # Instantly trigger UI reload to pull the new database timestamp
                        st.rerun()

                with col2:
                    if st.button("🅿️ PARKED VEHICLE", key=ticket+"park"):
                        update_status(ticket, "Parked Vehicle")
                        st.success(f"Status changed to Parked!")
                        st.rerun()

                with col3:
                    if st.button("✅ DELIVERED VEHICLE", key=ticket+"deliver"):
                        update_status(ticket, "Delivered Vehicle")
                        st.success(f"Status changed to Delivered!")
                        st.rerun()

                st.divider()
