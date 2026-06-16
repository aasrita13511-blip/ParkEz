import streamlit as st

def apply_corporate_theme():
    """Injects professional startup CSS styling across any page it is called on."""
    st.markdown("""
    <style>
        /* Global Background & Premium Typography */
        .stApp {
            background-color: #FFFFFF !important; /* Pure White Main Canvas */
            font-family: 'Inter', -apple-system, sans-serif !important;
        }
        
        /* Light Theme Clean Sidebar Redesign (Fixes Dark Text Visibility Issues) */
        section[data-testid="stSidebar"] {
            background-color: #FAFAFA !important; 
            border-right: 1px solid #E5E7EB !important;
        }
        section[data-testid="stSidebar"] * {
            color: #1F2937 !important; /* Rich Dark Slate text on your sidebar tabs */
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            font-size: 13px !important;
            font-weight: 700 !important;
        }
        
        /* Modern App Header Hero Banner */
        .brand-container {
            text-align: center;
            padding: 1.5rem 1rem;
            background: #FFFFFF;
            border-radius: 12px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
            border: 1px solid #FEE2E2;
        }
        .brand-title {
            font-size: 38px !important;
            font-weight: 800 !important;
            color: #1F2937 !important; 
            margin: 0 !important;
        }
        .brand-accent {
            color: #DC2626 !important; /* Brand Red Accent */
        }
        .brand-tagline {
            font-size: 15px !important;
            color: #4B5563 !important; 
            margin-top: 4px !important;
            font-weight: 500 !important;
        }

        /* Clean Form Input Boxes */
        div[data-testid="stMarkdownContainer"] p {
            font-weight: 600 !important;
            color: #1F2937 !important;
            margin-bottom: 4px !important;
        }
        .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTimeInput input {
            background-color: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 8px !important;
            padding: 10px !important;
            color: #1F2937 !important;
        }
        
        /* Red and White Tab Layout Design */
        div[data-testid="stTabs"] button {
            font-size: 14px !important;
            font-weight: 700 !important;
            color: #4B5563 !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #DC2626 !important; /* Active indicator brand red */
            border-bottom: 3px solid #DC2626 !important;
        }

        /* High-Conversion Full-Width Primary Red Buttons */
        div.stButton > button {
            background-color: #DC2626 !important; /* Bright Operational Red */
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            padding: 12px 24px !important;
            border-radius: 8px !important;
            border: none !important;
            width: 100% !important; 
            box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.1) !important;
        }
        div.stButton > button:hover {
            background-color: #B91C1C !important; /* Darker red on hover event */
        }
        
        /* Metrics & Cards Display Layouts */
        div[data-testid="stMetricValue"] {
            font-size: 30px !important;
            font-weight: 800 !important;
            color: #DC2626 !important;
        }
        .driver-card, .card {
            background: #FFFFFF !important;
            padding: 20px !important;
            border-radius: 12px !important;
            border: 1px solid #FEE2E2 !important;
            margin-bottom: 15px !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_brand_header(subtitle_text):
    """Renders the matching stylized commercial banner at the top of pages."""
    st.markdown(
        f"""
        <div class="brand-container">
            <h1 style="text-align: center; margin: 0; font-size: 36px; font-weight: 800; color: #1F2937;">
                🚗 Park<span style="color: #DC2626;">E</span>z
            </h1>
            <p style="text-align: center; margin: 4px 0 0 0; font-size: 15px; color: #4B5563; font-weight: 500;">
                {subtitle_text}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
