import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from io import BytesIO

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="NexusTrade AI | Intelligent Supply Chain", layout="wide", page_icon="📈")

# --- CUSTOM CSS FOR MODERN & VIBRANT UI ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
    }
    div.stButton > button:first-child {
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        color: white; border: none; border-radius: 12px; height: 3em; font-weight: bold; transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 15px; border: 1px solid #ffffff;
    }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3192, #1bffff); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- GEMINI AI SETUP ---
API_KEY = "AIzaSyAnKtF3VIydi5rpQ621TsFKYhq8f756oQA" 

def get_ai_response(context, question, lang):
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        instruction = "Answer in English." if lang == "English" else "বাংলায় উত্তর দিন।"
        prompt = f"{instruction}\nSystem Role: Logistics Expert\nContext: {context}\nQuestion: {question}"
        response = model.generate_content(prompt)
        return response.text
    except:
        return "AI analysis offline." if lang == "English" else "AI বিশ্লেষণ অফলাইন।"

# --- SESSION STATE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "lang" not in st.session_state: st.session_state.lang = "English"

# --- MULTILINGUAL DICTIONARY ---
t = {
    "English": {
        "p_name": "NexusTrade AI",
        "tagline": "Intelligent Supply Chain Engine",
        "login": "Secure Portal Access",
        "metrics": ["Total Volume", "Active Ships", "Risk Level", "Conversion"],
        "ai_auditor": "AI Logistics Consultant",
        "reports": "Download CSV Report",
        "currency": "Live Converter (USD to PLN)"
    },
    "বাংলা": {
        "p_name": "নেক্সাসট্রেড এআই",
        "tagline": "ইন্টেলিজেন্ট সাপ্লাই চেইন ইঞ্জিন",
        "login": "নিরাপদ পোর্টাল অ্যাক্সেস",
        "metrics": ["মোট ভলিউম", "সক্রিয় শিপমেন্ট", "ঝুঁকির মাত্রা", "কনভার্সন"],
        "ai_auditor": "এআই লজিস্টিক কনসালট্যান্ট",
        "reports": "CSV রিপোর্ট ডাউনলোড",
        "currency": "লাইভ কনভার্টার (USD থেকে PLN)"
    }
}

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.title("🌐 Dashboard Settings")
    st.session_state.lang = st.selectbox("Language / ভাষা", ["English", "বাংলা"])
    sel = t[st.session_state.lang]
    
    st.divider()
    st.subheader(f"💱 {sel['currency']}")
    usd_amount = st.number_input("Amount (USD)", value=100.0)
    pln_rate = 4.02 # Current sample rate for Poland
    st.write(f"**{usd_amount} USD = {round(usd_amount * pln_rate, 2)} PLN**")

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title(f"🚀 {sel['p_name']}")
    st.write(sel['tagline'])
    
    with st.container():
        st.subheader(sel['login'])
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Sign In"):
            if user == "admin" and pwd == "eximp123":
                st.session_state.logged_in, st.session_state.role = True, "Admin"
                st.rerun()
            elif user == "user" and pwd == "user123":
                st.session_state.logged_in, st.session_state.role = True, "User"
                st.rerun()
            else: st.error("Access Denied!")
    st.stop()

# --- LOAD DATA ---
df = pd.read_csv('data_samples.csv')

# --- DASHBOARD CONTENT ---
st.title(f"📊 {sel['p_name']}")
st.write(f"Welcome back, **{st.session_state.role}** | Language: **{st.session_state.lang}**")

if st.session_state.role == "Admin":
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(sel['metrics'][0], f"${df['Value_USD'].sum():,}")
    m2.metric(sel['metrics'][1], len(df[df['Status'] != 'Delivered']))
    m3.metric(sel['metrics'][2], "High" if len(df[df['Status'] == 'Delayed']) > 0 else "Low")
    m4.metric(sel['metrics'][3], f"{pln_rate} PLN/USD")

    tab1, tab2, tab3 = st.tabs(["📈 Analytics", "🗄️ Master Database", "🤖 " + sel['ai_auditor']])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.pie(df, values='Value_USD', names='Status', hole=.4, title="Shipment Status Distribution")
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            fig2 = px.bar(df, x='Destination', y='Value_USD', color='Risk_Level', title="Market Value by Country")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Download Feature
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label=f"📥 {sel['reports']}", data=csv, file_name='NexusTrade_Report.csv', mime='text/csv')

    with tab2:
        st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
    with tab3:
        u_q = st.text_input("Query AI about Logistics Risks:")
        if u_q:
            with st.spinner("Analyzing..."):
                st.markdown(get_ai_response(df.to_string(), u_q, st.session_state.lang))

else:
    # User View
    st.subheader("📦 Real-time Shipment Tracking")
    st.dataframe(df, use_container_width=True)
    st.info("Language synced. Restricted Access: Editing & AI Auditor disabled for Interns.")

if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.rerun()
