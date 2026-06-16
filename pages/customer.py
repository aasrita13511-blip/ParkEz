import streamlit as st
import random
import pandas as pd
from database import (
    add_booking,
    get_available_driver,
    get_booking,
    update_status,
    get_customer_history_df
)
from styles import apply_corporate_theme, render_brand_header

st.set_page_config(
    page_title="Customer Portal",
    page_icon="🚗",
    layout="wide"
)

apply_corporate_theme()
render_brand_header("Customer Operations Panel")

tab1, tab2, tab3 = st.tabs(
    [
        "🚗 REQUEST VALET",
        "🔑 RETRIEVE VEHICLE",
        "📊 MY PARKING HISTORY"
    ]
)

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

    if st.button("REQUEST DRIVER"):
        if name and phone and car_model and vehicle_number:
            ticket = "VAL" + str(random.randint(1000, 9999))
            driver = get_available_driver()

            add_booking((
                ticket, name, phone, car_model, vehicle_number,
                str(arrival), driver, "Driver Assigned", "Just Now"
            ))

            st.success("Valet Driver Assigned Successfully")
            st.info(f"🎫 Ticket ID : {ticket}  \n🚘 Driver : {driver}  \n📍 Status : Driver Assigned")
        else:
            st.warning("Please fill all details")

# ================= RETRIEVE & TRACK VEHICLE (STABLE MAP FRAGMENT) =================
with tab2:
    st.subheader("Request Vehicle Retrieval")
    search_ticket = st.text_input("Enter Ticket ID to Track")

    if search_ticket:
        booking = get_booking(search_ticket)
        if booking:
            if st.button("🚨 REQUEST VEHICLE RETRIEVAL"):
                update_status(search_ticket, "Vehicle Returning")
                st.success("Driver has been notified!")

            st.divider()
            st.subheader("📍 LIVE DRIVER LOCATOR MAP")

            # --- CRITICAL: Safe auto-refresh component container block ---
            @st.fragment(run_every=4.0)
            def render_live_tracker(t_id):
                live_data = get_booking(t_id)
                if live_data:
                    # Map structural variables accurately matching index configurations
                    current_status = live_data[8]
                    lat = live_data[10] if live_data[10] is not None else 17.545
                    lon = live_data[11] if live_data[11] is not None else 78.390

                    st.info(f"**Current Vehicle Status:** {current_status} | **Last Updated:** {live_data[9]}")
                    
                    # Package metrics array directly to map framework data grids
                    map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
                    st.map(map_df, zoom=15)
                else:
                    st.error("Tracking signal disconnected.")

            # Fire execution sequence safely inline
            render_live_tracker(search_ticket)
        else:
            st.error("Ticket ID not found in system.")

# ================= PARKING HISTORY =================
with tab3:
    st.subheader("Your Completed Bookings")
    user_phone = st.session_state.get("user_phone", "")
    if user_phone:
        try:
            history_df = get_customer_history_df(user_phone)
            if not history_df.empty:
                st.dataframe(history_df, use_container_width=True, hide_index=True)
            else:
                st.info("No records found.")
        except Exception as e:
            st.error(f"Error: {e}")
