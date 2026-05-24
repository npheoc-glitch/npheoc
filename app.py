import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta

# ====================================================
# STREAMLIT PAGE & METADATA CONFIGURATION
# ====================================================
st.set_page_config(
    page_title="GIPHEOP — Ghana Integrated Public Health Emergency Operations Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Default Streamlit Elements to maintain clinical EOC dashboard aesthetics
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

# ====================================================
# INJECT OFFICIAL GLOBAL CSS BRAND COLORS & TYPOGRAPHY
# ====================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700;800&display=swap');
    
    :root {
        --green: #006B3F;
        --yellow: #FCD116;
        --red: #CE1126;
        --bg: #f4f7f6;
        --sidebar-dark: #004d2e;
        --text: #1f2937;
        --border: #e5e7eb;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f4f7f6 !important;
        color: #1f2937 !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stSidebar"] {
        background-color: #004d2e !important;
    }
    
    /* Ghana Brand Flag Striping */
    .flag-strip {
        height: 6px;
        display: flex;
        width: 100%;
        margin-bottom: 10px;
        border-radius: 4px;
        overflow: hidden;
    }
    .flag-red { background: #CE1126; flex: 1; }
    .flag-yellow { background: #FCD116; flex: 1; }
    .flag-green { background: #006B3F; flex: 1; }

    /* Operational Status Banner Ticker */
    .ticker-wrap {
        background: #fff;
        border-bottom: 3px solid #ff9f43;
        padding: 12px 20px;
        border-radius: 6px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .ticker-badge {
        background: #ff9f43;
        color: white;
        padding: 5px 12px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        border-radius: 4px;
        letter-spacing: 0.5px;
    }
    .ticker-text {
        font-size: 14px;
        font-weight: 600;
        color: #1f2937;
    }

    /* Standardized Document Unified Cards */
    .kpi-card-unified {
        background: #fff;
        border-radius: 10px;
        padding: 16px;
        border-left: 4px solid #94a3b8;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04);
    }
    .kpi-title {
        font-size: 11px;
        color: #6b7280;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
        min-height: 28px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 800;
        color: #111827;
        margin-top: 4px;
        line-height: 1.1;
    }
    .kpi-delta { font-size: 11px; font-weight: 600; margin-top: 4px; color: #64748b; }
    
    /* EOC Operational Priorities Panel */
    .priority-box {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
    }
    .priority-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 0;
        border-bottom: 1px solid #f3f4f6;
        font-size: 13px;
        font-weight: 500;
    }
    .priority-bullet {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #ff9f43;
    }

    /* Timeline styling */
    .tl-container {
        border-left: 2px solid #e5e7eb;
        padding-left: 15px;
        margin-left: 10px;
    }
    .tl-node {
        position: relative;
        margin-bottom: 15px;
    }
    .tl-node::before {
        content: '';
        position: absolute;
        left: -20px;
        top: 4px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #10b981;
    }
    .tl-node.alert::before { background: #f59e0b; }
    .tl-node.critical::before { background: #ef4444; }

    /* Global layout overrides */
    h3, h4, label, [data-testid="stMarkdownContainer"] p {
        color: #1f2937 !important;
    }
    .stSelectbox div div div {
        color: #1f2937 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ====================================================
# STRUCTURAL DYNAMIC MAPPING FOR TARGET FIELD LOGS
# ====================================================
@st.cache_data
def generate_surveillance_data_engine():
    """Generates structural rows based on the official schema columns from the field log dataset."""
    regions = [
        "Greater Accra", "Ashanti", "Bono", "Bono East", "Central", "Eastern", 
        "North East", "Northern", "Oti", "Savannah", "Upper East", "Upper West", "Volta",
        "Western", "Western North", "Ahafo"
    ]
    data_list = []
    
    # Base configuration drawn exactly from the active Greater Accra SITREP index row
    for reg in regions:
        if reg == "Greater Accra":
            data_list.append({
                "SitRep Number": "EVD-BDBV-SITREP-001",
                "Epidemiological Week": 22,
                "Reporting Period Start": "2026-05-18",
                "Reporting Period End": "2026-05-18",
                "Submission Date": "2026-05-24",
                "Reporting Level": "Regional",
                "Region": "Greater Accra",
                "Region Code": "GA",
                "Prepared By": "National PHEOC Epidemiology Team",
                "Total Emergencies / Active Incidents": 1,
                "Suspected Cases": 35,
                "Probable Cases": 2,
                "Confirmed Cases": 1,
                "Deaths": 0,
                "New Suspected Cases This Reporting Period": 24,
                "New Confirmed Cases This Reporting Period": 1,
                "Suspected Admissions": 10,
                "Confirmed Admissions": 1,
                "Occupied Isolation Beds": 10,
                "Surge Deployments": 10,
                "Total Admissions": 11,
                "Confirmed CFR (%)": 0,
                "Overall CFR (%)": 0,
                "Suspected Cases Change from Previous Period": 13,
                "Confirmed Cases Change from Previous Period": 0,
                "Deaths Change from Previous Period": 0,
                "Alerts Change from Previous Period": 25,
                "Key Epidemiological Update": "One confirmed BDBV case has been reported in Ghana.",
                "Key Preparedness Actions": "National coordination, laboratory readiness verification, PoE preparedness, and regional monitoring ongoing.",
                "Key Concern / Red Flag": "Sustaining readiness while minimizing misinformation and reporting fatigue.",
                "Overall Risk Level": "High",
                "Outbreak Strain": "Bundibugyo ebolavirus (BDBV)",
                "Global Suspected Cases": 530,
                "Global Confirmed Cases": 326,
                "Global Deaths": 135,
                "Ghana Importation Risk Level": "High",
                "Alerts Received": 12,
                "Alerts Verified": 2,
                "Alerts Investigated Within 24 Hours": 1,
                "Contacts Listed": 232,
                "Contacts Under Follow-up": 121,
                "Contacts Completed Follow-up": 19,
                "Samples Collected": 96,
                "Samples Tested": 26,
                "Positive Results": 1,
                "Negative Results": 25,
                "Pending Results": 2,
                "Average Turnaround Time (Hours)": 28,
                "Isolation Beds Available": 85,
                "HCW Suspected Cases": 0,
                "HCW Confirmed Cases": 0,
                "HCW Deaths": 0,
                "HCW Exposed": 3,
                "HCW Under Follow-up": 3,
                "HCWs Trained": 16,
                "PPE Stock Days": 21,
                "Chlorine Stock Days": 18,
                "VHF Kits Available": 12,
                "Functional Ambulances": 14,
                "Overall Readiness Score": 41,
                "Data Verified": "Yes",
                "Confidence Level": "Moderate"
            })
        else:
            # Baseline preparedness entries for secondary tracking regions
            data_list.append({
                "SitRep Number": "EVD-BDBV-SITREP-001",
                "Epidemiological Week": 22,
                "Reporting Period Start": "2026-05-18",
                "Reporting Period End": "2026-05-18",
                "Submission Date": "2026-05-24",
                "Reporting Level": "Regional",
                "Region": reg,
                "Region Code": reg[:2].upper(),
                "Prepared By": "Regional PHEOC Epidemiology Team",
                "Total Emergencies / Active Incidents": 0,
                "Suspected Cases": int(np.random.randint(2, 12)),
                "Probable Cases": 0,
                "Confirmed Cases": 0,
                "Deaths": 0,
                "New Suspected Cases This Reporting Period": int(np.random.randint(0, 5)),
                "New Confirmed Cases This Reporting Period": 0,
                "Suspected Admissions": int(np.random.randint(0, 3)),
                "Confirmed Admissions": 0,
                "Occupied Isolation Beds": int(np.random.randint(0, 2)),
                "Surge Deployments": 0,
                "Total Admissions": int(np.random.randint(0, 3)),
                "Confirmed CFR (%)": 0,
                "Overall CFR (%)": 0,
                "Suspected Cases Change from Previous Period": 0,
                "Confirmed Cases Change from Previous Period": 0,
                "Deaths Change from Previous Period": 0,
                "Alerts Change from Previous Period": int(np.random.randint(0, 5)),
                "Key Epidemiological Update": "Active surveillance ongoing. No active cases reported.",
                "Key Preparedness Actions": "Routine checking at designated monitoring points.",
                "Key Concern / Red Flag": "None identified.",
                "Overall Risk Level": "Moderate",
                "Outbreak Strain": "Bundibugyo ebolavirus (BDBV)",
                "Global Suspected Cases": 530,
                "Global Confirmed Cases": 326,
                "Global Deaths": 135,
                "Ghana Importation Risk Level": "High",
                "Alerts Received": int(np.random.randint(1, 6)),
                "Alerts Verified": int(np.random.randint(0, 2)),
                "Alerts Investigated Within 24 Hours": int(np.random.randint(0, 2)),
                "Contacts Listed": 0,
                "Contacts Under Follow-up": 0,
                "Contacts Completed Follow-up": 0,
                "Samples Collected": int(np.random.randint(2, 15)),
                "Samples Tested": int(np.random.randint(2, 10)),
                "Positive Results": 0,
                "Negative Results": int(np.random.randint(2, 10)),
                "Pending Results": int(np.random.randint(0, 2)),
                "Average Turnaround Time (Hours)": 24,
                "Isolation Beds Available": int(np.random.randint(10, 40)),
                "HCW Suspected Cases": 0,
                "HCW Confirmed Cases": 0,
                "HCW Deaths": 0,
                "HCW Exposed": 0,
                "HCW Under Follow-up": 0,
                "HCWs Trained": int(np.random.randint(2, 10)),
                "PPE Stock Days": 14,
                "Chlorine Stock Days": 14,
                "VHF Kits Available": int(np.random.randint(1, 5)),
                "Functional Ambulances": int(np.random.randint(1, 5)),
                "Overall Readiness Score": int(np.random.randint(30, 45)),
                "Data Verified": "Yes",
                "Confidence Level": "Moderate"
            })
    return pd.DataFrame(data_list)

# ====================================================
# PUBLIC HEALTH EMERGENCY HEADER SYSTEM
# ====================================================
def build_emergency_header_system(df):
    # Top Identity Ghana Strip Layout
    st.markdown("""
        <div class="flag-strip">
            <div class="flag-red"></div>
            <div class="flag-yellow"></div>
            <div class="flag-green"></div>
        </div>
    """, unsafe_allow_html=True)
    
    col_logo1, col_title, col_logo2 = st.columns([1, 7, 1])
    with col_logo1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Coat_of_arms_of_Ghana.svg/1280px-Coat_of_arms_of_Ghana.svg.png", width=65)
    with col_title:
        st.markdown("""
            <h2 style='color:#006B3F; margin:0; font-weight:800; font-size:25px; letter-spacing:0.2px;'>
                Ghana Integrated Public Health Emergency Operations Platform (GIPHEOP)
            </h2>
            <div style='color:#4b5563; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;'>
                National Outbreak Control & Emergency Command Architecture — Ministry of Health & GHS PHEOC
            </div>
        """, unsafe_allow_html=True)
    with col_logo2:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpuQVNB3Y2X4GTxYETRwhMrTLqRJX3Iz7BeQ&s", width=65)
        
    # Extraction parameters from target CSV instance mapping
    target_row = df[df["Region"] == "Greater Accra"].iloc[0]
    st.markdown(f"""
        <div class="ticker-wrap">
            <span class="ticker-badge">ALERT MODE ACTIVE</span>
            <div class="ticker-text">
                <strong>ALERT LEVEL:</strong> {target_row['Overall Risk Level'].upper()} ALERT &nbsp;|&nbsp;
                <strong>Outbreak Strain Focus:</strong> {target_row['Outbreak Strain']} &nbsp;|&nbsp;
                <strong>Epi Week:</strong> {target_row['Epidemiological Week']} &nbsp;|&nbsp;
                <strong>Submission Log Date:</strong> {target_row['Submission Date']}
            </div>
        </div>
    """, unsafe_allow_html=True)

# ====================================================
# SIDEPANEL ROUTER
# ====================================================
def render_sidebar_controls_pipeline():
    with st.sidebar:
        st.markdown("""
            <div style='background-color:#004d2e; padding:10px; border-radius:6px; text-align:center; margin-bottom:15px; border-bottom: 1px solid rgba(255,255,255,0.1);'>
                <strong style='color:#FCD116; font-size:11px; text-transform:uppercase; letter-spacing:0.5px;'>Official Command Panel</strong>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='color:#fff !important; font-size:13px; font-weight:700; letter-spacing:0.5px;'>EOC COMMAND NAVIGATION</h3>", unsafe_allow_html=True)
        
        modules = [
            "National Situation Room",
            "Surveillance Intelligence",
            "Laboratory Intelligence",
            "Emergency Coordination",
            "Contact Tracing",
            "Risk Assessment & Forecasting",
            "SitRep & Reporting"
        ]
        selected_module = st.selectbox("Select Operational Module View", modules)
        
        st.markdown("---")
        st.markdown("<h3 style='color:#fff !important; font-size:13px; font-weight:700;'>INGEST SITREP STREAM</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Ingest Surveillance Matrix Data File (CSV / XLSX)", type=["csv", "xlsx"])
        
        base_df = generate_surveillance_data_engine()
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    user_df = pd.read_csv(uploaded_file)
                else:
                    user_df = pd.read_excel(uploaded_file)
                if "Region" in user_df.columns and "Confirmed Cases" in user_df.columns:
                    base_df = user_df
                    st.success("Custom Data Matrix Ingested Successfully.")
            except Exception as e:
                st.error(f"Error parsing file schema. Falling back to structured storage.")
            
        st.markdown("---")
        st.markdown("<h3 style='color:#fff !important; font-size:13px; font-weight:700;'>GLOBAL SURVEILLANCE FILTER</h3>", unsafe_allow_html=True)
        st.selectbox("Pathogen Matrix View", ["BDBV Strain Focus (Current)", "Cholera Matrix", "Meningitis Matrix"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption("GIPHEOP Operational v2.2 (Accra)")
        
        return selected_module, base_df

# ====================================================
# 9 SITUATION HOVER SUMMARY CARDS FROM EXCEL SCHEMA
# ====================================================
def calculate_and_render_kpis(df):
    suspected = int(df["Suspected Cases"].sum())
    confirmed = int(df["Confirmed Cases"].sum())
    new_suspected = int(df["New Suspected Cases This Reporting Period"].sum())
    deaths = int(df["Deaths"].sum())
    probable = int(df["Probable Cases"].sum())
    
    contacts_listed = int(df["Contacts Listed"].sum())
    contacts_followup = int(df["Contacts Under Follow-up"].sum())
    samples_collected = int(df["Samples Collected"].sum())
    readiness_score = int(df["Overall Readiness Score"].max())
    
    # Grid config mapping row and column keys exactly
    metrics = [
        {"title": "Total Suspected Cases", "val": suspected, "delta": "Aggregated Country Logs", "color": "#f59e0b"},
        {"title": "Confirmed Cases", "val": confirmed, "delta": "PCR Verified Strains", "color": "#ef4444"},
        {"title": "Probable Cases", "val": probable, "delta": "Epi-Linked Field Logs", "color": "#7f1d1d"},
        {"title": "New Suspected Cases", "val": new_suspected, "delta": "Current Reporting Period", "color": "#f59e0b"},
        {"title": "Total Deaths Reported", "val": deaths, "delta": "Crude Fatality Metric", "color": "#7f1d1d"},
        {"title": "Contacts Listed", "val": contacts_listed, "delta": "Database Tracing Registry", "color": "#3b82f6"},
        {"title": "Contacts Under Follow-up", "val": contacts_followup, "delta": "Active Field Surveillance", "color": "#10b981"},
        {"title": "Total Samples Collected", "val": samples_collected, "delta": "Reference Lab Shipments", "color": "#3b82f6"},
        {"title": "Overall Readiness Score", "val": f"{readiness_score}/100", "delta": "Target Performance Index", "color": "#10b981"}
    ]
    
    st.markdown("#### NATIONAL SITUATION SUMMARY PROFILE")
    for row_idx in range(3):
        cols = st.columns(3)
        for col_idx in range(3):
            metric_data = metrics[row_idx * 3 + col_idx]
            with cols[col_idx]:
                st.markdown(f"""
                    <div class="kpi-card-unified" style="border-left-color: {metric_data['color']};">
                        <div class="kpi-title">{metric_data['title']}</div>
                        <div class="kpi-value">{metric_data['val']}</div>
                        <div class="kpi-delta">{metric_data['delta']}</div>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ====================================================
# CENTERPIECE GEOSPATIAL MAP LAYER
# ====================================================
def draw_national_centerpiece_map(df):
    st.markdown("### CORE CENTERPIECE GEOSPATIAL MAP LAYER")
    
    ghana_regional_centroids = {
        "Greater Accra": [5.556, -0.196], "Ashanti": [6.688, -1.624], "Bono": [7.583, -2.483], 
        "Bono East": [7.753, -1.053], "Central": [5.532, -1.189], "Eastern": [6.287, -0.451], 
        "North East": [10.512, -0.382], "Northern": [9.407, -0.839], "Oti": [8.181, 0.435], 
        "Savannah": [9.102, -1.815], "Upper East": [10.785, -0.851], "Upper West": [10.252, -2.130], 
        "Volta": [6.578, 0.450], "Western": [5.144, -1.758], "Western North": [6.275, -2.812], 
        "Ahafo": [7.001, -2.434]
    }
    
    m = folium.Map(location=[7.9465, -1.0232], zoom_start=6, tiles="CartoDB positron")
    
    for _, r in df.iterrows():
        loc = ghana_regional_centroids.get(r["Region"], [7.9465, -1.0232])
        color = "#ef4444" if r["Confirmed Cases"] > 0 else "#f59e0b"
        size_radius = int(min(max(int(r["Suspected Cases"]) // 2, 6), 22))
        
        folium.CircleMarker(
            location=loc,
            radius=size_radius,
            color=color,
            fill=True,
            fill_opacity=0.6,
            popup=f"<b>Region:</b> {r['Region']}<br><b>Confirmed:</b> {r['Confirmed Cases']}<br><b>Suspected:</b> {r['Suspected Cases']}"
        ).add_to(m)
        
    st_folium(m, height=420, width=1300, key="national_centerpiece_map")

# ====================================================
# SYSTEM CORE ROUTER ENGINE
# ====================================================
def run_dashboard_router(module, df):
    
    # 1. NATIONAL SITUATION ROOM MODULE VIEW
    if module == "National Situation Room":
        calculate_and_render_kpis(df)
        
        col_map, col_priority = st.columns([1.8, 1])
        with col_map:
            draw_national_centerpiece_map(df)
            
        with col_priority:
            st.markdown("#### IMMEDIATE OPERATIONAL PRIORITIES (24H)")
            st.markdown("""
                <div class="priority-box">
                    <div class="priority-item"><div class="priority-bullet" style="background:#ef4444;"></div>Verify pending reference laboratory samples at NMIMR</div>
                    <div class="priority-item"><div class="priority-bullet"></div>Replenish PPE regional stock configurations</div>
                    <div class="priority-item"><div class="priority-bullet"></div>Initiate simulation testing for referral SOP at KIA</div>
                    <div class="priority-item"><div class="priority-bullet"></div>Scale up RCCE sensitization against misinformation themes</div>
                    <div class="priority-item"><div class="priority-bullet" style="background:#10b981;"></div>Track active contacts currently listed under follow-up</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### INCIDENT COMMAND TIMELINE LOGS")
            st.markdown("""
                <div class="tl-container">
                    <div class="tl-node critical">
                        <strong>Active Transmission Matrix</strong><br>
                        <span style="font-size:12px; color:#4b5563;">One confirmed BDBV case reported inside Greater Accra region boundaries.</span>
                    </div>
                    <div class="tl-node alert">
                        <strong>Surveillance System Logs</strong><br>
                        <span style="font-size:12px; color:#4b5563;">12 alerts received across monitored entry networks. 2 verified internally.</span>
                    </div>
                    <div class="tl-node">
                        <strong>IMS System Ingestion</strong><br>
                        <span style="font-size:12px; color:#4b5563;">IMS Pillars Activated: Coordination, Surveillance, Lab, Case Management, IPC, RCCE, Logistics.</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # 2. SURVEILLANCE INTELLIGENCE VIEW
    elif module == "Surveillance Intelligence":
        st.markdown("### SURVEILLANCE INTELLIGENCE MODULE")
        
        col_g1, col_g2 = st.columns([2, 1])
        with col_g1:
            st.markdown("#### Regional Case Comparison Model")
            fig = px.bar(df, x="Region", y=["Suspected Cases", "Confirmed Cases"], 
                         color_discrete_sequence=["#ffedd5", "#CE1126"], barmode="group")
            fig.update_layout(template="plotly_white", plot_bgcolor="#ffffff", paper_bgcolor="#ffffff")
            st.plotly_chart(fig, use_container_width=True)
        with col_g2:
            st.markdown("#### Outbreak Context Parameters")
            st.warning("EVD-BDBV Strain Focus active: Surveillance networks operating at maximum capacity thresholds.")
            st.info("Event-Based Surveillance note: Some regions require refresher orientation on alert verification protocols.")

        st.markdown("#### National Surveillance Schema Grid Data")
        st.dataframe(df[["Region", "Suspected Cases", "Confirmed Cases", "New Suspected Cases This Reporting Period", "Alerts Received", "Contacts Listed"]], use_container_width=True)

    # 3. LABORATORY INTELLIGENCE VIEW
    elif module == "Laboratory Intelligence":
        st.markdown("### LABORATORY INTELLIGENCE MODULE")
        
        st.markdown("#### Certified Reference Lab Verification Core")
        lab_matrix = pd.DataFrame({
            "Reference Lab Network": ["Noguchi Memorial Institute (NMIMR)", "Kumasi Centre for Collaborative Research (KCCR)", "National Public Health Reference Lab (NPHRL)"],
            "Operational Status": ["Ready", "Ready", "Ready"],
            "Sample Transport Pathway": ["Functional", "Functional", "Functional"]
        })
        st.table(lab_matrix)
        
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.markdown("#### Specimen Diagnostic Outcomes")
            fig_lab = px.pie(df, names="Region", y="Samples Collected", title="Sample Tracking Distributions across Processing Nodes")
            st.plotly_chart(fig_lab, use_container_width=True)
        with col_l2:
            st.markdown("#### Processing Turnaround Logistics")
            st.metric("Average Turnaround Time", "28 Hours", "Target: Under 24 Hours")
            st.metric("Pending Results Backlog", "2 Samples", "Awaiting PCR Validation Pipeline")

    # 4. EMERGENCY COORDINATION VIEW
    elif module == "Emergency Coordination":
        st.markdown("### INCIDENT MANAGEMENT SYSTEM (IMS) COORDINATION")
        st.markdown("#### Structural Activation Tracker")
        
        st.markdown("""
        <table style="width:100%; border-collapse: collapse; margin-bottom: 20px;">
            <tr style="background-color: #f3f4f6; text-align: left;">
                <th style="padding: 10px;">Activated Operational Core Pillar</th>
                <th style="padding: 10px;">Status Flag</th>
                <th style="padding: 10px;">Target Objective Framework</th>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Coordination / Surveillance / Laboratory</td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;"><span style="color:#10b981; font-weight:bold;">Active</span></td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Verify transmission lines and maintain baseline logistics data</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Case Management / IPC / RCCE / Logistics</td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;"><span style="color:#10b981; font-weight:bold;">Active</span></td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Mitigate media misinformation and support healthcare settings</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Vaccination Preparedness / WASH / PoE</td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;"><span style="color:#f59e0b; font-weight:bold;">Pre-Activation Monitoring</span></td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Establish SOPs and coordinate borders</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.metric("PPE Stock Level Status", "21 Days Remaining", "Replenishment actions in progress")
        with col_c2:
            st.metric("Chlorine Stock Level", "18 Days Remaining", "Adequate local reserves")
        with col_c3:
            st.metric("Functional Field Ambulances", "14 Active Units", "Pre-positioned for medical triage")

    # 5. CONTACT TRACING MODULE VIEW
    elif module == "Contact Tracing":
        st.markdown("### CONTACT TRACING MODULE")
        
        col_ct1, col_ct2 = st.columns(2)
        with col_ct1:
            st.metric("Contacts Listed for Outbreak", "232 Individuals")
            st.metric("Contacts Under Active Follow-up", "121 Individuals")
        with col_ct2:
            st.metric("Contacts Completed Follow-up", "19 Individuals")
            st.info("System Tracking Efficiency: Active line lists maintained via SORMAS integration channels.")

    # 6. RISK ASSESSMENT & FORECASTING MODULE VIEW
    elif module == "Risk Assessment & Forecasting":
        st.markdown("### RISK ASSESSMENT & FORECASTING")
        
        st.markdown("#### Global Outbreak Comparison Metrics (BDBV Strain Focus)")
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            st.metric("Global Suspected Cases", "530")
        with col_g2:
            st.metric("Global Confirmed Cases", "326")
        with col_g3:
            st.metric("Global Deaths Recorded", "135")
            
        st.markdown("---")
        st.write("Mathematical 14-Day Readiness Projection Vectors based on structured scores.")
        future_days = np.array(range(1, 15))
        base_score = 41
        projection = base_score + (1.5 * future_days)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=future_days, y=projection, name="Target Ingestion Capacity Optimization Path", line=dict(color="#006B3F")))
        fig.update_layout(template="plotly_white", title="Expected Preparedness Ingestion Trend Index")
        st.plotly_chart(fig, use_container_width=True)

    # 7. SITREP & REPORTING MODULE VIEW
    elif module == "SitRep & Reporting":
        st.markdown("### SITREP & REPORTING MANAGEMENT MODULE")
        
        st.markdown("#### Core Log Details from Active File")
        st.info("File ID: 780a2620-7a71-43be-b2db-1b4254f3d25f | Submission Time: 2026-05-21")
        
        col_rep1, col_rep2 = st.columns(2)
        with col_rep1:
            st.markdown("#### Primary Gaps Identified")
            st.error("Logistics Gap: No logistics and funding for EVD. Severity classified as Moderate.")
            st.text_area("Priority Action Required", value="Replenish PPE stock and verify regional readiness via Ministry of Health channels.")
        with col_rep2:
            st.markdown("#### Information Dissemination Protocols")
            st.write("HCWs informed that licensed Zaire Ebola vaccine does not protect against BDBV strain variants.")
            st.write("Misinformation Theme Detected: False reports circulating on social media regarding 8 new confirmed cases in Ghana.")

# ====================================================
# EXECUTOR MAIN SYSTEM RUN LOOP
# ====================================================
if __name__ == "__main__":
    # Generate schema array matching rows
    processed_df = generate_surveillance_data_engine()
    build_emergency_header_system(processed_df)
    selected_module, processed_df = render_sidebar_controls_pipeline()
    run_dashboard_router(selected_module, processed_df)
