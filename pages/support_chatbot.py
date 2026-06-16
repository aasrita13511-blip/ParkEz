import streamlit as st
import database as db

st.set_page_config(page_title="Support Chatbot", page_icon="🤖")
st.title("💬 ParkEz Support Chatbot")
st.subheader("How can we help you today?")

# Initialize chat history using session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your ParkEz assistant. Ask me about our parking slots, digital pass deliveries, refunds, cancellations, payment channels, or booking statuses."}
    ]

# Render current message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Intelligent rule engine reading from your database fields
def process_reply(user_text):
    text = user_text.lower()
    
    # 1. Product Knowledge (Mapped to ParkEz Valet and Driver system)
    if any(k in text for k in ["product", "item", "stock", "parking", "spot", "pass", "service"]):
        return ("Our homepage offers premium digital valet booking slots! We feature secure on-demand "
                "parking zones managed by our active drivers (Rahul, Arjun, and Vikram). All spots shown "
                "on your panel are active and ready to book.")
    
    # 2. Delivery Questions
    elif any(k in text for k in ["delivery", "ship", "arrive", "mail", "sent"]):
        return ("ParkEz is completely digital! Your valet ticket receipt generated on the checkout panel "
                "is your official digital token. No physical delivery is required.")
    
    # 3. Refunds
    elif "refund" in text:
        return "Valet cancellations and refund balances are safely processed back to your card statement within 5-7 business days."
    
    # 4. Returns (Cancellations)
    elif "return" in text:
        return "Digital ticket slots cannot be 'returned', but you can instantly cancel unfulfilled vehicle requests right from your customer panel dashboard."
    
    # 5. Payment Methods
    elif any(k in text for k in ["payment", "pay", "card", "credit", "cash"]):
        return "We accept all major international Credit/Debit cards, digital wallets, and local mobile banking gateways at check-in."
    
    # 6. Order Status (Dynamic Database Extraction mapped to database.py)
    elif any(k in text for k in ["order", "status", "track", "booking", "ticket"]):
        words = text.split()
        ticket_found = None
        for word in words:
            if len(word) >= 3 and any(char.isdigit() for char in word):
                ticket_found = word.upper().strip(".,!?")
                break
                
        if ticket_found:
            booking = db.get_booking(ticket_found)
            if booking:
                # Correct indices extracted from your specific SELECT * tuple
                b_driver = booking[7]
                b_status = booking[8]
                b_time = booking[9] if booking[9] else "Not updated yet"
                return f"🔍 **Ticket {ticket_found} found!** \n\n* **Current Status:** {b_status}\n* **Assigned Driver:** {b_driver}\n* **Last Update:** {b_time}"
            else:
                return f"I tried looking for ticket **{ticket_found}** in our active ledger database, but couldn't find a record. Please verify your ticket reference text."
        
        return "To check your live booking or order status instantly, type your inquiry along with your exact **Ticket Number** (e.g., 'What is the status of ticket TKT123?')."
        
    # Default fallback response
    else:
        return "I didn't quite catch that. Could you please specify if you have questions regarding products, delivery, refunds, returns, payments, or order status?"

# Capture new input using st.chat_input
if prompt := st.chat_input("Ask a support question..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate database-aware rule-based reply
    bot_reply = process_reply(prompt)
    
    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
