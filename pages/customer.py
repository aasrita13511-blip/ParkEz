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




/* BUTTON STYLE */

div.stButton > button{

background:#1A365D !important;

color:white !important;

border-radius:30px !important;

font-weight:bold !important;

width:100% !important;

}




/* SIDEBAR DARK STYLE */

section[data-testid="stSidebar"]{

background:#212529 !important;

}



/* SIDEBAR ALL TEXT CAPITAL */

section[data-testid="stSidebar"] *,
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] span {


color:white !important;

text-transform:uppercase !important;

letter-spacing:1.2px !important;

font-weight:700 !important;


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





# ================= REQUEST VALET =================



with book:



    st.subheader(
    "Book Your Valet Driver"
    )


    name = st.text_input(
    "Customer Name"
    )


    phone = st.text_input(
    "Phone Number"
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


        if name and phone and car_model and vehicle_number:



            ticket = (

            "VAL" +

            str(random.randint(1000,9999))

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
            "VALET DRIVER ASSIGNED SUCCESSFULLY"
            )



            st.info(

f"""

🎫 TICKET ID : {ticket}


🚘 DRIVER : {driver}


📍 STATUS : DRIVER ASSIGNED

"""

)





        else:


            st.warning(
            "PLEASE FILL ALL DETAILS"
            )







# ================= RETRIEVE VEHICLE =================



with retrieve:



    st.subheader(
    "REQUEST VEHICLE RETRIEVAL"
    )



    ticket = st.text_input(
    "ENTER TICKET ID"
    )



    leave_time = st.selectbox(

    "WHEN ARE YOU LEAVING?",

    [

    "2 MINUTES",

    "5 MINUTES",

    "10 MINUTES"

    ]

    )




    if st.button(
    "BRING MY CAR"
    ):



        booking = get_booking(ticket)




        if booking:



            update_status(

            ticket,

            "VEHICLE RETURNING"

            )



            st.success(
            "DRIVER HAS BEEN NOTIFIED"
            )



            st.subheader(
            "📍 LIVE TRACKING"
            )



            tracking = st.empty()


            progress = st.progress(0)




            steps=[


            "DRIVER ASSIGNED 🚘",


            "DRIVER GOING TO PARKING AREA 📍",


            "VEHICLE LOCATED 🔎",


            "VEHICLE MOVING 🚗",


            "ARRIVING AT PICKUP POINT ✅"


            ]




            for i,step in enumerate(steps):


                time.sleep(1)


                tracking.info(step)


                progress.progress(
                (i+1)/len(steps)
                )




            st.success(

f"""

VEHICLE READY!


ETA : {leave_time}


DRIVER : {booking[7]}

"""

)





        else:


            st.error(
            "INVALID TICKET ID"
            )









# ================= FEATURES =================



st.divider()


st.markdown(
"### EXPLORE WHAT YOU CAN DO WITH PARKEZ"
)



col1,col2,col3 = st.columns(3)





with col1:


    st.markdown(

"""
<div class="benefit-card">

<h3>🚗 BOOK SPOT</h3>

<p>
Reserve parking before arrival.
</p>

</div>

""",

unsafe_allow_html=True

)



    if st.button(
    "DETAILS",
    key="spot"
    ):


        st.info(

"""

🚗 BOOK SPOT


Reserve your parking before arrival.


HOW IT WORKS:


1. ENTER CUSTOMER DETAILS

2. ADD VEHICLE DETAILS

3. SELECT ARRIVAL TIME

4. REQUEST VALET DRIVER

5. RECEIVE TICKET ID



BENEFITS:


✓ NO WAITING QUEUES

✓ QUICK DRIVER ASSIGNMENT

✓ LIVE TRACKING

✓ EASY RETRIEVAL


"""

)





with col2:


    st.markdown(

"""
<div class="benefit-card">

<h3>📅 MONTHLY PASS</h3>

<p>
Fixed parking access for regular customers.
</p>

</div>

""",

unsafe_allow_html=True

)



    if st.button(
    "DETAILS",
    key="pass"
    ):


        st.info(

"""

📅 MONTHLY PASS


ENJOY EASIER PARKING WITH PARKEZ.


FEATURES:


✓ FIXED MONTHLY RATES

✓ FASTER PARKING ACCESS

✓ NO REPEATED BOOKINGS

✓ CONVENIENT FOR REGULAR USERS



PERFECT FOR:


• OFFICE EMPLOYEES

• FREQUENT VISITORS


"""

)






with col3:


    st.markdown(

"""
<div class="benefit-card">

<h3>⚡ EV CHARGING</h3>

<p>
Charge your EV while parked.
</p>

</div>

""",

unsafe_allow_html=True

)



    if st.button(
    "DETAILS",
    key="ev"
    ):


        st.info(

"""

⚡ EV CHARGING


CHARGE YOUR ELECTRIC VEHICLE WITH PARKEZ.


FEATURES:


✓ EV SUPPORT

✓ SECURE PARKING

✓ CHARGING WHILE PARKED

✓ SAVES TIME



AVAILABILITY DEPENDS ON VENUE.


"""

)







# ================= CHATBOT =================



if st.button(
"💬",
key="chat"
):


    st.switch_page(
    "pages/support_chatbot.py"
    )