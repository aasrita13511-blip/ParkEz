import streamlit as st
import pandas as pd
from database import (
    total_cars,
    retrieved_cars,
    active_drivers,
    get_bookings_df
)
from styles import apply_corporate_theme, render_brand_header

st.set_page_config(
    page_title="Manager Dashboard",
    page_icon="📊",
    layout="wide"
)

apply_corporate_theme()
render_brand_header("Enterprise Administration Dashboard")

st.write("Monitor valet operations in real time.")
st.divider()

# ------------ ANALYTICS ------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🚗 TOTAL CARS", total_cars())

with col2:
    st.metric("✅ CARS RETRIEVED", retrieved_cars())

with col3:
    st.metric("👨‍✈️ ACTIVE DRIVERS", len(active_drivers()))

with col4:
    st.metric("⏱ AVG WAIT TIME", "3 Minutes")

st.divider()

# ------------ DRIVER DETAILS ------------
st.subheader("👨‍✈️ DRIVER AVAILABILITY")
drivers = active_drivers()

if drivers:
    driver_cols = st.columns(min(len(drivers), 4))
    for idx, driver in enumerate(drivers):
        with driver_cols[idx % 4]:
            st.markdown(
                f"""
                <div class="card">
                    <h4>👨‍✈️ {driver[1]}</h4>
                    <p style="margin:4px 0;"><b>📞 Phone:</b> {driver[2]}</p>
                    <p style="margin:4px 0; color: #16A34A;"><b>Status:</b> 🟢 {driver[3]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.warning("No drivers available")

st.divider()

# ------------ VEHICLE ACTIVITY ------------
st.subheader("🚗 LIVE VEHICLE ACTIVITY LOG")

try:
    df = get_bookings_df()
except Exception as e:
    st.error(f"Error reading booking records: {e}")
    df = pd.DataFrame()

if not df.empty:
    search = st.text_input("🔍 Search Activity Log (Type Name, Ticket, or Car Model to filter):")
    
    if search:
        df = df[
            df['customer'].str.contains(search, case=False, na=False) |
            df['ticket'].str.contains(search, case=False, na=False) |
            df['car_model'].str.contains(search, case=False, na=False) |
            df['vehicle_number'].str.contains(search, case=False, na=False)
        ]
    
    # Hide tracking coordinate columns from display log table view
    st.dataframe(df.drop(columns=['current_lat', 'current_lon'], errors='ignore'), use_container_width=True, hide_index=True)
    
    csv_report = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Operational Activity Report (CSV)",
        data=csv_report,
        file_name="parkez_operations_log.csv",
        mime="text/csv"
    )
else:
    st.info("No vehicle activity logged yet.")
