import streamlit as st
import database as db

st.set_page_config(page_title="Support Chatbot", page_icon="🤖")
st.title("💬 ParkEz Support Chatbot")
st.subheader("How can we help you today?")

# Initialize chat history using session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your ParkEz assistant. Ask me about our parking slots, digital tickets, refunds, cancellations, payment options, or live booking statuses."}
    ]

# Render message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Intelligent rule engine reading from your exact fields
def process_reply(user_text):
    text = user_text.lower()
    
    # 1. Product Knowledge (Mapped to your homepage/customer valet services)
    if any(k in text for k in ["product", "item", "stock", "parking", "spot", "pass", "service"]):
        return ("Our customer page features our on-demand interactive Valet Space service. "
                "You can request available valet drivers (like Rahul, Arjun, or Vikram) to safely park and manage your car.")
    
    # 2. Delivery Questions
    elif any(k in text for k in ["delivery", "ship", "arrive", "mail", "sent"]):
        return ("Our parking passes are entirely digital! As soon as you click 'REQUEST DRIVER', "
                "your unique tracking Ticket ID is generated instantly on your dashboard.")
    
    # 3. Refunds
    elif "refund" in text:
        return "Valet booking adjustments or refunds are processed back to your payment card statement within 5-7 business days."
    
    # 4. Returns (Cancellations)
    elif "return" in text:
        return "Digital ticket slots cannot be returned, but you can request vehicle retrieval immediately via the 'LIVE STATUS TRACKER' panel tab."
    
    # 5. Payment Methods
    elif any(k in text for k in ["payment", "pay", "card", "credit", "cash"]):
        return "We accept all major secure Credit/Debit cards, digital tokens, and mobile banking systems."
    
    # 6. Order Status (Dynamic Database Extraction matching customer.py structure)
    elif any(k in text for k in ["order", "status", "track", "booking", "ticket", "val"]):
        words = text.split()
        ticket_found = None
        for word in words:
            # Look for your ticket pattern containing digits or starting with 'val'
            if "val" in word or (len(word) >= 4 and any(char.isdigit() for char in word)):
                ticket_found = word.upper().strip(".,!?")
                break
                
        if ticket_found:
            booking = db.get_booking(ticket_found)
            if booking:
                # Based on your database schema: index 7 is driver, index 8 is status
                driver_name = booking[7] if len(booking) > 7 else "Assigned Driver"
                current_status = booking[8] if len(booking) > 8 else "Driver Assigned"
                
                # Format live milestone strings matching your portal timeline
                step_info = ""
                if current_status == "Driver Assigned":
                    step_info = "🔵 **STEP 1/4:** Driver Confirmed."
                elif current_status == "Picked Up":
                    step_info = "🟠 **STEP 2/4:** Vehicle Picked Up."
                elif current_status == "Parked Vehicle":
                    step_info = "🟢 **STEP 3/4:** Secured in Lot."
                elif current_status == "Vehicle Returning":
                    step_info = "🔴 **STEP 4/4:** Vehicle Returning!"
                elif current_status == "Delivered Vehicle":
                    step_info = "✅ **COMPLETE:** Car Delivered!"
                else:
                    step_info = f"🔄 **Current State:** {current_status}"

                return f"🔍 **Ticket Look-Up:** `{ticket_found}`\n\n* **Assigned Driver:** {driver_name}\n* **Live Progress:** {step_info}"
            else:
                return f"I couldn't find ticket ID **{ticket_found}** in our active database. Please verify the code and try again."
        
        return "To check your live booking or order status instantly, type your inquiry along with your exact **Ticket ID** (e.g., 'What is the status of ticket VAL1234?')."
        
    # Default fallback response
    else:
        return "I didn't quite catch that. Could you please specify if you have questions regarding products, delivery, refunds, returns, payments, or order status?"

# Capture user input using st.chat_input
if prompt := st.chat_input("Ask a support question..."):
    # Display user query
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Process rule-based matching reply
    bot_reply = process_reply(prompt)
    
    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
