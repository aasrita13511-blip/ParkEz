# Intelligent rule engine reading from your exact fields
def process_reply(user_text):

    text = user_text.lower().strip(".,!?:;()\"'")


    # =====================================================================
    # 50 EXPANDED KNOWLEDGE BASE QUESTIONS & ANSWERS MAPPING
    # =====================================================================


    # Category 1: Greetings & Core Assistance

    if text in ["hi", "hello", "hey", "greetings", "good morning", "good afternoon"]:
        return "Hello! Welcome to ParkEz Support. How can I assist you with your valet parking or vehicle retrieval today?"

    elif "how are you" in text:
        return "I am doing great and ready to assist you! How can I help make your parking experience seamless today?"

    elif "who are you" in text or "your name" in text:
        return "I am the ParkEz Virtual Assistant, here to guide you through bookings, vehicle tracking, and account help."

    elif any(k in text for k in ["help", "what can you do", "features"]):
        return "I can help you with valet booking, driver assignment, vehicle tracking, retrieval, pricing, and account support."

    elif text in ["bye", "goodbye", "thanks", "thank you"]:
        return "You're very welcome! Thank you for choosing ParkEz. Enjoy your ride!"


    # Category 2: Booking & Valet Requests


    elif "how to book" in text or "request valet" in text:
        return "To request a valet driver, go to Customer Portal, enter Name, Phone Number, Car Model, and Vehicle Number, then click REQUEST DRIVER."

    elif "who is my driver" in text or "driver assignment" in text:
        return "Our system automatically assigns an available professional valet driver after your request is submitted."

    elif "how long to assign" in text or "assignment time" in text:
        return "Driver assignment happens within a few seconds depending on driver availability."

    elif "cancel booking" in text or "cancel request" in text:
        return "You can cancel your request before vehicle processing starts. Contact support if you need help."

    elif "multiple cars" in text or "book two cars" in text:
        return "Each customer can have one active booking at a time. Create another request after completing the current one."

    elif "pre book" in text or "reserve in advance" in text:
        return "Yes, you can select your expected arrival time while requesting valet service."

    elif "where to drop" in text or "valet location" in text:
        return "Please arrive at the ParkEz valet drop-off zone. Your assigned driver will assist you."

    elif "wrong car info" in text or "change vehicle details" in text:
        return "Please contact the manager to update your vehicle information."

    elif "valet cost" in text or "parking free" in text:
        return "Parking charges depend on the venue. Prices will be shown before booking."

    elif "driver didn't show" in text or "where is my driver" in text:
        return "Check your booking status. If your driver is delayed, contact support."


    # Category 3: Retrieval & Tracking


    elif "retrieve vehicle" in text or "get my car" in text:
        return "Open Retrieve Vehicle, enter your Ticket ID, select leaving time, and request your vehicle."

    elif "ticket id" in text or "where is my ticket" in text:
        return "Your Ticket ID is generated after booking confirmation. Example: VAL1234."

    elif "lost ticket" in text or "forgot ticket id" in text:
        return "Contact the venue manager. They can find your booking using your registered phone number."

    elif "track my car" in text or "live tracking" in text:
        return "Vehicle tracking shows Driver Assigned, Moving, Parked, Retrieval Started, and Ready for Pickup."

    elif "how long to retrieve" in text or "retrieval eta" in text:
        return "Vehicle retrieval usually takes around 3-10 minutes depending on parking location."

    elif "change leaving time" in text:
        return "Contact the valet team if you need to update your retrieval time."

    elif "pickup point" in text:
        return "Your vehicle will be delivered to the ParkEz pickup point."

    elif "is my car ready" in text:
        return "Enter your Ticket ID to check your vehicle status."

    elif "progress bar" in text:
        return "The progress bar updates as your vehicle moves through each retrieval stage."


    # Category 4: Account & Login


    elif "login roles" in text or "account type" in text:
        return "ParkEz supports Customer, Driver, and Manager accounts."

    elif "driver login" in text:
        return "Drivers login using their registered phone number and assigned password."

    elif "manager login" in text:
        return "Manager access is only available for authorized administrators."

    elif "logout" in text:
        return "Use the navigation panel to return to the login page."

    elif "change password" in text or "reset pin" in text:
        return "Password reset can be requested through your administrator."


    # Category 5: Safety & Operations


    elif "operating hours" in text or "open now" in text:
        return "ParkEz availability depends on venue operating hours."

    elif "is my car safe" in text or "insurance" in text:
        return "Your vehicle is handled by verified valet drivers and monitored parking operations."

    elif "no driver available" in text:
        return "Your request will stay in queue until a driver becomes available."

    elif "overnight parking" in text:
        return "Overnight parking depends on venue rules."

    elif "valet benefits" in text or "why use parkez" in text:
        return "ParkEz saves time, reduces waiting, provides secure valet service, and makes vehicle retrieval easier."

    elif "feedback" in text:
        return "We appreciate your feedback. It helps us improve ParkEz."

    elif "complaint" in text or "issue" in text:
        return "Please contact support or the venue manager for assistance."


    # Extra Support Questions


    elif "payment" in text or "pay" in text:
        return "Payment options depend on the venue and available services."

    elif "refund" in text:
        return "Refund requests can be handled through venue management."

    elif "location" in text:
        return "ParkEz is available at partnered venues."

    elif "app not working" in text:
        return "Please refresh the app and check your internet connection."

    elif "thank" in text:
        return "You're welcome! Enjoy using ParkEz 🚗"


    else:
        return "I couldn't understand that. Please ask about booking, drivers, vehicle tracking, retrieval, pricing, or support."