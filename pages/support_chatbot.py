import streamlit as st
import database as db

st.set_page_config(
    page_title="Support Chatbot", 
    page_icon="🤖",
    layout="wide"
)

# ---------------- Option 2 Theme Styling ----------------
st.markdown("""
<style>
/* Global Canvas Background Adjustments */
.stApp {
    background-color: #F8F9FA !important; 
    font-family: 'Inter', -apple-system, sans-serif !important;
}

/* Header Text Theme Styling */
h1 {
    color: #1A365D !important; /* Corporate Deep Blue */
    font-weight: 800 !important;
}
h3 {
    color: #718096 !important; /* Muted Slate Grey */
    font-weight: 500 !important;
}

/* High-Contrast Charcoal Sidebar Layout Base */
section[data-testid="stSidebar"] {
    background-color: #212529 !important; /* Dark Slate Charcoal Option 2 Sidebar */
    border-right: none !important;
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
    text-transform: uppercase !important; /* Forces all sidebar letters to be CAPITALS */
    letter-spacing: 1.2px !important;
    font-weight: 700 !important;
}

/* Modern Input Boxes overrides */
div[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #1A202C !important;
}
</style>
""", unsafe_allow_html=True)

st.title("💬 ParkEz Support Chatbot")
st.subheader("How can we help you today?")

# Initialize chat history using session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your ParkEz assistant. Ask me anything about how the app works, valet requests, vehicle retrieval, hours, pricing, or track your live ticket status!"}
    ]

# Render message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Dictionary containing all 50 pre-programmed responses
RESPONSES = {
    # Greetings & Core Assistance
    "hi": "Hello! Welcome to ParkEz Support. How can I assist you with your valet parking or vehicle retrieval today?",
    "hello": "Hello! Welcome to ParkEz Support. How can I assist you with your valet parking or vehicle retrieval today?",
    "hey": "Hello! Welcome to ParkEz Support. How can I assist you with your valet parking or vehicle retrieval today?",
    "greetings": "Hello! Welcome to ParkEz Support. How can I assist you with your valet parking or vehicle retrieval today?",
    "good morning": "Hello! Welcome to ParkEz Support. How can I assist you with your valet parking or vehicle retrieval today?",
    "good afternoon": "Hello! Welcome to ParkEz Support. How can I assist you with your valet parking or vehicle retrieval today?",
    "how are you": "I am doing great and ready to assist you! How can I help make your parking experience seamless today?",
    "who are you": "I am the ParkEz Virtual Assistant, here to guide you through bookings, vehicle tracking, and account help.",
    "your name": "I am the ParkEz Virtual Assistant, here to guide you through bookings, vehicle tracking, and account help.",
    "help": "I can help you look up live parking ticket statuses, request drivers, explain retrieval times, or troubleshoot app settings.",
    "what can you do": "I can help you look up live parking ticket statuses, request drivers, explain retrieval times, or troubleshoot app settings.",
    "features": "I can help you look up live parking ticket statuses, request drivers, explain retrieval times, or troubleshoot app settings.",
    "bye": "You're very welcome! Thank you for choosing ParkEz. Enjoy your ride, and let us know if you need anything else later.",
    "goodbye": "You're very welcome! Thank you for choosing ParkEz. Enjoy your ride, and let us know if you need anything else later.",
    "thanks": "You're very welcome! Thank you for choosing ParkEz. Enjoy your ride, and let us know if you need anything else later.",
    "thank you": "You're very welcome! Thank you for choosing ParkEz. Enjoy your ride, and let us know if you need anything else later.",

    # Booking & Valet Requests
    "how to book": "To request a valet driver, head to your Customer Portal, fill in your Name, Phone Number, Car Model, and Vehicle Number, then click 'REQUEST DRIVER'.",
    "request valet": "To request a valet driver, head to your Customer Portal, fill in your Name, Phone Number, Car Model, and Vehicle Number, then click 'REQUEST DRIVER'.",
    "who is my driver": "Our system automatically matches you with an available professional driver nearby (such as Rahul, Arjun, or Vikram) the moment you submit a request.",
    "driver assignment": "Our system automatically matches you with an available professional driver nearby (such as Rahul, Arjun, or Vikram) the moment you submit a request.",
    "how long to assign": "Driver matching happens instantly! A valet driver is usually assigned to your ticket within a few seconds of clicking request.",
    "assignment time": "Driver matching happens instantly! A valet driver is usually assigned to your ticket within a few seconds of clicking request.",
    "cancel booking": "Once a driver has picked up your vehicle, the operation cannot be canceled. If you need your car back immediately, go to the 'RETRIEVE VEHICLE' tab.",
    "cancel request": "Once a driver has picked up your vehicle, the operation cannot be canceled. If you need your car back immediately, go to the 'RETRIEVE VEHICLE' tab.",
    "multiple cars": "Currently, each customer account processes one active ticket at a time. To book another car, submit an additional request once the active transaction concludes.",
    "book two cars": "Currently, each customer account processes one active ticket at a time. To book another car, submit an additional request once the active transaction concludes.",
    "pre book": "Yes! You can use the 'Arrival Time' selector in the Request Valet tab to let our driver network know exactly when you plan to arrive at the venue.",
    "reserve in advance": "Yes! You can use the 'Arrival Time' selector in the Request Valet tab to let our driver network know exactly when you plan to arrive at the venue.",
    "valet location": "Drive directly to the designated ParkEz valet drop-off zone at your venue entrance. Our assigned driver will meet you right there.",
    "where to drop": "Drive directly to the designated ParkEz valet drop-off zone at your venue entrance. Our assigned driver will meet you right there.",
    "wrong car info": "If you submitted the wrong car model or vehicle number, please inform the driver directly upon arrival or contact venue management to fix the ticket.",
    "change vehicle details": "If you submitted the wrong car model or vehicle number, please inform the driver directly upon arrival or contact venue management to fix the ticket.",
    "valet cost": "Standard parking fees vary depending on your location and venue agreement. Rates will be displayed clearly on your portal screen before booking.",
    "is parking free": "Standard parking fees vary depending on your location and venue agreement. Rates will be displayed clearly on your portal screen before booking.",
    "driver didn't show": "If your driver is taking longer than expected, verify your live status tracking window on the dashboard or request support from the manager panel.",
    "where is my driver": "If your driver is taking longer than expected, verify your live status tracking window on the dashboard or request support from the manager panel.",

    # Vehicle Retrieval & Tracking
    "how to get my car": "To get your car back, go to the '🔑 RETRIEVE VEHICLE' tab, enter your unique Ticket ID, select your leaving window, and press 'BRING MY CAR'.",
    "retrieve vehicle": "To get your car back, go to the '🔑 RETRIEVE VEHICLE' tab, enter your unique Ticket ID, select your leaving window, and press 'BRING MY CAR'.",
    "what is a ticket id": "Your Ticket ID is a unique code (e.g., VAL1234) generated automatically on your screen as soon as your valet request is confirmed.",
    "where is my ticket": "Your Ticket ID is a unique code (e.g., VAL1234) generated automatically on your screen as soon as your valet request is confirmed.",
    "lost my ticket": "Don't worry! If you lose your Ticket ID, the Venue Manager can look up your registration details using your registered phone number via the Manager Dashboard.",
    "forgot ticket id": "Don't worry! If you lose your Ticket ID, the Venue Manager can look up your registration details using your registered phone number via the Manager Dashboard.",
    "what is live tracking": "Our live tracking system updates you instantly through 5 milestones: Driver Assigned, Moving to Lot, Parked, Vehicle Moving, and Ready at Pickup Point.",
    "track my car": "Our live tracking system updates you instantly through 5 milestones: Driver Assigned, Moving to Lot, Parked, Vehicle Moving, and Ready at Pickup Point.",
    "how long to retrieve": "Average vehicle retrieval takes approximately 3 to 10 minutes, depending on the leaving window option you select when requesting your car.",
    "retrieval eta": "Average vehicle retrieval takes approximately 3 to 10 minutes, depending on the leaving window option you select when requesting your car.",
    "can i change retrieval time": "Retrieval requests dispatch drivers immediately. If your plans change, let the drop-off booth attendants know right away.",
}
# ================= CHATBOT RESPONSE ENGINE =================

def get_response(user_input):

    user_input = user_input.lower().strip()

    for question, answer in RESPONSES.items():

        if question in user_input:
            return answer

    return (
        "Sorry, I could not understand that. "
        "Please ask about booking, valet service, vehicle retrieval, "
        "ticket ID, driver status, or ParkEz features."
    )


# CHAT INPUT

if prompt := st.chat_input("Ask me anything about ParkEz..."):


    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    response = get_response(prompt)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


    st.rerun()