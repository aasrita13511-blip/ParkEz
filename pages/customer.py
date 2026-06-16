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


st.set_page_config(
    page_title="Customer Portal",
    page_icon="🚗",
    layout="wide"
)


# ---------------- STYLE ----------------

st.markdown("""
<style>

.portal-title{
text-align:center;
font-size:40px;
font-weight:bold;
color:#0B3D91;
}

.card{
background:white;
padding:25px;
border-radius:20px;
box-shadow:0px 5px 15px #ddd;
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
<div class="portal-title">
👤 CUSTOMER PORTAL
</div>
""",
unsafe_allow_html=True
)


st.divider()


# ---------------- TABS ----------------

book, retrieve, history = st.tabs(
[
"🚗 REQUEST VALET",
"🔑 RETRIEVE VEHICLE",
"📊 MY PARKING HISTORY"
]
)



# ================= BOOK VALET =================


with book:

    st.subheader(
        "Book Your Valet Driver"
    )

    # Automatically fill user details if stored in app.py session state memory
    default_name = st.session_state.get("user_name", "")
    default_phone = st.session_state.get("user_phone", "")

    name = st.text_input(
        "Customer Name",
        value=default_name
    )

    phone = st.text_input(
        "Phone Number",
        value=default_phone
    )

    car_model = st.text_input(
        "Car Model"
    )

    vehicle_number = st.text_input(
        "Vehicle Number"
    )

    arrival = st.time_input(
        "Arrival Time"
    )

    if st.button(
        "REQUEST DRIVER"
    ):

        if (
            name
            and phone
            and car_model
            and vehicle_number
        ):

            ticket = (
                "VAL"
                +
                str(
                    random.randint(
                        1000,
                        9999
                    )
                )
            )

            driver = get_available_driver()

            add_booking(
                (
                ticket,
                name,
                phone,
                car_model,
                vehicle_number,
                str(arrival),
                driver,
                "Driver Assigned",
                "Just Now"
                )
            )

            st.success(
                "Valet Driver Assigned Successfully"
            )

            st.info(
                f"""
🎫 Ticket ID : {ticket}

🚘 Driver : {driver}

📍 Status : Driver Assigned
"""
            )

        else:
            st.warning(
                "Please fill all details"
            )




# ================= RETRIEVE VEHICLE =================



with retrieve:

    st.subheader(
        "Request Vehicle Retrieval"
    )

    ticket = st.text_input(
        "Enter Ticket ID"
    )

    leave_time = st.selectbox(
        "When are you leaving?",
        [
            "2 Minutes",
            "5 Minutes",
            "10 Minutes"
        ]
    )

    if st.button(
        "BRING MY CAR"
    ):

        booking = get_booking(ticket)

        if booking:

            update_status(
                ticket,
                "Vehicle Returning"
            )

            st.success(
                "Driver has been notified"
            )

            st.divider()

            st.subheader(
                "📍 LIVE DRIVER TRACKING MAP"
            )

            # Set up layout containers for map animation side-by-side with text status
            map_col, text_col = st.columns([2, 1])

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

            # Simulating route points starting near a terminal moving toward pick-up center
            start_lat, start_lon = 17.545, 78.390 
            end_lat, end_lon = 17.549, 78.395

            lats = np.linspace(start_lat, end_lat, len(steps))
            lons = np.linspace(start_lon, end_lon, len(steps))

            for i, step in enumerate(steps):
                time.sleep(1.2)

                # Update step metrics text description
                tracking.info(step)
                progress.progress((i + 1) / len(steps))

                # Build spatial coordinate point trace using map elements
                map_df = pd.DataFrame({
                    'lat': [lats[i]],
                    'lon': [lons[i]]
                })
                
                # Renders structural visualization map live pointing tracker position
                map_placeholder.map(map_df, zoom=14)

            st.success(
                f"""
Vehicle Ready!

ETA : {leave_time}

Driver : {booking[7]}
"""
            )

        else:
            st.error(
                "Invalid Ticket ID"
            )


# ================= MY PARKING HISTORY (NEW PANDAS FEATURE) =================

with history:
    st.subheader("Your Completed Bookings")
    
    user_phone = st.session_state.get("user_phone", "")
    
    if user_phone:
        try:
            # Load specific individual entries instantly from our database pandas function
            history_df = get_customer_history_df(user_phone)
            
            if not history_df.empty:
                # Format dataframe layout display cleanly
                st.dataframe(history_df, use_container_width=True, hide_index=True)
                
                # Download report action toggle logic
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
            st.error(f"Error loading dashboard report layout structure: {e}")
    else:
        st.warning("Please log in from the main portal homepage first to safely load your private records.")
