import streamlit as st
import random

from database import *


st.set_page_config(
    page_title="Customer Portal",
    page_icon="🚗"
)


st.title("🚗 Customer Portal")

st.write(
"Request your valet driver before arrival and retrieve your car without waiting."
)



option = st.radio(
    "Choose Action",
    [
        "Book Valet Driver",
        "Retrieve Vehicle"
    ]
)



# ---------------- BOOKING ----------------

if option == "Book Valet Driver":


    st.subheader("🚘 Vehicle Booking")


    name = st.text_input(
        "Customer Name"
    )


    phone = st.text_input(
        "Phone Number"
    )


    car = st.text_input(
        "Car Model / Name"
    )


    number = st.text_input(
        "Vehicle Number Plate"
    )


    arrival = st.time_input(
        "Expected Arrival Time"
    )



    if st.button("Request Valet Driver"):


        ticket = "VAL" + str(
            random.randint(1000,9999)
        )


        driver = get_driver()



        add_booking(

        (
        ticket,
        name,
        phone,
        car,
        number,
        str(arrival),
        driver,
        "Driver Assigned",
        ""
        )

        )



        st.success(
        "Valet booking confirmed"
        )


        st.info(
        f"""
        Ticket ID:

        {ticket}


        Assigned Driver:

        {driver}


        Status:

        Driver is ready for pickup
        """
        )





# ---------------- RETRIEVE ----------------


else:


    st.subheader(
    "🔑 Retrieve Vehicle"
    )



    ticket = st.text_input(
        "Enter Ticket ID"
    )



    leave = st.selectbox(
        "When are you leaving?",
        [
        "2 Minutes",
        "5 Minutes",
        "10 Minutes"
        ]
    )




    if st.button("Bring My Car"):


        booking = get_booking(ticket)



        if booking:


            update_status(
            ticket,
            "Driver bringing vehicle"
            )



            st.success(
            "Driver has been notified"
            )


            st.write(
            """
            Vehicle Tracking:

            ✅ Request Received

            ✅ Driver going to parking area

            ✅ Vehicle picked up

            🚗 Coming to pickup point

            """
            )


            st.info(
            f"Estimated arrival time: {leave}"
            )



        else:


            st.error(
            "Invalid Ticket ID"
            )