import streamlit as st
import random
import pandas as pd
from database import add_booking, get_booking, update_status, get_customer_history_df
from styles import apply_corporate_theme, render_brand_header

st.set_page_config(
    page_title="Customer App Interface", 
    page_icon="🚗", 
    layout="wide"
)

# Apply global red & white styles
apply_corporate_theme()
render_brand_header("Customer Interactive Valet Space")

tab1, tab2, tab3 = st.tabs(["🚗 REQUEST VALET", "🔑 LIVE TELEMETRY TRACKER", "📊 MY PARKING HISTORY"])

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

# ================= RETRIEVE & TRACK VEHICLE (SWIGGY / ZOMATO MULTI-MILESTONE TRACKER) =================
with tab2:
    st.subheader("Live Telemetry Radar Tracker")
    search_ticket = st.text_input("Enter Ticket ID to start live tracker")

    if search_ticket:
        booking = get_booking(search_ticket)
        if booking:
            if st.button("🚨 BROADCAST VEHICLE RETRIEVAL SIGNAL"):
                update_status(search_ticket, "Vehicle Returning")
                st.toast("⚡ Signal broadcast successfully to driver display panels!")

            st.divider()
            
            # --- SAFE WEB REFRESH SUBCOMPONENT FRAGMENT (No looping crashes) ---
            @st.fragment(run_every=4.0)
            def run_radar_telemetry(t_id):
                live_data = get_booking(t_id)
                if live_data:
                    current_status = live_data[8]
                    lat = live_data[10] if live_data[10] is not None else 17.545
                    lon = live_data[11] if live_data[11] is not None else 78.390
                    driver_name = live_data[7] if live_data[7] is not None else "Assigned Driver"
                    
                    # --- SWIGGY/ZOMATO STYLE STEP PROGRESS INDICATOR CARD ---
                    st.markdown(f"### 🛵 Live Driver Dispatch: {driver_name}")
                    st.write(f"📍 **Current Telemetry Beacon:** Lat `{lat:.4f}`, Lon `{lon:.4f}`")
                    
                    # Modern step indicator matrix cards
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if current_status == "Driver Assigned":
                            st.markdown("<div style='background:#EFF6FF; border-left:5px solid #1E3A8A; padding:15px; border-radius:8px;'><b>🔵 STEP 1/4</b><br>Driver Dispatched</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='background:#F1F5F9; padding:15px; border-radius:8px; color:#94A3B8;'>✓ Driver Dispatched</div>", unsafe_allow_html=True)
                            
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
                            st.markdown("<div style='background:#F1F5F9; padding:15px; border-radius:8px; color:#94A3B8;'>🔒 Step 4: Retrieval Ready</div>", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Stable corporate roads map grid without memory loops crashing your frame
                    map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
                    st.map(map_df, zoom=15)
                else:
                    st.error("Telemetry link lost.")

            run_radar_telemetry(search_ticket)
        else:
            st.error("Ticket ID not found inside database records.")

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
