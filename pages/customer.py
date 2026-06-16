import streamlit as st
import random
import time
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

# Apply global red & white enterprise styles instantly
apply_corporate_theme()
render_brand_header("Customer Interactive Valet Space")

# --- CONSOLIDATED STABLE MULTI-TAB VIEW PORTS ---
tab1, tab2, tab3 = st.tabs(
    [
        "🚗 REQUEST VALET", 
        "🔑 LIVE STATUS TRACKER", 
        "📊 MY PARKING HISTORY"
    ]
)

# ================= REQUEST VALET =================
with tab1:
    st.subheader("Book Your Valet Driver")
    
    # Safely unpack saved customer profiles directly out of active sessions
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
            driver_data = get_available_driver()
            
            # Check query string results formats cleanly
            driver = driver_data[0] if isinstance(driver_data, (list, tuple)) else driver_data

            add_booking((
                ticket, name, phone, car_model, vehicle_number, 
                str(arrival), driver, "Driver Assigned", "Just Now"
            ))

            st.success("Valet Driver Assigned Successfully")
            st.info(f"🎫 **Ticket ID :** {ticket}  \n👨‍✈️ **Assigned Driver :** {driver}  \n📌 **Status :** Driver Assigned")
        else:
            st.warning("Please fill all details")

# ================= LIVE STATUS TRACKER (STABLE SWIGGY/ZOMATO MILESTONES) =================
with tab2:
    st.subheader("Request Vehicle Retrieval")
    ticket_id = st.text_input("Enter Ticket ID")
    leave_time = st.selectbox("When are you leaving?", ["2 Minutes", "5 Minutes", "10 Minutes"])

    if st.button("BRING MY CAR"):
        booking = get_booking(ticket_id)
        if booking:
            update_status(ticket_id, "Vehicle Returning")
            st.success("Driver has been notified successfully!")
            st.divider()

            st.subheader("🛰️ LIVE DISPATCH TRACKING PROGRESS")
            
            # Use isolated single-render element controls to safely bypass loop thread blocks
            status_box = st.empty()
            progress_bar = st.progress(0)

            steps = [
                "Driver Assigned 🚘",
                "Driver Going To Parking Area 📍",
                "Vehicle Located 🔎",
                "Vehicle Moving 🚗",
                "Arriving At Pickup Point ✅"
            ]

            # Loop updates text states cleanly without overloading browser engine canvases
            for idx, step in enumerate(steps):
                status_box.info(f"**Current Status:** {step}")
                progress_bar.progress((idx + 1) / len(steps))
                time.sleep(1)

            disp_driver = booking[7] if len(booking) > 7 else "Your Assigned Valet"
            st.success(f"🎉 **Your vehicle is ready at the pickup point!**  \n⏱️ **ETA :** {leave_time}  \n👨‍✈️ **Driver :** {disp_driver}")
        else:
            st.error("Invalid Ticket ID. Could not boot operational progress matrix.")

# ================= MY PARKING HISTORY (PANDAS DATA GRID) =================
with tab3:
    st.subheader("Your Completed Bookings")
    user_phone = st.session_state.get("user_phone", "")
    
    if user_phone:
        try:
            history_df = get_customer_history_df(user_phone)
            if not history_df.empty:
                # Render clean structural tabular sorting grids natively using Pandas
                st.dataframe(history_df, use_container_width=True, hide_index=True)
                
                # Single action click data exporter report downloader setup
                csv_file = history_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download My History (CSV)",
                    data=csv_file,
                    file_name=f"parkez_history_{user_phone}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No booking records found matching your active phone number profile.")
        except Exception as e:
            st.error(f"Error compiling user dashboard reporting structures: {e}")
    else:
        st.warning("Please log in from the main portal authentication homepage first to trace your history profiles.")
