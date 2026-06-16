import streamlit as st
import pandas as pd  # <--- NEW: Integrated for summary reports and grids
from database import (
    total_cars,
    retrieved_cars,
    active_drivers,
    get_bookings_df  # <--- NEW: Fast Pandas data framework query
)

st.set_page_config(
    page_title="Manager Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------ STYLE ------------

st.markdown("""
<style>

.title{
text-align:center;
font-size:42px;
font-weight:bold;
color:#0B3D91;
}

.card{
background:white;
padding:20px;
border-radius:18px;
box-shadow:0px 5px 15px #ddd;
margin-bottom: 15px;
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
<div class="title">
📊 VENUE MANAGER DASHBOARD
</div>
""",
unsafe_allow_html=True
)

st.write("Monitor valet operations in real time.")
st.divider()

# ------------ ANALYTICS ------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Extracted first element to avoid bracket rendering errors
    tot = total_cars()
    val_tot = tot[0] if isinstance(tot, (list, tuple)) else tot
    st.metric("🚗 TOTAL CARS", val_tot)

with col2:
    ret = retrieved_cars()
    val_ret = ret[0] if isinstance(ret, (list, tuple)) else ret
    st.metric("✅ CARS RETRIEVED", val_ret)

with col3:
    st.metric("👨‍✈️ ACTIVE DRIVERS", len(active_drivers()))

with col4:
    st.metric("⏱ AVG WAIT TIME", "3 Minutes")

st.divider()

# ------------ DRIVER DETAILS ------------

st.subheader("👨‍✈️ DRIVER AVAILABILITY")
drivers = active_drivers()

if drivers:
    # Use clean multi-column layouts instead of long single scrolls
    driver_cols = st.columns(min(len(drivers), 4))
    for idx, driver in enumerate(drivers):
        with driver_cols[idx % 4]:
            st.markdown(
                f"""
                <div class="card">
                    <h4>👨‍✈️ {driver[1]}</h4>
                    <p style="margin:4px 0;"><b>📞 Phone:</b> {driver[2]}</p>
                    <p style="margin:4px 0; color: #16A34A;"><b>Status:</b> 🟢 {driver[3] if len(driver) > 3 else "Available"}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.warning("No drivers available")

st.divider()

# ------------ VEHICLE ACTIVITY (UPGRADED WITH PANDAS) ------------

st.subheader("🚗 LIVE VEHICLE ACTIVITY LOG")

try:
    df = get_bookings_df()
except Exception as e:
    st.error(f"Error reading booking records: {e}")
    df = pd.DataFrame()

if not df.empty:
    # Beautiful Pandas features: Clean string search filter
    search = st.text_input("🔍 Search Activity Log (Type Name, Ticket, or Car Model to filter):")
    
    if search:
        df = df[
            df['customer'].str.contains(search, case=False, na=False) |
            df['ticket'].str.contains(search, case=False, na=False) |
            df['car_model'].str.contains(search, case=False, na=False) |
            df['vehicle_number'].str.contains(search, case=False, na=False)
        ]
    
    # Render interactive, clean table
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Download automated Excel/CSV operational reports 
    csv_report = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Operational Activity Report (CSV)",
        data=csv_report,
        file_name="parkez_operations_log.csv",
        mime="text/csv"
    )
else:
    st.info("No vehicle activity logged yet.")
