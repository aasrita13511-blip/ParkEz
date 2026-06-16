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

# Apply global red & white enterprise styles instantly
apply_corporate_theme()
render_brand_header("Enterprise Administration Dashboard")

st.write("Monitor valet operations in real time.")
st.divider()

# ------------ ANALYTICS ------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    tot = total_cars()
    val_tot = tot if isinstance(tot, (list, tuple)) else tot
    st.metric("🚗 TOTAL CARS", val_tot)

with col2:
    ret = retrieved_cars()
    val_ret = ret if isinstance(ret, (list, tuple)) else ret
    st.metric("✅ CARS RETRIEVED", val_ret)

with col3:
    st.metric("👨‍✈️ ACTIVE DRIVERS", len(active_drivers()))

with col4:
    st.metric("⏱ AVG WAIT TIME", "3 Minutes")

st.divider()

# ------------ LOADING DATABASE DATAFRAME ------------
try:
    df = get_bookings_df()
except Exception as e:
    st.error(f"Error reading booking records from database: {e}")
    df = pd.DataFrame()

# ------------ INTERACTIVE OPERATIONAL CHARTS (PANDAS DATA ENGINE) ------------
if not df.empty:
    st.subheader("📊 REAL-TIME OPERATIONS ANALYTICS")
    
    # Calculate operational metrics per status group seamlessly
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status Category', 'Number of Vehicles']
    
    # Render interactive matching operational metrics bar chart
    st.bar_chart(
        data=status_counts, 
        x='Status Category', 
        y='Number of Vehicles', 
        use_container_width=True
    )
    st.divider()

# ------------ DRIVER DETAILS ------------
st.subheader("👨‍✈️ DRIVER AVAILABILITY")
drivers = active_drivers()

if drivers:
    driver_cols = st.columns(min(len(drivers), 4))
    for idx, driver in enumerate(drivers):
        # Extract flat strings array elements cleanly safely
        d_name = driver if isinstance(driver, (list, tuple)) and len(driver) > 1 else driver
        with driver_cols[idx % 4]:
            st.markdown(
                f"""
                <div class="card">
                    <h4>👨‍✈️ {d_name}</h4>
                    <p style="margin:4px 0;"><b>Status:</b> <span style="color:#16A34A;">🟢 Available</span></p>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.warning("No drivers available")

st.divider()

# ------------ VEHICLE ACTIVITY LOG ------------
st.subheader("🚗 LIVE VEHICLE ACTIVITY LOG")

if not df.empty:
    search = st.text_input("🔍 Search Activity Log (Type Name, Ticket, or Car Model to filter):")
    
    if search:
        df = df[
            df['customer'].str.contains(search, case=False, na=False) |
            df['ticket'].str.contains(search, case=False, na=False) |
            df['car_model'].str.contains(search, case=False, na=False) |
            df['vehicle_number'].str.contains(search, case=False, na=False)
        ]
    
    # Render clean structural tabular sorting grids natively using Pandas
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # One-click operations logging downloader utility activation 
    csv_report = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Operational Activity Report (CSV)",
        data=csv_report,
        file_name="parkez_operations_log.csv",
        mime="text/csv"
    )
else:
    st.info("No vehicle activity logged yet.")
