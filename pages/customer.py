import streamlit as st
import random
import pandas as pd
import folium
from streamlit_folium import st_folium
from database import add_booking, get_booking, update_status, get_customer_history_df
from styles import apply_corporate_theme, render_brand_header

st.set_page_config(page_title="Customer App Interface", page_icon="🚗", layout="wide")
apply_corporate_theme()
render_brand_header("Customer Interactive Valet Space")

tab1, tab2, tab3 = st.tabs(["🚗 REQUEST VALET", "🔑 LIVE RADAR TRACKER", "📊 MY PARKING HISTORY"])

# ================= REQUEST VALET =================
with tab1:
    st.subheader("Book Your Valet Driver")
    default_name = st.session_state.get("user_name", "")
    default_phone = st.session_state.get("user_phone", "")

    name = st.text_input("Customer Name", value=default_name)
    phone = st.text_input("Phone Number", value=default_phone)
    car_model = st.text_input("Car Model")
    vehicle_number = st.text_input("Vehicle Number")
    arrival = st.time_input("Arrival Time")

    if st.button("SUBMIT SERVICE REQUEST"):
        if name and phone and car_model and vehicle_number:
            ticket = "VAL" + str(random.randint(1000, 9999))
            add_booking((ticket, name, phone, car_model, vehicle_number, str(arrival), "Rahul", "Driver Assigned", "Just Now"))
            st.success("Valet Request Sent to Systems Matrix!")
            st.info(f"🎫 **Ticket ID Issued:** {ticket} | Copy this code to start telemetry tracking.")
        else:
            st.warning("Please input all configuration fields.")

# ================= RETRIEVE & TRACK VEHICLE (FOLIUM TRACKER ENGINE) =================
with tab2:
    st.subheader("Interactive Tracking Matrix")
    search_ticket = st.text_input("Enter Ticket ID to boot live tracking system")

    if search_ticket:
        booking = get_booking(search_ticket)
        if booking:
            if st.button("🚨 BROADCAST VEHICLE RETRIEVAL SIGNAL"):
                update_status(search_ticket, "Vehicle Returning")
                st.toast("⚡ Signal broadcast successfully to driver display panels!")

            st.divider()
            
            # --- SAFE WEB REFRESH SUBCOMPONENT FRAGMENT ---
            @st.fragment(run_every=4.0)
            def run_radar_telemetry(t_id):
                live_data = get_booking(t_id)
                if live_data:
                    current_status = live_data
                    lat = live_data if live_data is not None else 17.545
                    lon = live_data if live_data is not None else 78.390
                    driver_name = live_data if live_data is not None else "Assigned Driver"
                    
                    st.info(f"🛰️ **Live Operational Status:** {current_status} | **Driver En Route:** {driver_name}")
                    
                    # 1. Initialize Folium Baseline OpenStreetMap Canvas Engine
                    m = folium.Map(location=[lat, lon], zoom_start=15, control_scale=True)
                    
                    # 2. Render moving driver target coordinate pin with interactive popup layout
                    folium.Marker(
                        [lat, lon],
                        popup=f"<b>Your Valet Driver ({driver_name})</b><br>Status: {current_status}",
                        tooltip="Click to view driver information",
                        icon=folium.Icon(color='red', icon='car', prefix='fa')
                    ).add_to(m)
                    
                    # 3. Add a fixed destination drop-off checkpoint hub marker (Pure White / Blue tint pin)
                    folium.Marker(
                        [17.5490, 78.3950],
                        popup="<b>ParkEz Drop-off/Pickup Hub</b>",
                        icon=folium.Icon(color='blue', icon='flag')
                    ).add_to(m)
                    
                    # 4. Draw a clear navigational path line between the car and the pickup hub
                    folium.PolyLine(
                        locations=[[lat, lon], [17.5490, 78.3950]],
                        color="#DC2626",
                        weight=4,
                        opacity=0.7
                    ).add_to(m)
                    
                    # Render map inline directly within the view grids
                    st_folium(m, width="100%", height=500, key=f"map_{lat}_{lon}")
                else:
                    st.error("Telemetry link lost.")

            run_radar_telemetry(search_ticket)
        else:
            st.error("Ticket hash index not detected inside database records.")

# ================= MY PARKING HISTORY =================
with tab3:
    st.subheader("Your Completed Bookings")
    user_phone = st.session_state.get("user_phone", "")
    if user_phone:
        try:
            history_df = get_customer_history_df(user_phone)
            if not history_df.empty:
                st.dataframe(history_df, use_container_width=True, hide_index=True)
            else:
                st.info("No logs matched your records profiles.")
        except Exception as e:
            st.error(f"Data link trace failed: {e}")
