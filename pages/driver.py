import streamlit as st
import pandas as pd
from datetime import datetime
from database import get_bookings_df, update_status
from styles import apply_corporate_theme, render_brand_header

st.set_page_config(
    page_title="Driver Portal",
    page_icon="🚘",
    layout="wide"
)

# Apply global red & white enterprise styles instantly
apply_corporate_theme()
render_brand_header("Valet Driver Interactive Workload Dispatch")

st.write("Manage customer vehicles and update valet status.")
st.divider()

# ------------ LOADING LOG DATAFRAME VIA PANDAS ------------
try:
    df = get_bookings_df()
except Exception as e:
    st.error(f"Error loading system log: {e}")
    df = pd.DataFrame()

if df.empty:
    st.info("No active valet requests on the grid.")
else:
    # --- NEW INTERACTIVE FILTER COMPONENT ---
    filter_status = st.selectbox(
        "🔍 Select Operational View Filter:",
        ["All Current Tasks", "Driver Assigned", "Picked Up", "Parked Vehicle", "Vehicle Returning", "Delivered Vehicle"]
    )
    if "All" not in filter_status:
        df = df[df['status'] == filter_status]

    st.divider()

    if df.empty:
        st.info(f"No active vehicles currently match status filter: '{filter_status}'")
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
                st.subheader(f"🎫 Work Order ID : {ticket}")
                
                # Interactive Color Status Badging
                badge_color = "#1E3A8A" # Blue
                if status == "Picked Up": badge_color = "#D97706" # Orange
                elif "Parked" in status: badge_color = "#16A34A" # Green
                elif "Returning" in status: badge_color = "#DC2626" # Red

                st.markdown(f"Status Indicator: <span style='background:{badge_color}; color:white; padding:4px 10px; border-radius:50px; font-size:12px;'>{status}</span>", unsafe_allow_html=True)
                
                st.write(
                f"""
                👤 **Customer Name:** {customer}  
                📞 **Phone Number:** {phone}  
                🚗 **Car Model Type:** {car}  
                🔢 **Vehicle Plate Number:** {number}  
                👨‍✈️ **Assigned Valet:** {driver}  
                ⏰ **Last Operational Check-in:** {updated}
                """
                )
                st.markdown('</div>', unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🚗 MARK AS PICKED UP", key=ticket+"pickup_btn"):
                        update_status(ticket, "Picked Up")
                        st.toast(f"Status for {ticket} changed to Picked Up!")
                        st.rerun() # Instantly triggers UI reload to pull the fresh database timestamp
                        
                with col2:
                    if st.button("🅿️ MARK AS PARKED", key=ticket+"park_btn"):
                        update_status(ticket, "Parked Vehicle")
                        st.toast(f"Status for {ticket} changed to Parked!")
                        st.rerun()
                        
                with col3:
                    if st.button("✅ MARK AS DELIVERED", key=ticket+"deliver_btn"):
                        update_status(ticket, "Delivered Vehicle")
                        st.toast(f"Status for {ticket} changed to Delivered!")
                        st.rerun()
                        
                st.divider()
