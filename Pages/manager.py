import streamlit as st

from database import *



st.set_page_config(
    page_title="Manager Dashboard",
    page_icon="📊"
)



st.title(
"📊 Venue Manager Dashboard"
)


st.write(
"Monitor valet operations in real time."
)



# Metrics


c1,c2,c3,c4 = st.columns(4)



with c1:

    st.metric(
    "Total Cars",
    total_cars()
    )



with c2:

    st.metric(
    "Cars Retrieved",
    cars_retrieved()
    )



with c3:

    st.metric(
    "Average Wait Time",
    f"{average_wait()} mins"
    )



with c4:

    st.metric(
    "Active Drivers",
    len(active_drivers())
    )



st.divider()



# Drivers


st.subheader(
"🚘 Driver Details"
)



drivers = active_drivers()



for d in drivers:


    st.success(

    f"""
    Driver Name:

    {d[0]}


    Phone:

    {d[1]}


    Status:

    Available

    """

    )




st.divider()



# Cars


st.subheader(
"🚗 Vehicle Activity"
)



data = all_bookings()



for row in data:


    st.write(

    f"""
    Ticket:

    {row[1]}


    Customer:

    {row[2]}


    Car:

    {row[4]}


    Driver:

    {row[7]}


    Status:

    {row[8]}

    """
    )


    st.divider()