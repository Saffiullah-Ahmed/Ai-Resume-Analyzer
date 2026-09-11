import streamlit as st


def inject_custom_css():
    """Injects custom CSS styling matching the modern AI SaaS sidebar reference."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background-color: #0F172A;
        }

        /* -------------------------------------------------- */
        /* SIDEBAR CONTAINER                                  */
        /* -------------------------------------------------- */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #030712 0%, #0B1528 50%, #060D1B 100%) !important;
            border-right: 1px solid #1E293B !important;
            min-width: 320px !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 1.6rem 1.2rem !important;
        }

        /* -------------------------------------------------- */
        /* SIDEBAR RADIO NAVIGATION TEXT (WHITE, REGULAR & SPACED) */
        /* -------------------------------------------------- */
        [data-testid="stSidebar"] [data-testid="stRadio"] label,
        [data-testid="stSidebar"] [data-testid="stRadio"] label *,
        [data-testid="stSidebar"] [data-testid="stRadio"] p,
        [data-testid="stSidebar"] [data-testid="stRadio"] span {
            color: #FFFFFF !important;
            font-size: 16px !important;
            font-weight: 500 !important;
        }

        /* Spacing between each radio button option */
        [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {
            margin-bottom: 12px !important;
            display: flex !important;
            align-items: center !important;
        }

        /* Sidebar Navigation Buttons (Inactive State) */
        [data-testid="stSidebar"] button[kind="secondary"] {
            background-color: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 10px !important;
            color: #94A3B8 !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding: 12px 16px !important;
            transition: all 0.2s ease !important;
            margin-bottom: 6px !important;
        }

        [data-testid="stSidebar"] button[kind="secondary"]:hover {
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #FFFFFF !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
        }

        /* Sidebar Navigation Buttons (Active State) */
        [data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(90deg, #2563EB 0%, #4F46E5 100%) !important;
            border: none !important;
            border-left: 4px solid #38BDF8 !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding: 12px 16px !important;
            box-shadow: 0 4px 20px rgba(37, 99, 235, 0.4) !important;
            margin-bottom: 6px !important;
        }

        /* Thin Subtle Horizontal Dividers */
        .sidebar-divider {
            height: 1px !important;
            background: #1E293B !important;
            margin: 18px 0 !important;
            border: none !important;
        }

        /* Tech Stack Grid Badges */
        .tech-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 10px;
        }

        .tech-badge {
            background: #0F172A;
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 8px 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: #E2E8F0;
            font-size: 13px;
            font-weight: 600;
        }

        .tech-badge-full {
            grid-column: span 1;
        }

        /* Main Content Hero Banner */
        .hero-container {
            background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
            border-radius: 16px;
            padding: 28px 32px;
            color: #FFFFFF;
            margin-bottom: 24px;
        }

        .hero-title {
            font-family: 'Outfit', sans-serif;
            font-size: 26px;
            font-weight: 800;
            color: #FFFFFF;
        }

        .hero-subtitle {
            font-size: 14px;
            color: #C7D2FE;
            margin-top: 4px;
        }

        .feature-card {
            background: #1E293B;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 16px;
            color: #F8FAFC;
        }

        .metric-card-container {
            background: #1E293B;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 18px;
            color: #F8FAFC;
        }

        .upload-card-title {
            font-family: 'Outfit', sans-serif;
            font-size: 16px;
            font-weight: 700;
            color: #F8FAFC;
        }

        .upload-card-desc {
            font-size: 12px;
            color: #94A3B8;
        }
        </style>
        """,
        unsafe_allow_html=True
    )