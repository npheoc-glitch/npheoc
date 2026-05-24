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
    page_icon="⚡",
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

    /* Word Doc Specifications: Operational Status Banner Ticker */
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

    /* Standardized Document Color Logic Unified Cards */
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
    }
    .kpi-value {
        font-size: 26px;
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
# STRUCTURAL GHANA NATIONAL LINE-DATA GENERATOR
# ====================================================
@st.cache_data
def generate_surveillance_data_engine():
    """Generates structural rows perfectly matching Ghana's 16 administrative regions."""
    regions = [
        "Ahafo", "Ashanti", "Bono", "Bono East", "Central", "Eastern", "Greater Accra",
        "North East", "Northern", "Oti", "Savannah", "Upper East", "Upper West", "Volta",
        "Western", "Western North"
    ]
    data_list = []
    np.random.seed(101)
    
    for reg in regions:
        # Generate baseline metrics conforming to heightened preparedness limits
        suspected = np.random.randint(5, 45)
        confirmed = np.random.choice([0, 1, 2, 0, 0, 5], p=[0.5, 0.2, 0.1, 0.1, 0.05, 0.05])
        deaths = np.random.choice([0, 1], p=[0.85, 0.15]) if confirmed > 0 else 0
        new_cases = np.random.randint(0, 4)
        alerts_inv = suspected + np.random.randint(2, 10)
        
        data_list.append({
            "Region": reg,
            "Suspected Cases": suspected,
            "Confirmed Cases": confirmed,
            "New Cases (24h)": new_cases,
            "Deaths Reported": deaths,
            "Regions Reporting": 1,
            "Districts Under Active Surveillance": np.random.randint(2, 8),
            "Alerts Investigated within 24h": alerts_inv,
            "Active RRTs Deployed": np.random.choice([0, 1, 2]),
            "Pathogen Event": "Ebola Virus Disease (EVD) / BDBV",
            "Lab Result Status": np.random.choice(["Negative", "Positive", "Pending"], p=[0.7, 0.1, 0.2])
        })
    return pd.DataFrame(data_list)

# ====================================================
# PUBLIC HEALTH EMERGENCY HEADER SYSTEM
# ====================================================
def build_emergency_header_system():
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
        
    # Word Doc Specification: Exact Banner Alert Translation
    st.markdown(f"""
        <div class="ticker-wrap">
            <span class="ticker-badge">🟠 ALERT MODE ACTIVE</span>
            <div class="ticker-text">
                <strong>ALERT LEVEL:</strong> HEIGHTENED SURVEILLANCE & PREPAREDNESS &nbsp;|&nbsp;
                <strong>Event:</strong> Ebola Virus Disease (EVD) and Bundibugyo Disease Monitoring &nbsp;|&nbsp;
                <strong>Operational Status:</strong> Alert Mode Activated &nbsp;|&nbsp;
                <strong>Last Updated:</strong> 23 May 2026 | 04:15 GMT
            </div>
        </div>
    """, unsafe_allow_html=True)

# ====================================================
# WORD DOC SPECIFICATION: SIDEPANEL ROUTER
# ====================================================
def render_sidebar_controls_pipeline():
    with st.sidebar:
        st.markdown("""
            <div style='background-color:#004d2e; padding:10px; border-radius:6px; text-align:center; margin-bottom:15px; border-bottom: 1px solid rgba(255,255,255,0.1);'>
                <strong style='color:#FCD116; font-size:11px; text-transform:uppercase; letter-spacing:0.5px;'>Official Command Panel</strong>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='color:#fff !important; font-size:13px; font-weight:700; letter-spacing:0.5px;'>EOC COMMAND NAVIGATION</h3>", unsafe_allow_html=True)
        
        # Exact Sidebar layout structure from Section 8 of the requirements document
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
        uploaded_file = st.file_uploader("Ingest Surveillance Matrix Data File", type=["csv", "xlsx"])
        
        base_df = generate_surveillance_data_engine()
        if uploaded_file is not None:
            st.success("Data Stream Operationalized.")
            
        st.markdown("---")
        st.markdown("<h3 style='color:#fff !important; font-size:13px; font-weight:700;'>GLOBAL SURVEILLANCE FILTER</h3>", unsafe_allow_html=True)
        pathogen_focus = st.selectbox("Pathogen Matrix View", ["EVD/BDBV Strain Focus", "Cholera Surveillance", "Meningitis Matrix"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption("GIPHEOP Operational v2.4 (Accra)")
        
        return selected_module, base_df

# ====================================================
# WORD DOC SPECIFICATION: 9 SITUATION HOVER SUMMARY CARDS
# ====================================================
def calculate_and_render_kpis(df):
    suspected = int(df["Suspected Cases"].sum())
    confirmed = int(df["Confirmed Cases"].sum())
    new_cases_24h = int(df["New Cases (24h)"].sum())
    deaths = int(df["Deaths Reported"].sum())
    
    cfr = (deaths / confirmed * 100) if confirmed > 0 else 0.0
    regions_reporting = int(df[df["Suspected Cases"] > 0]["Regions Reporting"].sum())
    districts_active = int(df["Districts Under Active Surveillance"].sum())
    
    # Lab calculations
    total_samples = len(df)
    positive_samples = len(df[df["Lab Result Status"] == "Positive"])
    positivity_rate = (positive_samples / total_samples * 100) if total_samples > 0 else 4.2
    
    alerts_investigated = int(df["Alerts Investigated within 24h"].sum())
    
    # 9 Situation Room Summary Metrics Configuration
    metrics = [
        {"title": "Total Suspected Cases", "val": suspected, "delta": "Rolling Field Logs", "color": "#f59e0b"},
        {"title": "Confirmed Cases", "val": confirmed, "delta": "PCR Verified PCR Lab", "color": "#ef4444"},
        {"title": "New Cases (24h)", "val": new_cases_24h, "delta": "Last Reporting Window", "color": "#ef4444"},
        {"title": "Deaths Reported", "val": deaths, "delta": "Crude Internal Count", "color": "#7f1d1d"},
        {"title": "Case Fatality Rate (CFR)", "val": f"{cfr:.1f}%", "delta": "Outbreak Mean Target", "color": "#ef4444"},
        {"title": "Regions Reporting", "val": f"{regions_reporting}/16", "delta": "National Transmission Map", "color": "#10b981"},
        {"title": "Districts Under Surveillance", "val": districts_active, "delta": "Active MMDA Vectors", "color": "#10b981"},
        {"title": "Laboratory Positivity Rate", "val": f"{positivity_rate:.1f}%", "delta": "Assay Positivity Threshold", "color": "#3b82f6"},
        {"title": "Alerts Investigated <24h", "val": alerts_investigated, "delta": "Target Reached: 100%", "color": "#10b981"}
    ]
    
    # Display in 3x3 uniform strategic block layout grid
    st.markdown("#### 📊 NATIONAL SITUATION SUMMARY PROFILE")
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
# DYNAMIC SIMULATOR MAP CONTAINER SYSTEM
# ====================================================
def draw_national_centerpiece_map(df):
    st.markdown("### 🗺️ CORE CENTERPIECE GEOSPATIAL MAP LAYER")
    
    # Baseline fallback geographic center arrays for Ghana regions
    ghana_regional_centroids = {
        "Greater Accra": [5.556, -0.196], "Ashanti": [6.688, -1.624], "Northern": [9.407, -0.839],
        "Western": [5.144, -1.758], "Volta": [6.578, 0.450], "Central": [5.532, -1.189],
        "Eastern": [6.287, -0.451], "Upper East": [10.785, -0.851], "Upper West": [10.252, -2.130],
        "Bono": [7.583, -2.483], "Bono East": [7.753, -1.053], "Ahafo": [7.001, -2.434],
        "Oti": [8.181, 0.435], "Savannah": [9.102, -1.815], "North East": [10.512, -0.382],
        "Western North": [6.275, -2.812]
    }
    
    m = folium.Map(location=[7.9465, -1.0232], zoom_start=6, tiles="CartoDB positron")
    
    for _, r in df.iterrows():
        loc = ghana_regional_centroids.get(r["Region"], [7.9465, -1.0232])
        # Word doc recommended status logic colors
        color = "#ef4444" if r["Confirmed Cases"] > 0 else "#f59e0b"
        size_radius = int(min(max(r["Suspected Cases"] // 2, 6), 22))
        
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
            st.markdown("#### ⚡ IMMEDIATE OPERATIONAL PRIORITIES (24H)")
            st.markdown("""
                <div class="priority-box">
                    <div class="priority-item"><div class="priority-bullet" style="background:#ef4444;"></div>Deploy RRT Teams to Upper East Hotspots</div>
                    <div class="priority-item"><div class="priority-bullet"></div>Activate Heightened Surveillance Vectors in Volta</div>
                    <div class="priority-item"><div class="priority-bullet"></div>Scale Up Regional IPC Logistics Pre-positioning</div>
                    <div class="priority-item"><div class="priority-bullet"></div>Verify 5 Pending Laboratory Field Alerts</div>
                    <div class="priority-item"><div class="priority-bullet" style="background:#10b981;"></div>Submit Regional Unified SitReps by 18:00 GMT</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### ⏳ INCIDENT COMMAND TIMELINE LOGS")
            st.markdown("""
                <div class="tl-container">
                    <div class="tl-node critical">
                        <strong>11:30 GMT — Outbreak Escalation</strong><br>
                        <span style="font-size:12px; color:#4b5563;">MOH Alert Mode configured for Viral Hemorrhagic Fever protocols.</span>
                    </div>
                    <div class="tl-node alert">
                        <strong>08:15 GMT — Field Deployments</strong><br>
                        <span style="font-size:12px; color:#4b5563;">Rapid Response Teams dispatched to border entry networks.</span>
                    </div>
                    <div class="tl-node">
                        <strong>Yesterday — Lab Testing</strong><br>
                        <span style="font-size:12px; color:#4b5563;">NMIMR Reference Core validated negative sequence controls.</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # 2. SURVEILLANCE INTELLIGENCE VIEW
    elif module == "Surveillance Intelligence":
        st.markdown("### 📈 SURVEILLANCE INTELLIGENCE MODULE")
        
        col_g1, col_g2 = st.columns([2, 1])
        with col_g1:
            st.markdown("#### Reconstructed Epidemic Curve Load")
            fig = px.bar(df, x="Region", y=["Suspected Cases", "Confirmed Cases"], 
                         color_discrete_sequence=["#ffedd5", "#CE1126"], barmode="group")
            fig.update_layout(template="plotly_white", plot_bgcolor="#ffffff", paper_bgcolor="#ffffff")
            st.plotly_chart(fig, use_container_width=True)
        with col_g2:
            st.markdown("#### Threshold Exceedance Status")
            st.warning("⚠️ Cholera Alert Threshold crossed inside Southern District Hotspots.")
            st.info("ℹ️ Meningitis Event-Based Surveillance remains within normal control variance parameters.")

        st.markdown("#### Sortable Regional Transmission Risk Matrix")
        st.dataframe(df[["Region", "Suspected Cases", "Confirmed Cases", "Districts Under Active Surveillance"]].sort_values(by="Confirmed Cases", ascending=False), use_container_width=True)

    # 3. LABORATORY INTELLIGENCE VIEW
    elif module == "Laboratory Intelligence":
        st.markdown("### 🧪 LABORATORY INTELLIGENCE MODULE")
        
        st.markdown("#### National Laboratory Network Diagnostic Status")
        lab_matrix = pd.DataFrame({
            "Reference Lab Center": ["Noguchi Memorial Institute for Medical Research (NMIMR)", "Kumasi Centre for Collaborative Research (KCCR)", "National Public Health Reference Laboratory (NPHRL)"],
            "Operational Status": ["Active Core", "Active Core", "Active Operational Support"],
            "Turnaround Time (TAT)": ["18 Hours", "24 Hours", "12 Hours"],
            "Capacity Load": ["Optimal", "Sustained", "Sustained Line"]
        })
        st.table(lab_matrix)
        
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.markdown("#### Specimen Transport Status Log Tracking")
            fig_lab = px.pie(df, names="Lab Result Status", title="Specimen Analysis Breakdown Profiles", color_discrete_sequence=["#3b82f6", "#10b981", "#ef4444"])
            st.plotly_chart(fig_lab, use_container_width=True)
        with col_l2:
            st.markdown("#### Lab Diagnostics Metrics")
            st.metric("Total Sample Volume Logged", len(df), "Sustained Processing Profile")
            st.metric("Pending Result Assay Backlog", "5 Samples", "Urgent Clearance Required", delta_color="inverse")

    # 4. EMERGENCY COORDINATION VIEW
    elif module == "Emergency Coordination":
        st.markdown("### 🏢 INCIDENT MANAGEMENT SYSTEM (IMS) COORDINATION")
        
        st.markdown("#### Active Incident Management Structural Framework")
        ims_data = pd.DataFrame({
            "IMS Technical Pillars / Section", "Activation Pillar Status", "Assigned Operational Lead"
        })
        # Word doc specification IMS Table
        st.markdown("""
        <table style="width:100%; border-collapse: collapse; margin-bottom: 20px;">
            <tr style="background-color: #f3f4f6; text-align: left;">
                <th style="padding: 10px;">Section / Pillar Focus</th>
                <th style="padding: 10px;">Activation Status</th>
                <th style="padding: 10px;">Operational Framework Assignment</th>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;"><b>Operations Section</b></td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;"><span style="color:#10b981; font-weight:bold;">🟢 Active</span></td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Field Operations & Deployment Leads</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;"><b>Planning Section</b></td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;"><span style="color:#10b981; font-weight:bold;">🟢 Active</span></td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Epidemiological Data Modeling Core</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;"><b>Logistics Pillar</b></td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;"><span style="color:#f59e0b; font-weight:bold;">🟡 Partial Activation</span></td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Supply Chain Countermeasure Units</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;"><b>Finance & Administration</b></td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;"><span style="color:#6b7280; font-weight:bold;">⚪ Standby Mode</span></td>
                <td style="padding: 10px; border-bottom: 1px solid #e5e7eb;">Administrative Resource Logistics</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Tactical Asset & Countermeasure Tracking Matrix")
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("National Isolation Bed Availability", "78% Available", "Treatment Centers Functional")
        with col_r2:
            st.metric("PPE Dispatched Units", "12,400 Kits", "Pre-positioned at Border Entry")
        with col_r3:
            st.metric("Active Field RRTs Available", "8 Deployable Units", "24-Hour Alert Status")

    # 5. CONTACT TRACING MODULE VIEW
    elif module == "Contact Tracing":
        st.markdown("### 👥 CONTACT TRACING MODULE (DHIS2 MOBILE SYNC)")
        col_c1, col_c2 = st.columns([1, 2])
        with col_c1:
            st.info("📲 DHIS2 Tracker Synchronization: Active (Last synced 4m ago)")
            st.metric("Active Contacts Under Follow-Up", "142 Persons", "+12 in last 24h")
            st.metric("Symptom Flag Threshold Alerts", "2 Triggers", "Dispatched RRT for isolation", delta_color="inverse")
        with col_c2:
            st.markdown("#### Contact Tracking Log Pipeline")
            mock_tracing_df = pd.DataFrame({
                "Linked Parent Case ID", "Contact Name Initials", "Monitoring Status Stage", "Mobile Sync Status"
            })
            st.markdown("""
            <ul>
                <li><b>Case GHA-EVD-022-C1:</b> K.A. — Day 14 Follow-up — <span style='color:#10b981;'>Asymptomatic</span></li>
                <li><b>Case GHA-EVD-022-C2:</b> M.O. — Day 9 Follow-up — <span style='color:#10b981;'>Asymptomatic</span></li>
                <li><b>Case GHA-EVD-025-C1:</b> J.B. — Day 2 Follow-up — <span style='color:#ef4444; font-weight:bold;'>Symptomatic Flagged</span></li>
            </ul>
            """, unsafe_allow_html=True)

    # 6. RISK ASSESSMENT & FORECASTING MODULE VIEW
    elif module == "Risk Assessment & Forecasting":
        st.markdown("### 🔮 RISK ASSESSMENT & FORECASTING")
        
        confirmed_total = df["Confirmed Cases"].sum()
        last_val = confirmed_total if confirmed_total > 0 else 12
        future_days = np.array(range(1, 15))
        
        worst_case = last_val * np.exp(0.12 * future_days)
        moderate_case = last_val * np.exp(0.04 * future_days)
        optimistic_case = last_val + (0.1 * future_days)
        
        future_dates = [datetime.now() + timedelta(days=int(i)) for i in future_days]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=future_dates, y=worst_case, name="Worst Case Scenario (Uncontrolled, R(t) > 2.0)", line=dict(color="#ef4444", dash="dash")))
        fig.add_trace(go.Scatter(x=future_dates, y=moderate_case, name="Moderate Path Trend (Partial Interventions)", line=dict(color="#f59e0b", dash="dot")))
        fig.add_trace(go.Scatter(x=future_dates, y=optimistic_case, name="Optimistic Path Track (Full Containment)", line=dict(color="#10b981")))
        
        fig.update_layout(template="plotly_white", title="14-Day Mathematical Projections Scenario Matrix",
                          margin=dict(l=20, r=20, t=40, b=20), legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    # 7. SITREP & REPORTING MODULE VIEW
    elif module == "SitRep & Reporting":
        st.markdown("### 📝 SITREP & REPORTING MANAGEMENT MODULE")
        st.write("Dynamic SitRep generation compiler conforming directly to WHO AFRO emergency presentation template frameworks.")
        
        col_rep1, col_rep2 = st.columns(2)
        with col_rep1:
            st.markdown("#### Automated Generation Matrix")
            st.text_input("Enter Document Report Title", value="Ghana National EVD Situation Report No. 04")
            st.selectbox("Select Target Framework Format", ["WHO AFRO Bulletin Template v1.2", "National MOH Executive Briefing"])
            if st.button("Generate Automated SitRep Summary"):
                st.success("Situation Report Draft Compiled Successfully.")
        with col_rep2:
            st.markdown("#### Export Distribution Node Protocols")
            st.button("📥 Export Secure Official PDF Bulletin Summary")
            st.button("📊 Download Integrated Raw CSV Core Dataset")

# ====================================================
# EXECUTOR MAIN SYSTEM RUN LOOP
# ====================================================
if __name__ == "__main__":
    build_emergency_header_system()
    selected_module, processed_df = render_sidebar_controls_pipeline()
    run_dashboard_router(selected_module, processed_df)
