import streamlit as st
import pandas as pd
from database import get_bookings_df, update_status, update_driver_location
from styles import apply_corporate_theme, render_brand_header

st.set_page_config(page_title="Driver Dashboard", page_icon="🚘", layout="wide")
apply_corporate_theme()
render_brand_header("Valet Driver Interactive Mission Control")

try:
    df = get_bookings_df()
except Exception as e:
    st.error(f"Error loading systems dashboard: {e}")
    df = pd.DataFrame()

if df.empty:
    st.info("No active valet requests on the grid.")
else:
    filter_status = st.selectbox(
        "🔍 Select Operational View Filter:",
        ["All Current Tasks", "Driver Assigned", "Picked Up", "Parked Vehicle", "Vehicle Returning", "Delivered Vehicle"]
    )
    if "All" not in filter_status:
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
            st.subheader(f"🎫 Work Order ID : {ticket} — Customer: {customer}")
            
            badge_color = "#1E3A8A" 
            if status == "Picked Up": badge_color = "#D97706" 
            elif "Parked" in status: badge_color = "#16A34A" 
            elif "Returning" in status: badge_color = "#DC2626" 

            st.markdown(f"Status Indicator: <span style='background:{badge_color}; color:white; padding:4px 10px; border-radius:50px; font-size:12px;'>{status}</span>", unsafe_allow_html=True)
            st.write(f"📍 **Current Live GPS Tracking Broadcast:** Latitude `{lat:.4f}`, Longitude `{lon:.4f}`")
            
            # --- INTERACTIVE LIVE GPS SIMULATOR ---
            st.markdown("##### 🎮 Live GPS Tracking Simulation Controls")
            new_lat = st.slider(f"Adjust Latitude Location Offset ({ticket})", min_value=17.5400, max_value=17.5600, value=float(lat), step=0.0005)
            new_lon = st.slider(f"Adjust Longitude Location Offset ({ticket})", min_value=78.3800, max_value=78.4000, value=float(lon), step=0.0005)
            
            if new_lat != lat or new_lon != lon:
                update_driver_location(ticket, new_lat, new_lon)
                st.toast(f"📍 GPS coordinates updated live for {ticket}!")
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🚗 INITIALIZE CAR PICKUP", key=ticket+"p_int"):
                    update_status(ticket, "Picked Up")
                    update_driver_location(ticket, 17.5460, 78.3910)
                    st.rerun()
            with col2:
                if st.button("🅿️ SECURE IN PARKING STRUCTURE", key=ticket+"pk_int"):
                    update_status(ticket, "Parked Vehicle")
                    update_driver_location(ticket, 17.5480, 78.3930)
                    st.rerun()
            with col3:
                if st.button("✅ FINALIZE HANDOFF DELIVERY", key=ticket+"dl_int"):
                    update_status(ticket, "Delivered Vehicle")
                    update_driver_location(ticket, 17.5490, 78.3950)
                    st.rerun()
            st.divider()
