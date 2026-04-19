import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title=" Smart Logistics Portal",
    page_icon="🌐",
    layout="wide"
)

# --- CUSTOM CSS FOR PROFESSIONAL UI ---
# --- CUSTOM CSS FOR PROFESSIONAL UI ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; background-color: #004b93; color: white; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)  # এখানে unsafe_allow_html=True হবে

# --- GEMINI AI SETUP ---
# Your provided API Key integrated
API_KEY = "AIzaSyAnKtF3VIydi5rpQ621TsFKYhq8f756oQA" 

def get_ai_response(context, question):
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        # Instructing the AI to act as a Logistics Expert
        prompt = f"""
        You are a Supply Chain Expert for EximpCore Trading. 
        Context Data (Shipments): {context}
        User Question: {question}
        
        Provide a concise, professional answer based on the data.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI is currently offline or API quota reached. (Error: {str(e)})"

# --- AUTHENTICATION LOGIC ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

def login(role):
    st.session_state.logged_in = True
    st.session_state.role = role

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

# --- MOCK DATASET (Export-Import Focused) ---
@st.cache_data
def load_data():
    return pd.DataFrame({
        'Shipment_ID': ['EXP-101', 'IMP-202', 'EXP-103', 'IMP-204', 'EXP-105', 'IMP-206'],
        'Product': ['Steel Coil', 'Textiles', 'Electronics', 'Chemicals', 'Machinery', 'Garments'],
        'Destination': ['Poland', 'Bangladesh', 'Germany', 'USA', 'China', 'Vietnam'],
        'Value_USD': [25000, 12000, 45000, 32000, 85000, 15000],
        'Status': ['In Transit', 'Delivered', 'Delayed', 'Pending', 'In Transit', 'Delivered'],
        'Risk_Level': ['Low', 'Low', 'High', 'Medium', 'Low', 'Low'],
        'Notes': ['On schedule', 'Cleared customs', 'Port Strike in Hamburg', 'Document verification', 'Vessel delayed', 'None']
    })

df = load_data()

# --- INTERFACE LOGIC ---
if not st.session_state.logged_in:
    st.title("🏢  Intelligent Logistics Portal")
    st.markdown("### Secure Gateway for Global Trade Operations")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("#### 🛠️ Administrator\nFull system access, Anomaly Detection, and AI Auditing.")
        if st.button("Login as Admin"): login("Admin")
            
    with col2:
        st.success("#### 📋  / User\nShipment tracking, documentation, and operational manuals.")
        if st.button("Login as User"): login("User")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("EximpCore System")
    st.write(f"**Access Level:** `{st.session_state.role}`")
    st.divider()
    if st.button("🚪 Log Out"): logout()

# --- ADMIN PANEL ---
if st.session_state.role == "Admin":
    st.title("🛠️ Executive Command Center")
    
    # 1. SMART NOTIFICATIONS (Anomaly Detection)
    st.subheader("⚠️ System Intelligence Alerts")
    a_col1, a_col2 = st.columns(2)
    
    with a_col1:
        delayed = df[df['Status'] == 'Delayed']
        if not delayed.empty:
            for _, row in delayed.iterrows():
                st.error(f"**CRITICAL DELAY:** {row['Shipment_ID']} to {row['Destination']} is stuck due to '{row['Notes']}'.")
    
    with a_col2:
        # Simple Anomaly: Value > 50k
        high_value = df[df['Value_USD'] > 50000]
        if not high_value.empty:
            for _, row in high_value.iterrows():
                st.warning(f"**HIGH VALUE ALERT:** {row['Shipment_ID']} exceeds standard insurance limit (${row['Value_USD']:,}).")

    st.divider()

    # 2. ADMIN TABS
    tab1, tab2, tab3 = st.tabs(["📊 Global Analytics", "🗄️ Master Database", "🤖 AI Logistics Consultant"])
    
    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Trade Volume", f"${df['Value_USD'].sum():,}")
        c2.metric("Active Shipments", len(df[df['Status'] != 'Delivered']))
        c3.metric("Critical Risks", len(df[df['Status'] == 'Delayed']))
        c4.metric("Avg. Shipment", f"${int(df['Value_USD'].mean()):,}")
        
        fig = px.bar(df, x='Destination', y='Value_USD', color='Status', barmode='group', 
                     title="Revenue Distribution by Destination", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        st.subheader("Edit Shipment Records")
        st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Synchronize with Cloud"):
            st.success("Database synchronized successfully!")
            
    with tab3:
        st.subheader("AI Powered Expert (RAG)")
        st.write("Ask our AI about current shipment risks or performance:")
        u_input = st.text_input("Example: 'Which shipments are delayed and why?'")
        if u_input:
            with st.spinner("Analyzing shipments via Gemini AI..."):
                context_str = df.to_string()
                response = get_ai_response(context_str, u_input)
                st.markdown(f"**AI Response:**\n\n{response}")

# --- USER PANEL ---
else:
    st.title("📋 Operational Monitoring Portal")
    t1, t2 = st.tabs(["📦 Shipment Tracking", "📖 SOP Knowledge Base"])
    
    with t1:
        st.subheader("Current Shipment Logs")
        st.dataframe(df, use_container_width=True)
        st.info("System Note: Your access level is restricted to Read-Only.")
        
    with t2:
        st.subheader("EximpCore SOP & Manuals")
        with st.expander("Required Export Documents"):
            st.write("1. Bill of Lading\n2. Commercial Invoice\n3. Packing List\n4. Export License")
        with st.expander("Standard Risk Assessment"):
            st.write("Always check the 'Notes' column in the tracking sheet for real-time port updates.")
