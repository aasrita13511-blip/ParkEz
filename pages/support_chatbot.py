import streamlit as st

from database import *

create_tables()

st.set_page_config(
    page_title="ParkEz",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
<style>

/* Global Canvas Background (Option 2 Muted Tone Setup) */
.stApp {
    background-color: #F8F9FA !important; 
    font-family: 'Inter', -apple-system, sans-serif !important;
}

.big-title{
text-align:center;
font-size:65px;
font-weight:bold;
color:#1A365D; /* Corporate Deep Blue Accent */
}

.tagline{
text-align:center;
font-size:25px;
color:#718096; /* Modern Slate Grey Muted Description Text */
margin-bottom:40px;
}

.block-container{
padding-top:2rem;
}

/* Modern Clean Styling overrides for Text Fields & Selection Boxes */
.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #1A202C !important;
    padding: 10px !important;
}

/* Option 2 Input Labels Typography */
div[data-testid="stMarkdownContainer"] p {
    font-weight: 600 !important;
    color: #1A202C !important;
}

/* Blue and Red Navigation Tab Setup Layout */
div[data-testid="stTabs"] button {
    font-size: 14px !important;
    font-weight: 700 !important;
    color: #718096 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #DE2910 !important; /* Active indicator brand operational red */
    border-bottom: 3px solid #DE2910 !important;
}

/* Primary High-Conversion Corporate Blue Button Layout */
div.stButton > button {
    background-color: #1A365D !important; /* Brand Corporate Deep Blue Canvas */
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 12px 24px !important;
    border-radius: 30px !important; /* Premium rounded pill shape adjustments */
    border: none !important;
    width: 100% !important; 
    box-shadow: 0 4px 6px -1px rgba(26, 54, 93, 0.1) !important;
}
div.stButton > button:hover {
    background-color: #122542 !important; /* Darker navy shade applied on active hover */
}

/* High-Contrast Charcoal Sidebar Layout Base */
section[data-testid="stSidebar"] {
    background-color: #212529 !important; /* Dark Slate Charcoal Option 2 Sidebar */
    border-right: none !important;
}

/* 
   PERMANENT VISIBILITY BUG FIX:
   Force all deeply nested Streamlit page list links, text nodes, spans, 
   and utility selectors within the sidebar container area to pure white.
*/
section[data-testid="stSidebar"] *, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebarNavItems"] span,
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] span,
.st-emotion-cache-16ids9d,
.st-emotion-cache-6q9w0q {
    color: #FFFFFF !important; /* Crisp white elements over dark background */
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    font-weight: 600 !important;
}

/* Light Grey Feature Info Bubbles Layout */
.benefit-section-title {
    color: #1A365D !important;
    font-weight: 700 !important;
    margin-top: 20px !important;
    margin-bottom: 15px !important;
}
.benefit-card {
    background-color: #EEEEEE !important; /* Solid light grey bubble background */
    border-radius: 12px !important;
    padding: 20px !important;
    min-height: 180px !important;
    margin-bottom: 15px;
}
.benefit-card h4 {
    color: #1A365D !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    margin: 0 0 10px 0 !important;
}
.benefit-card ul {
    margin: 0 !important;
    padding-left: 20px !important;
}
.benefit-card li {
    color: #4B5563 !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
    margin-bottom: 6px !important;
    font-weight: 500 !important;
}

/* --- FLOATING CHAT BUTTON POSITIONING --- */
div.stActionButton {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 999999;
}
.stActionButton button {
    background-color: #ff4b4b !important;
    color: white !important;
    border-radius: 50% !important;
    width: 60px !important;
    height: 60px !important;
    font-size: 28px !important;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
    border: none !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.stActionButton button:hover {
    background-color: #e04040 !important;
    transform: scale(1.05) !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
"""
<div class='big-title'>
🚗 ParkEz
</div>

<div class='tagline'>
Skip the Wait, Enjoy the Ride
</div>
""",
unsafe_allow_html=True
)

tab1, tab2 = st.tabs(
    [
        "🔐 LOGIN",
        "📝 SIGN UP"
    ]
)

# ---------------- LOGIN ----------------

with tab1:

    role = st.selectbox(
        "Login As",
        [
            "Customer",
            "Driver",
            "Manager"
        ]
    )

    phone = st.text_input(
        "Enter Phone Number"
    )

    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("LOGIN"):

        if role == "Customer":

            user = customer_login(
                phone,
                password
            )

            if user:

                st.success(
                    f"Welcome {user}"
                )

                st.switch_page(
                    "pages/customer.py"
                )

            else:

                st.error(
                    "Invalid Credentials"
                )

        elif role == "Driver":

            if (
                phone == "8888888888"
                and password == "1234"
            ):

                st.switch_page(
                    "pages/driver.py"
                )

            else:

                st.error(
                    "Invalid Credentials"
                )

        elif role == "Manager":

            if (
                phone == "7777777777"
                and password == "1234"
            ):

                st.switch_page(
                    "pages/manager.py"
                )

            else:

                st.error(
                    "Invalid Credentials"
                )

# ---------------- SIGNUP ----------------

with tab2:

    st.subheader(
        "Create Customer Account"
    )

    name = st.text_input(
        "Full Name"
    )

    phone = st.text_input(
        "Phone Number "
    )

    password = st.text_input(
        "Password ",
        type="password"
    )

    if st.button("SIGN UP"):

        success = register_customer(
            name,
            phone,
            password
        )

        if success:

            st.success(
                "Account Created Successfully"
            )

        else:

            st.error(
                "Phone Number Already Exists"
            )


# =====================================================================
# CUSTOMER & BUSINESS BENEFITS GRID (BELOW THE LOGIN FORM)
# =====================================================================
st.write("")
st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
        <div class="benefit-card">
            <h4>For Customers</h4>
            <ul>
                <li>Easy access to valet parking at crowded locations</li>
                <li>Request vehicle before leaving to reduce waiting time</li>
                <li>Real-time vehicle status updates</li>
                <li>Faster and convenient parking experience</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
        <div class="benefit-card">
            <h4>For Businesses</h4>
            <ul>
                <li>Provide valet service without hiring extra staff</li>
                <li>Improve customer experience</li>
                <li>Better parking operation management</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


# ================= FLOATING SUPPORT BUTTON LAYER =================
with st.container():
    st.markdown('<div class="stActionButton">', unsafe_allow_html=True)
    if st.button("💬", key="global_homepage_chat_action"):
        st.switch_page("pages/support_chatbot.py")
    st.markdown('</div>', unsafe_allow_html=True)
