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

/* Sidebar Custom Adjustments */
section[data-testid="stSidebar"] {
    background-color: #212529 !important; /* High-Contrast Charcoal Sidebar */
    border-right: none !important;
}

/* Force all text elements, links, spans, and navigation text in the sidebar to Pure White */
section[data-testid="stSidebar"] *, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebarNavItems"] span,
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] span {
    color: #FFFFFF !important; /* Crisp white elements over dark background */
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    font-weight: 600 !important;
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

# Intelligent rule engine reading from your exact fields
def process_reply(user_text):
    # Fixed string strip layout to safely avoid syntax highlights cracking
    clean_chars = ".,!?:;()\"'"
    text = user_text.lower().strip(clean_chars)
    
    # =====================================================================
    # 50 EXPANDED KNOWLEDGE BASE QUESTIONS & ANSWERS MAPPING
    # =====================================================================
    
    # Category 1: Greetings & Core Assistance (5 Qs)
    if text in ["hi", "hello", "hey", "greetings", "good morning", "good afternoon"]:
        return "Hello! Welcome to ParkEz Support. How can I assist you with your valet parking or vehicle retrieval today?"
    elif "how are you" in text:
        return "I am doing great and ready to assist you! How can I help make your parking experience seamless today?"
    elif "who are you" in text or "your name" in text:
        return "I am the ParkEz Virtual Assistant, here to guide you through bookings, vehicle tracking, and account help."
    elif any(k in text for k in ["help", "what can you do", "features"]):
        return "I can help you look up live parking ticket statuses, request drivers, explain retrieval times, or troubleshoot app settings."
    elif text in ["bye", "goodbye", "thanks", "thank you"]:
        return "You're very welcome! Thank you for choosing ParkEz. Enjoy your ride, and let us know if you need anything else later."

    # Category 2: Booking & Valet Requests (10 Qs)
    elif "how to book" in text or "request valet" in text:
        return "To request a valet driver, head to your Customer Portal, fill in your Name, Phone Number, Car Model, and Vehicle Number, then click 'REQUEST DRIVER'."
    elif "who is my driver" in text or "driver assignment" in text:
        return "Our system automatically matches you with an available professional driver nearby (such as Rahul, Arjun, or Vikram) the moment you submit a request."
    elif "how long to assign" in text or "assignment time" in text:
        return "Driver matching happens instantly! A valet driver is usually assigned to your ticket within a few seconds of clicking request."
    elif "cancel booking" in text or "cancel request" in text:
        return "Once a driver has picked up your vehicle, the operation cannot be canceled. If you need your car back immediately, go to the 'RETRIEVE VEHICLE' tab."
    elif "multiple cars" in text or "book two cars" in text:
        return "Currently, each customer account processes one active ticket at a time. To book another car, submit an additional request once the active transaction concludes."
    elif "pre book" in text or "reserve in advance" in text:
        return "Yes! You can use the 'Arrival Time' selector in the Request Valet tab to let our driver network know exactly when you plan to arrive at the venue."
    elif "valet location" in text or "where to drop" in text:
        return "Drive directly to the designated ParkEz valet drop-off zone at your venue entrance. Our assigned driver will meet you right there."
    elif "wrong car info" in text or "change vehicle details" in text:
        return "If you submitted the wrong car model or vehicle number, please inform the driver directly upon arrival or contact venue management to fix the ticket."
    elif "valet cost" in text or "is parking free" in text:
        return "Standard parking fees vary depending on your location and venue agreement. Rates will be displayed clearly on your portal screen before booking."
    elif "driver didn't show" in text or "where is my driver" in text:
        return "If your driver is taking longer than expected, verify your live status tracking window on the dashboard or request support from the manager panel."

    # Category 3: Vehicle Retrieval & Tracking (10 Qs)
    elif "how to get my car" in text or "retrieve vehicle" in text:
        return "To get your car back, go to the '🔑 RETRIEVE VEHICLE' tab, enter your unique Ticket ID, select your leaving window, and press 'BRING MY CAR'."
    elif "what is a ticket id" in text or "where is my ticket" in text:
        return "Your Ticket ID is a unique code (e.g., VAL1234) generated automatically on your screen as soon as your valet request is confirmed."
    elif "lost my ticket" in text or "forgot ticket id" in text:
        return "Don't worry! If you lose your Ticket ID, the Venue Manager can look up your registration details using your registered phone number via the Manager Dashboard."
    elif "what is live tracking" in text or "track my car" in text:
        return "Our live tracking system updates you instantly through 5 milestones: Driver Assigned, Moving to Lot, Parked, Vehicle Moving, and Ready at Pickup Point."
    elif "how long to retrieve" in text or "retrieval eta" in text:
        return "Average vehicle retrieval takes approximately 3 to 10 minutes, depending on the leaving window option you select when requesting your car."
    elif "can i change retrieval time" in text or "change leaving time" in text:
        return "Retrieval requests dispatch drivers immediately. If your plans change, let the drop-off booth attendants know right away."
    elif "where do i pick up my car" in text or "pickup point" in text:
        return "Your vehicle will be delivered directly back to the primary venue entrance pickup lane where you originally dropped it off."
    elif "is my car ready" in text:
        return "Enter your Ticket ID in the retrieval tracker tab. The progress bar will clearly display 'Arriving At Pickup Point ✅' when your car is ready."
    elif "driver name on retrieval" in text:
        return "The system assigns a secure driver to pull your vehicle from our parking lots. Their name is displayed directly on your live retrieval confirmation box."
    elif "stuck on progress bar" in text:
        return "The progress bar updates dynamically as our driver updates their actions. Please allow a few moments for the driver to reach your parking zone location."

    # Category 4: User Roles & Access (5 Qs)
    elif "login roles" in text or "account type" in text:
        return "ParkEz supports three distinct roles: 'Customer' for car owners, 'Driver' for valet operators, and 'Manager' for operational overview."
    elif "driver login credentials" in text or "how do drivers log in" in text:
        return "Valet drivers log in securely using their registered mobile phone numbers and unique access PIN codes assigned by the venue manager."
    elif "manager access" in text or "how to log in as manager" in text:
        return "Manager portals are restricted to authorized administrators. Access requires custom company master login keys for verification."
    elif "how to log out" in text:
        return "To switch user accounts or log out, simply use the Streamlit navigation panel on the left to return to the main login landing page screen."
    elif "change my password" in text or "reset pin" in text:
        return "Password resets can be requested directly from your system administrator or by visiting the venue manager's help desk station."

    # Category 5: Operations & Safety Policies (10 Qs)
    elif "operating hours" in text or "is it open now" in text:
        return "ParkEz operational hours are synchronized with the operating hours of your specific host venue or commercial parking complex."
    elif "is my car safe" in text or "insurance coverage" in text:
        return "Your car's safety is our priority. All parking zones are secured, monitored, and handled exclusively by fully verified valet drivers."
    elif "what happens if a driver isn't available" in text:
        return "If all drivers are currently busy handling requests, your ticket enters a brief priority queue and updates instantly when a driver completes their trip."
