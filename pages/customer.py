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

/* 
   PERMANENT VISIBILITY & CAPITALIZATION FIX:
   Forces all sidebar items into uppercase letters and overrides Streamlit's
   default dark font color to a clear, high-contrast crisp white.
*/
section[data-testid="stSidebar"] *, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebarNavItems"] span,
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] span,
.st-emotion-cache-16ids9d,
.st-emotion-cache-6q9w0q {
    color: #FFFFFF !important; 
    text-transform: uppercase !important; /* Forces all bar letters to be CAPITALS */
    letter-spacing: 1.2px !important;
    font-weight: 700 !important;
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

Driver : {booking}
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
        # Clean transition directly routing user to dedicated feature script
        st.switch_page("pages/book_spot_details.py")





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
        # Clean transition directly routing user to dedicated feature script
        st.switch_page("pages/monthly_pass_details.py")





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
        # Clean transition directly routing user to dedicated feature script
        st.switch_page("pages/ev_charging_details.py")






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
