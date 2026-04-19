import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
import streamlit.components.v1 as components

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NEXOPORT — Global Trade Intelligence",
    layout="wide",
    page_icon="🌐",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  FLAG COLOR PALETTE
#  BD  🇧🇩 : #006A4E (green)  #F42A41 (red)
#  PS  🇵🇸 : #000000 (black)  #009736 (green)  #EF3340 (red)
#  USA 🇺🇸 : #B22234 (red)   #3C3B6E (blue)
#  IRN 🇮🇷 : #239F40 (green)  #DA0000 (red)
#  UK  🇬🇧 : #012169 (blue)   #CF142B (red)
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800&display=swap');

:root {
  --bg:      #03080f;
  --surface: #080f1c;
  --card:    #0c1525;
  --card2:   #0f1d31;
  --border:  #162440;
  --red1:    #F42A41;
  --red2:    #EF3340;
  --red3:    #CF142B;
  --red4:    #B22234;
  --grn1:    #006A4E;
  --grn2:    #009736;
  --grn3:    #239F40;
  --blu1:    #3C3B6E;
  --blu2:    #012169;
  --text:    #eef2ff;
  --muted:   #5a7294;
  --dim:     #2a3f5f;
}
html, body, .stApp {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Outfit', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.4rem 2rem !important; max-width: 100% !important; }

/* Rainbow flag top bar */
.stApp::before {
  content: '';
  display: block;
  position: fixed;
  top: 0; left: 0; right: 0; height: 3px; z-index: 9999;
  background: linear-gradient(90deg,
    #F42A41 0%, #006A4E 14%, #EF3340 28%, #000 35%,
    #009736 42%, #B22234 56%, #3C3B6E 70%,
    #DA0000 78%, #239F40 86%, #CF142B 92%, #012169 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebarNav"] { display: none; }

/* Cards */
.nx-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1rem;
}

/* Metric cards */
.metric-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.25rem 1.4rem;
  position: relative; overflow: hidden;
}
.metric-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--red1), var(--grn2));
}
.metric-card.red::before   { background: linear-gradient(90deg,#F42A41,#CF142B); }
.metric-card.green::before { background: linear-gradient(90deg,#006A4E,#239F40); }
.metric-card.blue::before  { background: linear-gradient(90deg,#012169,#3C3B6E); }
.metric-card.gold::before  { background: linear-gradient(90deg,#d97706,#f59e0b); }
.metric-label { font-size:.72rem; color:var(--muted); text-transform:uppercase;
                letter-spacing:.1em; font-weight:600; }
.metric-value { font-family:'Bebas Neue',sans-serif; font-size:2.4rem; letter-spacing:.04em;
                color:var(--text); margin:.15rem 0 .1rem; line-height:1; }
.metric-sub   { font-size:.76rem; font-weight:500; }

/* Page header */
.page-header {
  display:flex; align-items:center; gap:1rem;
  margin-bottom:1.8rem; padding-bottom:1rem;
  border-bottom:1px solid var(--border);
}
.page-header h1 {
  font-family:'Bebas Neue',sans-serif;
  font-size:2.2rem; letter-spacing:.06em;
  background: linear-gradient(135deg,#F42A41 0%,#ff6b35 40%,#239F40 70%,#3C3B6E 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  margin:0;
}
.hbadge {
  padding:.28rem .85rem; border-radius:999px;
  font-size:.72rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase;
}
.hbadge-admin { background:rgba(244,42,65,.12); border:1px solid rgba(244,42,65,.35); color:#F42A41; }
.hbadge-user  { background:rgba(35,159,64,.12); border:1px solid rgba(35,159,64,.35); color:#239F40; }

/* Buttons */
div.stButton > button {
  background: linear-gradient(135deg,#F42A41,#CF142B) !important;
  color:#fff !important; border:none !important;
  border-radius:10px !important; font-weight:700 !important;
  font-family:'Outfit',sans-serif !important;
  padding:.5rem 1.4rem !important;
  letter-spacing:.02em !important;
  transition: all .2s !important;
}
div.stButton > button:hover { opacity:.82 !important; }
.logout-btn div.stButton > button {
  background:rgba(244,42,65,.1) !important;
  color:#F42A41 !important;
  border:1px solid rgba(244,42,65,.3) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea textarea {
  background:var(--card2) !important; border:1px solid var(--border) !important;
  border-radius:10px !important; color:var(--text) !important;
  font-family:'Outfit',sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
  border-color:var(--red1) !important;
  box-shadow:0 0 0 3px rgba(244,42,65,.12) !important;
}

/* Tabs */
[data-testid="stTabs"] button {
  font-family:'Outfit',sans-serif !important; font-weight:600 !important;
  color:var(--muted) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color:#F42A41 !important; border-bottom:2px solid #F42A41 !important;
}

/* Table / Dataframe */
.stDataFrame, .stTable { border-radius:12px; overflow:hidden; }

/* Chat bubbles */
.chat-user {
  background:rgba(244,42,65,.08); border:1px solid rgba(244,42,65,.18);
  border-radius:14px 14px 2px 14px;
  padding:.85rem 1.1rem; margin:.6rem 0; max-width:84%; margin-left:auto;
}
.chat-ai {
  background:var(--card); border:1px solid var(--border);
  border-radius:14px 14px 14px 2px;
  padding:.85rem 1.1rem; margin:.6rem 0; max-width:90%;
}
.chat-lbl { font-size:.68rem; font-weight:700; text-transform:uppercase;
            letter-spacing:.1em; margin-bottom:.3rem; }

/* Status badges */
.s-transit   { background:rgba(245,158,11,.13); color:#f59e0b; border:1px solid rgba(245,158,11,.28); }
.s-delivered { background:rgba(35,159,64,.13);  color:#239F40; border:1px solid rgba(35,159,64,.28); }
.s-delayed   { background:rgba(244,42,65,.13);  color:#F42A41; border:1px solid rgba(244,42,65,.28); }
.st-badge    { padding:.2rem .7rem; border-radius:999px; font-size:.72rem; font-weight:700; }

/* Login */
.login-outer {
  max-width:430px; margin:5vh auto 0;
  background:var(--card); border:1px solid var(--border);
  border-radius:22px; padding:2.8rem 3rem;
  box-shadow:0 30px 80px rgba(0,0,0,.6);
  position:relative; overflow:hidden;
}
.login-outer::before {
  content:''; position:absolute; top:0; left:0; right:0; height:4px;
  background:linear-gradient(90deg,
    #F42A41,#006A4E,#EF3340,#3C3B6E,#239F40,#CF142B,#012169);
}
.login-brand {
  text-align:center; margin-bottom:.2rem;
  font-family:'Bebas Neue',sans-serif; font-size:3rem; letter-spacing:.12em;
  background:linear-gradient(135deg,#F42A41 0%,#ff6b35 35%,#239F40 65%,#3C3B6E 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.login-sub  { text-align:center; color:var(--muted); font-size:.82rem; margin-bottom:.5rem; }
.flag-row   { text-align:center; font-size:1.35rem; letter-spacing:.3rem; margin-bottom:1.8rem; }

/* Sidebar brand */
.sb-brand {
  font-family:'Bebas Neue',sans-serif; font-size:1.75rem; letter-spacing:.14em;
  background:linear-gradient(135deg,#F42A41,#ff6b35,#239F40);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  text-align:center; margin-bottom:.3rem;
}
.sb-flags { text-align:center; font-size:1.05rem; letter-spacing:.18rem; margin-bottom:.55rem; }
.role-pill {
  text-align:center; padding:.35rem 1rem; border-radius:999px;
  font-size:.72rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; margin-bottom:.9rem;
}
.role-admin { background:rgba(244,42,65,.12); border:1px solid rgba(244,42,65,.3); color:#F42A41; }
.role-user  { background:rgba(35,159,64,.12);  border:1px solid rgba(35,159,64,.3);  color:#239F40; }
.nav-section { font-size:.67rem; text-transform:uppercase; letter-spacing:.1em;
               color:var(--muted); font-weight:700; margin:.8rem 0 .35rem .2rem; }

/* Map wrapper */
.map-outer { border:1px solid var(--border); border-radius:16px; overflow:hidden; }

/* Select */
div[data-baseweb="select"] > div {
  background:var(--card2) !important; border:1px solid var(--border) !important;
  border-radius:10px !important;
}
div[data-baseweb="select"] span { color:var(--text) !important; }
div[data-baseweb="popover"] { background:var(--card2) !important; border:1px solid var(--border) !important; }

.stAlert { border-radius:12px !important; }
.stSpinner > div { border-top-color:#F42A41 !important; }
hr { border-color:var(--border) !important; }
[data-testid="stExpander"] {
  background:var(--card) !important;
  border:1px solid var(--border) !important;
  border-radius:12px !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
GEMINI_KEY = "AIzaSyAnKtF3VIydi5rpQ621TsFKYhq8f756oQA"
GMAP_KEY   = "AQ.Ab8RN6Ks6hOuPdror8yjpazHawSuylGNA9xmDVHEJmjm1t5jCA"
FLAGS      = "🇧🇩 🇵🇸 🇺🇸 🇮🇷 🇬🇧"
BRAND      = "NEXOPORT"
TAGLINE    = "Global Trade Intelligence Platform"

STATUS_COLORS = {
    "Delivered":  "#239F40",
    "In Transit": "#f59e0b",
    "Delayed":    "#F42A41",
}


# ─────────────────────────────────────────────
#  AI / RAG
# ─────────────────────────────────────────────
def get_ai_response(context: str, question: str, history: list) -> str:
    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel("gemini-pro")
        hist_text = "".join(
            [f"User: {t['q']}\nAssistant: {t['a']}\n\n" for t in history[-6:]]
        )
        prompt = f"""You are NEXOPORT's Senior Logistics Intelligence Analyst.
Analyse the live shipment database carefully and give precise, data-driven answers.
Cite specific Shipment IDs and numbers when relevant.

=== LIVE SHIPMENT DATABASE ===
{context}
=== END ===

Previous conversation:
{hist_text}

User question: {question}"""
        return model.generate_content(prompt).text
    except Exception as e:
        return f"AI unavailable: {str(e)}"


# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data_samples.csv")
    except Exception:
        return pd.DataFrame({
            "Shipment_ID": ["EXP-101","IMP-202","EXP-103","IMP-304","EXP-405","IMP-506","EXP-607"],
            "Destination": ["Poland","Bangladesh","Germany","USA","Japan","France","UK"],
            "Value_USD":   [25000, 12000, 45000, 33000, 18500, 61000, 29000],
            "Status":      ["In Transit","Delivered","Delayed","In Transit","Delivered","In Transit","Delayed"],
            "Carrier":     ["DHL","FedEx","UPS","Maersk","DHL","UPS","FedEx"],
            "ETA_Days":    [3, 0, 7, 5, 0, 2, 9],
            "Lat":         [52.2297, 23.8103, 52.5200, 40.7128, 35.6762, 48.8566, 51.5074],
            "Lon":         [21.0122, 90.4125, 13.4050,-74.0060,139.6503,  2.3522, -0.1278],
        })

df = load_data()


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
for k, v in {
    "logged_in":   False,
    "role":        None,
    "rag_history": [],
    "admin_tab":   "analytics",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ═════════════════════════════════════════════
#  LOGIN
# ═════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown(f"""
    <div class="login-outer">
      <div class="login-brand">{BRAND}</div>
      <div class="login-sub">{TAGLINE}</div>
      <div class="flag-row">{FLAGS}</div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.55, 1])
    with col:
        st.markdown('<div style="height:.3rem"></div>', unsafe_allow_html=True)
        username = st.text_input("u", placeholder="Username", label_visibility="collapsed")
        password = st.text_input("p", type="password", placeholder="Password", label_visibility="collapsed")
        st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)
        if st.button("Sign In  ›", use_container_width=True):
            if username == "admin" and password == "eximp123":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.rerun()
            elif username == "user" and password == "user123":
                st.session_state.logged_in = True
                st.session_state.role = "User"
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.markdown("""
        <div style="margin-top:1.4rem;padding:.9rem 1rem;
                    background:rgba(255,255,255,.03);border:1px solid #162440;
                    border-radius:10px;font-size:.76rem;line-height:2;color:#5a7294">
          <span style="color:#94a3b8;font-weight:700">Demo Accounts</span><br>
          🛡️ Admin → admin / eximp123<br>
          📦 User  → user / user123
        </div>
        """, unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────
#  COMPUTED COUNTS
# ─────────────────────────────────────────────
in_transit = len(df[df["Status"] == "In Transit"])
delivered  = len(df[df["Status"] == "Delivered"])
delayed    = len(df[df["Status"] == "Delayed"])


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f'<div class="sb-brand">{BRAND}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sb-flags">{FLAGS}</div>', unsafe_allow_html=True)
    pill_cls = "role-admin" if st.session_state.role == "Admin" else "role-user"
    icon_txt = "🛡️ ADMINISTRATOR" if st.session_state.role == "Admin" else "📦 USER"
    st.markdown(f'<div class="role-pill {pill_cls}">{icon_txt}</div>', unsafe_allow_html=True)
    st.markdown('<hr style="margin:.5rem 0 .8rem">', unsafe_allow_html=True)

    if st.session_state.role == "Admin":
        st.markdown('<div class="nav-section">Navigation</div>', unsafe_allow_html=True)
        if st.button("📊  Analytics Dashboard", use_container_width=True):
            st.session_state.admin_tab = "analytics"; st.rerun()
        st.markdown('<div style="height:.3rem"></div>', unsafe_allow_html=True)
        if st.button("🤖  AI RAG Consultant", use_container_width=True):
            st.session_state.admin_tab = "rag"; st.rerun()
        st.markdown('<div style="height:.3rem"></div>', unsafe_allow_html=True)
        if st.button("📋  Data Manager", use_container_width=True):
            st.session_state.admin_tab = "data"; st.rerun()
    else:
        st.markdown('<div class="nav-section">Navigation</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex;flex-direction:column;gap:.4rem;padding-top:.3rem">
          <div style="display:flex;align-items:center;gap:.6rem;padding:.6rem .9rem;
               background:rgba(35,159,64,.08);border:1px solid rgba(35,159,64,.2);
               border-radius:9px;font-size:.85rem;font-weight:600;color:#239F40">
            📍 Live Tracking Map
          </div>
          <div style="display:flex;align-items:center;gap:.6rem;padding:.6rem .9rem;
               border-radius:9px;font-size:.85rem;color:#5a7294">
            📋 Shipment Status
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr style="margin:.8rem 0">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:.77rem;line-height:2.2">
      <div style="color:#5a7294;font-size:.67rem;font-weight:700;letter-spacing:.08em;
                  text-transform:uppercase;margin-bottom:.3rem">Live Stats</div>
      💰 <span style="color:#8fa8c8">Total Value</span>
         <b style="color:#eef2ff;float:right">${df['Value_USD'].sum():,}</b><br>
      🟡 <span style="color:#8fa8c8">In Transit</span>
         <b style="color:#f59e0b;float:right">{in_transit}</b><br>
      🟢 <span style="color:#8fa8c8">Delivered</span>
         <b style="color:#239F40;float:right">{delivered}</b><br>
      🔴 <span style="color:#8fa8c8">Delayed</span>
         <b style="color:#F42A41;float:right">{delayed}</b>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr style="margin:.8rem 0">', unsafe_allow_html=True)
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("⏻  Sign Out", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center;font-size:.63rem;color:#2a3f5f;margin-top:.8rem">{BRAND} © 2025</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PLOTLY BASE
# ─────────────────────────────────────────────
PL = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Outfit", color="#7a9cc0"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
    margin=dict(t=45, b=35, l=10, r=10),
    xaxis=dict(gridcolor="#162440", linecolor="#162440"),
    yaxis=dict(gridcolor="#162440", linecolor="#162440"),
)
SC = STATUS_COLORS


# ═════════════════════════════════════════════
#  ADMIN PANEL
# ═════════════════════════════════════════════
if st.session_state.role == "Admin":

    active = st.session_state.get("admin_tab", "analytics")
    titles = {
        "analytics": ("📊", "Analytics Dashboard"),
        "rag":        ("🤖", "AI RAG Consultant"),
        "data":       ("📋", "Data Manager"),
    }
    hicon, htitle = titles.get(active, ("🛠️", "Command Center"))

    st.markdown(f"""
    <div class="page-header">
      <span style="font-size:2.2rem">{hicon}</span>
      <div>
        <h1>{htitle}</h1>
        <p style="margin:0;color:#5a7294;font-size:.82rem">
          {FLAGS} &nbsp;·&nbsp; {BRAND} Administrator Command Center
        </p>
      </div>
      <span class="hbadge hbadge-admin" style="margin-left:auto">ADMIN ACCESS</span>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    for col, lbl, val, sub, color, cls in [
        (k1, "Total Cargo Value",  f"${df['Value_USD'].sum():,}", f"↑ {len(df)} shipments",  "#F42A41", "red"),
        (k2, "In Transit",         str(in_transit),               "Active movement",           "#f59e0b", "gold"),
        (k3, "Delayed",            str(delayed),                   "Requires attention",        "#F42A41", "red"),
        (k4, "Delivered",          str(delivered),                 "Successfully completed",    "#239F40", "green"),
    ]:
        col.markdown(f"""
        <div class="metric-card {cls}">
          <div class="metric-label">{lbl}</div>
          <div class="metric-value">{val}</div>
          <div class="metric-sub" style="color:{color}">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:.6rem"></div>', unsafe_allow_html=True)

    # ── ANALYTICS ──
    if active == "analytics":
        st.markdown('<div class="nx-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(df, x="Destination", y="Value_USD", color="Status",
                         color_discrete_map=SC, title="Cargo Value by Destination",
                         labels={"Value_USD":"Value (USD)"}, template="plotly_dark")
            fig.update_layout(**PL)
            fig.update_traces(marker_line_width=0, marker_corner_radius=4)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            sc2 = df["Status"].value_counts().reset_index()
            sc2.columns = ["Status","Count"]
            fig2 = px.pie(sc2, names="Status", values="Count",
                          color="Status", color_discrete_map=SC,
                          title="Status Distribution", hole=.58, template="plotly_dark")
            fig2.update_layout(**PL)
            st.plotly_chart(fig2, use_container_width=True)

        cv = df.groupby("Carrier")["Value_USD"].sum().reset_index()
        fig3 = px.bar(cv, x="Value_USD", y="Carrier", orientation="h",
                      title="Total Value by Carrier",
                      color="Value_USD",
                      color_continuous_scale=["#0f1d31","#F42A41","#f59e0b"],
                      labels={"Value_USD":"USD"}, template="plotly_dark")
        fig3.update_layout(**PL)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── AI RAG ──
    elif active == "rag":
        st.markdown('<div class="nx-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex;align-items:center;gap:.8rem;margin-bottom:1rem">
          <span style="font-size:1.6rem">🤖</span>
          <div>
            <div style="font-weight:700;font-size:1.05rem">AI Logistics Intelligence</div>
            <div style="color:#5a7294;font-size:.78rem">Gemini RAG — live shipment database as context</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.rag_history:
            for turn in st.session_state.rag_history:
                st.markdown(f"""
                <div class="chat-user">
                  <div class="chat-lbl" style="color:#F42A41">You</div>
                  {turn['q']}
                </div>
                <div class="chat-ai">
                  <div class="chat-lbl" style="color:#239F40">NEXOPORT AI</div>
                  {turn['a']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:2.8rem 1rem;color:#2a3f5f">
              <div style="font-size:3rem;margin-bottom:.6rem">💬</div>
              <div style="font-size:.9rem;color:#3d5a80;font-weight:600">Ask your first question</div>
              <div style="font-size:.76rem;color:#2a3f5f;margin-top:.4rem">
                "Which shipments are at risk?" &nbsp;·&nbsp; "Carrier performance summary?"
              </div>
            </div>
            """, unsafe_allow_html=True)

        qc, bc = st.columns([5,1])
        with qc:
            user_q = st.text_input("q2", label_visibility="collapsed",
                                   placeholder="Ask about shipments, risks, routes, carriers…",
                                   key="rag_q")
        with bc:
            send = st.button("Send ›", use_container_width=True)

        cl1, cl2, _ = st.columns([1.2,1.2,5])
        with cl1:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.rag_history = []; st.rerun()

        if send and user_q.strip():
            with st.spinner("🧠 Analysing…"):
                ans = get_ai_response(df.to_string(), user_q, st.session_state.rag_history)
            st.session_state.rag_history.append({"q": user_q, "a": ans})
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("📄 RAG Context — Live Database"):
            st.dataframe(df, use_container_width=True)

    # ── DATA MANAGER ──
    elif active == "data":
        st.markdown('<div class="nx-card">', unsafe_allow_html=True)
        fc1, fc2, _ = st.columns([2,2,3])
        with fc1:
            sf = st.selectbox("Status", ["All"] + df["Status"].unique().tolist())
        with fc2:
            cf = st.selectbox("Carrier", ["All"] + df["Carrier"].unique().tolist())

        filt = df.copy()
        if sf != "All": filt = filt[filt["Status"] == sf]
        if cf != "All": filt = filt[filt["Carrier"] == cf]

        edited = st.data_editor(
            filt, use_container_width=True, num_rows="dynamic",
            column_config={
                "Value_USD": st.column_config.NumberColumn("Value (USD)", format="$%,d"),
                "ETA_Days":  st.column_config.NumberColumn("ETA (Days)"),
                "Lat":       st.column_config.NumberColumn("Latitude",  format="%.4f"),
                "Lon":       st.column_config.NumberColumn("Longitude", format="%.4f"),
            },
        )
        d1, _ = st.columns([2,5])
        with d1:
            st.download_button("⬇ Export CSV",
                edited.to_csv(index=False).encode(),
                "nexoport_export.csv","text/csv",use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════
#  USER PANEL
# ═════════════════════════════════════════════
else:
    st.markdown(f"""
    <div class="page-header">
      <span style="font-size:2.2rem">📍</span>
      <div>
        <h1>Live Shipment Tracker</h1>
        <p style="margin:0;color:#5a7294;font-size:.82rem">
          {FLAGS} &nbsp;·&nbsp; Real-time global cargo tracking
        </p>
      </div>
      <span class="hbadge hbadge-user" style="margin-left:auto">USER VIEW</span>
    </div>
    """, unsafe_allow_html=True)

    u1, u2, u3, u4 = st.columns(4)
    for col, lbl, val, sub, color, cls in [
        (u1, "Total Shipments", str(len(df)),    "All tracked",     "#5a8dee", "blue"),
        (u2, "In Transit",      str(in_transit), "Moving now",       "#f59e0b", "gold"),
        (u3, "Delivered",       str(delivered),  "Completed",        "#239F40", "green"),
        (u4, "Delayed",         str(delayed),    "Needs attention",  "#F42A41", "red"),
    ]:
        col.markdown(f"""
        <div class="metric-card {cls}">
          <div class="metric-label">{lbl}</div>
          <div class="metric-value">{val}</div>
          <div class="metric-sub" style="color:{color}">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:.9rem"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:.7rem;margin-bottom:.7rem">
      <span style="font-size:1.3rem">🗺️</span>
      <span style="font-weight:700;font-size:1.05rem">Live Google Maps — Global Cargo Locations</span>
      <span style="font-size:.72rem;color:#5a7294;margin-left:.2rem">Click markers for details</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Build JS markers ──
    markers_js = ""
    for _, row in df.iterrows():
        sc   = STATUS_COLORS.get(row["Status"], "#888")
        fval = f"${row['Value_USD']:,}"
        eta  = "Arrived ✓" if row["ETA_Days"] == 0 else f"{row['ETA_Days']} days"
        sid  = str(row["Shipment_ID"])
        dest = str(row["Destination"])
        carr = str(row["Carrier"])
        stat = str(row["Status"])

        markers_js += f"""
(function(){{
  var pos={{lat:{row['Lat']},lng:{row['Lon']}}};
  new google.maps.Marker({{
    position:pos,map:map,zIndex:0,
    icon:{{path:google.maps.SymbolPath.CIRCLE,
           fillColor:'{sc}',fillOpacity:.15,
           strokeColor:'{sc}',strokeWeight:1,scale:24}}
  }});
  var m=new google.maps.Marker({{
    position:pos,map:map,title:"{sid}",zIndex:1,
    icon:{{path:google.maps.SymbolPath.CIRCLE,
           fillColor:'{sc}',fillOpacity:1,
           strokeColor:'#ffffff',strokeWeight:2.5,scale:11}}
  }});
  var iw=new google.maps.InfoWindow({{
    content:`<div style="font-family:Outfit,sans-serif;padding:10px 12px;
              min-width:210px;background:#0c1525;border-radius:10px;
              border:1px solid #162440">
      <div style="font-weight:800;font-size:1rem;color:#eef2ff;margin-bottom:4px">{sid}</div>
      <div style="font-size:.8rem;color:#7a9cc0;margin-bottom:7px">🌍 {dest}</div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;font-size:.76rem;margin-bottom:6px">
        <span style="background:rgba(255,255,255,.06);padding:2px 8px;border-radius:6px;color:#c8d8f0">📦 {carr}</span>
        <span style="background:rgba(255,255,255,.06);padding:2px 8px;border-radius:6px;color:#c8d8f0">💰 {fval}</span>
        <span style="background:rgba(255,255,255,.06);padding:2px 8px;border-radius:6px;color:#c8d8f0">⏱ {eta}</span>
      </div>
      <div style="font-size:.76rem;font-weight:700;color:{sc}">● {stat}</div>
    </div>`
  }});
  m.addListener('click',function(){{iw.open(map,m);}});
}})();
"""

    clat = df["Lat"].mean()
    clon = df["Lon"].mean()

    gmap_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{background:#03080f;font-family:'Outfit',sans-serif;position:relative;}}
#map {{width:100%;height:490px;}}
#legend {{
  position:absolute;bottom:30px;left:14px;z-index:10;
  background:rgba(8,15,28,.92);border:1px solid #162440;
  border-radius:12px;padding:10px 14px;font-size:.73rem;
  backdrop-filter:blur(8px);
}}
#legend .row {{display:flex;align-items:center;gap:7px;margin-bottom:5px;color:#c8d8f0;}}
#legend .row:last-child {{margin-bottom:0;}}
#legend .dot {{width:11px;height:11px;border-radius:50%;flex-shrink:0;border:2px solid #fff;}}
#flag-bar {{
  position:absolute;top:0;left:0;right:0;height:3px;z-index:10;
  background:linear-gradient(90deg,
    #F42A41 0%,#006A4E 14%,#EF3340 28%,#000 35%,
    #009736 42%,#B22234 56%,#3C3B6E 70%,
    #DA0000 78%,#239F40 86%,#CF142B 92%,#012169 100%);
}}
</style>
</head>
<body>
<div id="flag-bar"></div>
<div id="map"></div>
<div id="legend">
  <div style="font-weight:700;color:#eef2ff;margin-bottom:8px;font-size:.78rem;letter-spacing:.06em">
    NEXOPORT
  </div>
  <div class="row"><div class="dot" style="background:#f59e0b"></div>In Transit</div>
  <div class="row"><div class="dot" style="background:#239F40"></div>Delivered</div>
  <div class="row"><div class="dot" style="background:#F42A41"></div>Delayed</div>
</div>
<script>
function initMap() {{
  var map = new google.maps.Map(document.getElementById('map'), {{
    center:{{lat:{clat:.4f},lng:{clon:.4f}}},
    zoom:2,
    mapTypeControl:true,
    fullscreenControl:true,
    styles:[
      {{"elementType":"geometry","stylers":[{{"color":"#0d1b2e"}}]}},
      {{"elementType":"labels.text.fill","stylers":[{{"color":"#6b90b8"}}]}},
      {{"elementType":"labels.text.stroke","stylers":[{{"color":"#0a1520"}}]}},
      {{"featureType":"administrative","elementType":"geometry","stylers":[{{"visibility":"simplified"}}]}},
      {{"featureType":"administrative.country","elementType":"geometry.stroke","stylers":[{{"color":"#1e3a5f"}}]}},
      {{"featureType":"administrative.country","elementType":"labels.text.fill","stylers":[{{"color":"#5a82a8"}}]}},
      {{"featureType":"water","elementType":"geometry","stylers":[{{"color":"#04080f"}}]}},
      {{"featureType":"water","elementType":"labels.text.fill","stylers":[{{"color":"#1e3a5f"}}]}},
      {{"featureType":"road","elementType":"geometry","stylers":[{{"color":"#162440"}}]}},
      {{"featureType":"road","elementType":"geometry.stroke","stylers":[{{"color":"#0f1d31"}}]}},
      {{"featureType":"road","elementType":"labels.text.fill","stylers":[{{"color":"#3d5a80"}}]}},
      {{"featureType":"landscape","elementType":"geometry","stylers":[{{"color":"#0c1828"}}]}},
      {{"featureType":"landscape.natural","elementType":"geometry","stylers":[{{"color":"#0a1623"}}]}},
      {{"featureType":"poi","elementType":"geometry","stylers":[{{"color":"#0f1d31"}}]}},
      {{"featureType":"poi","elementType":"labels","stylers":[{{"visibility":"off"}}]}},
      {{"featureType":"transit","elementType":"labels","stylers":[{{"visibility":"off"}}]}}
    ]
  }});
  {markers_js}
}}
</script>
<script async defer
  src="https://maps.googleapis.com/maps/api/js?key={GMAP_KEY}&callback=initMap">
</script>
</body>
</html>
"""

    st.markdown('<div class="map-outer">', unsafe_allow_html=True)
    components.html(gmap_html, height=500)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Shipment cards ──
    st.markdown('<div style="height:.9rem"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;gap:.7rem;margin-bottom:.8rem">
      <span style="font-size:1.2rem">📋</span>
      <span style="font-weight:700;font-size:1.05rem">Shipment Status Details</span>
    </div>
    """, unsafe_allow_html=True)

    for _, row in df.iterrows():
        sc   = STATUS_COLORS.get(row["Status"], "#888")
        scls = {"In Transit":"s-transit","Delivered":"s-delivered","Delayed":"s-delayed"}.get(row["Status"],"")
        eta  = "Arrived ✓" if row["ETA_Days"] == 0 else f"{row['ETA_Days']} days"
        st.markdown(f"""
        <div class="nx-card" style="display:flex;align-items:center;gap:1.4rem;
             flex-wrap:wrap;border-left:3px solid {sc}">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.35rem;
                      letter-spacing:.06em;color:{sc};min-width:95px">
            {row['Shipment_ID']}
          </div>
          <div style="flex:1;min-width:110px">
            <div style="font-size:.67rem;color:#5a7294;text-transform:uppercase;
                        letter-spacing:.08em;font-weight:700">Destination</div>
            <div style="font-weight:600;margin-top:.1rem">🌍 {row['Destination']}</div>
          </div>
          <div style="flex:1;min-width:100px">
            <div style="font-size:.67rem;color:#5a7294;text-transform:uppercase;
                        letter-spacing:.08em;font-weight:700">Carrier</div>
            <div style="font-weight:600;margin-top:.1rem">📦 {row['Carrier']}</div>
          </div>
          <div style="flex:1;min-width:100px">
            <div style="font-size:.67rem;color:#5a7294;text-transform:uppercase;
                        letter-spacing:.08em;font-weight:700">Value</div>
            <div style="font-weight:600;margin-top:.1rem">💰 ${row['Value_USD']:,}</div>
          </div>
          <div style="flex:1;min-width:80px">
            <div style="font-size:.67rem;color:#5a7294;text-transform:uppercase;
                        letter-spacing:.08em;font-weight:700">ETA</div>
            <div style="font-weight:600;margin-top:.1rem;color:#7a9cc0">⏱ {eta}</div>
          </div>
          <span class="st-badge {scls}">{row['Status']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;padding:1.2rem;font-size:.72rem;color:#2a3f5f;margin-top:.4rem">
      🔒 Read-only access &nbsp;·&nbsp; {FLAGS} &nbsp;·&nbsp; {BRAND} Global Trade Intelligence
    </div>
    """, unsafe_allow_html=True)
