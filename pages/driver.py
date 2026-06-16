import streamlit as st
import pandas as pd
from datetime import datetime

from database import (
    get_bookings_df,
    update_status
)
from styles import apply_corporate_theme, render_brand_header

st.set_page_config(
    page_title="Driver Portal",
    page_icon="🚘",
    layout="wide"
)

apply_corporate_theme()
render_brand_header("Valet Driver Workload Dispatch")

st.write("Manage customer vehicles and update valet status.")

try:
    df = get_bookings_df()
except Exception as e:
    st.error(f"Database error: {e}")
    df = pd.DataFrame()

if df.empty:
    st.info("No active valet requests")
else:
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
