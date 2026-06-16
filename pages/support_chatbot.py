import streamlit as st
from openai import OpenAI
from styles import apply_corporate_theme, render_brand_header

st.set_page_config(
    page_title="ParkEz - AI Support Chat",
    page_icon="💬",
    layout="wide"
)

apply_corporate_theme()
render_brand_header("ParkEz AI Assistant Helpdesk")

# Initialize OpenAI via the secure local secrets file mapping
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("🔑 OpenAI API Access Token Missing inside secrets configurations.")
    st.stop()

# --- SYSTEM ASSISTANT ALIGNMENT PROMPT FOR PARKEZ ---
SYSTEM_PROMPT = """
You are a highly professional, polite, and helpful Customer Support Representative for ParkEz — a Smart Valet Parking application.
Your goal is to answer user queries accurately based ONLY on the app parameters and business policies outlined below:

PARKEZ SERVICE MATRIX & APP PAGES:
1. Customer Portal: Users can request a valet driver by inputting Name, Phone Number, Car Model, and Vehicle Number. They can also request vehicle retrieval by typing their Ticket ID.
2. Driver Portal: Valet drivers manage tasks, accept pickups, and update vehicle status seamlessly.
3. Manager Dashboard: Administrators view operational metrics (Total Cars, Cars Retrieved, Active Drivers), look at real-time bar charts, and download CSV reports.

BUSINESS & OPERATIONS POLICIES:
- Default Drivers: Rahul, Arjun, and Vikram are our three official demo valet drivers.
- Valet Status Updates: A booking progresses through: 'Driver Assigned' -> 'Picked Up' -> 'Parked Vehicle' -> 'Vehicle Returning' -> 'Delivered Vehicle'.

STRICT OPERATIONAL CONSTRAINT:
You are an expert specialized ONLY in ParkEz operational queries (Valet Booking, Ticket Tracking, Driver Assignments, Status Updates, App Navigation). 
If the user asks unrelated questions (e.g., writing code, cooking recipes, math, general world facts), politely decline and redirect them back to ParkEz parking support topics.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if user_query := st.chat_input("How can I help you with your valet request or tracking today?"):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.3
            )
            full_response = completion.choices.message.content
            message_placeholder.markdown(full_response)
        except Exception as api_err:
            st.error(f"Streaming connectivity failure: {api_err}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
