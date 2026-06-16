import streamlit as st
import random
import time

from database import (
    add_booking,
    get_available_driver,
    get_booking,
    update_status
)


st.set_page_config(
    page_title="Customer Portal",
    page_icon="🚗",
    layout="wide"
)


# ---------------- STYLE ----------------

st.markdown("""
<style>

.stApp {
    background-color:#F8F9FA !important;
    font-family:'Inter',sans-serif !important;
}


.portal-title{
text-align:center;
font-size:40px;
font-weight:bold;
color:#1A365D;
}


.benefit-card{

background:#EEEEEE;

border-radius:12px;

padding:24px;

min-height:160px;

}


.benefit-card h3{

color:#1A202C;

font-size:20px;

}


.benefit-card p{

color:#718096;

}


div.stButton > button{

background:#1A365D !important;

color:white !important;

border-radius:30px !important;

font-weight:bold !important;

width:100% !important;

}



section[data-testid="stSidebar"]{

background:#212529 !important;

}


section[data-testid="stSidebar"] *{

color:white !important;

}

</style>

""", unsafe_allow_html=True)



# ---------------- TITLE ----------------


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


book,retrieve = st.tabs(
[
"🚗 REQUEST VALET",
"🔑 RETRIEVE VEHICLE"
]
)




# ================= BOOK VALET =================


with book:


    st.subheader("Book Your Valet Driver")


    name = st.text_input("Customer Name")

    phone = st.text_input("Phone Number")

    car_model = st.text_input("Car Model")

    vehicle_number = st.text_input("Vehicle Number")

    arrival = st.time_input("Arrival Time")



    if st.button("REQUEST DRIVER"):


        if name and phone and car_model and vehicle_number:


            ticket = "VAL" + str(random.randint(1000,9999))


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





# ================= RETRIEVE =================


with retrieve:


    st.subheader("Request Vehicle Retrieval")


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



    if st.button("BRING MY CAR"):


        booking = get_booking(ticket)



        if booking:


            update_status(
            ticket,
            "Vehicle Returning"
            )


            st.success(
            "Driver has been notified"
            )


            st.subheader(
            "📍 LIVE TRACKING"
            )



            tracking = st.empty()


            progress = st.progress(0)



            steps=[

            "Driver Assigned 🚘",

            "Driver Going To Parking Area 📍",

            "Vehicle Located 🔎",

            "Vehicle Moving 🚗",

            "Arriving At Pickup Point ✅"

            ]



            for i,step in enumerate(steps):


                time.sleep(1)

                tracking.info(step)

                progress.progress(
                (i+1)/len(steps)
                )



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





# =================================================
# EXPLORE PARK EZ FEATURES
# =================================================


st.divider()

st.markdown(
"### Explore what you can do with ParkEz"
)



col1,col2,col3 = st.columns(3)




# BOOK SPOT


with col1:


    st.markdown(
"""
<div class="benefit-card">

<h3>🚗 Book Spot</h3>

<p>
Reserve parking in advance.
Skip waiting lines.
</p>

</div>

""",
unsafe_allow_html=True
)



    if st.button(
    "Details",
    key="spot"
    ):


        st.info(
"""
🚗 BOOK SPOT


Reserve your parking before arrival.


How it works:

1. Enter customer details

2. Add vehicle details

3. Select arrival time

4. Request valet driver

5. Receive Ticket ID


Benefits:

✓ No waiting queues

✓ Quick valet assignment

✓ Live tracking

✓ Easy retrieval

"""
)





# MONTHLY PASS


with col2:


    st.markdown(
"""
<div class="benefit-card">

<h3>📅 Monthly Pass</h3>

<p>
Fixed parking access for regular customers.
</p>

</div>

""",
unsafe_allow_html=True
)



    if st.button(
    "Details",
    key="pass"
    ):


        st.info(
"""
📅 MONTHLY PASS


Enjoy easier parking with ParkEz.


How it works:

1. Register for a monthly plan

2. Select parking location

3. Activate your pass


Benefits:

✓ Fixed monthly rates

✓ Faster parking access

✓ No repeated booking

✓ Convenient for regular users


Perfect for:

• Office employees

• Frequent visitors

"""
)





# EV CHARGING


with col3:


    st.markdown(
"""
<div class="benefit-card">

<h3>⚡ EV Charging</h3>

<p>
Charge your EV while parked.
</p>

</div>

""",
unsafe_allow_html=True
)



    if st.button(
    "Details",
    key="ev"
    ):


        st.info(
"""
⚡ EV CHARGING


Charge your electric vehicle with ParkEz.


How it works:

1. Select EV parking location

2. Park your vehicle

3. Connect charging station

4. Monitor charging status


Features:

✓ EV support

✓ Secure parking

✓ Charging while parked

✓ Saves time


Availability depends on venue.

"""
)






# =================================================
# CHATBOT BUTTON
# =================================================


if st.button(
"💬",
key="chat"
):

    st.switch_page(
    "pages/support_chatbot.py"
    )