import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(page_title="NEXOPORT", layout="wide")

GEMINI_KEY = "YOUR_API_KEY"
genai.configure(api_key=GEMINI_KEY)

# ─────────────────────────────
# LOAD DATA (SAFE)
# ─────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data_samples.csv")
    except:
        df = pd.DataFrame({
            "Shipment_ID": ["EXP-101","IMP-202"],
            "Destination": ["Poland","Bangladesh"],
            "Value_USD": [25000,12000],
            "Status": ["In Transit","Delivered"],
            "Carrier": ["DHL","FedEx"],
            "ETA_Days": [3,0],
            "Lat": [52.2297,23.8103],
            "Lon": [21.0122,90.4125],
        })

    # ✅ Ensure required columns
    REQUIRED_COLUMNS = [
        "Shipment_ID","Destination","Value_USD",
        "Status","Carrier","ETA_Days","Lat","Lon"
    ]

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            if col in ["Value_USD","ETA_Days","Lat","Lon"]:
                df[col] = 0
            else:
                df[col] = "Unknown"

    return df

df = load_data()

# ─────────────────────────────
# 🌍 LANGUAGE SYSTEM
# ─────────────────────────────
LANG_OPTIONS = {
    "English": "English",
    "বাংলা": "Bengali",
    "العربية": "Arabic"
}

selected_lang = st.selectbox("🌐 Language", list(LANG_OPTIONS.keys()))
target_lang = LANG_OPTIONS[selected_lang]

def translate(text):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Translate into {target_lang}: {text}"
        return model.generate_content(prompt).text
    except:
        return text

# ─────────────────────────────
# 🤖 AI FUNCTION (SAFE)
# ─────────────────────────────
def ask_ai(context, question):
    try:
        model = genai.GenerativeModel("gemini-pro")

        prompt = f"""
Respond in {target_lang}.

Data:
{context}

Question: {question}
"""
        return model.generate_content(prompt).text
    except Exception as e:
        return f"AI Error: {e}"

# ─────────────────────────────
# UI
# ─────────────────────────────
st.title(translate("NEXOPORT Global Trade Dashboard"))

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Shipments", len(df))
col2.metric("In Transit", (df["Status"] == "In Transit").sum())
col3.metric("Delivered", (df["Status"] == "Delivered").sum())

# ─────────────────────────────
# 📊 CHART (FIXED)
# ─────────────────────────────
fig = px.bar(df, x="Destination", y="Value_USD", color="Status")

# ❌ removed marker_corner_radius
fig.update_traces(marker_line_width=0)

st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────
# 📋 FILTER (SAFE)
# ─────────────────────────────
if "Carrier" in df.columns:
    carriers = ["All"] + df["Carrier"].dropna().unique().tolist()
else:
    carriers = ["All"]

selected_carrier = st.selectbox("Filter Carrier", carriers)

filtered_df = df.copy()
if selected_carrier != "All":
    filtered_df = filtered_df[filtered_df["Carrier"] == selected_carrier]

st.dataframe(filtered_df)

# ─────────────────────────────
# 🗺️ SAFE ETA DISPLAY
# ─────────────────────────────
st.subheader("Shipment Status")

for _, row in df.iterrows():
    eta_days = row.get("ETA_Days", None)

    if eta_days is None:
        eta = "Unknown"
    elif eta_days == 0:
        eta = "Arrived ✓"
    else:
        eta = f"{eta_days} days"

    st.write(f"{row['Shipment_ID']} → {row['Destination']} | ETA: {eta}")

# ─────────────────────────────
# 🤖 AI CHAT
# ─────────────────────────────
st.subheader("AI Assistant")

user_q = st.text_input("Ask about shipments...")

if st.button("Ask AI"):
    response = ask_ai(df.to_string(), user_q)
    st.success(response)
