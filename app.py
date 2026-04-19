import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import streamlit.components.v1 as components
import os
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="NEXOPORT v3 — Enterprise Trade Intelligence",
    layout="wide",
    page_icon="🌐",
    initial_sidebar_state="expanded",
)

# =========================
# ENV SECURITY
# =========================
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
GMAP_KEY   = os.getenv("GMAP_KEY", "")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# =========================
# DATA LAYER
# =========================
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Shipment_ID": ["EXP-101","IMP-202","EXP-103","IMP-304","EXP-405","IMP-506","EXP-607"],
        "Destination": ["Poland","Bangladesh","Germany","USA","Japan","France","UK"],
        "Value_USD":   [25000,12000,45000,33000,18500,61000,29000],
        "Status":      ["In Transit","Delivered","Delayed","In Transit","Delivered","In Transit","Delayed"],
        "Carrier":     ["DHL","FedEx","UPS","Maersk","DHL","UPS","FedEx"],
        "ETA_Days":    [3,0,7,5,0,2,9],
        "Lat":         [52.2297,23.8103,52.5200,40.7128,35.6762,48.8566,51.5074],
        "Lon":         [21.0122,90.4125,13.4050,-74.0060,139.6503,2.3522,-0.1278],
    })

df = load_data()

# =========================
# SESSION STATE
# =========================
defaults = {
    "auth": False,
    "role": None,
    "page": "dashboard",
    "chat": [],
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================
# AI ENGINE (RAG v3)
# =========================
def rag_engine(question):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")

        context = df.to_string()
        history = "\n".join(
            [f"Q:{c['q']} A:{c['a']}" for c in st.session_state.chat[-7:]]
        )

        prompt = f"""
You are NEXOPORT AI — a logistics intelligence system.

RULES:
- Use shipment data only
- Mention Shipment_ID when possible
- Be precise and analytical

DATA:
{context}

HISTORY:
{history}

QUESTION:
{question}
"""
        return model.generate_content(prompt).text

    except Exception as e:
        return f"AI Error: {str(e)}"

# =========================
# METRICS ENGINE
# =========================
def metrics():
    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Shipments", len(df))
    c2.metric("Delivered", len(df[df.Status=="Delivered"]))
    c3.metric("In Transit", len(df[df.Status=="In Transit"]))
    c4.metric("Delayed", len(df[df.Status=="Delayed"]))

# =========================
# DASHBOARD
# =========================
def dashboard():
    st.title("📊 Global Trade Intelligence Dashboard")

    metrics()

    col1,col2 = st.columns(2)

    with col1:
        fig = px.bar(df, x="Destination", y="Value_USD", color="Status",
                     title="Cargo Value by Destination")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(df, names="Status", title="Shipment Status Distribution")
        st.plotly_chart(fig2, use_container_width=True)

# =========================
# AI CHAT
# =========================
def ai_chat():
    st.title("🤖 AI Logistics Assistant v3")

    for c in st.session_state.chat:
        st.markdown(f"**🧑 You:** {c['q']}")
        st.markdown(f"**🤖 AI:** {c['a']}")

    q = st.text_input("Ask about shipments, risk, carriers...")

    col1,col2 = st.columns([1,5])

    with col1:
        send = st.button("Send")

    if send and q:
        ans = rag_engine(q)
        st.session_state.chat.append({"q": q, "a": ans})
        st.rerun()

    if st.button("Clear Chat"):
        st.session_state.chat = []
        st.rerun()

# =========================
# MAP ENGINE (CLEAN)
# =========================
def map_view():
    st.title("🗺 Global Shipment Tracking")

    markers = []
    for _,r in df.iterrows():
        markers.append({
            "lat": r["Lat"],
            "lng": r["Lon"],
            "id": r["Shipment_ID"],
            "status": r["Status"]
        })

    html = f"""
    <html>
    <head>
    <script src="https://maps.googleapis.com/maps/api/js?key={GMAP_KEY}"></script>
    </head>
    <body>
    <div id="map" style="height:520px;"></div>

    <script>
    function initMap(){{
        var map = new google.maps.Map(document.getElementById('map'), {{
            zoom:2,
            center: {{lat:20, lng:0}}
        }});

        var data = {markers};

        data.forEach(m => {{
            new google.maps.Marker({{
                position: {{lat:m.lat,lng:m.lng}},
                map: map,
                title: m.id
            }});
        }});
    }}
    initMap();
    </script>
    </body>
    </html>
    """

    components.html(html, height=540)

# =========================
# DATA CONTROL PANEL
# =========================
def data_panel():
    st.title("📋 Data Control Center")

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Export Data",
        df.to_csv(index=False).encode(),
        "nexoport_v3.csv",
        "text/csv"
    )

# =========================
# LOGIN SYSTEM
# =========================
def login():
    st.title("🌐 NEXOPORT v3 LOGIN")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "admin123":
            st.session_state.auth = True
            st.session_state.role = "Admin"
            st.rerun()

        elif u == "user" and p == "user123":
            st.session_state.auth = True
            st.session_state.role = "User"
            st.rerun()
        else:
            st.error("Invalid credentials")

# =========================
# SIDEBAR ROUTER
# =========================
def sidebar():
    st.sidebar.title("NEXOPORT v3")

    if st.session_state.role == "Admin":
        if st.sidebar.button("📊 Dashboard"):
            st.session_state.page = "dashboard"
        if st.sidebar.button("🤖 AI Assistant"):
            st.session_state.page = "ai"
        if st.sidebar.button("📋 Data"):
            st.session_state.page = "data"

    else:
        if st.sidebar.button("🗺 Live Map"):
            st.session_state.page = "map"

    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# =========================
# MAIN ROUTER
# =========================
def main():
    sidebar()

    if st.session_state.role == "Admin":
        if st.session_state.page == "dashboard":
            dashboard()
        elif st.session_state.page == "ai":
            ai_chat()
        elif st.session_state.page == "data":
            data_panel()

    else:
        if st.session_state.page == "map":
            map_view()

# =========================
# RUN APP
# =========================
if not st.session_state.auth:
    login()
else:
    main()
