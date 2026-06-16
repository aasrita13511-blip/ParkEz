import streamlit as st
import random
from database import add_booking, get_booking, update_status, get_customer_history_df
from styles import apply_corporate_theme, render_brand_header

st.set_page_config(
    page_title="Customer Portal",
    page_icon="🚗",
    layout="wide"
)

apply_corporate_theme()
render_brand_header("Customer Interactive Valet Space")

tab1, tab2, tab3 = st.tabs(["🚗 REQUEST VALET", "🔑 LIVE STATUS TRACKER", "📊 MY PARKING HISTORY"])

# ================= REQUEST VALET =================
with tab1:
    st.subheader("Book Your Valet Driver")
    default_name = st.session_state.get("user_name", "")
    default_phone = st.session_state.get("user_phone", "")

    name = st.text_input("Customer Name", value=default_name, key="c_name")
    phone = st.text_input("Phone Number", value=default_phone, key="c_phone")
    car_model = st.text_input("Car Model", key="c_car")
    vehicle_number = st.text_input("Vehicle Number", key="c_num")
    arrival = st.time_input("Arrival Time", key="c_time")

    if st.button("REQUEST DRIVER"):
        if name and phone and car_model and vehicle_number:
            ticket = "VAL" + str(random.randint(1000, 9999))
            add_booking((ticket, name, phone, car_model, vehicle_number, str(arrival), "Rahul", "Driver Assigned", "Just Now"))
            st.success("Valet Request Sent Successfully!")
            st.info(f"🎫 **Ticket ID:** {ticket} | Copy this code to track your car.")
        else:
            st.warning("Please fill all details")

# ================= LIVE STATUS TRACKER (100% STABLE - NO LOOPS) =================
with tab2:
    st.subheader("Live Progress Tracking Dashboard")
    search_ticket = st.text_input("Enter Ticket ID to look up status", key="track_t_id")

    if search_ticket:
        booking = get_booking(search_ticket)
        if booking:
            if st.button("🚨 REQUEST VEHICLE RETRIEVAL"):
                update_status(search_ticket, "Vehicle Returning")
                st.toast("Retrieval request broadcasted to drivers!")
                st.rerun()

            st.divider()
            
            # Read status statically out of database row
            current_status = booking[8] if len(booking) > 8 else "Driver Assigned"
            driver_name = booking[7] if len(booking) > 7 else "Assigned Driver"
            
            st.markdown(f"### 👨‍✈️ Driver Assigned: {driver_name}")
            
            # --- STATIC TIMELINE MILESTONES ---
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if current_status == "Driver Assigned":
                    st.markdown("<div style='background:#EFF6FF; border-left:5px solid #1E3A8A; padding:15px; border-radius:8px;'><b>🔵 STEP 1/4</b><br>Driver Confirmed</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='background:#F1F5F9; padding:15px; border-radius:8px; color:#94A3B8;'>✓ Driver Confirmed</div>", unsafe_allow_html=True)
                    
            with col2:
                if current_status == "Picked Up":
                    st.markdown("<div style='background:#FEF3C7; border-left:5px solid #D97706; padding:15px; border-radius:8px;'><b>🟠 STEP 2/4</b><br>Vehicle Picked Up</div>", unsafe_allow_html=True)
                elif current_status in ["Parked Vehicle", "Vehicle Returning", "Delivered Vehicle"]:
                    st.markdown("<div style='background:#F1F5F9; padding:15px; border-radius:8px; color:#94A3B8;'>✓ Vehicle Picked Up</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='background:#F1F5F9; padding:15px; border-radius:8px; color:#94A3B8;'>🔒 Step 2: Pickup Pending</div>", unsafe_allow_html=True)
                    
            with col3:
                if current_status == "Parked Vehicle":
                    st.markdown("<div style='background:#DCFCE7; border-left:5px solid #16A34A; padding:15px; border-radius:8px;'><b>🟢 STEP 3/4</b><br>Secured in Lot</div>", unsafe_allow_html=True)
                elif current_status in ["Vehicle Returning", "Delivered Vehicle"]:
                    st.markdown("<div style='background:#F1F5F9; padding:15px; border-radius:8px; color:#94A3B8;'>✓ Secured in Lot</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='background:#F1F5F9; padding:15px; border-radius:8px; color:#94A3B8;'>🔒 Step 3: Lot Transit</div>", unsafe_allow_html=True)
                    
            with col4:
                if current_status == "Vehicle Returning":
                    st.markdown("<div style='background:#FEE2E2; border-left:5px solid #DC2626; padding:15px; border-radius:8px;'><b>🔴 STEP 4/4</b><br>Vehicle Returning!</div>", unsafe_allow_html=True)
                elif current_status == "Delivered Vehicle":
                    st.markdown("<div style='background:#DCFCE7; border-left:5px solid #16A34A; padding:15px; border-radius:8px;'><b>✅ COMPLETE</b><br>Car Delivered!</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='background:#F1F5F9; padding:15px; border-radius:8px; color:#94A3B8;'>🔒 Step 4: Ready at Terminal</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.success(f"Current System State: The vehicle status is currently **'{current_status}'**.")
        else:
            st.error("Ticket ID not found.")

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
                st.info("No records found.")
        except Exception as e:
            st.error(f"Error: {e}")


# ================= FLOATING CHAT BUTTON REQUIREMENT =================
st.markdown(
    """
    <style>
    div.stActionButton {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 999999;
    }
    .stActionButton button {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        font-size: 28px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
        border: none !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stActionButton button:hover {
        background-color: #e04040 !important;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Container rendering the navigation chat action target
with st.container():
    st.markdown('<div class="stActionButton">', unsafe_allow_html=True)
    if st.button("💬", key="customer_floating_chat_action"):
        st.switch_page("pages/support_chatbot.py")
    st.markdown('</div>', unsafe_allow_html=True)
