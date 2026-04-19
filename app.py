import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="EximpCore Smart Portal", layout="wide", page_icon="🌐")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    div.stButton > button:first-child {
        background: linear-gradient(to right, #00c6ff, #0072ff);
        color: white; border: none; border-radius: 15px; font-weight: bold;
    }
    .stMetric { background: white; padding: 20px; border-radius: 15px; box-shadow: 5px 5px 15px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- API SETUP ---
API_KEY = "AIzaSyAnKtF3VIydi5rpQ621TsFKYhq8f756oQA" 

def get_ai_response(context, question):
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"You are a Logistics Expert. Data: {context}\nQuestion: {question}"
        response = model.generate_content(prompt)
        return response.text
    except:
        return "AI analysis unavailable at the moment."

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv('data_samples.csv')
    except:
        return pd.DataFrame({
            'Shipment_ID': ['EXP-101', 'IMP-202', 'EXP-103'],
            'Destination': ['Poland', 'Bangladesh', 'Germany'],
            'Value_USD': [25000, 12000, 45000],
            'Status': ['In Transit', 'Delivered', 'Delayed'],
            'Lat': [52.2297, 23.8103, 52.5200], # Coordinates for Map
            'Lon': [21.0122, 90.4125, 13.4050]
        })

df = load_data()

# --- LOGIN ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏢 EximpCore Smart Portal Login")
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

# --- SIDEBAR ---
st.sidebar.title(f"Role: {st.session_state.role}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# --- ADMIN PANEL ---
if st.session_state.role == "Admin":
    st.title("🛠️ Administrator Command Center")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Value", f"${df['Value_USD'].sum():,}")
    m2.metric("Active Shipments", len(df))
    m3.metric("System Health", "Optimal")

    tab1, tab2 = st.tabs(["📊 Analytics", "🤖 AI Auditor (RAG)"])
    
    with tab1:
        st.plotly_chart(px.bar(df, x='Destination', y='Value_USD', color='Status'))
        st.data_editor(df, use_container_width=True)
        
    with tab2:
        st.subheader("LLM Logistics Consultant")
        q = st.text_input("Ask about optimization or risks:")
        if q:
            with st.spinner("AI is thinking..."):
                st.info(get_ai_response(df.to_string(), q))

# --- USER PANEL ---
else:
    st.title("📦 User Tracking Portal")
    st.subheader("Live Shipment Location Tracking")
    
    # Google Maps Interaction (Using Streamlit Map)
    st.map(df[['Lat', 'Lon']])
    
    st.divider()
    st.write("### Shipment Status Details")
    st.table(df[['Shipment_ID', 'Destination', 'Status']])
    st.info("Note: Users can only view shipment locations and status.")
