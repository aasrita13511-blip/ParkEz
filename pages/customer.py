import streamlit as st
import random
import time
import pandas as pd
import numpy as np

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

# ================= BOOK VALET =================
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

# ================= RETRIEVE VEHICLE =================
with tab2:
    st.subheader("Request Vehicle Retrieval")
    ticket = st.text_input("Enter Ticket ID")
    leave_time = st.selectbox("When are you leaving?", ["2 Minutes", "5 Minutes", "10 Minutes"])

    if st.button("BRING MY CAR"):
        booking = get_booking(ticket)
        if booking:
            update_status(ticket, "Vehicle Returning")
            st.success("Driver has been notified")
            st.divider()

            st.subheader("📍 LIVE DRIVER TRACKING MAP")
            map_col, text_col = st.columns(2)

            with text_col:
                tracking = st.empty()
                progress = st.progress(0)

            with map_col:
                map_placeholder = st.empty()

            steps = [
                "Driver Assigned 🚘",
                "Driver Going To Parking Area 📍",
                "Vehicle Located 🔎",
                "Vehicle Moving 🚗",
                "Arriving At Pickup Point ✅"
            ]

            start_lat, start_lon = 17.545, 78.390 
            end_lat, end_lon = 17.549, 78.395
            lats = np.linspace(start_lat, end_lat, len(steps))
            lons = np.linspace(start_lon, end_lon, len(steps))

            for i, step in enumerate(steps):
                time.sleep(1.2)
                tracking.info(step)
                progress.progress((i + 1) / len(steps))

                map_df = pd.DataFrame({'lat': [lats[i]], 'lon': [lons[i]]})
                map_placeholder.map(map_df, zoom=14)

            disp_driver = booking[7] if isinstance(booking, (list, tuple)) and len(booking) > 7 else "Assigned Valet"
            st.success(f"Vehicle Ready!  \nETA : {leave_time}  \nDriver : {disp_driver}")
        else:
            st.error("Invalid Ticket ID")

# ================= MY PARKING HISTORY =================
with tab3:
    st.subheader("Your Completed Bookings")
    user_phone = st.session_state.get("user_phone", "")
    
    if user_phone:
        try:
            history_df = get_customer_history_df(user_phone)
            if not history_df.empty:
                st.dataframe(history_df, use_container_width=True, hide_index=True)
                csv_file = history_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download My History (CSV)",
                    data=csv_file,
                    file_name=f"parkez_history_{user_phone}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No booking records found for your phone number.")
        except Exception as e:
            st.error(f"Error loading dashboard: {e}")
    else:
        st.warning("Please log in from the main portal homepage first.")
