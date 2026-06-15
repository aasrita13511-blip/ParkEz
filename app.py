import streamlit as st
from database import create_tables


st.set_page_config(
    page_title="ParkEz",
    page_icon="🚗",
    layout="centered"
)


create_tables()



# -------------------------
# Custom Styling
# -------------------------

st.markdown(
"""
<style>


/* Main background */

.stApp {

background-color:#F5F9FF;

}



/* Logo title */

.logo {

text-align:center;

font-size:55px;

font-weight:800;

color:#0B3D91;

margin-top:20px;

}



/* Tagline */

.tagline {

text-align:center;

font-size:32px;

font-weight:700;

color:#1E293B;

}



/* Description */

.desc {

text-align:center;

font-size:18px;

color:#475569;

}



/* Login card */

.login-box {

background:white;

padding:35px;

border-radius:20px;

box-shadow:0px 8px 25px rgba(0,0,0,0.08);

margin-top:35px;

}



/* Buttons */

.stButton button {


background:#0B3D91;

color:white;

border-radius:12px;

height:45px;

width:100%;

font-size:18px;


}


.stButton button:hover {

background:#06275F;

}



/* Feature cards */


.feature {


background:#E8F1FF;

padding:20px;

border-radius:15px;

text-align:center;

color:#0B3D91;


}



</style>

""",

unsafe_allow_html=True
)






# -------------------------
# Header
# -------------------------


st.markdown(
"""
<div class="logo">

🚗 ParkEz

</div>


<div class="tagline">

Skip the Wait, Enjoy the Ride

</div>


<div class="desc">

Your smart valet parking solution for malls, hotels,
clubs, restaurants and events.

</div>

""",

unsafe_allow_html=True
)





# -------------------------
# Login
# -------------------------


st.markdown(
'<div class="login-box">',

unsafe_allow_html=True
)



st.subheader(
"🔐 Login"
)



phone = st.text_input(
"Phone Number"
)


password = st.text_input(
"Password",
type="password"
)



role = st.selectbox(

"Login As",

[
"Customer",
"Driver",
"Venue Manager"
]

)





users = {


"9999999999":
{
"password":"1234",
"role":"Customer"
},


"8888888888":
{
"password":"1234",
"role":"Driver"
},


"7777777777":
{
"password":"1234",
"role":"Venue Manager"
}

}






if st.button("Login"):



    if phone in users and users[phone]["password"] == password:



        if users[phone]["role"] == role:



            if role=="Customer":

                st.switch_page(
                "pages/customer.py"
                )



            elif role=="Driver":

                st.switch_page(
                "pages/driver.py"
                )



            else:

                st.switch_page(
                "pages/manager.py"
                )



        else:

            st.error(
            "Select correct role"
            )



    else:

        st.error(
        "Invalid login details"
        )



st.markdown(
"</div>",
unsafe_allow_html=True
)







# -------------------------
# Features
# -------------------------


st.write("")



c1,c2,c3 = st.columns(3)



with c1:

    st.markdown(
    """
    <div class="feature">

    🚗 <b>Easy Valet Booking</b>

    <br><br>

    Request your driver before arrival

    </div>

    """,

    unsafe_allow_html=True
    )



with c2:


    st.markdown(
    """
    <div class="feature">

    📍 <b>Live Vehicle Tracking</b>

    <br><br>

    Know when your car arrives

    </div>

    """,

    unsafe_allow_html=True
    )




with c3:


    st.markdown(
    """
    <div class="feature">

    📊 <b>Smart Management</b>

    <br><br>

    Complete venue dashboard

    </div>

    """,

    unsafe_allow_html=True
    )