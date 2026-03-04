import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import hashlib
from datetime import datetime, timedelta
import random


# Always show a way to open sidebar
with st.sidebar:
    pass  # keeps sidebar always initialized

# Add a visible menu button when sidebar is collapsed  
st.markdown("""
<style>
section[data-testid="stSidebar"][aria-expanded="false"] {
    margin-left: -21rem;
}
[data-testid="collapsedControl"] {
    display: block !important;
    visibility: visible !important;
    position: fixed !important;
    top: 50% !important;
    left: 0px !important;
    z-index: 999999 !important;
    background: #13141f !important;
    border: 1px solid rgba(110,231,247,0.4) !important;
    border-left: none !important;
    border-radius: 0 12px 12px 0 !important;
    padding: 12px 6px !important;
    color: #6ee7f7 !important;
    box-shadow: 4px 0 20px rgba(110,231,247,0.15) !important;
}
</style>
""", unsafe_allow_html=True)
# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'transactions' not in st.session_state:
    st.session_state.transactions = [
        {"date": "2024-07-15", "description": "Salary Credit", "category": "Income", "amount": 85000, "type": "Income"},
        {"date": "2024-07-14", "description": "Amazon Shopping", "category": "Shopping", "amount": -3200, "type": "Expense"},
        {"date": "2024-07-13", "description": "Zomato Order", "category": "Food & Dining", "amount": -450, "type": "Expense"},
        {"date": "2024-07-12", "description": "Uber Ride", "category": "Transport", "amount": -280, "type": "Expense"},
        {"date": "2024-07-11", "description": "Netflix Subscription", "category": "Entertainment", "amount": -649, "type": "Expense"},
        {"date": "2024-07-10", "description": "Freelance Payment", "category": "Income", "amount": 15000, "type": "Income"},
        {"date": "2024-07-09", "description": "Electricity Bill", "category": "Utilities", "amount": -1200, "type": "Expense"},
        {"date": "2024-07-08", "description": "Rent Payment", "category": "Rent", "amount": -18000, "type": "Expense"},
        {"date": "2024-07-07", "description": "Swiggy Delivery", "category": "Food & Dining", "amount": -320, "type": "Expense"},
        {"date": "2024-07-06", "description": "Gym Membership", "category": "Health", "amount": -1500, "type": "Expense"},
        {"date": "2024-07-05", "description": "ATM Withdrawal", "category": "Others", "amount": -5000, "type": "Expense"},
        {"date": "2024-07-04", "description": "Dividend Income", "category": "Income", "amount": 2200, "type": "Income"},
        {"date": "2024-07-03", "description": "Petrol Fill-up", "category": "Transport", "amount": -2500, "type": "Expense"},
        {"date": "2024-07-02", "description": "Medical Checkup", "category": "Health", "amount": -800, "type": "Expense"},
        {"date": "2024-07-01", "description": "Mobile Recharge", "category": "Utilities", "amount": -599, "type": "Expense"},
    ]

# ============= STYLING =============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-primary:    #07080f;
        --bg-secondary:  #0e0f1a;
        --bg-card:       #13141f;
        --bg-card-hover: #191a28;
        --bg-surface:    #1e1f30;
        --accent-1: #6ee7f7;
        --accent-2: #818cf8;
        --accent-3: #f472b6;
        --accent-gold: #fbbf24;
        --accent-green: #34d399;
        --accent-red: #fb7185;
        --grad-main:  linear-gradient(135deg, #6ee7f7 0%, #818cf8 50%, #f472b6 100%);
        --grad-card:  linear-gradient(160deg, #13141f 0%, #0e0f1a 100%);
        --grad-glow:  rgba(110, 231, 247, 0.15);
        --text-bright:   #f0f4ff;
        --text-primary:  #c8d0e8;
        --text-secondary:#8892b0;
        --text-muted:    #4a5270;
        --border:       rgba(110, 231, 247, 0.08);
        --border-hover: rgba(110, 231, 247, 0.28);
        --border-card:  rgba(255,255,255,0.06);
        --success:    #34d399;
        --success-bg: rgba(52, 211, 153, 0.12);
        --danger:     #fb7185;
        --danger-bg:  rgba(251, 113, 133, 0.12);
        --warning:    #fbbf24;
        --info:       #60a5fa;
        --radius-lg:  18px;
        --radius-md:  12px;
        --radius-sm:  8px;
    }

    * { font-family: 'Sora', sans-serif; box-sizing: border-box; }
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse 80% 50% at 20% 10%, rgba(110,231,247,0.04) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 80%, rgba(244,114,182,0.04) 0%, transparent 60%),
            radial-gradient(ellipse 50% 50% at 50% 50%, rgba(129,140,248,0.03) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }
    #MainMenu, header, footer,
    [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stHeader"] { background: transparent !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-secondary); }
    ::-webkit-scrollbar-thumb { background: rgba(110,231,247,0.3); border-radius: 3px; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0c18 0%, var(--bg-primary) 100%) !important;
        border-right: 1px solid var(--border-card) !important;
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 2rem !important; }
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-secondary) !important;
        padding: 13px 18px !important;
        width: 100% !important;
        text-align: left !important;
        font-weight: 500 !important;
        font-size: 13.5px !important;
        transition: all 0.25s ease !important;
        margin-bottom: 3px !important;
        letter-spacing: 0.01em !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(110,231,247,0.07) !important;
        border-color: var(--border-hover) !important;
        color: var(--accent-1) !important;
        transform: translateX(5px) !important;
        box-shadow: inset 0 0 20px rgba(110,231,247,0.04) !important;
    }
    .main .block-container { padding: 2rem 3rem !important; max-width: 1600px !important; }
    .metric-card {
        background: var(--grad-card);
        border: 1px solid var(--border-card);
        border-radius: var(--radius-lg);
        padding: 26px;
        position: relative;
        overflow: hidden;
        transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    }
    .metric-card::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: var(--radius-lg);
        background: radial-gradient(circle at 80% 20%, rgba(110,231,247,0.05) 0%, transparent 60%);
        pointer-events: none;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: var(--border-hover);
        box-shadow: 0 20px 50px rgba(110,231,247,0.08), 0 0 0 1px rgba(110,231,247,0.1);
    }
    .chart-card {
        background: var(--grad-card);
        border: 1px solid var(--border-card);
        border-radius: var(--radius-lg);
        padding: 28px;
        margin-bottom: 24px;
        transition: border-color 0.3s ease;
    }
    .chart-card:hover { border-color: var(--border-hover); }
    .metric-label {
        color: var(--text-muted);
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 14px;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 34px;
        font-weight: 600;
        letter-spacing: -1px;
        margin-bottom: 10px;
        background: var(--grad-main);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-change {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 5px 11px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .metric-change.positive { background: var(--success-bg); color: var(--success); }
    .metric-change.negative { background: var(--danger-bg);  color: var(--danger);  }
    .metric-subtext { color: var(--text-secondary); font-size: 12.5px; margin-top: 10px; line-height: 1.65; }
    .metric-footer { display: flex; gap: 18px; margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--border-card); }
    .metric-footer-item { color: var(--text-muted); font-size: 11.5px; display: flex; align-items: center; gap: 6px; }
    .chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 22px; flex-wrap: wrap; gap: 14px; }
    .chart-title { font-size: 16px; font-weight: 700; color: var(--text-bright); letter-spacing: -0.2px; }
    .currency-badge {
        background: var(--bg-surface);
        border: 1px solid var(--border-card);
        border-radius: 20px; padding: 6px 14px;
        font-size: 11px; font-weight: 600;
        color: var(--text-secondary);
        display: inline-flex; align-items: center; gap: 6px;
        letter-spacing: 0.04em;
    }
    .page-header { margin-bottom: 36px; }
    .page-title {
        font-size: 38px; font-weight: 800;
        letter-spacing: -1.5px; margin-bottom: 6px;
        background: var(--grad-main);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 200% auto;
        animation: shimmer 4s linear infinite;
    }
    @keyframes shimmer {
        0%   { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    .page-subtitle { color: var(--text-secondary); font-size: 14px; font-weight: 400; letter-spacing: 0.01em; }
    .legend-item { display: flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; }
    .legend-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .legend-text { color: var(--text-secondary); font-size: 12.5px; font-weight: 500; }
    .logo-container { display: flex; align-items: center; gap: 12px; margin-bottom: 36px; padding: 0 10px; }
    .logo-icon {
        width: 40px; height: 40px;
        background: var(--grad-main);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 18px; font-weight: 800; color: #07080f;
        box-shadow: 0 4px 20px rgba(110,231,247,0.3);
    }
    .logo-text { font-size: 20px; font-weight: 800; color: var(--text-bright); letter-spacing: -0.5px; }
    .nav-section-title {
        color: var(--text-muted); font-size: 10px; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1.5px; padding: 14px 18px 6px;
    }
    .action-buttons { display: flex; gap: 12px; justify-content: flex-end; margin-bottom: 28px; }
    .btn-primary {
        background: var(--grad-main); border: none; border-radius: var(--radius-md);
        padding: 11px 24px; color: #07080f; font-size: 13px; font-weight: 700;
        cursor: pointer; letter-spacing: 0.02em;
        box-shadow: 0 4px 20px rgba(110,231,247,0.2);
    }
    .btn-secondary {
        background: var(--bg-surface); border: 1px solid var(--border-card);
        border-radius: var(--radius-md); padding: 11px 24px;
        color: var(--text-primary); font-size: 13px; font-weight: 600; cursor: pointer;
    }
    .profile-header {
        background: var(--grad-card); border: 1px solid var(--border-card);
        border-radius: 22px; padding: 44px; text-align: center;
        position: relative; overflow: hidden; margin-bottom: 28px;
    }
    .profile-header::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: var(--grad-main);
    }
    .profile-avatar {
        width: 110px; height: 110px; background: var(--grad-main);
        border-radius: 50%; margin: 0 auto 20px;
        display: flex; align-items: center; justify-content: center;
        font-size: 40px; font-weight: 800; color: #07080f;
        box-shadow: 0 0 40px rgba(110,231,247,0.3);
    }
    .profile-name { font-size: 26px; font-weight: 800; color: var(--text-bright); margin-bottom: 6px; letter-spacing: -0.5px; }
    .profile-email { color: var(--accent-1); font-size: 13px; margin-bottom: 18px; opacity: 0.85; }
    .profile-badges { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 28px; }
    .badge { padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .badge-premium { background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color: #1a1a1a; }
    .badge-verified { background: linear-gradient(135deg, #34d399 0%, #10b981 100%); color: #1a1a1a; }
    .profile-stats { display: flex; justify-content: center; gap: 44px; padding-top: 28px; border-top: 1px solid var(--border-card); }
    .profile-stat { text-align: center; }
    .profile-stat-value { font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 600; color: var(--accent-1); }
    .profile-stat-label { color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }
    .profile-section { background: var(--grad-card); border: 1px solid var(--border-card); border-radius: var(--radius-lg); padding: 26px; margin-bottom: 20px; transition: border-color 0.3s ease; }
    .profile-section:hover { border-color: var(--border-hover); }
    .section-title { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 20px; }
    .profile-field { display: flex; justify-content: space-between; align-items: center; padding: 14px 0; border-bottom: 1px solid var(--border-card); }
    .profile-field:last-child { border-bottom: none; }
    .profile-field-label { color: var(--text-secondary); font-size: 13px; }
    .profile-field-value { color: var(--text-bright); font-size: 13px; font-weight: 600; }
    .edit-btn { background: rgba(110,231,247,0.08); border: 1px solid rgba(110,231,247,0.2); border-radius: var(--radius-sm); padding: 7px 14px; color: var(--accent-1); font-size: 11.5px; font-weight: 600; cursor: pointer; }
    .preference-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; background: var(--bg-secondary); border: 1px solid var(--border-card); border-radius: var(--radius-md); margin-bottom: 10px; }
    .preference-label { color: var(--text-bright); font-size: 13.5px; font-weight: 600; }
    .preference-sublabel { color: var(--text-muted); font-size: 11.5px; margin-top: 3px; }
    .toggle-switch { width: 44px; height: 24px; background: var(--grad-main); border-radius: 12px; position: relative; cursor: pointer; flex-shrink: 0; }
    .toggle-switch::after { content: ''; position: absolute; width: 20px; height: 20px; background: white; border-radius: 50%; top: 2px; right: 2px; }
    .auth-container { max-width: 420px; margin: 60px auto; padding: 44px; background: var(--grad-card); border: 1px solid var(--border-card); border-radius: 22px; box-shadow: 0 30px 60px rgba(0,0,0,0.6); position: relative; overflow: hidden; }
    .auth-container::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-main); }
    .auth-title { font-size: 30px; font-weight: 800; text-align: center; margin-bottom: 8px; background: var(--grad-main); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: -0.5px; }
    .auth-subtitle { color: var(--text-secondary); text-align: center; font-size: 13px; margin-bottom: 28px; line-height: 1.6; }
    .auth-mode-indicator { display: flex; gap: 8px; justify-content: center; margin-bottom: 28px; }
    .mode-badge { padding: 9px 20px; border-radius: 25px; font-size: 12.5px; font-weight: 600; border: 1px solid var(--border-card); cursor: pointer; }
    .mode-badge.active { background: var(--grad-main); border-color: transparent; color: #07080f; box-shadow: 0 4px 20px rgba(110,231,247,0.25); }
    .mode-badge.inactive { background: transparent; color: var(--text-muted); }
    .stTextInput > div > div > input {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-card) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-bright) !important;
        padding: 13px 16px !important; font-size: 14px !important;
        font-family: 'Sora', sans-serif !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-1) !important;
        box-shadow: 0 0 0 3px rgba(110,231,247,0.12) !important;
    }
    .stTextInput > div > div > input::placeholder { color: var(--text-muted) !important; }
    label[data-testid="stWidgetLabel"] { color: var(--text-secondary) !important; font-size: 13px !important; }
    .stSelectbox > div > div { background: var(--bg-secondary) !important; border: 1px solid var(--border-card) !important; border-radius: var(--radius-md) !important; color: var(--text-bright) !important; }
    .stNumberInput > div > div > input { background: var(--bg-secondary) !important; border: 1px solid var(--border-card) !important; border-radius: var(--radius-md) !important; color: var(--text-bright) !important; }
    .stButton > button[kind="primary"] {
        background: var(--grad-main) !important; border: none !important;
        border-radius: var(--radius-md) !important; color: #07080f !important;
        font-weight: 700 !important; font-family: 'Sora', sans-serif !important;
        box-shadow: 0 4px 20px rgba(110,231,247,0.2) !important;
        letter-spacing: 0.02em !important;
    }
    .stButton > button[kind="secondary"] {
        background: var(--bg-surface) !important; border: 1px solid var(--border-card) !important;
        border-radius: var(--radius-md) !important; color: var(--text-primary) !important;
        font-weight: 600 !important; font-family: 'Sora', sans-serif !important;
    }
    .wallet-card {
        background: linear-gradient(135deg, #1a1040 0%, #2d1b69 50%, #1e3a5f 100%);
        border: 1px solid rgba(110,231,247,0.15);
        border-radius: 20px; padding: 28px; color: white; position: relative; overflow: hidden; margin-bottom: 16px;
    }
    .wallet-card::before { content: ''; position: absolute; top: -30px; right: -30px; width: 120px; height: 120px; border-radius: 50%; background: rgba(110,231,247,0.08); }
    .wallet-card-2 {
        background: linear-gradient(135deg, #0d2137 0%, #1a3a5c 50%, #0f2744 100%);
        border: 1px solid rgba(96,165,250,0.15);
        border-radius: 20px; padding: 28px; color: white; position: relative; overflow: hidden; margin-bottom: 16px;
    }
    .wallet-card-2::before { content: ''; position: absolute; top: -30px; right: -30px; width: 120px; height: 120px; border-radius: 50%; background: rgba(96,165,250,0.08); }
    .wallet-card-3 {
        background: linear-gradient(135deg, #2d1515 0%, #5c2030 50%, #3d1a28 100%);
        border: 1px solid rgba(251,113,133,0.15);
        border-radius: 20px; padding: 28px; color: white; position: relative; overflow: hidden; margin-bottom: 16px;
    }
    .wallet-card-3::before { content: ''; position: absolute; top: -30px; right: -30px; width: 120px; height: 120px; border-radius: 50%; background: rgba(251,113,133,0.08); }
    .wallet-card h3, .wallet-card-2 h3, .wallet-card-3 h3 {
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px; font-weight: 600; margin: 0 0 6px 0; letter-spacing: -0.5px;
    }
    .goal-card { background: var(--grad-card); border: 1px solid var(--border-card); border-radius: var(--radius-lg); padding: 22px; margin-bottom: 14px; transition: border-color 0.3s ease; }
    .goal-card:hover { border-color: var(--border-hover); }
    .goal-title { font-size: 15px; font-weight: 700; color: var(--text-bright); margin-bottom: 3px; }
    .goal-amount { font-size: 12px; color: var(--text-muted); margin-bottom: 14px; }
    .progress-bar-bg { background: rgba(255,255,255,0.06); border-radius: 6px; height: 8px; margin-bottom: 6px; overflow: hidden; }
    .txn-row { display: flex; justify-content: space-between; align-items: center; padding: 13px 0; border-bottom: 1px solid var(--border-card); }
    .txn-row:last-child { border-bottom: none; }
    .txn-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 17px; margin-right: 12px; flex-shrink: 0; }
    .setting-row { display: flex; justify-content: space-between; align-items: center; padding: 16px 0; border-bottom: 1px solid var(--border-card); }
    .setting-row:last-child { border-bottom: none; }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
    .animate-in { animation: fadeInUp 0.45s ease-out forwards; }
    .stExpander { background: var(--bg-card) !important; border: 1px solid var(--border-card) !important; border-radius: var(--radius-lg) !important; }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    /* Always show the sidebar toggle button */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        background: #13141f !important;
        border: 1px solid rgba(110,231,247,0.2) !important;
        border-radius: 0 10px 10px 0 !important;
        color: #6ee7f7 !important;
    }
</style>
""", unsafe_allow_html=True)
# ============= AUTH FUNCTIONS =============
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    try:
        email = email.lower().strip()
        if email not in st.session_state.users_db:
            return False, "Email not found. Please sign up first."
        if st.session_state.users_db[email]['password'] == hash_password(password):
            st.session_state.user = {"email": email, "localId": hash_password(email)[:16], "name": st.session_state.users_db[email].get('name', '')}
            st.session_state.user_email = email
            st.session_state.user_id = hash_password(email)[:16]
            st.session_state.user_name = st.session_state.users_db[email].get('name', '')
            return True, "Login successful!"
        return False, "Invalid email or password"
    except Exception as e:
        return False, f"Login error: {str(e)}"

def signup_user(email, password, name=""):
    try:
        email = email.lower().strip()
        name = name.strip()
        if '@' not in email or '.' not in email:
            return False, "Invalid email format"
        if len(password) < 6:
            return False, "Password should be at least 6 characters"
        if email in st.session_state.users_db:
            return False, "Email already exists. Please login instead."
        st.session_state.users_db[email] = {'password': hash_password(password), 'name': name}
        st.session_state.user = {"email": email, "localId": hash_password(email)[:16], "name": name}
        st.session_state.user_email = email
        st.session_state.user_id = hash_password(email)[:16]
        st.session_state.user_name = name
        return True, "Account created successfully!"
    except Exception as e:
        return False, f"Signup error: {str(e)}"

def logout_user():
    st.session_state.user = None
    st.session_state.user_email = None
    st.session_state.user_id = None
    st.session_state.user_name = ""

# ============= AUTH PAGE =============
if st.session_state.user is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="auth-mode-indicator">
            <div class="mode-badge {'active' if st.session_state.auth_mode == 'login' else 'inactive'}">🔐 Login</div>
            <div class="mode-badge {'active' if st.session_state.auth_mode == 'signup' else 'inactive'}">✨ Sign Up</div>
        </div>
        <div class="auth-container">
            <div class="auth-title">{"Welcome Back" if st.session_state.auth_mode == 'login' else "Get Started"}</div>
            <div class="auth-subtitle">{"Sign in to access your financial dashboard" if st.session_state.auth_mode == 'login' else "Create your account to start managing your finances"}</div>
        </div>
        """, unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="Enter your email", key="auth_email", label_visibility="collapsed")
        if st.session_state.auth_mode == 'signup':
            name = st.text_input("Full Name", placeholder="Enter your full name", key="auth_name", label_visibility="collapsed")
        else:
            name = ""
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="auth_password", label_visibility="collapsed")
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        if st.session_state.auth_mode == 'login':
            if st.button("🔐 Sign In", use_container_width=True, type="primary"):
                if email and password:
                    success, message = login_user(email, password)
                    if success:
                        st.success(message); st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please enter both email and password")
        else:
            if st.button("✨ Create Account", use_container_width=True, type="primary"):
                if email and password:
                    success, message = signup_user(email, password, name)
                    if success:
                        st.success(message); st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please fill in all required fields")
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        if st.session_state.auth_mode == 'login':
            st.markdown("<div style='text-align: center; color: var(--text-muted);'>Don't have an account?</div>", unsafe_allow_html=True)
            if st.button("Create Account", use_container_width=True, key="switch_signup"):
                st.session_state.auth_mode = 'signup'; st.rerun()
        else:
            st.markdown("<div style='text-align: center; color: var(--text-muted);'>Already have an account?</div>", unsafe_allow_html=True)
            if st.button("Sign In", use_container_width=True, key="switch_login"):
                st.session_state.auth_mode = 'login'; st.rerun()
    st.stop()

# ============= SIDEBAR =============
with st.sidebar:
    st.markdown("""
    <div class="logo-container">
        <div class="logo-icon">L</div>
        <span class="logo-text">LumenMoney</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="nav-section-title">Main Menu</div>', unsafe_allow_html=True)
    if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
        st.session_state.current_page = 'dashboard'; st.rerun()
    if st.button("💳 Transactions", key="nav_transactions", use_container_width=True):
        st.session_state.current_page = 'transactions'; st.rerun()
    if st.button("👛 Wallet", key="nav_wallet", use_container_width=True):
        st.session_state.current_page = 'wallet'; st.rerun()
    if st.button("🎯 Goals", key="nav_goals", use_container_width=True):
        st.session_state.current_page = 'goals'; st.rerun()
    if st.button("💰 Budget", key="nav_budget", use_container_width=True):
        st.session_state.current_page = 'budget'; st.rerun()
    if st.button("📈 Analytics", key="nav_analytics", use_container_width=True):
        st.session_state.current_page = 'analytics'; st.rerun()
    st.markdown('<div class="nav-section-title" style="margin-top: 24px;">Settings</div>', unsafe_allow_html=True)
    if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
        st.session_state.current_page = 'settings'; st.rerun()
    if st.button("👤 Profile", key="nav_profile", use_container_width=True):
        st.session_state.current_page = 'profile'; st.rerun()
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
        logout_user(); st.rerun()

# ============= PAGE HEADER =============
top_col1, top_col2 = st.columns([6, 1])
with top_col1:
    page_titles = {
        'dashboard': ('LumenMoney', 'Your financial overview at a glance'),
        'transactions': ('Transactions', 'View and manage all your transactions'),
        'wallet': ('Wallet', 'Manage your digital wallets'),
        'goals': ('Goals', 'Track your financial goals'),
        'budget': ('Budget', 'Plan and monitor your budget'),
        'analytics': ('Analytics', 'Deep insights into your finances'),
        'settings': ('Settings', 'Customize your preferences'),
        'profile': ('Profile', 'Manage your account')
    }
    title, subtitle = page_titles.get(st.session_state.current_page, ('Dashboard', ''))
    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">{title}</h1>
        <p class="page-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PAGE: DASHBOARD
# ============================================================
if st.session_state.current_page == 'dashboard':
    st.markdown("""
    <div class="action-buttons">
        <button class="btn-secondary">⚙ Manage Widgets</button>
        <button class="btn-primary">＋ Add Widget</button>
    </div>
    """, unsafe_allow_html=True)

    metric_cols = st.columns(3, gap="large")
    with metric_cols[0]:
        st.markdown("""
        <div class="metric-card animate-in">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                <span class="metric-label">Total Balance</span>
                <span class="currency-badge">INR ▾</span>
            </div>
            <div class="metric-value">₹1,57,000<span style="opacity:0.5;">.00</span></div>
            <span class="metric-change positive">▲ 12.1% from last month</span>
            <div class="metric-subtext">You have ₹17,000 extra compared to last month</div>
            <div class="metric-footer">
                <span class="metric-footer-item">📊 50 transactions</span>
                <span class="metric-footer-item">📁 15 categories</span>
            </div>
        </div>""", unsafe_allow_html=True)
    with metric_cols[1]:
        st.markdown("""
        <div class="metric-card animate-in" style="animation-delay:0.1s;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                <span class="metric-label">Income</span>
                <span class="currency-badge">INR ▾</span>
            </div>
            <div class="metric-value">₹1,02,200<span style="opacity:0.5;">.00</span></div>
            <span class="metric-change positive">▲ 6.3% from last month</span>
            <div class="metric-subtext">You earned ₹6,000 more compared to last month</div>
            <div class="metric-footer">
                <span class="metric-footer-item">📊 27 transactions</span>
                <span class="metric-footer-item">📁 6 categories</span>
            </div>
        </div>""", unsafe_allow_html=True)
    with metric_cols[2]:
        st.markdown("""
        <div class="metric-card animate-in" style="animation-delay:0.2s;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                <span class="metric-label">Expense</span>
                <span class="currency-badge">INR ▾</span>
            </div>
            <div class="metric-value">₹62,200<span style="opacity:0.5;">.00</span></div>
            <span class="metric-change negative">▲ 2.4% from last month</span>
            <div class="metric-subtext">You spent ₹1,500 more compared to last month</div>
            <div class="metric-footer">
                <span class="metric-footer-item">📊 23 transactions</span>
                <span class="metric-footer-item">📁 9 categories</span>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
    chart_cols = st.columns([2, 1], gap="large")
    with chart_cols[0]:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown("""
        <div class="chart-header">
            <span class="chart-title">Balance Overview</span>
            <div style="display:flex;gap:20px;align-items:center;">
                <div class="legend-item"><div class="legend-dot" style="background:#6ee7f7;"></div><span class="legend-text">This month</span></div>
                <div class="legend-item"><div class="legend-dot" style="background:#4a5270;"></div><span class="legend-text">Last month</span></div>
            </div>
        </div>""", unsafe_allow_html=True)
        days = ['1 Jul','3 Jul','5 Jul','7 Jul','9 Jul','11 Jul','13 Jul','15 Jul','17 Jul','19 Jul']
        this_month = [140000,135000,150000,142000,158000,148000,162000,155000,160000,157000]
        last_month  = [130000,128000,132000,138000,135000,142000,140000,145000,148000,150000]
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=days,y=last_month,mode='lines',line=dict(color='#4a5270',width=2,dash='dot'),hovertemplate='₹%{y:,.0f}<extra></extra>'))
        fig1.add_trace(go.Scatter(x=days,y=this_month,mode='lines',line=dict(color='#6ee7f7',width=3),fill='tozeroy',fillcolor='rgba(110,231,247,0.07)',hovertemplate='₹%{y:,.0f}<extra></extra>'))
        fig1.update_layout(height=280,margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',showlegend=False,xaxis=dict(showgrid=False,zeroline=False,tickfont=dict(size=11,color='#4a5270')),yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,0.04)',zeroline=False,tickfont=dict(size=11,color='#4a5270'),tickformat='₹,.0f'),hovermode='x unified')
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_cols[1]:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown("""
        <div class="chart-header"><span class="chart-title">Expense Breakdown</span></div>
        <div style="text-align:center;color:#4a5270;font-size:12px;margin-bottom:16px;">By category</div>
        """, unsafe_allow_html=True)
        categories = ['Rent','Food & Dining','Transport','Entertainment','Utilities','Others']
        values = [18000,8500,5200,3200,2800,2500]
        colors = ['#6ee7f7','#818cf8','#f472b6','#34d399','#60a5fa','#4a5270']
        fig2 = go.Figure(data=[go.Pie(labels=categories,values=values,hole=0.7,marker=dict(colors=colors,line=dict(color='#0e0f1a',width=3)),textposition='outside',textinfo='percent',textfont=dict(size=11,color='#8892b0'),hovertemplate='<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>')])
        fig2.update_layout(height=300,margin=dict(l=20,r=20,t=20,b=20),paper_bgcolor='rgba(0,0,0,0)',showlegend=False,annotations=[dict(text='<b>Total</b><br>₹40,200',x=0.5,y=0.5,font=dict(size=12,color='#8892b0'),showarrow=False,align='center')])
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        st.markdown("""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:0 4px;">
            <div class="legend-item"><div class="legend-dot" style="background:#6ee7f7;"></div><span class="legend-text">Rent</span></div>
            <div class="legend-item"><div class="legend-dot" style="background:#818cf8;"></div><span class="legend-text">Food</span></div>
            <div class="legend-item"><div class="legend-dot" style="background:#f472b6;"></div><span class="legend-text">Transport</span></div>
            <div class="legend-item"><div class="legend-dot" style="background:#34d399;"></div><span class="legend-text">Entertainment</span></div>
            <div class="legend-item"><div class="legend-dot" style="background:#60a5fa;"></div><span class="legend-text">Utilities</span></div>
            <div class="legend-item"><div class="legend-dot" style="background:#4a5270;"></div><span class="legend-text">Others</span></div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-header">
        <span class="chart-title">Budget vs Expense Comparison</span>
        <div style="display:flex;gap:20px;align-items:center;">
            <div class="legend-item"><div class="legend-dot" style="background:#818cf8;"></div><span class="legend-text">Expense</span></div>
            <div class="legend-item"><div class="legend-dot" style="background:#f472b6;"></div><span class="legend-text">Budget</span></div>
        </div>
    </div>""", unsafe_allow_html=True)
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul']
    expenses_m = [58000,35000,62000,72000,55000,78000,68000]
    budgets_m  = [60000,40000,65000,70000,60000,75000,72000]
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=months,y=budgets_m,name='Budget',marker=dict(color='#f472b6'),width=0.35,offset=-0.18,hovertemplate='Budget: ₹%{y:,.0f}<extra></extra>'))
    fig3.add_trace(go.Bar(x=months,y=expenses_m,name='Expense',marker=dict(color='#818cf8'),width=0.35,offset=0.18,hovertemplate='Expense: ₹%{y:,.0f}<extra></extra>'))
    fig3.update_layout(height=300,margin=dict(l=0,r=0,t=20,b=0),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',showlegend=False,barmode='group',bargap=0.4,xaxis=dict(showgrid=False,zeroline=False,tickfont=dict(size=12,color='#4a5270')),yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,0.04)',zeroline=False,tickfont=dict(size=11,color='#4a5270'),tickformat='₹,.0f'))
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: TRANSACTIONS
# ============================================================
elif st.session_state.current_page == 'transactions':
    with st.expander("➕ Add New Transaction", expanded=False):
        c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 1.5, 1])
        with c1:
            t_desc = st.text_input("Description", placeholder="e.g. Grocery Shopping", key="t_desc")
        with c2:
            t_cat = st.selectbox("Category", ["Income","Rent","Food & Dining","Transport","Entertainment","Utilities","Shopping","Health","Others"], key="t_cat")
        with c3:
            t_amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0, key="t_amount")
        with c4:
            t_type = st.selectbox("Type", ["Expense","Income"], key="t_type")
        with c5:
            st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
            if st.button("Add", type="primary", use_container_width=True):
                if t_desc and t_amount > 0:
                    sign = 1 if t_type == "Income" else -1
                    st.session_state.transactions.insert(0, {
                        "date": datetime.today().strftime("%Y-%m-%d"),
                        "description": t_desc, "category": t_cat,
                        "amount": sign * t_amount, "type": t_type
                    })
                    st.success("Transaction added!"); st.rerun()

    fc1, fc2, fc3 = st.columns([2, 2, 2])
    with fc1:
        search = st.text_input("Search", placeholder="🔍 Search transactions...", key="txn_search", label_visibility="collapsed")
    with fc2:
        filter_type = st.selectbox("Filter by type", ["All","Income","Expense"], key="txn_filter", label_visibility="collapsed")
    with fc3:
        filter_cat = st.selectbox("Filter by category", ["All","Income","Rent","Food & Dining","Transport","Entertainment","Utilities","Shopping","Health","Others"], key="txn_cat", label_visibility="collapsed")

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    total_income  = sum(t['amount'] for t in st.session_state.transactions if t['amount'] > 0)
    total_expense = sum(abs(t['amount']) for t in st.session_state.transactions if t['amount'] < 0)
    sc1, sc2, sc3 = st.columns(3)
    for col, label, val in [(sc1,"Total Income",f"₹{total_income:,.0f}"),(sc2,"Total Expense",f"₹{total_expense:,.0f}"),(sc3,"Net Balance",f"₹{total_income-total_expense:,.0f}")]:
        with col:
            st.markdown(f"""<div class="metric-card" style="padding:20px;">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size:26px;">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title" style="margin-bottom:20px;">All Transactions</div>', unsafe_allow_html=True)

    cat_icons = {"Income":"💵","Rent":"🏠","Food & Dining":"🍽️","Transport":"🚗","Entertainment":"🎬","Utilities":"💡","Shopping":"🛍️","Health":"💊","Others":"📦"}
    cat_colors = {"Income":"rgba(52,211,153,0.15)","Rent":"rgba(110,231,247,0.15)","Food & Dining":"rgba(251,191,36,0.15)","Transport":"rgba(96,165,250,0.15)","Entertainment":"rgba(244,114,182,0.15)","Utilities":"rgba(20,184,166,0.15)","Shopping":"rgba(129,140,248,0.15)","Health":"rgba(251,113,133,0.15)","Others":"rgba(74,82,112,0.15)"}

    filtered = st.session_state.transactions
    if search:
        filtered = [t for t in filtered if search.lower() in t['description'].lower()]
    if filter_type != "All":
        filtered = [t for t in filtered if t['type'] == filter_type]
    if filter_cat != "All":
        filtered = [t for t in filtered if t['category'] == filter_cat]

    for txn in filtered:
        icon  = cat_icons.get(txn['category'], '📦')
        bg    = cat_colors.get(txn['category'], 'rgba(74,82,112,0.15)')
        color = "#34d399" if txn['amount'] > 0 else "#fb7185"
        sign  = "+" if txn['amount'] > 0 else ""
        st.markdown(f"""
        <div class="txn-row">
            <div style="display:flex;align-items:center;gap:14px;">
                <div class="txn-icon" style="background:{bg};">{icon}</div>
                <div>
                    <div style="color:#f0f4ff;font-weight:600;font-size:14px;">{txn['description']}</div>
                    <div style="color:#4a5270;font-size:12px;">{txn['category']} · {txn['date']}</div>
                </div>
            </div>
            <div style="color:{color};font-weight:700;font-size:15px;font-family:'JetBrains Mono',monospace;">{sign}₹{abs(txn['amount']):,.0f}</div>
        </div>""", unsafe_allow_html=True)

    if not filtered:
        st.markdown("<div style='text-align:center;color:#4a5270;padding:40px;'>No transactions found</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: WALLET
# ============================================================
elif st.session_state.current_page == 'wallet':
    wc1, wc2 = st.columns([1, 1], gap="large")
    with wc1:
        st.markdown("""
        <div class="wallet-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <span style="font-size:12px;opacity:0.7;font-weight:700;letter-spacing:1.5px;">HDFC BANK</span>
                <span style="font-size:20px;">💳</span>
            </div>
            <h3>₹85,400.00</h3>
            <div style="opacity:0.6;font-size:12px;margin-bottom:24px;letter-spacing:0.5px;">Savings Account</div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:14px;letter-spacing:3px;opacity:0.8;font-family:'JetBrains Mono',monospace;">•••• •••• •••• 4821</span>
                <span style="font-size:11px;opacity:0.6;">09/27</span>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="wallet-card-3">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <span style="font-size:12px;opacity:0.7;font-weight:700;letter-spacing:1.5px;">ICICI BANK</span>
                <span style="font-size:20px;">💳</span>
            </div>
            <h3>₹32,150.00</h3>
            <div style="opacity:0.6;font-size:12px;margin-bottom:24px;letter-spacing:0.5px;">Current Account</div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:14px;letter-spacing:3px;opacity:0.8;font-family:'JetBrains Mono',monospace;">•••• •••• •••• 7293</span>
                <span style="font-size:11px;opacity:0.6;">12/26</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with wc2:
        st.markdown("""
        <div class="wallet-card-2">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <span style="font-size:12px;opacity:0.7;font-weight:700;letter-spacing:1.5px;">SBI BANK</span>
                <span style="font-size:20px;">💳</span>
            </div>
            <h3>₹24,800.00</h3>
            <div style="opacity:0.6;font-size:12px;margin-bottom:24px;letter-spacing:0.5px;">Savings Account</div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:14px;letter-spacing:3px;opacity:0.8;font-family:'JetBrains Mono',monospace;">•••• •••• •••• 5517</span>
                <span style="font-size:11px;opacity:0.6;">03/28</span>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="chart-card" style="margin-top:0;">
            <div class="chart-title" style="margin-bottom:16px;">💰 Digital Wallets</div>
            <div class="txn-row">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div style="width:40px;height:40px;border-radius:10px;background:rgba(110,231,247,0.15);display:flex;align-items:center;justify-content:center;font-size:18px;">📱</div>
                    <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">PhonePe</div><div style="color:#4a5270;font-size:12px;">UPI Wallet</div></div>
                </div>
                <div style="color:#6ee7f7;font-weight:700;font-family:'JetBrains Mono',monospace;">₹5,200</div>
            </div>
            <div class="txn-row">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div style="width:40px;height:40px;border-radius:10px;background:rgba(52,211,153,0.15);display:flex;align-items:center;justify-content:center;font-size:18px;">💚</div>
                    <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Paytm</div><div style="color:#4a5270;font-size:12px;">Mobile Wallet</div></div>
                </div>
                <div style="color:#6ee7f7;font-weight:700;font-family:'JetBrains Mono',monospace;">₹3,750</div>
            </div>
            <div class="txn-row">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div style="width:40px;height:40px;border-radius:10px;background:rgba(96,165,250,0.15);display:flex;align-items:center;justify-content:center;font-size:18px;">🔵</div>
                    <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Google Pay</div><div style="color:#4a5270;font-size:12px;">UPI Wallet</div></div>
                </div>
                <div style="color:#6ee7f7;font-weight:700;font-family:'JetBrains Mono',monospace;">₹1,400</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title" style="margin-bottom:20px;">Wallet Balance Distribution</div>', unsafe_allow_html=True)
    wallet_names = ['HDFC Savings','ICICI Current','SBI Savings','PhonePe','Paytm','Google Pay']
    wallet_vals  = [85400, 32150, 24800, 5200, 3750, 1400]
    fig_w = go.Figure(go.Bar(x=wallet_vals,y=wallet_names,orientation='h',marker=dict(color=['#6ee7f7','#818cf8','#4f46e5','#34d399','#60a5fa','#fbbf24'],line=dict(color='rgba(0,0,0,0)',width=0)),hovertemplate='%{y}: ₹%{x:,.0f}<extra></extra>'))
    fig_w.update_layout(height=260,margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,0.04)',zeroline=False,tickfont=dict(size=11,color='#4a5270'),tickformat='₹,.0f'),yaxis=dict(showgrid=False,tickfont=dict(size=12,color='#8892b0')))
    st.plotly_chart(fig_w, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: GOALS
# ============================================================
elif st.session_state.current_page == 'goals':
    goals = [
        {"name": "Emergency Fund", "icon": "🛡️", "target": 200000, "saved": 145000, "deadline": "Dec 2024", "color": "#6ee7f7"},
        {"name": "New Car", "icon": "🚗", "target": 800000, "saved": 320000, "deadline": "Jun 2025", "color": "#60a5fa"},
        {"name": "Vacation to Europe", "icon": "✈️", "target": 150000, "saved": 82000, "deadline": "Mar 2025", "color": "#fbbf24"},
        {"name": "Home Down Payment", "icon": "🏠", "target": 1500000, "saved": 430000, "deadline": "Dec 2026", "color": "#34d399"},
        {"name": "MacBook Pro", "icon": "💻", "target": 180000, "saved": 180000, "deadline": "Achieved!", "color": "#818cf8"},
        {"name": "Wedding Fund", "icon": "💍", "target": 500000, "saved": 75000, "deadline": "Sep 2025", "color": "#f472b6"},
    ]
    gc1, gc2, gc3 = st.columns(3)
    active   = len([g for g in goals if g['saved'] < g['target']])
    achieved = len([g for g in goals if g['saved'] >= g['target']])
    total_saved = sum(g['saved'] for g in goals)
    for col, label, val in [(gc1,"Active Goals",str(active)),(gc2,"Goals Achieved",str(achieved)),(gc3,"Total Saved",f"₹{total_saved:,.0f}")]:
        with col:
            st.markdown(f"""<div class="metric-card" style="padding:20px;">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size:30px;">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    g_cols = st.columns(2, gap="large")
    for i, g in enumerate(goals):
        pct = min(100, int(g['saved'] / g['target'] * 100))
        remaining = max(0, g['target'] - g['saved'])
        with g_cols[i % 2]:
            st.markdown(f"""
            <div class="goal-card animate-in">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
                    <div style="display:flex;align-items:center;gap:12px;">
                        <div style="width:44px;height:44px;border-radius:12px;background:rgba(110,231,247,0.1);display:flex;align-items:center;justify-content:center;font-size:22px;">{g['icon']}</div>
                        <div>
                            <div class="goal-title">{g['name']}</div>
                            <div class="goal-amount">Target: ₹{g['target']:,.0f} · {g['deadline']}</div>
                        </div>
                    </div>
                    <div style="color:{g['color']};font-weight:800;font-size:17px;font-family:'JetBrains Mono',monospace;">{pct}%</div>
                </div>
                <div class="progress-bar-bg">
                    <div style="height:8px;border-radius:6px;background:{g['color']};width:{pct}%;"></div>
                </div>
                <div style="display:flex;justify-content:space-between;margin-top:8px;">
                    <span style="color:#8892b0;font-size:12px;">Saved: <b style="color:#f0f4ff;font-family:'JetBrains Mono',monospace;">₹{g['saved']:,.0f}</b></span>
                    <span style="color:#4a5270;font-size:12px;">{'🎉 Achieved!' if remaining==0 else f'₹{remaining:,.0f} to go'}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title" style="margin-bottom:20px;">Goals Progress Overview</div>', unsafe_allow_html=True)
    fig_g = go.Figure()
    fig_g.add_trace(go.Bar(name='Target',x=[g['name'] for g in goals],y=[g['target'] for g in goals],marker_color='rgba(110,231,247,0.2)',hovertemplate='Target: ₹%{y:,.0f}<extra></extra>'))
    fig_g.add_trace(go.Bar(name='Saved',x=[g['name'] for g in goals],y=[g['saved'] for g in goals],marker_color='#6ee7f7',hovertemplate='Saved: ₹%{y:,.0f}<extra></extra>'))
    fig_g.update_layout(height=280,margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',barmode='overlay',showlegend=True,legend=dict(font=dict(color='#8892b0'),bgcolor='rgba(0,0,0,0)'),xaxis=dict(showgrid=False,tickfont=dict(size=11,color='#4a5270')),yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,0.04)',tickfont=dict(size=11,color='#4a5270'),tickformat='₹,.0f'))
    st.plotly_chart(fig_g, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: BUDGET
# ============================================================
elif st.session_state.current_page == 'budget':
    budgets = [
        {"category":"🏠 Rent",         "budget":20000,"spent":18000,"color":"#6ee7f7"},
        {"category":"🍽️ Food & Dining", "budget":10000,"spent":8500, "color":"#fbbf24"},
        {"category":"🚗 Transport",     "budget":6000, "spent":5200, "color":"#60a5fa"},
        {"category":"🎬 Entertainment", "budget":4000, "spent":4600, "color":"#fb7185"},
        {"category":"💡 Utilities",     "budget":3500, "spent":2800, "color":"#34d399"},
        {"category":"🛍️ Shopping",      "budget":8000, "spent":3200, "color":"#818cf8"},
        {"category":"💊 Health",        "budget":3000, "spent":2300, "color":"#06b6d4"},
        {"category":"📦 Others",        "budget":5000, "spent":2500, "color":"#4a5270"},
    ]
    total_budget = sum(b['budget'] for b in budgets)
    total_spent  = sum(b['spent']  for b in budgets)
    bc1, bc2, bc3 = st.columns(3)
    for col, label, val in [(bc1,"Total Budget",f"₹{total_budget:,.0f}"),(bc2,"Total Spent",f"₹{total_spent:,.0f}"),(bc3,"Remaining",f"₹{total_budget-total_spent:,.0f}")]:
        with col:
            st.markdown(f"""<div class="metric-card" style="padding:20px;">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size:26px;">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title" style="margin-bottom:24px;">Monthly Budget Tracker</div>', unsafe_allow_html=True)
    for b in budgets:
        pct  = min(100, int(b['spent'] / b['budget'] * 100))
        over = b['spent'] > b['budget']
        bar_color = "#fb7185" if over else b['color']
        status = f"<span style='color:#fb7185;font-weight:700;font-size:12px;'>Over ₹{b['spent']-b['budget']:,}</span>" if over else f"<span style='color:#4a5270;font-size:12px;'>₹{b['budget']-b['spent']:,} left</span>"
        st.markdown(f"""
        <div style="margin-bottom:20px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="color:#c8d0e8;font-weight:600;font-size:13px;">{b['category']}</span>
                <div style="display:flex;gap:16px;align-items:center;">
                    {status}
                    <span style="color:#8892b0;font-size:12px;font-family:'JetBrains Mono',monospace;">₹{b['spent']:,} / ₹{b['budget']:,}</span>
                    <span style="color:{bar_color};font-weight:700;font-size:13px;">{pct}%</span>
                </div>
            </div>
            <div class="progress-bar-bg">
                <div style="height:8px;border-radius:6px;background:{bar_color};width:{pct}%;"></div>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title" style="margin-bottom:20px;">Budget vs Actual Spending</div>', unsafe_allow_html=True)
    fig_b = go.Figure()
    fig_b.add_trace(go.Bar(name='Budget',x=[b['category'] for b in budgets],y=[b['budget'] for b in budgets],marker_color='rgba(129,140,248,0.35)',hovertemplate='Budget: ₹%{y:,.0f}<extra></extra>'))
    fig_b.add_trace(go.Bar(name='Spent', x=[b['category'] for b in budgets],y=[b['spent']  for b in budgets],marker_color='#6ee7f7',hovertemplate='Spent: ₹%{y:,.0f}<extra></extra>'))
    fig_b.update_layout(height=280,margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',barmode='group',bargap=0.3,showlegend=True,legend=dict(font=dict(color='#8892b0'),bgcolor='rgba(0,0,0,0)'),xaxis=dict(showgrid=False,tickfont=dict(size=11,color='#4a5270')),yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,0.04)',tickfont=dict(size=11,color='#4a5270'),tickformat='₹,.0f'))
    st.plotly_chart(fig_b, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: ANALYTICS
# ============================================================
elif st.session_state.current_page == 'analytics':
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title" style="margin-bottom:20px;">Income vs Expense — 12 Month Trend</div>', unsafe_allow_html=True)
    months_12  = ['Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul']
    income_12  = [88000,92000,85000,95000,102000,98000,96000,100000,91000,99000,96000,102200]
    expense_12 = [54000,58000,62000,71000,82000,65000,59000,63000,55000,61000,67000,62200]
    savings_12 = [i-e for i,e in zip(income_12,expense_12)]
    fig_a1 = go.Figure()
    fig_a1.add_trace(go.Scatter(x=months_12,y=income_12,mode='lines+markers',name='Income',line=dict(color='#34d399',width=3),marker=dict(size=6),hovertemplate='Income: ₹%{y:,.0f}<extra></extra>'))
    fig_a1.add_trace(go.Scatter(x=months_12,y=expense_12,mode='lines+markers',name='Expense',line=dict(color='#fb7185',width=3),marker=dict(size=6),hovertemplate='Expense: ₹%{y:,.0f}<extra></extra>'))
    fig_a1.add_trace(go.Bar(x=months_12,y=savings_12,name='Savings',marker_color='rgba(110,231,247,0.2)',hovertemplate='Savings: ₹%{y:,.0f}<extra></extra>'))
    fig_a1.update_layout(height=300,margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',showlegend=True,legend=dict(font=dict(color='#8892b0'),bgcolor='rgba(0,0,0,0)',orientation='h',yanchor='bottom',y=1.02),xaxis=dict(showgrid=False,tickfont=dict(size=12,color='#4a5270')),yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,0.04)',tickfont=dict(size=11,color='#4a5270'),tickformat='₹,.0f'),hovermode='x unified')
    st.plotly_chart(fig_a1, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    an_c1, an_c2 = st.columns(2, gap="large")
    with an_c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title" style="margin-bottom:20px;">Spending by Category (YTD)</div>', unsafe_allow_html=True)
        cats_a = ['Rent','Food','Transport','Entertainment','Utilities','Shopping','Health','Others']
        vals_a = [216000,102000,62400,45000,33600,38400,27600,30000]
        cols_a = ['#6ee7f7','#fbbf24','#60a5fa','#fb7185','#34d399','#818cf8','#06b6d4','#4a5270']
        fig_a2 = go.Figure(go.Pie(labels=cats_a,values=vals_a,hole=0.6,marker=dict(colors=cols_a,line=dict(color='#0e0f1a',width=2)),textposition='outside',textinfo='percent+label',textfont=dict(size=10,color='#8892b0'),hovertemplate='<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>'))
        fig_a2.update_layout(height=320,margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor='rgba(0,0,0,0)',showlegend=False,annotations=[dict(text='<b>YTD</b><br>₹7.5L',x=0.5,y=0.5,font=dict(size=13,color='#8892b0'),showarrow=False)])
        st.plotly_chart(fig_a2, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with an_c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title" style="margin-bottom:20px;">Savings Rate by Month</div>', unsafe_allow_html=True)
        savings_rate = [round(s/i*100,1) for s,i in zip(savings_12,income_12)]
        fig_a3 = go.Figure(go.Bar(x=months_12,y=savings_rate,marker=dict(color=savings_rate,colorscale=[[0,'#fb7185'],[0.3,'#fbbf24'],[0.6,'#34d399'],[1,'#6ee7f7']],showscale=False),hovertemplate='%{x}: %{y}% savings<extra></extra>',text=[f'{r}%' for r in savings_rate],textposition='outside',textfont=dict(color='#8892b0',size=10)))
        fig_a3.update_layout(height=320,margin=dict(l=0,r=0,t=30,b=0),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',showlegend=False,xaxis=dict(showgrid=False,tickfont=dict(size=11,color='#4a5270')),yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,0.04)',tickfont=dict(size=11,color='#4a5270'),ticksuffix='%'))
        st.plotly_chart(fig_a3, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title" style="margin-bottom:20px;">Daily Spending — Last 30 Days</div>', unsafe_allow_html=True)
    dates_30 = [(datetime.today() - timedelta(days=i)).strftime('%d %b') for i in range(29,-1,-1)]
    spend_30 = [random.randint(500,4500) for _ in range(30)]
    fig_a4 = go.Figure(go.Scatter(x=dates_30,y=spend_30,mode='lines',fill='tozeroy',line=dict(color='#6ee7f7',width=2),fillcolor='rgba(110,231,247,0.06)',hovertemplate='%{x}: ₹%{y:,.0f}<extra></extra>'))
    fig_a4.update_layout(height=220,margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',showlegend=False,xaxis=dict(showgrid=False,tickfont=dict(size=10,color='#4a5270'),tickmode='array',tickvals=dates_30[::5]),yaxis=dict(showgrid=True,gridcolor='rgba(255,255,255,0.04)',tickfont=dict(size=11,color='#4a5270'),tickformat='₹,.0f'),hovermode='x unified')
    st.plotly_chart(fig_a4, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: SETTINGS
# ============================================================
elif st.session_state.current_page == 'settings':
    set_c1, set_c2 = st.columns(2, gap="large")
    with set_c1:
        st.markdown("""
        <div class="profile-section">
            <div class="section-title">💱 Currency & Region</div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Primary Currency</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">Default currency for all transactions</div></div>
                <span style="color:#6ee7f7;font-weight:700;font-size:13px;">INR (₹)</span>
            </div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Date Format</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">How dates are displayed</div></div>
                <span style="color:#6ee7f7;font-weight:700;font-size:13px;">DD/MM/YYYY</span>
            </div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Time Zone</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">Your local time zone</div></div>
                <span style="color:#6ee7f7;font-weight:700;font-size:13px;">IST (UTC+5:30)</span>
            </div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Language</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">App display language</div></div>
                <span style="color:#6ee7f7;font-weight:700;font-size:13px;">English</span>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="profile-section">
            <div class="section-title">🔔 Notifications</div>
            <div class="preference-item"><div><div class="preference-label">Email Alerts</div><div class="preference-sublabel">Receive weekly summary emails</div></div><div class="toggle-switch"></div></div>
            <div class="preference-item"><div><div class="preference-label">Budget Warnings</div><div class="preference-sublabel">Alert when 80% of budget is used</div></div><div class="toggle-switch"></div></div>
            <div class="preference-item"><div><div class="preference-label">Goal Milestones</div><div class="preference-sublabel">Celebrate when goals hit 25%, 50%, 75%</div></div><div class="toggle-switch"></div></div>
            <div class="preference-item"><div><div class="preference-label">Large Transactions</div><div class="preference-sublabel">Alert for transactions above ₹10,000</div></div><div class="toggle-switch"></div></div>
        </div>""", unsafe_allow_html=True)

    with set_c2:
        st.markdown("""
        <div class="profile-section">
            <div class="section-title">🎨 Appearance</div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Theme</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">App color theme</div></div>
                <span style="color:#6ee7f7;font-weight:700;font-size:13px;">Dark Mode</span>
            </div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Accent Color</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">Primary highlight color</div></div>
                <span style="color:#6ee7f7;font-weight:700;font-size:13px;">🩵 Cyan</span>
            </div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Chart Style</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">Default chart type</div></div>
                <span style="color:#6ee7f7;font-weight:700;font-size:13px;">Line Charts</span>
            </div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Compact Mode</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">Reduce spacing between elements</div></div>
                <span style="color:#4a5270;font-weight:700;font-size:13px;">Off</span>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="profile-section">
            <div class="section-title">🔐 Privacy & Security</div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Two-Factor Auth</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">Extra login security</div></div>
                <span style="color:#34d399;font-weight:700;font-size:13px;">✓ Enabled</span>
            </div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Biometric Login</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">Use fingerprint/face ID</div></div>
                <span style="color:#4a5270;font-weight:700;font-size:13px;">Disabled</span>
            </div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Data Export</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">Download your financial data</div></div>
                <button class="edit-btn">Export CSV</button>
            </div>
            <div class="setting-row">
                <div><div style="color:#f0f4ff;font-weight:600;font-size:14px;">Delete Account</div><div style="color:#4a5270;font-size:12px;margin-top:3px;">Permanently remove your data</div></div>
                <button style="background:rgba(251,113,133,0.1);border:1px solid rgba(251,113,133,0.3);border-radius:8px;padding:7px 14px;color:#fb7185;font-size:12px;font-weight:600;cursor:pointer;">Delete</button>
            </div>
        </div>""", unsafe_allow_html=True)

# ============================================================
# PAGE: PROFILE
# ============================================================
elif st.session_state.current_page == 'profile':
    user_email = st.session_state.get('user_email', 'user@example.com')
    stored_name = st.session_state.get('user_name', '')
    if stored_name:
        user_display_name = stored_name
        name_parts = user_display_name.split()
    else:
        user_name_part = user_email.split('@')[0]
        user_display_name = user_name_part.replace('.', ' ').replace('_', ' ').title()
        name_parts = user_display_name.split()
    user_initials = (name_parts[0][0] + name_parts[1][0]).upper() if len(name_parts) >= 2 else user_display_name[:2].upper()

    st.markdown(f"""
    <div class="profile-header animate-in">
        <div class="profile-avatar">{user_initials}</div>
        <div class="profile-name">{user_display_name}</div>
        <div class="profile-email">{user_email}</div>
        <div class="profile-badges">
            <span class="badge badge-premium">⭐ Premium</span>
            <span class="badge badge-verified">✓ Verified</span>
        </div>
        <div class="profile-stats">
            <div class="profile-stat"><div class="profile-stat-value">₹1,57,000</div><div class="profile-stat-label">Total Balance</div></div>
            <div class="profile-stat"><div class="profile-stat-value">6</div><div class="profile-stat-label">Active Goals</div></div>
            <div class="profile-stat"><div class="profile-stat-value">89%</div><div class="profile-stat-label">Budget Score</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="profile-section animate-in">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <span class="section-title">Personal Information</span>
                <button class="edit-btn">Edit</button>
            </div>
            <div class="profile-field"><span class="profile-field-label">First Name</span><span class="profile-field-value">{name_parts[0] if name_parts else 'Not Set'}</span></div>
            <div class="profile-field"><span class="profile-field-label">Last Name</span><span class="profile-field-value">{name_parts[1] if len(name_parts) > 1 else 'Not Set'}</span></div>
            <div class="profile-field"><span class="profile-field-label">Email</span><span class="profile-field-value">{user_email}</span></div>
            <div class="profile-field"><span class="profile-field-label">Phone</span><span class="profile-field-value">+91 98765 43210</span></div>
            <div class="profile-field"><span class="profile-field-label">Location</span><span class="profile-field-value">Hyderabad, India</span></div>
        </div>
        <div class="profile-section animate-in">
            <span class="section-title">Financial Overview</span>
            <div class="profile-field"><span class="profile-field-label">Primary Currency</span><span class="profile-field-value">INR (₹)</span></div>
            <div class="profile-field"><span class="profile-field-label">Member Since</span><span class="profile-field-value">January 2024</span></div>
            <div class="profile-field"><span class="profile-field-label">Total Transactions</span><span class="profile-field-value">1,247</span></div>
            <div class="profile-field"><span class="profile-field-label">Linked Accounts</span><span class="profile-field-value">4 Accounts</span></div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="profile-section animate-in">
            <span class="section-title">Preferences</span>
            <div class="preference-item"><div><div class="preference-label">Email Notifications</div><div class="preference-sublabel">Receive updates about your finances</div></div><div class="toggle-switch"></div></div>
            <div class="preference-item"><div><div class="preference-label">Budget Alerts</div><div class="preference-sublabel">Get notified when exceeding budget</div></div><div class="toggle-switch"></div></div>
            <div class="preference-item"><div><div class="preference-label">Goal Reminders</div><div class="preference-sublabel">Weekly progress updates</div></div><div class="toggle-switch"></div></div>
            <div class="preference-item"><div><div class="preference-label">Transaction Alerts</div><div class="preference-sublabel">Real-time notifications</div></div><div class="toggle-switch"></div></div>
        </div>
        <div class="profile-section animate-in">
            <span class="section-title">Security</span>
            <div class="profile-field"><span class="profile-field-label">Password</span><button class="edit-btn">Change</button></div>
            <div class="profile-field"><span class="profile-field-label">Two-Factor Auth</span><span style="color:#34d399;font-weight:600;">✓ Enabled</span></div>
            <div class="profile-field"><span class="profile-field-label">Login Sessions</span><button class="edit-btn">Manage</button></div>
            <div class="profile-field"><span class="profile-field-label">Connected Devices</span><span class="profile-field-value">3 Devices</span></div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
