import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
import streamlit.components.v1 as components
import json

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="EximpCore Smart Portal",
    layout="wide",
    page_icon="🌐",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  (professional dark-navy theme)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette ── */
:root{
  --bg:       #0a0f1e;
  --surface:  #111827;
  --card:     #161f35;
  --border:   #1e2d4a;
  --accent:   #3b82f6;
  --accent2:  #06b6d4;
  --success:  #10b981;
  --warning:  #f59e0b;
  --danger:   #ef4444;
  --text:     #e2e8f0;
  --muted:    #64748b;
}

/* ── Base ── */
html, body, .stApp {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebarNav"] { display: none; }

/* ── Cards ── */
.eximp-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1rem;
}

/* ── Metric cards ── */
.metric-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.2rem 1.4rem;
  position: relative;
  overflow: hidden;
}
.metric-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.metric-label { font-size: .78rem; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 800; color: var(--text); margin: .2rem 0; }
.metric-sub   { font-size: .78rem; color: var(--success); }

/* ── Page header ── */
.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.8rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}
.page-header h1 {
  font-family: 'Syne', sans-serif;
  font-size: 1.9rem;
  font-weight: 800;
  background: linear-gradient(135deg, #60a5fa, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}
.page-header .badge {
  background: rgba(59,130,246,.15);
  border: 1px solid rgba(59,130,246,.3);
  color: #60a5fa;
  padding: .25rem .75rem;
  border-radius: 999px;
  font-size: .75rem;
  font-weight: 600;
}

/* ── Buttons ── */
div.stButton > button {
  background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-family: 'DM Sans', sans-serif !important;
  padding: .5rem 1.4rem !important;
  transition: opacity .2s !important;
}
div.stButton > button:hover { opacity: .85 !important; }

/* ── Logout button ── */
.logout-btn > button {
  background: rgba(239,68,68,.12) !important;
  color: #ef4444 !important;
  border: 1px solid rgba(239,68,68,.3) !important;
}

/* ── Text inputs ── */
.stTextInput > div > div > input,
.stTextArea textarea {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(59,130,246,.15) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] button {
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  color: var(--muted) !important;
  border-radius: 8px 8px 0 0 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--accent) !important;
  border-bottom: 2px solid var(--accent) !important;
}

/* ── Dataframe / Table ── */
.stDataFrame, .stTable { border-radius: 12px; overflow: hidden; }

/* ── Chat bubbles ── */
.chat-user {
  background: rgba(59,130,246,.12);
  border: 1px solid rgba(59,130,246,.2);
  border-radius: 12px 12px 2px 12px;
  padding: .8rem 1.1rem;
  margin: .5rem 0;
  max-width: 85%;
  margin-left: auto;
}
.chat-ai {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px 12px 12px 2px;
  padding: .8rem 1.1rem;
  margin: .5rem 0;
  max-width: 90%;
}
.chat-label {
  font-size: .7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .08em;
  margin-bottom: .35rem;
}

/* ── Status badges ── */
.badge-transit  { background:rgba(245,158,11,.15); color:#f59e0b; border:1px solid rgba(245,158,11,.3); }
.badge-delivered{ background:rgba(16,185,129,.15); color:#10b981; border:1px solid rgba(16,185,129,.3); }
.badge-delayed  { background:rgba(239,68,68,.15);  color:#ef4444; border:1px solid rgba(239,68,68,.3);  }
.status-badge   { padding:.18rem .65rem; border-radius:999px; font-size:.73rem; font-weight:600; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Alerts ── */
.stAlert { border-radius: 12px !important; }

/* ── Select box ── */
.stSelectbox select {
  background: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
}

/* ── LOGIN PAGE ── */
.login-wrap {
  max-width: 420px;
  margin: 6vh auto 0;
  padding: 2.8rem;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  box-shadow: 0 25px 60px rgba(0,0,0,.5);
}
.login-logo {
  text-align: center;
  font-family: 'Syne', sans-serif;
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #60a5fa, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: .3rem;
}
.login-sub {
  text-align: center;
  color: var(--muted);
  font-size: .85rem;
  margin-bottom: 2rem;
}

/* ── Sidebar role pill ── */
.role-pill {
  background: rgba(59,130,246,.12);
  border: 1px solid rgba(59,130,246,.25);
  border-radius: 999px;
  padding: .4rem 1rem;
  font-size: .78rem;
  font-weight: 700;
  color: #60a5fa;
  text-align: center;
  margin-bottom: 1.2rem;
}

/* ── Sidebar nav links ── */
.nav-item {
  display: flex;
  align-items: center;
  gap: .7rem;
  padding: .65rem 1rem;
  border-radius: 10px;
  font-size: .88rem;
  font-weight: 500;
  color: var(--muted) !important;
  cursor: pointer;
  transition: all .18s;
  text-decoration: none;
}
.nav-item:hover, .nav-item.active {
  background: rgba(59,130,246,.1);
  color: var(--text) !important;
}

/* ── Map wrapper ── */
.map-wrap { border-radius: 16px; overflow: hidden; border: 1px solid var(--border); }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  API SETUP
# ─────────────────────────────────────────────
API_KEY = "AIzaSyAnKtF3VIydi5rpQ621TsFKYhq8f756oQA"

def get_ai_response(context: str, question: str, history: list) -> str:
    """RAG-style response using shipment data as context."""
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-pro")

        # Build conversation turns for RAG
        history_text = ""
        for turn in history[-6:]:          # last 3 Q&A pairs
            history_text += f"User: {turn['q']}\nAssistant: {turn['a']}\n\n"

        system_prompt = f"""You are EximpCore's Senior Logistics Intelligence Analyst.
You have access to the live shipment database below. Analyse it carefully and give
precise, data-driven answers. Use numbers and specific shipment IDs when relevant.
Keep replies concise but insightful.

=== LIVE SHIPMENT DATABASE ===
{context}
=== END DATABASE ===

Previous conversation:
{history_text}
"""
        prompt = f"{system_prompt}\nUser question: {question}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI analysis unavailable: {str(e)}"


# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data_samples.csv")
    except Exception:
        return pd.DataFrame({
            "Shipment_ID":  ["EXP-101", "IMP-202", "EXP-103", "IMP-304", "EXP-405", "IMP-506"],
            "Destination":  ["Poland",  "Bangladesh", "Germany", "USA",    "Japan",   "France"],
            "Value_USD":    [25000, 12000, 45000, 33000, 18500, 61000],
            "Status":       ["In Transit","Delivered","Delayed","In Transit","Delivered","In Transit"],
            "Carrier":      ["DHL","FedEx","UPS","Maersk","DHL","UPS"],
            "ETA_Days":     [3, 0, 7, 5, 0, 2],
            "Lat":          [52.2297, 23.8103, 52.5200, 40.7128, 35.6762, 48.8566],
            "Lon":          [21.0122, 90.4125, 13.4050, -74.0060, 139.6503, 2.3522],
        })

df = load_data()


# ─────────────────────────────────────────────
#  SESSION STATE DEFAULTS
# ─────────────────────────────────────────────
for key, val in {
    "logged_in": False,
    "role":      None,
    "rag_history": [],
    "admin_tab": "analytics",
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ═════════════════════════════════════════════
#  LOGIN PAGE
# ═════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-wrap">
      <div class="login-logo">🌐 EximpCore</div>
      <div class="login-sub">Smart Export-Import Intelligence Portal</div>
    </div>
    """, unsafe_allow_html=True)

    # Render the form inside the card via columns trick
    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        st.markdown('<div style="height:.4rem"></div>', unsafe_allow_html=True)
        if st.button("Sign In  →", use_container_width=True):
            if username == "admin" and password == "eximp123":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.rerun()
            elif username == "user" and password == "user123":
                st.session_state.logged_in = True
                st.session_state.role = "User"
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")

        st.markdown("""
        <div style="margin-top:1.6rem; padding:1rem; background:rgba(255,255,255,.04);
                    border-radius:10px; font-size:.78rem; color:#64748b; line-height:1.7;">
          <b style="color:#94a3b8">Demo credentials</b><br>
          Admin &nbsp;→&nbsp; admin / eximp123<br>
          User &nbsp;&nbsp;→&nbsp; user / user123
        </div>
        """, unsafe_allow_html=True)
    st.stop()


# ═════════════════════════════════════════════
#  SIDEBAR  (shared)
# ═════════════════════════════════════════════
with st.sidebar:
    st.markdown(f'<div class="login-logo" style="font-size:1.4rem;margin-bottom:.5rem">🌐 EximpCore</div>', unsafe_allow_html=True)
    role_color = "#3b82f6" if st.session_state.role == "Admin" else "#06b6d4"
    icon = "🛡️" if st.session_state.role == "Admin" else "📦"
    st.markdown(f'<div class="role-pill">{icon} {st.session_state.role} Panel</div>', unsafe_allow_html=True)

    st.markdown("---")

    if st.session_state.role == "Admin":
        st.markdown("**Navigation**")
        if st.button("📊 Analytics Dashboard", use_container_width=True):
            st.session_state.admin_tab = "analytics"
        if st.button("🤖 AI RAG Consultant", use_container_width=True):
            st.session_state.admin_tab = "rag"
        if st.button("📋 Data Manager", use_container_width=True):
            st.session_state.admin_tab = "data"
    else:
        st.markdown("**Navigation**")
        st.markdown("""
        <div style="display:flex;flex-direction:column;gap:.4rem;margin-top:.5rem">
          <div class="nav-item active">📍 Live Tracking Map</div>
          <div class="nav-item">📋 Shipment Status</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Stats in sidebar
    total_val = df["Value_USD"].sum()
    in_transit = len(df[df["Status"] == "In Transit"])
    delayed    = len(df[df["Status"] == "Delayed"])
    st.markdown(f"""
    <div style="font-size:.78rem; color:#64748b; line-height:2">
      💰 Total Value &nbsp;<b style="color:#e2e8f0">${total_val:,}</b><br>
      🚢 In Transit &nbsp;&nbsp;<b style="color:#f59e0b">{in_transit}</b><br>
      ⚠️ Delayed &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b style="color:#ef4444">{delayed}</b><br>
      ✅ Delivered &nbsp;&nbsp;&nbsp;<b style="color:#10b981">{len(df[df['Status']=='Delivered'])}</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("⏻  Logout", use_container_width=True):
        for k in ["logged_in", "role", "rag_history", "admin_tab"]:
            st.session_state[k] = False if k == "logged_in" else ([] if k == "rag_history" else None)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PLOTLY THEME HELPER
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#94a3b8"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
    margin=dict(t=40, b=40, l=20, r=20),
)
STATUS_COLORS = {
    "Delivered":  "#10b981",
    "In Transit": "#f59e0b",
    "Delayed":    "#ef4444",
}


# ═════════════════════════════════════════════
#  ██████████  ADMIN  ██████████
# ═════════════════════════════════════════════
if st.session_state.role == "Admin":

    # ── Header ──────────────────────────────
    st.markdown("""
    <div class="page-header">
      <span style="font-size:2rem">🛠️</span>
      <div>
        <h1>Administrator Command Center</h1>
        <p style="margin:0;color:#64748b;font-size:.85rem">Full logistics intelligence dashboard</p>
      </div>
      <span class="badge" style="margin-left:auto">ADMIN ACCESS</span>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ─────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    for col, label, value, sub, color in [
        (k1, "Total Cargo Value",    f"${df['Value_USD'].sum():,}",           "↑ 12% vs last month", "#10b981"),
        (k2, "Active Shipments",     str(len(df)),                             f"{in_transit} in transit", "#f59e0b"),
        (k3, "Delayed Shipments",    str(delayed),                             "Needs attention", "#ef4444"),
        (k4, "System Health",        "Optimal",                                "All services online", "#10b981"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-sub" style="color:{color}">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)

    # ── Tab routing ─────────────────────────
    active = st.session_state.get("admin_tab", "analytics")

    # ────────────────────────────────────────
    #  TAB: ANALYTICS
    # ────────────────────────────────────────
    if active == "analytics":
        st.markdown('<div class="eximp-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Shipment Analytics")
        c1, c2 = st.columns(2)

        with c1:
            fig_bar = px.bar(
                df, x="Destination", y="Value_USD", color="Status",
                color_discrete_map=STATUS_COLORS,
                title="Cargo Value by Destination",
                labels={"Value_USD": "Value (USD)"},
            )
            fig_bar.update_layout(**PLOT_LAYOUT)
            fig_bar.update_traces(marker_line_width=0)
            st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            status_counts = df["Status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            fig_pie = px.pie(
                status_counts, names="Status", values="Count",
                color="Status", color_discrete_map=STATUS_COLORS,
                title="Status Distribution",
                hole=.55,
            )
            fig_pie.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig_pie, use_container_width=True)

        # Carrier breakdown
        carrier_val = df.groupby("Carrier")["Value_USD"].sum().reset_index()
        fig_h = px.bar(
            carrier_val, x="Value_USD", y="Carrier",
            orientation="h", title="Value by Carrier",
            color="Value_USD", color_continuous_scale=["#1e3a5f", "#3b82f6", "#06b6d4"],
            labels={"Value_USD": "Total Value (USD)"},
        )
        fig_h.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_h, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ────────────────────────────────────────
    #  TAB: AI RAG CONSULTANT
    # ────────────────────────────────────────
    elif active == "rag":
        st.markdown('<div class="eximp-card">', unsafe_allow_html=True)
        st.markdown("""
        #### 🤖 AI Logistics Consultant  <span style="font-size:.75rem;color:#64748b;font-weight:400">— powered by Gemini RAG</span>
        """, unsafe_allow_html=True)
        st.caption("Ask anything about your shipments — optimisation, risks, route analysis, carrier performance.")

        # Chat history display
        if st.session_state.rag_history:
            for turn in st.session_state.rag_history:
                st.markdown(f"""
                <div class="chat-user">
                  <div class="chat-label" style="color:#60a5fa">You</div>
                  {turn['q']}
                </div>
                <div class="chat-ai">
                  <div class="chat-label" style="color:#06b6d4">EximpCore AI</div>
                  {turn['a']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:2.5rem 1rem;color:#374151">
              <div style="font-size:2.5rem;margin-bottom:.5rem">💬</div>
              <div style="font-size:.9rem">Ask your first question below</div>
              <div style="font-size:.78rem;color:#64748b;margin-top:.4rem">
                e.g. "Which shipments are at risk?" or "Summarise carrier performance"
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Input row
        q_col, btn_col = st.columns([5, 1])
        with q_col:
            user_q = st.text_input(
                "Ask the AI", label_visibility="collapsed",
                placeholder="Type your logistics question here…",
                key="rag_input",
            )
        with btn_col:
            send = st.button("Send ➤", use_container_width=True)

        ctrl1, ctrl2 = st.columns([1, 5])
        with ctrl1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.rag_history = []
                st.rerun()

        if send and user_q.strip():
            with st.spinner("🧠 Analysing shipment data…"):
                answer = get_ai_response(
                    df.to_string(),
                    user_q,
                    st.session_state.rag_history,
                )
            st.session_state.rag_history.append({"q": user_q, "a": answer})
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # Context preview
        with st.expander("📄 RAG Context — Live Database (what the AI sees)"):
            st.dataframe(df, use_container_width=True)

    # ────────────────────────────────────────
    #  TAB: DATA MANAGER
    # ────────────────────────────────────────
    elif active == "data":
        st.markdown('<div class="eximp-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Shipment Data Manager")

        filter_col1, filter_col2, _ = st.columns([2, 2, 3])
        with filter_col1:
            status_filter = st.selectbox("Filter by Status", ["All"] + df["Status"].unique().tolist())
        with filter_col2:
            carrier_filter = st.selectbox("Filter by Carrier", ["All"] + df["Carrier"].unique().tolist())

        filtered = df.copy()
        if status_filter != "All":
            filtered = filtered[filtered["Status"] == status_filter]
        if carrier_filter != "All":
            filtered = filtered[filtered["Carrier"] == carrier_filter]

        edited = st.data_editor(
            filtered,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "Value_USD": st.column_config.NumberColumn("Value (USD)", format="$%,d"),
                "ETA_Days":  st.column_config.NumberColumn("ETA (Days)"),
                "Lat": st.column_config.NumberColumn("Latitude",  format="%.4f"),
                "Lon": st.column_config.NumberColumn("Longitude", format="%.4f"),
            },
        )

        dl1, dl2, _ = st.columns([2, 2, 4])
        with dl1:
            st.download_button(
                "⬇ Export CSV",
                edited.to_csv(index=False).encode(),
                "shipments_export.csv",
                "text/csv",
                use_container_width=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════
#  ██████████  USER  ██████████
# ═════════════════════════════════════════════
else:
    # ── Header ──────────────────────────────
    st.markdown("""
    <div class="page-header">
      <span style="font-size:2rem">📦</span>
      <div>
        <h1>Live Shipment Tracker</h1>
        <p style="margin:0;color:#64748b;font-size:.85rem">Real-time location and status of your cargo</p>
      </div>
      <span class="badge" style="margin-left:auto;background:rgba(6,182,212,.12);
            border-color:rgba(6,182,212,.3);color:#06b6d4">USER VIEW</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick stats ─────────────────────────
    u1, u2, u3 = st.columns(3)
    for col, label, val, sub, color in [
        (u1, "My Shipments",  str(len(df)),          "All tracked", "#3b82f6"),
        (u2, "In Transit",    str(in_transit),         "Active now",  "#f59e0b"),
        (u3, "Delivered",     str(len(df[df["Status"]=="Delivered"])), "Completed", "#10b981"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{val}</div>
          <div class="metric-sub" style="color:{color}">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════
    #  GOOGLE MAPS  (via JS API embed)
    # ══════════════════════════════════════
    st.markdown("#### 🗺️ Live Google Maps — Shipment Locations")

    # Build marker data for JS
    markers_js = ""
    info_windows = ""
    for _, row in df.iterrows():
        sc = STATUS_COLORS.get(row["Status"], "#888")
        markers_js += f"""
        (function(){{
          var pos = {{lat:{row['Lat']}, lng:{row['Lon']}}};
          var marker = new google.maps.Marker({{
            position: pos, map: map,
            title: "{row['Shipment_ID']}",
            icon: {{
              path: google.maps.SymbolPath.CIRCLE,
              fillColor: '{sc}',
              fillOpacity: 1,
              strokeColor: '#fff',
              strokeWeight: 2,
              scale: 10
            }}
          }});
          var iw = new google.maps.InfoWindow({{
            content: `<div style="font-family:DM Sans,sans-serif;padding:8px;min-width:180px">
              <b style="color:#1e293b;font-size:.95rem">{row['Shipment_ID']}</b><br>
              <span style="color:#64748b;font-size:.8rem">🌍 {row['Destination']}</span><br>
              <span style="font-size:.8rem">📦 {row['Carrier']}</span><br>
              <span style="font-size:.8rem;font-weight:600;color:{sc}">● {row['Status']}</span><br>
              <span style="font-size:.8rem;color:#334155">💰 ${ '{:,}'.format(row['Value_USD']) }</span>
            </div>`
          }});
          marker.addListener('click', function(){{ iw.open(map, marker); }});
        }})();
        """

    # Centre of all shipments
    centre_lat = df["Lat"].mean()
    centre_lon = df["Lon"].mean()

    google_maps_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#0a0f1e; }}
  #map {{ width:100%; height:480px; border-radius:16px; }}
</style>
</head>
<body>
<div id="map"></div>
<script>
function initMap() {{
  var map = new google.maps.Map(document.getElementById('map'), {{
    center: {{lat:{centre_lat:.4f}, lng:{centre_lon:.4f}}},
    zoom: 2,
    mapTypeId: 'roadmap',
    styles: [
      {{"elementType":"geometry","stylers":[{{"color":"#1d2c4d"}}]}},
      {{"elementType":"labels.text.fill","stylers":[{{"color":"#8ec3b9"}}]}},
      {{"elementType":"labels.text.stroke","stylers":[{{"color":"#1a3646"}}]}},
      {{"featureType":"administrative.country","elementType":"geometry.stroke","stylers":[{{"color":"#4b6878"}}]}},
      {{"featureType":"water","elementType":"geometry","stylers":[{{"color":"#0e1626"}}]}},
      {{"featureType":"water","elementType":"labels.text.fill","stylers":[{{"color":"#4e6d70"}}]}},
      {{"featureType":"road","elementType":"geometry","stylers":[{{"color":"#304a7d"}}]}},
      {{"featureType":"road","elementType":"geometry.stroke","stylers":[{{"color":"#255763"}}]}},
      {{"featureType":"road","elementType":"labels.text.fill","stylers":[{{"color":"#98a5be"}}]}},
      {{"featureType":"transit","elementType":"labels.text.fill","stylers":[{{"color":"#98a5be"}}]}},
      {{"featureType":"landscape","elementType":"geometry","stylers":[{{"color":"#163d4f"}}]}},
      {{"featureType":"poi","elementType":"geometry","stylers":[{{"color":"#283d6a"}}]}},
      {{"featureType":"poi","elementType":"labels.text.fill","stylers":[{{"color":"#6f9ba5"}}]}}
    ]
  }});
  {markers_js}
}}
</script>
<script async defer
  src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAnKtF3VIydi5rpQ621TsFKYhq8f756oQA&callback=initMap">
</script>
</body>
</html>
"""

    components.html(google_maps_html, height=490)

    # ── Shipment detail cards ────────────────
    st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)
    st.markdown("#### 📋 Shipment Status Details")

    for _, row in df.iterrows():
        sc  = STATUS_COLORS.get(row["Status"], "#888")
        cls = {
            "In Transit": "badge-transit",
            "Delivered":  "badge-delivered",
            "Delayed":    "badge-delayed",
        }.get(row["Status"], "")
        eta_txt = "Arrived" if row["ETA_Days"] == 0 else f"{row['ETA_Days']} days"

        st.markdown(f"""
        <div class="eximp-card" style="display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap">
          <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                      min-width:90px;color:#e2e8f0">{row['Shipment_ID']}</div>
          <div style="flex:1;min-width:120px">
            <div style="font-size:.75rem;color:#64748b">DESTINATION</div>
            <div style="font-weight:600">🌍 {row['Destination']}</div>
          </div>
          <div style="flex:1;min-width:100px">
            <div style="font-size:.75rem;color:#64748b">CARRIER</div>
            <div style="font-weight:600">📦 {row['Carrier']}</div>
          </div>
          <div style="flex:1;min-width:100px">
            <div style="font-size:.75rem;color:#64748b">VALUE</div>
            <div style="font-weight:600">💰 ${row['Value_USD']:,}</div>
          </div>
          <div style="flex:1;min-width:90px">
            <div style="font-size:.75rem;color:#64748b">ETA</div>
            <div style="font-weight:600;color:#94a3b8">⏱ {eta_txt}</div>
          </div>
          <span class="status-badge {cls}">{row['Status']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:1rem;font-size:.75rem;color:#374151;margin-top:1rem">
      🔒 User view — read-only access &nbsp;|&nbsp; Contact admin for modifications
    </div>
    """, unsafe_allow_html=True)
