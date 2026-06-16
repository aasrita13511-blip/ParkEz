import streamlit as st

def apply_corporate_theme():
    """Injects premium Option 2 (High-Contrast Modern) CSS styling across any page it is called on."""
    st.markdown("""
    <style>
        /* Global Background & Premium Typography */
        .stApp {
            background-color: #F8F9FA !important; /* Soft Premium Off-White Canvas */
            font-family: 'Inter', -apple-system, sans-serif !important;
        }
        
        /* Dark Slate Sidebar Redesign (Option 2 Dark Mode Sidebar) */
        section[data-testid="stSidebar"] {
            background-color: #212529 !important; /* Dark Slate Charcoal */
            border-right: none !important;
        }
        section[data-testid="stSidebar"] * {
            color: #FFFFFF !important; /* Pure White text on dark sidebar */
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
            border: 1px solid #E5E7EB;
        }
        .brand-title {
            font-size: 38px !important;
            font-weight: 800 !important;
            color: #1A365D !important; /* Corporate Deep Blue */
            margin: 0 !important;
        }
        .brand-accent {
            color: #DE2910 !important; /* Brand Operational Red */
        }
        .brand-tagline {
            font-size: 15px !important;
            color: #718096 !important; 
            margin-top: 4px !important;
            font-weight: 500 !important;
        }

        /* Clean Form Input Boxes */
        div[data-testid="stMarkdownContainer"] p {
            font-weight: 600 !important;
            color: #1A202C !important;
            margin-bottom: 4px !important;
        }
        .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTimeInput input {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 8px !important;
            padding: 10px !important;
            color: #1A202C !important;
        }
        
        /* Blue and Red Tab Layout Design */
        div[data-testid="stTabs"] button {
            font-size: 14px !important;
            font-weight: 700 !important;
            color: #718096 !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #DE2910 !important; /* Active indicator brand red line */
            border-bottom: 3px solid #DE2910 !important;
        }

        /* High-Conversion Primary Corporate Blue Buttons */
        div.stButton > button {
            background-color: #1A365D !important; /* Brand Deep Blue Call-to-Action */
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            padding: 12px 24px !important;
            border-radius: 30px !important; /* Pill shape for elegant actions */
            border: none !important;
            width: 100% !important; 
            box-shadow: 0 4px 6px -1px rgba(26, 54, 93, 0.1) !important;
        }
        div.stButton > button:hover {
            background-color: #122542 !important; /* Darker blue on hover event */
        }
        
        /* Metrics & Cards Display Layouts */
        div[data-testid="stMetricValue"] {
            font-size: 30px !important;
            font-weight: 800 !important;
            color: #1A365D !important;
        }
        .driver-card, .card {
            background: #FFFFFF !important;
            padding: 20px !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            margin-bottom: 15px !important;
        }

        /* Light Grey Feature Bubble Squares (Uber Style) */
        .benefit-card {
            background-color: #EEEEEE !important; /* Solid light grey bubble background */
            border-radius: 12px !important;
            padding: 24px !important;
            min-height: 160px !important;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            margin-bottom: 15px;
        }
        .benefit-card h3 {
            color: #1A202C !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            margin: 0 0 8px 0 !important;
        }
        .benefit-card p {
            color: #718096 !important;
            font-size: 13px !important;
            line-height: 1.4 !important;
            margin: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_brand_header(subtitle_text):
    """Renders the matching stylized Option 2 commercial banner at the top of pages."""
    st.markdown(
        f"""
        <div class="brand-container">
            <h1 style="text-align: center; margin: 0; font-size: 36px; font-weight: 800; color: #1A365D;">
                🚗 Park<span style="color: #DE2910;">E</span>z
            </h1>
            <p style="text-align: center; margin: 4px 0 0 0; font-size: 15px; color: #718096; font-weight: 500;">
                {subtitle_text}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
