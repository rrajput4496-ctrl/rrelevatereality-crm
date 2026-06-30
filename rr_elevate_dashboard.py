"""
╔══════════════════════════════════════════════════════════════╗
║   RR ELEVATE REALTY — AI COMMAND CENTER DASHBOARD           ║
║   Built with Streamlit — God Mode                           ║
║   Run: streamlit run rr_elevate_dashboard.py                ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time
import csv
import os

# ── WEBSITE LEADS INTEGRATION ──────────────────
WEBSITE_LEADS_FILE = "leads_from_website.csv"

def load_website_leads():
    leads = []
    if os.path.exists(WEBSITE_LEADS_FILE):
        try:
            with open(WEBSITE_LEADS_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    leads.append(row)
        except Exception:
            pass
    return leads

def get_website_leads_df():
    leads = load_website_leads()
    if not leads:
        return pd.DataFrame()
    rows = []
    for l in leads:
        rows.append({
            "Name": l.get("Name", ""),
            "Location": l.get("City", ""),
            "Requirement": l.get("Interest", ""),
            "Budget": l.get("Budget", ""),
            "Score": int(l.get("Score", 50)),
            "Status": l.get("Status", "Warm"),
            "Source": "Website",
            "Date": l.get("Date", ""),
            "Phone": l.get("Phone", ""),
            "Email": l.get("Email", ""),
            "Message": l.get("Message", ""),
        })
    return pd.DataFrame(rows)
# ───────────────────────────────────────────────

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RR Elevate Realty | AI Command Center",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — BLACK + GOLD LUXURY THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── IMPORT FONTS ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── ROOT COLORS ── */
:root {
    --black: #0A0A0F;
    --dark: #111118;
    --dark2: #181820;
    --dark3: #1E1E28;
    --gold: #C9A227;
    --gold2: #E8BC3A;
    --gold3: #A07D1C;
    --white: #FFFFFF;
    --muted: #888888;
    --green: #06D6A0;
    --rose: #E84855;
    --blue: #3A86FF;
    --teal: #2EC4B6;
    --purple: #9B5DE5;
}

/* ── GLOBAL ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0A0A0F !important;
    color: #FFFFFF !important;
}

/* ── HIDE DEFAULT STREAMLIT ELEMENTS ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D0D15 0%, #0A0A12 100%) !important;
    border-right: 1px solid rgba(201,162,39,0.2) !important;
    width: 240px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: #181820 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    transition: all 0.3s !important;
}
[data-testid="metric-container"]:hover {
    border-color: rgba(201,162,39,0.35) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #C9A227 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.65rem !important;
    color: #888 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
}

/* ── CARDS ── */
.card {
    background: #181820;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 14px;
    transition: all 0.3s;
}
.card:hover { border-color: rgba(201,162,39,0.25); }
.card-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 4px;
}
.card-sub { font-size: 0.65rem; color: #888; margin-bottom: 14px; }

/* ── GOLD HEADER ── */
.gold-header {
    background: linear-gradient(135deg, #0D0D15, #111118);
    border-bottom: 1px solid rgba(201,162,39,0.2);
    padding: 14px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0;
}
.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: white;
}
.brand-name span { color: #C9A227; }
.ai-badge {
    font-size: 0.6rem;
    color: #C9A227;
    background: rgba(201,162,39,0.1);
    border: 1px solid rgba(201,162,39,0.25);
    border-radius: 20px;
    padding: 4px 12px;
    letter-spacing: 0.1em;
}

/* ── AGENT CARDS ── */
.agent-card {
    background: #1E1E28;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: all 0.3s;
}
.agent-card:hover {
    border-color: rgba(201,162,39,0.3);
    background: rgba(201,162,39,0.05);
}
.agent-icon {
    font-size: 1.4rem;
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    flex-shrink: 0;
}
.agent-name { font-size: 0.78rem; font-weight: 700; color: #FFFFFF; }
.agent-desc { font-size: 0.62rem; color: #888; margin-top: 2px; }
.agent-active {
    font-size: 0.58rem;
    color: #06D6A0;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 4px;
}
.active-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #06D6A0;
    display: inline-block;
    animation: blink 1.5s infinite;
}

/* ── LEAD TABLE ── */
.lead-row {
    background: #1E1E28;
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 6px;
    display: grid;
    grid-template-columns: 140px 110px 60px 70px 55px 65px;
    align-items: center;
    gap: 8px;
    font-size: 0.74rem;
    transition: all 0.25s;
    cursor: pointer;
}
.lead-row:hover { border-color: rgba(201,162,39,0.25); background: rgba(201,162,39,0.03); }
.score-hot { background: #06D6A0; color: #000; padding: 2px 8px; border-radius: 12px; font-size: 0.6rem; font-weight: 800; }
.score-warm { background: #C9A227; color: #000; padding: 2px 8px; border-radius: 12px; font-size: 0.6rem; font-weight: 800; }
.score-cold { background: #444; color: #fff; padding: 2px 8px; border-radius: 12px; font-size: 0.6rem; font-weight: 800; }
.status-hot { background: rgba(232,72,85,0.15); color: #E84855; border: 1px solid rgba(232,72,85,0.3); padding: 2px 8px; border-radius: 12px; font-size: 0.58rem; font-weight: 700; }
.status-warm { background: rgba(201,162,39,0.15); color: #C9A227; border: 1px solid rgba(201,162,39,0.3); padding: 2px 8px; border-radius: 12px; font-size: 0.58rem; font-weight: 700; }
.status-cold { background: rgba(136,136,136,0.1); color: #888; border: 1px solid rgba(136,136,136,0.2); padding: 2px 8px; border-radius: 12px; font-size: 0.58rem; font-weight: 700; }

/* ── SCHEDULE ── */
.sched-item {
    background: #1E1E28;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    display: flex;
    gap: 12px;
    cursor: pointer;
    transition: all 0.25s;
}
.sched-item:hover { border-color: rgba(201,162,39,0.3); }
.sched-time { font-size: 0.68rem; color: #C9A227; font-weight: 700; width: 56px; flex-shrink: 0; }
.sched-title { font-size: 0.76rem; font-weight: 600; color: #fff; }
.sched-loc { font-size: 0.62rem; color: #888; margin-top: 2px; }

/* ── STAT PILL ── */
.stat-pill {
    background: linear-gradient(135deg, rgba(201,162,39,0.12), rgba(201,162,39,0.04));
    border: 1px solid rgba(201,162,39,0.2);
    border-radius: 8px;
    padding: 10px 14px;
    text-align: center;
}

/* ── BOTTOM QUOTE ── */
.quote-bar {
    background: linear-gradient(135deg, #0D0D15, #111118);
    border-top: 1px solid rgba(201,162,39,0.15);
    padding: 12px 24px;
    font-size: 0.72rem;
    color: rgba(255,255,255,0.5);
    font-style: italic;
    display: flex;
    align-items: center;
    gap: 16px;
}
.quote-bar strong { color: #C9A227; }

/* ── SIDEBAR LOGO ── */
.sb-logo-box {
    padding: 20px 18px 16px;
    border-bottom: 1px solid rgba(201,162,39,0.15);
    margin-bottom: 8px;
}
.rr-icon {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #A07D1C, #C9A227);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem; font-weight: 900;
    color: #000; margin-bottom: 10px;
    box-shadow: 0 4px 20px rgba(201,162,39,0.25);
}
.sb-brand-name { font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 700; color: #fff; }
.sb-brand-name span { color: #C9A227; }
.sb-tagline { font-size: 0.56rem; color: #666; letter-spacing: 0.15em; text-transform: uppercase; margin-top: 2px; }

/* ── NAV ITEM ── */
.nav-item {
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 0.78rem;
    color: rgba(255,255,255,0.55);
    cursor: pointer;
    margin-bottom: 2px;
    transition: all 0.25s;
    display: flex;
    align-items: center;
    gap: 10px;
}
.nav-item:hover { background: rgba(201,162,39,0.08); color: rgba(255,255,255,0.85); }
.nav-item.active {
    background: linear-gradient(135deg,rgba(201,162,39,0.15),rgba(201,162,39,0.05));
    color: #C9A227; border: 1px solid rgba(201,162,39,0.2);
    border-left: 3px solid #C9A227;
}

/* ── DATAFRAME STYLING ── */
.stDataFrame { background: #181820 !important; border-radius: 10px !important; }
[data-testid="stDataFrameContainer"] { border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 10px !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #A07D1C, #C9A227) !important;
    color: #000 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #C9A227, #E8BC3A) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(201,162,39,0.3) !important;
}

/* ── SELECTBOX / INPUT ── */
.stSelectbox > div > div, .stTextInput > div > div {
    background: #1E1E28 !important;
    border: 1px solid rgba(201,162,39,0.15) !important;
    border-radius: 8px !important;
    color: #fff !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #181820 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    color: #888 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(201,162,39,0.12) !important;
    color: #C9A227 !important;
}

/* ── PROGRESS BAR ── */
.stProgress > div > div { background: #C9A227 !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: #1E1E28 !important;
    border: 1px solid rgba(201,162,39,0.15) !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-size: 0.8rem !important;
}

/* ── PLOTLY CHARTS ── */
.js-plotly-plot { border-radius: 10px !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0A0A0F; }
::-webkit-scrollbar-thumb { background: #A07D1C; border-radius: 2px; }

/* ── DIVIDER ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(201,162,39,0.12) !important;
    margin: 10px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
GOLD = "#C9A227"
GOLD2 = "#E8BC3A"
DARK = "#181820"
DARK2 = "#1E1E28"
DARK3 = "#252530"
GREEN = "#06D6A0"
ROSE = "#E84855"
BLUE = "#3A86FF"
TEAL = "#2EC4B6"
PURPLE = "#9B5DE5"
ORANGE = "#FB8500"

LEADS_DATA = get_website_leads_df()
if LEADS_DATA.empty:
    LEADS_DATA = pd.DataFrame(columns=["Name", "Location", "Requirement", "Budget", "Score", "Status", "Source", "Date", "Phone", "Email", "Message"])

WEEK_DATES = pd.date_range(end=datetime.today(), periods=7).strftime("%d %b").tolist()
WEEK_LEADS = [28, 45, 38, 72, 85, 60, 52]
WEEK_VISITS = [4, 8, 5, 12, 10, 7, 8]
WEEK_DEALS = [1, 2, 1, 3, 2, 2, 1]

MONTH_WEEKS = ["Week 1", "Week 2", "Week 3", "Week 4"]
MONTH_LEADS = [120, 180, 145, 210]

AI_AGENTS = [
    {"icon": "🤖", "name": "AI Receptionist", "desc": "Handles all incoming chats, calls & queries", "bg": "rgba(58,134,255,0.12)", "tasks": 8, "status": "Active"},
    {"icon": "🧠", "name": "Lead Qualification AI", "desc": "Qualifies & scores leads automatically", "bg": "rgba(201,162,39,0.12)", "tasks": 14, "status": "Active"},
    {"icon": "🏠", "name": "Property Match AI", "desc": "Matches leads with best suitable properties", "bg": "rgba(155,93,229,0.12)", "tasks": 6, "status": "Active"},
    {"icon": "📲", "name": "Follow-up AI", "desc": "Automated follow-ups via WhatsApp, SMS, Email", "bg": "rgba(46,196,182,0.12)", "tasks": 22, "status": "Active"},
    {"icon": "📣", "name": "Marketing AI", "desc": "Creates content, ads & campaigns automatically", "bg": "rgba(232,72,85,0.12)", "tasks": 5, "status": "Active"},
    {"icon": "💼", "name": "CRM AI", "desc": "Manages CRM, reminds follow-ups & tasks", "bg": "rgba(6,214,160,0.12)", "tasks": 11, "status": "Active"},
    {"icon": "📊", "name": "Analytics AI", "desc": "Generates reports & business insights", "bg": "rgba(251,133,0,0.12)", "tasks": 3, "status": "Active"},
]

PROPERTIES = [
    {"name": "3 BHK Luxury Apartment", "loc": "Bopal, Ahmedabad", "price": "₹85L", "bed": 3, "bath": 3, "area": "1450 sq.ft", "status": "Hot"},
    {"name": "4 BHK Premium Villa", "loc": "Prahlad Nagar", "price": "₹2.4Cr", "bed": 4, "bath": 4, "area": "3200 sq.ft", "status": "New"},
    {"name": "2 BHK Smart Home", "loc": "Gota, Ahmedabad", "price": "₹58L", "bed": 2, "bath": 2, "area": "1050 sq.ft", "status": "Available"},
    {"name": "Penthouse Suite", "loc": "Satellite, Ahmedabad", "price": "₹4.5Cr", "bed": 5, "bath": 5, "area": "5200 sq.ft", "status": "Premium"},
    {"name": "Commercial Space", "loc": "SG Highway", "price": "₹1.8Cr", "bed": 0, "bath": 2, "area": "2800 sq.ft", "status": "Available"},
]

SCHEDULE_TODAY = []

# ─────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="rgba(255,255,255,0.7)", size=11),
    margin=dict(l=8, r=8, t=8, b=8),
    showlegend=False,
)

def gold_line_chart(x, y, title=""):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers",
        line=dict(color=GOLD, width=2.5, shape="spline"),
        marker=dict(color=GOLD, size=6, line=dict(color="#0A0A0F", width=2)),
        fill="tozeroy",
        fillcolor="rgba(201,162,39,0.08)",
        hovertemplate="<b>%{x}</b><br>Leads: %{y}<extra></extra>"
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        height=180,
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=9, color="rgba(255,255,255,0.35)")),
        yaxis=dict(showgrid=True, zeroline=False, gridcolor="rgba(255,255,255,0.04)",
                   tickfont=dict(size=9, color="rgba(255,255,255,0.35)")),
    )
    return fig

def donut_chart(labels, values, colors, height=220):
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color="#0A0A0F", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
    ))
    fig.update_layout(**CHART_LAYOUT, height=height)
    return fig

def funnel_chart(stages, values, colors):
    fig = go.Figure(go.Funnel(
        y=stages, x=values,
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=colors, line=dict(color="#0A0A0F", width=1)),
        connector=dict(line=dict(color="rgba(201,162,39,0.1)", width=1)),
        hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        height=260,
        funnelmode="stack",
        yaxis=dict(tickfont=dict(size=10, color="rgba(255,255,255,0.6)")),
    )
    return fig

def bar_chart(categories, values, color=GOLD, horizontal=False):
    if horizontal:
        fig = go.Figure(go.Bar(
            x=values, y=categories, orientation="h",
            marker=dict(color=color, opacity=0.85,
                       line=dict(color="rgba(0,0,0,0)", width=0)),
            hovertemplate="<b>%{y}</b><br>%{x}%<extra></extra>",
            text=[f"{v}%" for v in values],
            textposition="outside",
            textfont=dict(color="rgba(255,255,255,0.6)", size=10),
        ))
    else:
        fig = go.Figure(go.Bar(
            x=categories, y=values,
            marker=dict(color=color, opacity=0.85),
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
        ))
    fig.update_layout(
        **CHART_LAYOUT,
        height=220,
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(size=9, color="rgba(255,255,255,0.4)")),
        yaxis=dict(showgrid=True, zeroline=False,
                   gridcolor="rgba(255,255,255,0.04)",
                   tickfont=dict(size=9, color="rgba(255,255,255,0.4)")),
        bargap=0.3,
    )
    return fig

def multi_line_chart(x, datasets):
    fig = go.Figure()
    for ds in datasets:
        fig.add_trace(go.Scatter(
            x=x, y=ds["y"], name=ds["name"],
            mode="lines+markers",
            line=dict(color=ds["color"], width=2, shape="spline"),
            marker=dict(size=5),
            fill="tozeroy" if ds.get("fill") else "none",
            fillcolor=ds.get("fillcolor", "rgba(0,0,0,0)"),
        ))
    layout = dict(CHART_LAYOUT)
    layout["showlegend"] = True
    fig.update_layout(
        **layout,
        height=200,
        legend=dict(orientation="h", y=1.1, x=0, font=dict(size=9, color="rgba(255,255,255,0.6)")),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=9)),
    )
    return fig

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo-box">
        <div class="rr-icon">RR</div>
        <div class="sb-brand-name"><span>RR</span> Elevate Realty</div>
        <div class="sb-tagline">— Elevate Your Future —</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding:8px 10px'>", unsafe_allow_html=True)

    pages = {
        "📊 Dashboard": "Dashboard",
        "👥 Leads (128)": "Leads",
        "🏠 Properties": "Properties",
        "📅 Appointments": "Appointments",
        "💼 Deals (24)": "Deals",
        "👤 Clients": "Clients",
        "✅ Tasks": "Tasks",
        "📣 Marketing": "Marketing",
        "📈 Reports": "Reports",
        "🤖 AI Agents": "AI Agents",
        "⚙️ Settings": "Settings",
    }

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    for label, page in pages.items():
        active = "active" if st.session_state.page == page else ""
        if st.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Promo
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(201,162,39,0.1),rgba(201,162,39,0.03));
                border:1px solid rgba(201,162,39,0.2);border-radius:10px;
                padding:16px;text-align:center;margin:8px">
        <div style="font-size:2rem;margin-bottom:8px">🏙</div>
        <div style="font-size:0.78rem;font-weight:700;color:#fff;margin-bottom:4px">Grow Your Business</div>
        <div style="font-size:0.62rem;color:#888;margin-bottom:12px">With AI Power</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📊 View Analytics", use_container_width=True):
        st.session_state.page = "Reports"
        st.rerun()

    st.markdown(f"""
    <div style="padding:10px 10px 4px;font-size:0.62rem;color:#555;text-align:center">
        © 2026 RR Elevate Realty<br>
        <span style="color:#C9A227">RERA: GJ/REA/2024/XXXXX</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────
if st.session_state.page == "Dashboard":

    # ── HEADER ──
    now = datetime.now()
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0D0D15,#111118);
                border-bottom:1px solid rgba(201,162,39,0.2);
                padding:14px 24px;display:flex;align-items:center;gap:12px;margin-bottom:20px">
        <div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:1.15rem;font-weight:700;color:#fff">
                <span style="color:#C9A227">RR</span> Elevate Realty
            </div>
            <div style="font-size:0.6rem;color:#C9A227;margin-top:2px;letter-spacing:0.1em">
                🤖 AI Powered Real Estate Command Center &nbsp;·&nbsp; {now.strftime('%A, %d %B %Y %I:%M %p')}
            </div>
        </div>
        <div style="margin-left:auto;display:flex;align-items:center;gap:12px">
            <div style="background:rgba(6,214,160,0.1);border:1px solid rgba(6,214,160,0.25);
                        border-radius:20px;padding:4px 12px;font-size:0.6rem;color:#06D6A0;font-weight:700">
                ● 7/7 AI Agents Active
            </div>
            <div style="background:#1E1E28;border:1px solid rgba(255,255,255,0.08);
                        border-radius:8px;padding:6px 14px;font-size:0.72rem;font-weight:600">
                👤 Rishi Rajput &nbsp;<span style="color:#C9A227">Founder</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── STAT CARDS ──
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("👥 Total Leads", "128", "+18% This Week", delta_color="normal")
    with c2:
        st.metric("🔥 Hot Leads", "42", "+12% This Week", delta_color="normal")
    with c3:
        st.metric("📅 Site Visits Today", "8", "+5 This Week", delta_color="normal")
    with c4:
        st.metric("🤝 Deals in Progress", "24", "+8% This Week", delta_color="normal")
    with c5:
        st.metric("💰 Expected Revenue", "₹48.6L", "+15% This Month", delta_color="normal")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── ROW 2: FUNNEL + CHARTS ──
    col_left, col_right = st.columns([1, 1.7])

    with col_left:
        st.markdown('<div class="card"><div class="card-title">🔻 Lead Funnel</div><div class="card-sub">Conversion pipeline overview</div>', unsafe_allow_html=True)
        fig_funnel = funnel_chart(
            ["New Leads", "Contacted", "Qualified", "Site Visit", "Proposal", "Closed"],
            [128, 82, 58, 32, 18, 9],
            [GOLD, BLUE, PURPLE, TEAL, ORANGE, GREEN]
        )
        st.plotly_chart(fig_funnel, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="card"><div class="card-title">📈 Leads Overview</div><div class="card-sub">Daily lead activity</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["📅 This Week", "📆 This Month", "📊 Comparison"])
        with tab1:
            st.plotly_chart(gold_line_chart(WEEK_DATES, WEEK_LEADS), use_container_width=True, config={"displayModeBar": False})
        with tab2:
            st.plotly_chart(gold_line_chart(MONTH_WEEKS, MONTH_LEADS), use_container_width=True, config={"displayModeBar": False})
        with tab3:
            fig_comp = multi_line_chart(WEEK_DATES, [
                {"y": WEEK_LEADS, "name": "Leads", "color": GOLD, "fill": True, "fillcolor": "rgba(201,162,39,0.06)"},
                {"y": [v*3 for v in WEEK_VISITS], "name": "Visits×3", "color": TEAL},
                {"y": [v*15 for v in WEEK_DEALS], "name": "Deals×15", "color": GREEN},
            ])
            st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── ROW 3: DONUTS + TABLE ──
    d1, d2, d3 = st.columns([1, 1, 1.6])

    with d1:
        st.markdown('<div class="card"><div class="card-title">📍 Top Locations</div></div>', unsafe_allow_html=True)
        fig_loc = donut_chart(
            ["Bopal", "Prahlad Nagar", "Gota", "Shela", "Others"],
            [32, 24, 18, 14, 12],
            [GOLD, BLUE, PURPLE, TEAL, "#555"]
        )
        st.plotly_chart(fig_loc, use_container_width=True, config={"displayModeBar": False})

    with d2:
        st.markdown('<div class="card"><div class="card-title">🏠 Property Type Demand</div></div>', unsafe_allow_html=True)
        fig_prop = donut_chart(
            ["2 BHK", "3 BHK", "4 BHK", "Penthouse", "Commercial"],
            [45, 35, 12, 5, 3],
            [GOLD, BLUE, PURPLE, TEAL, "#555"]
        )
        st.plotly_chart(fig_prop, use_container_width=True, config={"displayModeBar": False})

    with d3:
        st.markdown('<div class="card"><div class="card-title">👥 Recent Leads</div>', unsafe_allow_html=True)

        # Table header
        st.markdown("""
        <div style="display:grid;grid-template-columns:130px 100px 60px 65px 55px 65px;
                    gap:8px;padding:6px 14px;font-size:0.58rem;color:#888;
                    text-transform:uppercase;letter-spacing:0.1em;font-weight:700">
            <div>Name</div><div>Location</div><div>Req.</div><div>Budget</div><div>Score</div><div>Status</div>
        </div>
        """, unsafe_allow_html=True)

        for _, row in LEADS_DATA.head(5).iterrows():
            score_class = "score-hot" if row["Score"] >= 80 else ("score-warm" if row["Score"] >= 55 else "score-cold")
            status_class = f"status-{row['Status'].lower()}"
            st.markdown(f"""
            <div class="lead-row">
                <div style="font-weight:600;color:#fff">👤 {row['Name']}</div>
                <div style="color:#888">{row['Location']}</div>
                <div style="color:#fff">{row['Requirement']}</div>
                <div style="color:#C9A227;font-weight:700">{row['Budget']}</div>
                <div><span class="{score_class}">{row['Score']}</span></div>
                <div><span class="{status_class}">{row['Status']}</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── ROW 4: SCHEDULE + PROPERTY + LEADS SOURCE ──
    r4a, r4b, r4c = st.columns([1.2, 1, 1])

    with r4a:
        today_str = now.strftime("%A, %d %B %Y")
        st.markdown(f'<div class="card"><div class="card-title">📅 Today\'s Schedule</div><div class="card-sub">{today_str}</div>', unsafe_allow_html=True)
        for s in SCHEDULE_TODAY:
            st.markdown(f"""
            <div class="sched-item">
                <div class="sched-time">{s['time']}</div>
                <div>
                    <div class="sched-title">{s['title']}</div>
                    <div class="sched-loc">{s['loc']}</div>
                    <div style="font-size:0.6rem;color:#C9A227;margin-top:3px;font-weight:600">With: {s['with']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r4b:
        st.markdown('<div class="card"><div class="card-title">🏠 Featured Properties</div>', unsafe_allow_html=True)
        for p in PROPERTIES[:3]:
            status_colors = {"Hot": ROSE, "New": TEAL, "Available": GREEN, "Premium": GOLD}
            color = status_colors.get(p["status"], GOLD)
            st.markdown(f"""
            <div style="background:#252530;border:1px solid rgba(255,255,255,0.06);
                        border-radius:8px;padding:12px;margin-bottom:8px;
                        border-left:3px solid {color};cursor:pointer;transition:all 0.25s">
                <div style="display:flex;justify-content:space-between;align-items:start">
                    <div>
                        <div style="font-size:0.76rem;font-weight:700;color:#fff">{p['name']}</div>
                        <div style="font-size:0.62rem;color:#888;margin-top:2px">📍 {p['loc']}</div>
                    </div>
                    <div style="background:{color};color:#000;font-size:0.55rem;font-weight:800;
                                padding:3px 8px;border-radius:12px">{p['status']}</div>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px">
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:1rem;
                                font-weight:800;color:#C9A227">{p['price']}</div>
                    <div style="font-size:0.6rem;color:#888">
                        {'🛏 '+str(p['bed'])+' Beds · ' if p['bed'] else ''}🚿 {p['bath']} Bath · 📐 {p['area']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r4c:
        st.markdown('<div class="card"><div class="card-title">📡 Leads by Source</div>', unsafe_allow_html=True)
        fig_src = bar_chart(
            ["Website", "WhatsApp", "Walk-in", "Call", "Referral"],
            [38, 32, 15, 10, 5],
            color=[GOLD, TEAL, BLUE, PURPLE, GREEN],
            horizontal=True
        )
        st.plotly_chart(fig_src, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── AI AGENTS ──
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.7rem;font-weight:700;color:#C9A227;
                letter-spacing:0.18em;text-transform:uppercase;margin-bottom:14px">
        🤖 AI Agents — 7/7 Active
    </div>
    """, unsafe_allow_html=True)

    agent_cols = st.columns(7)
    for i, agent in enumerate(AI_AGENTS):
        with agent_cols[i]:
            st.markdown(f"""
            <div class="agent-card" style="flex-direction:column;text-align:center;padding:16px 10px">
                <div style="font-size:1.8rem;margin-bottom:8px;background:{agent['bg']};
                            width:48px;height:48px;border-radius:10px;
                            display:flex;align-items:center;justify-content:center;margin:0 auto 10px">
                    {agent['icon']}
                </div>
                <div class="agent-name" style="font-size:0.7rem;margin-bottom:4px">{agent['name']}</div>
                <div class="agent-desc" style="font-size:0.58rem">{agent['desc']}</div>
                <div style="margin-top:8px;background:rgba(6,214,160,0.1);
                            border:1px solid rgba(6,214,160,0.2);border-radius:20px;
                            padding:3px 10px;font-size:0.58rem;color:#06D6A0;font-weight:700">
                    ● Active · {agent['tasks']} tasks
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── BOTTOM QUOTE ──
    st.markdown("""
    <div class="quote-bar" style="margin-top:16px">
        <strong>"</strong> Great things in business are never done by one person.
        They're done by a team of people.
        <span style="font-family:'Brush Script MT',cursive;font-size:1.1rem;color:#C9A227;margin-left:8px">Steve Jobs</span>
        <div style="margin-left:auto;display:flex;align-items:center;gap:12px">
            <div style="background:#1E1E28;border:1px solid rgba(255,255,255,0.08);
                        border-radius:8px;padding:8px 14px;display:flex;align-items:center;gap:8px">
                <span style="font-size:1.2rem">🌤</span>
                <div>
                    <div style="font-size:0.62rem;color:#888">Ahmedabad, IN</div>
                    <div style="font-size:0.95rem;font-weight:700;color:#fff">29°C <span style="font-size:0.6rem;color:#888">Haze</span></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: AI AGENTS (DEDICATED)
# ─────────────────────────────────────────────
elif st.session_state.page == "AI Agents":
    st.markdown("""
    <div style="padding:20px 0 16px">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700;color:#fff">
            🤖 AI Agents <span style="color:#C9A227">Command Center</span>
        </div>
        <div style="font-size:0.7rem;color:#888;margin-top:4px">
            7 specialized AI agents working 24/7 to grow your real estate business
        </div>
    </div>
    """, unsafe_allow_html=True)

    for i, agent in enumerate(AI_AGENTS):
        with st.expander(f"{agent['icon']} {agent['name']} — {agent['tasks']} tasks active", expanded=(i==0)):
            cols = st.columns([1, 2, 1])
            with cols[0]:
                st.markdown(f"""
                <div style="background:{agent['bg']};border:1px solid rgba(201,162,39,0.15);
                            border-radius:12px;padding:24px;text-align:center">
                    <div style="font-size:3rem;margin-bottom:12px">{agent['icon']}</div>
                    <div style="font-size:0.9rem;font-weight:700;color:#fff;margin-bottom:6px">{agent['name']}</div>
                    <div style="background:rgba(6,214,160,0.12);border:1px solid rgba(6,214,160,0.25);
                                border-radius:20px;padding:5px 14px;font-size:0.65rem;color:#06D6A0;font-weight:700">
                        ● ACTIVE — Running
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"""
                <div style="padding:0 16px">
                    <div style="font-size:0.7rem;color:#C9A227;letter-spacing:0.12em;text-transform:uppercase;
                                font-weight:700;margin-bottom:10px">Agent Description</div>
                    <div style="font-size:0.82rem;color:rgba(255,255,255,0.7);line-height:1.7;margin-bottom:16px">
                        {agent['desc']}. This AI agent operates 24/7, processing requests in real-time and
                        automating repetitive tasks so your team can focus on closing deals.
                    </div>
                    <div style="font-size:0.7rem;color:#C9A227;letter-spacing:0.12em;text-transform:uppercase;
                                font-weight:700;margin-bottom:10px">Current Tasks</div>
                    <div style="font-size:0.78rem;color:rgba(255,255,255,0.6);line-height:1.8">
                        ✅ Processing {agent['tasks']} active tasks<br>
                        ✅ Connected to CRM database<br>
                        ✅ WhatsApp & Email integration active<br>
                        ✅ Last action: {random.randint(1,15)} minutes ago
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with cols[2]:
                st.metric("Tasks Today", agent["tasks"], f"+{random.randint(1,5)} vs yesterday")
                st.metric("Accuracy", f"{random.randint(94,99)}%", "+2% this week")
                st.metric("Response Time", f"{random.randint(1,5)}s", "-0.5s improved")
                if st.button(f"Configure {agent['name'].split()[0]}", key=f"cfg_{i}"):
                    st.success(f"✅ Opening {agent['name']} configuration...")

# ─────────────────────────────────────────────
# PAGE: LEADS
# ─────────────────────────────────────────────
elif st.session_state.page == "Leads":

    real_count = len(LEADS_DATA)
    hot_count = len(LEADS_DATA[LEADS_DATA["Status"] == "Hot"]) if not LEADS_DATA.empty else 0

    st.markdown(f"""
    <div style="padding:20px 0 16px;display:flex;justify-content:space-between;align-items:center">
        <div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700;color:#fff">
                👥 Leads <span style="color:#C9A227">Management</span>
            </div>
            <div style="font-size:0.7rem;color:#888;margin-top:4px">
                {real_count} total leads · {hot_count} hot
            </div>
        </div>
        {"<div style='background:rgba(6,214,160,0.1);border:1px solid rgba(6,214,160,0.3);border-radius:20px;padding:6px 16px;font-size:0.65rem;color:#06D6A0;font-weight:700'>🌐 Live from Website</div>" if real_count > 0 else ""}
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Refresh Leads", use_container_width=False):
        st.rerun()

    def render_lead_row(row, show_phone=False):
        score_color = GREEN if int(row["Score"]) >= 80 else (GOLD if int(row["Score"]) >= 55 else "#555")
        status_colors = {"Hot": ROSE, "Warm": GOLD, "Cold": "#555"}
        scolor = status_colors.get(row["Status"], GOLD)
        phone_html = f'<div style="color:#2EC4B6;font-size:0.68rem">📞 {row.get("Phone","")}</div>' if show_phone and row.get("Phone") else ""
        email_html = f'<div style="color:#888;font-size:0.62rem">✉️ {row.get("Email","")}</div>' if show_phone and row.get("Email") else ""
        msg_html = f'<div style="color:#888;font-size:0.62rem;margin-top:4px">💬 {row.get("Message","")[:60]}...</div>' if show_phone and row.get("Message") else ""
        st.markdown(f"""
        <div style="background:#1E1E28;border:1px solid rgba(255,255,255,0.06);border-radius:10px;
                    padding:14px 18px;margin-bottom:8px;transition:all 0.25s">
            <div style="display:grid;grid-template-columns:160px 100px 80px 80px 55px 80px 90px 1fr;
                        align-items:center;gap:12px">
                <div style="font-weight:700;color:#fff;font-size:0.8rem">👤 {row['Name']}</div>
                <div style="color:#888;font-size:0.74rem">📍 {row['Location']}</div>
                <div style="color:#fff;font-size:0.74rem">{row['Requirement']}</div>
                <div style="color:#C9A227;font-weight:700;font-size:0.8rem">{row['Budget']}</div>
                <div style="background:{score_color};color:#000;font-size:0.62rem;font-weight:800;
                            padding:3px 8px;border-radius:12px;text-align:center">{row['Score']}</div>
                <div style="background:rgba(201,162,39,0.1);color:#C9A227;font-size:0.62rem;
                            padding:3px 8px;border-radius:12px;text-align:center">{row['Source']}</div>
                <div style="background:{scolor}22;color:{scolor};border:1px solid {scolor}44;
                            font-size:0.6rem;font-weight:700;padding:3px 8px;border-radius:12px;text-align:center">
                    {row['Status']}
                </div>
                <div style="color:#555;font-size:0.62rem">{row['Date']}</div>
            </div>
            {phone_html}{email_html}{msg_html}
        </div>
        """, unsafe_allow_html=True)

    if LEADS_DATA.empty:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px">
            <div style="font-size:3rem;margin-bottom:16px">🌐</div>
            <div style="font-size:1rem;font-weight:700;color:#fff;margin-bottom:8px">No Leads Yet</div>
            <div style="font-size:0.82rem;color:#888;max-width:360px;margin:0 auto;line-height:1.7">
                When someone fills the contact form on your website,
                their lead will appear here automatically in real-time.
            </div>
            <div style="margin-top:20px;background:rgba(201,162,39,0.08);border:1px solid rgba(201,162,39,0.2);
                        border-radius:10px;padding:14px 24px;font-size:0.78rem;color:#C9A227;display:inline-block">
                Make sure api.py is running so leads get captured
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        f1, f2, f3 = st.columns(3)
        with f1:
            status_filter = st.selectbox("Filter by Status", ["All", "Hot", "Warm", "Cold"])
        with f2:
            sort_by = st.selectbox("Sort by", ["Score (High)", "Score (Low)", "Name", "Date"])
        with f3:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

        df = LEADS_DATA.copy()
        if status_filter != "All":
            df = df[df["Status"] == status_filter]
        if "High" in sort_by:
            df = df.sort_values("Score", ascending=False)
        elif "Low" in sort_by:
            df = df.sort_values("Score", ascending=True)
        elif "Name" in sort_by:
            df = df.sort_values("Name")
        elif "Date" in sort_by:
            df = df.sort_values("Date", ascending=False)

        st.markdown(f"<div style='font-size:0.7rem;color:#888;margin-bottom:10px'>Showing {len(df)} leads</div>", unsafe_allow_html=True)
        for _, row in df.iterrows():
            render_lead_row(row, show_phone=True)

# ─────────────────────────────────────────────
# PAGE: PROPERTIES
# ─────────────────────────────────────────────
elif st.session_state.page == "Properties":
    st.markdown("""
    <div style="padding:20px 0 16px">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700;color:#fff">
            🏠 Properties <span style="color:#C9A227">Inventory</span>
        </div>
        <div style="font-size:0.7rem;color:#888;margin-top:4px">Manage all your property listings</div>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        if st.button("➕ Add Property", use_container_width=True):
            st.success("✅ Opening Add Property form...")
    with p2:
        prop_type = st.selectbox("Type", ["All Types", "Apartment", "Villa", "Plot", "Commercial"])
    with p3:
        budget_range = st.selectbox("Budget", ["Any Budget", "Under ₹50L", "₹50L–₹1Cr", "₹1Cr+"])

    for p in PROPERTIES:
        status_colors = {"Hot": ROSE, "New": TEAL, "Available": GREEN, "Premium": GOLD}
        color = status_colors.get(p["status"], GOLD)
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"""
            <div style="background:#1E1E28;border:1px solid rgba(255,255,255,0.06);
                        border-left:4px solid {color};border-radius:10px;padding:18px;margin-bottom:10px">
                <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:10px">
                    <div>
                        <div style="font-size:0.95rem;font-weight:700;color:#fff">{p['name']}</div>
                        <div style="font-size:0.7rem;color:#888;margin-top:3px">📍 {p['loc']}</div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.3rem;
                                    font-weight:800;color:#C9A227">{p['price']}</div>
                        <div style="background:{color};color:#000;font-size:0.58rem;font-weight:800;
                                    padding:3px 8px;border-radius:12px;margin-top:4px;display:inline-block">
                            {p['status']}
                        </div>
                    </div>
                </div>
                <div style="display:flex;gap:16px;font-size:0.7rem;color:#888">
                    {'<span>🛏 '+str(p["bed"])+' Beds</span>' if p["bed"] else ''}
                    <span>🚿 {p['bath']} Baths</span>
                    <span>📐 {p['area']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: REPORTS
# ─────────────────────────────────────────────
elif st.session_state.page == "Reports":
    st.markdown("""
    <div style="padding:20px 0 16px">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700;color:#fff">
            📈 Reports & <span style="color:#C9A227">Analytics</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_r1, tab_r2, tab_r3 = st.tabs(["📊 Lead Analytics", "💰 Revenue", "🏠 Property Performance"])

    with tab_r1:
        rc1, rc2 = st.columns(2)
        with rc1:
            st.markdown('<div class="card-title">Weekly Lead Trend</div>', unsafe_allow_html=True)
            st.plotly_chart(gold_line_chart(WEEK_DATES, WEEK_LEADS), use_container_width=True, config={"displayModeBar": False})
        with rc2:
            st.markdown('<div class="card-title">Leads by Source</div>', unsafe_allow_html=True)
            fig_src2 = bar_chart(["Website", "WhatsApp", "Walk-in", "Call", "Referral"], [38, 32, 15, 10, 5], color=GOLD)
            st.plotly_chart(fig_src2, use_container_width=True, config={"displayModeBar": False})

    with tab_r2:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
        revenue = [28, 35, 42, 38, 55, 48, 62]
        st.plotly_chart(gold_line_chart(months, revenue), use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:16px">
        """, unsafe_allow_html=True)
        rev_stats = [("Total Revenue YTD", "₹3.08Cr", "+22%"), ("Avg Deal Size", "₹85L", "+8%"), ("Best Month", "Jul — ₹62L", "🏆"), ("Target Achievement", "87%", "On Track")]
        cols = st.columns(4)
        for i, (label, val, trend) in enumerate(rev_stats):
            with cols[i]:
                st.metric(label, val, trend)

    with tab_r3:
        prop_names = [p["name"] for p in PROPERTIES]
        views = [random.randint(50, 300) for _ in PROPERTIES]
        inquiries = [random.randint(5, 40) for _ in PROPERTIES]
        fig_pp = go.Figure()
        fig_pp.add_trace(go.Bar(name="Views", x=prop_names, y=views, marker_color=GOLD, opacity=0.8))
        fig_pp.add_trace(go.Bar(name="Inquiries", x=prop_names, y=inquiries, marker_color=TEAL, opacity=0.8))
        pp_layout = dict(CHART_LAYOUT)
        pp_layout["showlegend"] = True
        fig_pp.update_layout(**pp_layout, height=280, barmode="group",
                             legend=dict(orientation="h", y=1.1, font=dict(size=9, color="rgba(255,255,255,0.6)")))
        st.plotly_chart(fig_pp, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# PAGE: DEALS
# ─────────────────────────────────────────────
elif st.session_state.page == "Deals":
    st.markdown("""
    <div style="padding:20px 0 16px">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700;color:#fff">
            💼 Deals <span style="color:#C9A227">Pipeline</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    stages = ["Negotiation", "Documentation", "Site Visit Done", "Loan Processing", "Closing"]
    stage_cols = st.columns(5)
    deals = [
        {"name": "Amit Shah", "prop": "3BHK Bopal", "val": "₹80L", "stage": 0, "days": 3},
        {"name": "Neha Patel", "prop": "2BHK Prahlad Nagar", "val": "₹55L", "stage": 1, "days": 7},
        {"name": "Krunal Desai", "prop": "3BHK Gota", "val": "₹70L", "stage": 2, "days": 12},
        {"name": "Dhruv Joshi", "prop": "4BHK Shela", "val": "₹1.2Cr", "stage": 3, "days": 18},
        {"name": "Rohan Mehta", "prop": "3BHK Satellite", "val": "₹95L", "stage": 4, "days": 25},
    ]
    stage_colors = [BLUE, PURPLE, TEAL, ORANGE, GREEN]
    for i, (stage, col) in enumerate(zip(stages, stage_cols)):
        with col:
            st.markdown(f"""
            <div style="background:#1E1E28;border:1px solid rgba(255,255,255,0.06);
                        border-top:3px solid {stage_colors[i]};border-radius:10px;padding:12px;margin-bottom:8px">
                <div style="font-size:0.65rem;font-weight:700;color:{stage_colors[i]};
                            text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px">{stage}</div>
            """, unsafe_allow_html=True)
            stage_deals = [d for d in deals if d["stage"] == i]
            for d in stage_deals:
                st.markdown(f"""
                <div style="background:#252530;border:1px solid rgba(255,255,255,0.06);
                            border-radius:8px;padding:10px;margin-bottom:6px">
                    <div style="font-size:0.74rem;font-weight:700;color:#fff">{d['name']}</div>
                    <div style="font-size:0.62rem;color:#888;margin:2px 0">{d['prop']}</div>
                    <div style="font-size:0.8rem;font-weight:800;color:#C9A227">{d['val']}</div>
                    <div style="font-size:0.58rem;color:#555;margin-top:4px">Day {d['days']} in pipeline</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: APPOINTMENTS
# ─────────────────────────────────────────────
elif st.session_state.page == "Appointments":
    st.markdown("""
    <div style="padding:20px 0 16px">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700;color:#fff">
            📅 Appointments <span style="color:#C9A227">Calendar</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("➕ Schedule New Appointment", use_container_width=False):
        st.success("✅ Opening appointment scheduler...")

    st.markdown("<div style='font-size:0.7rem;color:#C9A227;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;margin:16px 0 10px'>Today\'s Appointments</div>", unsafe_allow_html=True)
    for s in SCHEDULE_TODAY:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"""
            <div class="sched-item">
                <div class="sched-time">{s['time']}</div>
                <div style="flex:1">
                    <div class="sched-title">{s['title']}</div>
                    <div class="sched-loc">{s['loc']}</div>
                    <div style="font-size:0.62rem;color:#C9A227;margin-top:3px;font-weight:600">With: {s['with']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            if st.button("✅ Mark Done", key=f"done_{s['time']}"):
                st.success(f"Marked: {s['title']}")

# ─────────────────────────────────────────────
# OTHER PAGES — PLACEHOLDER
# ─────────────────────────────────────────────
elif st.session_state.page in ["Clients", "Tasks", "Marketing", "Settings"]:
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                height:60vh;text-align:center">
        <div style="font-size:4rem;margin-bottom:20px">🚀</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.6rem;font-weight:700;color:#fff;margin-bottom:10px">
            {st.session_state.page} <span style="color:#C9A227">Module</span>
        </div>
        <div style="font-size:0.9rem;color:#888;max-width:400px;line-height:1.7">
            This module is ready to be connected to your live data.<br>
            Contact RR Elevate team to activate full features.
        </div>
        <div style="margin-top:24px;background:rgba(201,162,39,0.1);border:1px solid rgba(201,162,39,0.25);
                    border-radius:10px;padding:16px 28px;font-size:0.8rem;color:#C9A227">
            📞 +91 98765 43210 &nbsp;·&nbsp; hello@rrelevate.in
        </div>
    </div>
    """, unsafe_allow_html=True)
