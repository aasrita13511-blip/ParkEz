import streamlit as st
import pandas as pd
from datetime import datetime
from database import get_bookings_df, update_status, update_driver_location
from styles import apply_corporate_theme, render_brand_header

st.set_page_config(page_title="Driver Portal", page_icon="🚘", layout="wide")
apply_corporate_theme()
render_brand_header("Valet Driver Workload Dispatch")

try:
    df = get_bookings_df()
except Exception as e:
    st.error(f"Error loading system entries: {e}")
    df = pd.DataFrame()

if df.empty:
    st.info("No active valet requests")
else:
    filter_status = st.selectbox(
        "🔍 Filter Workload By Status:",
        ["All Tasks", "Driver Assigned", "Picked Up", "Parked Vehicle", "Vehicle Returning", "Delivered Vehicle"]
    )
    if filter_status != "All Tasks":
        df = df[df['status'] == filter_status]

    st.divider()

    for index, row in df.iterrows():
        ticket = row['ticket']
        customer = row['customer']
        status = row['status']
        lat = row['current_lat']
        lon = row['current_lon']

        with st.container():
            st.markdown('<div class="driver-card">', unsafe_allow_html=True)
            st.subheader(f"🎫 Ticket : {ticket} | Customer: {customer}")
            st.write(f"📌 **Status:** {status} | **Coordinates:** Lat {lat:.4f}, Lon {lon:.4f}")
            st.markdown('</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🚗 PICKED UP", key=ticket+"p"):
                    update_status(ticket, "Picked Up")
                    # Drive simulated movements closer to secondary hub points 
                    update_driver_location(ticket, 17.546, 78.391)
                    st.rerun()
            with col2:
                if st.button("🅿️ PARKED", key=ticket+"pk"):
                    update_status(ticket, "Parked Vehicle")
                    update_driver_location(ticket, 17.548, 78.393)
                    st.rerun()
            with col3:
                if st.button("✅ DELIVERED", key=ticket+"dl"):
                    update_status(ticket, "Delivered Vehicle")
                    update_driver_location(ticket, 17.549, 78.395)
                    st.rerun()
            st.divider()
