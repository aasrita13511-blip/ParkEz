import streamlit as st

def apply_corporate_theme():
    """Injects professional startup CSS styling across any page it is called on."""
    st.markdown("""
    <style>
        /* Global Background & Premium Typography */
        .stApp {
            background-color: #F8FAFC !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }
        
        /* Premium Dark Navy Sidebar Redesign */
        section[data-testid="stSidebar"] {
            background-color: #0F172A !important; 
        }
        section[data-testid="stSidebar"] * {
            color: #F1F5F9 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }
        
        /* Modern App Header Hero Banner */
        .brand-container {
            text-align: center;
            padding: 2rem 1rem;
            background: #FFFFFF;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
            margin-bottom: 2rem;
            border: 1px solid #E2E8F0;
        }
        .brand-title {
            font-size: 42px !important;
            font-weight: 800 !important;
            color: #1E3A8A !important; 
            margin: 0 !important;
            letter-spacing: -1px !important;
        }
        .brand-accent {
            color: #DC2626 !important; 
        }
        .brand-tagline {
            font-size: 16px !important;
            color: #64748B !important; 
            margin-top: 6px !important;
            font-weight: 500 !important;
        }

        /* Commercial Form Input & Selectbox Styling */
        div[data-testid="stMarkdownContainer"] p {
            font-weight: 600 !important;
            color: #334155 !important;
            margin-bottom: 4px !important;
        }
        .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTimeInput input {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
            padding: 10px !important;
            color: #0F172A !important;
        }
        
        /* Clean Tab Design */
        div[data-testid="stTabs"] button {
            font-size: 15px !important;
            font-weight: 700 !important;
            color: #64748B !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #DC2626 !important;
            border-bottom: 3px solid #DC2626 !important;
        }

        /* High-Conversion Full-Width Primary Buttons */
        div.stButton > button {
            background-color: #DC2626 !important; 
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            padding: 12px 24px !important;
            border-radius: 8px !important;
            border: none !important;
            width: 100% !important; 
            box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.15) !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button:hover {
            background-color: #B91C1C !important; 
            transform: translateY(-1px) !important;
        }
        
        /* Sleek Operational Metrics & Cards */
        div[data-testid="stMetricValue"] {
            font-size: 32px !important;
            font-weight: 800 !important;
            color: #1E3A8A !important;
        }
        .driver-card, .card {
            background: #FFFFFF !important;
            padding: 20px !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 2px 4px 0 rgba(0,0,0,0.02) !important;
            margin-bottom: 15px !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_brand_header(subtitle_text):
    """Renders the matching stylized commercial banner at the top of pages."""
    st.markdown(
        f"""
        <div class="brand-container">
            <h1 class="brand-title">🚗 Park<span class="brand-accent">E</span>z</h1>
            <p class="brand-tagline">{subtitle_text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
