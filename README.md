# smart-logistics-portal
# 🌐 Smart Logistics & AI-Powered Supply Chain Portal

An enterprise-grade logistics management system developed for **EximpCore Trading**. This application integrates real-time data analytics, role-based access control (RBAC), and Large Language Model (LLM) capabilities to streamline export-import operations.

## ✨ Key Features

* **🔐 Dual-Role Authentication:** Secure login system with separate interfaces for **Administrators** (Full Control) and **Interns/Users** (View-Only Tracking).
* **📊 Interactive Analytics:** Dynamic dashboards using Plotly to track trade volume, shipment status, and destination-wise market value.
* **🤖 AI Logistics Assistant (RAG):** Integrated with **Google Gemini Pro** to analyze shipment logs and provide strategic insights using Retrieval-Augmented Generation (RAG).
* **⚠️ Smart Anomaly Detection:** Automated notification system that flags high-value transaction risks and critical shipment delays in real-time.
* **📝 Live Database Management:** Admin-exclusive data editor for instant synchronization of inventory and fleet logs directly from the UI.

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Framework:** Streamlit
* **Data Analysis:** Pandas, NumPy
* **Visualization:** Plotly Express
* **AI/LLM:** Google Generative AI (Gemini Pro API)
* **Deployment:** Streamlit Cloud

## 🚀 Installation & Local Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/smart-logistics-portal.git](https://github.com/YOUR_USERNAME/smart-logistics-portal.git)
    cd smart-logistics-portal
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key:**
    - Obtain a free API key from [Google AI Studio](https://aistudio.google.com/).
    - Replace `YOUR_GEMINI_API_KEY` in `app.py` with your actual key.

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 🎯 Project Objectives & Business Impact

This project demonstrates the practical application of **Computer Science** in the **Supply Chain & Trading** industry. By implementing this portal, a company can:
- **Reduce Manual Errors:** Automated tracking and data entry validation.
- **Enhance Decision Making:** AI-driven insights from complex logistics data.
- **Improve Security:** Ensure sensitive financial data is only accessible to authorized administrators.
- **Proactive Risk Management:** Detect anomalies and shipment delays before they impact the bottom line.

---
**Developed by:** [Mouno Uddin]  

