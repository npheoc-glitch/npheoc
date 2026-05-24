import streamlit as st
import pandas as pd
import numpy as np
import datetime

# =====================================================================
# 1. PAGE CONFIGURATION & THEME CUSTOMIZATION
# =====================================================================
st.set_page_config(
    page_title="Ghana Integrated Public Health Emergency Platform (GIPHEP)",
    page_icon="🇬🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Color System Injection (Matching Guidelines)
# Green: Stable/Prepared | Amber: Alert | Red: Active Response | Blue: Info | Grey: Inactive
st.markdown("""
    <style>
        :root {
            --green: #006B3F;
            --yellow: #FCD116;
            --red: #CE1126;
            --amber: #D97706;
            --blue: #2563EB;
            --grey: #6B7280;
        }
        /* Top Navigation Header Styling */
        .main-header-box {
            background-color: #ffffff;
            padding: 15px 20px;
            border-radius: 10px;
            border-bottom: 3px solid var(--red);
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .flag-strip {
            height: 6px;
            display: flex;
            margin-bottom: 10px;
        }
        .flag-red { background-color: var(--red); flex: 1; }
        .flag-yellow { background-color: var(--yellow); flex: 1; }
        .flag-green { background-color: var(--green); flex: 1; }
        
        /* Operational Operational Status Banner styling */
        .status-banner {
            background-color: #FFFBEB;
            border-left: 5px solid var(--amber);
            padding: 12px 20px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        /* KPI Card custom styling */
        .kpi-container {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid var(--green);
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .kpi-critical {
            border-left-color: var(--red) !important;
        }
        .kpi-warning {
            border-left-color: var(--amber) !important;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. APPLICATION HEADER & BRANDING
# =====================================================================
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
    st.markdown("<h2 style='color: #006B3F; margin-top: 5px;'>Ghana Integrated Public Health Emergency Operations Platform (GIPHEOP)</h2>", unsafe_allow_html=True)
    st.caption("Powered by Ghana National Public Health Emergency Operations Centre (PHEOC) & Ghana Health Service")
with col_logo2:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpuQVNB3Y2X4GTxYETRwhMrTLqRJX3Iz7BeQ&s", width=60)

# =====================================================================
# 3. NATIONAL OPERATIONAL STATUS BANNER (MIGRATED & REVISED)
# =====================================================================
# Updated exactly matching requested structural content values
st.markdown("""
    <div class="status-banner">
        <span style="font-size: 18px;">🟠 <b>ALERT LEVEL: HEIGHTENED SURVEILLANCE & PREPAREDNESS</b></span><br>
        <span style="font-size: 14px;"><b>Event:</b> Ebola Virus Disease (EVD) and Bundibugyo Disease Monitoring &nbsp;|&nbsp; 
        <b>Operational Status:</b> Alert Mode Activated &nbsp;|&nbsp; 
        <b>Last Updated:</b> 23 May 2026 | 04:15 GMT</span>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# 4. SIDEBAR NAVIGATION STRUCTURE (MIGRATED FROM FINAL REVISIONS)
# =====================================================================
st.sidebar.markdown("<h3 style='color: #FCD116;'>Navigation Room</h3>", unsafe_allow_html=True)

# Define exactly the functional groups from the Word Document Checklist
nav_category = st.sidebar.radio(
    "Select Module Component:",
    [
        "National Situation Room",
        "Surveillance Intelligence",
        "Laboratory Intelligence",
        "Emergency Coordination",
        "Contact Tracing",
        "Risk Assessment & Forecasting",
        "SitRep & Reporting"
    ]
)

# Shared Mock Field Datasets for Live Visualization
@st.cache_data
def get_historical_epi_data():
    dates = pd.date_range(start="2026-05-01", end="2026-05-23", freq="D")
    data = pd.DataFrame({
        'Date': dates,
        'Suspected': np.random.randint(2, 12, size=len(dates)),
        'Confirmed': np.random.randint(0, 3, size=len(dates)),
        'Alerts Received': np.random.randint(5, 20, size=len(dates))
    })
    return data

# =====================================================================
# MODULE CODEBLOCKS 
# =====================================================================

# ---------------------------------------------------------------------
# MODULE 1: National Situation Room (Executive Overview Component)
# ---------------------------------------------------------------------
if nav_category == "National Situation Room":
    st.markdown("### 📊 Executive Overview")
    
    # Recommended National Situation Summary Cards (CARDS 1 - 9 Implementation)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<div class="kpi-container"><h4>Suspected Cases</h4><h2>14</h2><small style="color:gray;">Cumulative National</small></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="kpi-container kpi-critical"><h4>Confirmed Cases</h4><h2>0</h2><small style="color:red;">0 Active Isolated</small></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="kpi-container kpi-warning"><h4>New Cases (24h)</h4><h2>+2</h2><small style="color:orange;">Pending Lab Results</small></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="kpi-container"><h4>Deaths Reported</h4><h2>0</h2><small style="color:gray;">CFR: 0.0%</small></div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="kpi-container"><h4>Case Fatality Rate</h4><h2>0.0%</h2><small style="color:gray;">Calculated CFR</small></div>', unsafe_allow_html=True)
        
    st.write("")
    col6, col7, col8, col9 = st.columns(4)
    with col6:
        st.markdown('<div class="kpi-container"><h4>Regions Reporting</h4><h2>3 / 16</h2><small style="color:gray;">Active Watch</small></div>', unsafe_allow_html=True)
    with col7:
        st.markdown('<div class="kpi-container"><h4>Districts Active</h4><h2>8</h2><small style="color:gray;">Under Surveillance</small></div>', unsafe_allow_html=True)
    with col8:
        st.markdown('<div class="kpi-container"><h4>Lab Positivity Rate</h4><h2>0.0%</h2><small style="color:gray;">Testing Matrix Base</small></div>', unsafe_allow_html=True)
    with col9:
        st.markdown('<div class="kpi-container kpi-critical"><h4>Alerts Investigated</h4><h2>100%</h2><small style="color:green;">Within 24h Threshold</small></div>', unsafe_allow_html=True)

    st.write("")
    
    # Layout Content Matrix
    panel_col1, panel_col2 = st.columns([1.5, 1])
    
    with panel_col1:
        st.markdown("#### 🗺️ Centerpiece Geo-Spatial National Ghana Map")
        st.info("Interactive layer map active overlays: Cases, Hotspots, Laboratories, RRT Deployments, Points of Entry (POEs), Flooding Risks, and Isolation Facilities.")
        
        # Simulating Map Visualization Interface with Dynamic Multi-layer toggles
        layers_selected = st.multiselect(
            "Toggle Visualization Map Overlay Layers:",
            ['Cases/Alert Cluster Locations', 'Hotspot Heatmaps', 'Diagnostic Laboratories Network', 'Active RRT Deployments', 'Border POEs Active Control', 'Environmental Flooding Markers'],
            default=['Cases/Alert Cluster Locations', 'Active RRT Deployments']
        )
        
        # Dynamic coordinate updates based on actual field locations
        map_points = pd.DataFrame({
            'lat': [5.556, 6.666, 10.985, 6.100],
            'lon': [-0.196, -1.616, -1.030, 0.600],
            'Location': ['Greater Accra (PHEOC HQ)', 'Ashanti (KCCR Support)', 'Upper East (Active Alert Cluster)', 'Volta (Enhanced Surveillance Zone)']
        })
        st.map(map_points)
        
    with panel_col2:
        st.markdown("#### 🚨 Immediate Operational Priorities (Next 24 Hours)")
        priorities = [
            "🚨 **Deploy RRT to Upper East** - Investigate 3 fresh suspected cluster validations.",
            "📡 **Activate enhanced surveillance in Volta** - Scale cross-border checkpoints tracking.",
            "📦 **Scale up IPC logistics** - Distribute Personal Protective Equipment (PPE) modules to regional holding centers.",
            "🔬 **Verify 5 pending alerts** - Streamline laboratory transfer routes tracking.",
            "📄 **Submit regional SitReps by 18:00 GMT** - National synthesis submission window close."
        ]
        for priority in priorities:
            st.markdown(f'<div style="padding: 8px; margin-bottom: 5px; background: #FFF; border-left: 3px solid #CE1126; font-size:13px;">{priority}</div>', unsafe_allow_html=True)

        st.markdown("#### ⏳ Incident Operations Timeline")
        timeline_events = pd.DataFrame({
            "Time (GMT)": ["02:15", "04:15", "07:30", "11:00", "14:20"],
            "Event Log": ["Alert validation triggered in Upper East Region", "National Banner status updated to Heightened Surveillance Mode", "PPE Logistics bundle dispatch authorization signed", "Specimen packages received safely at NMIMR facilities", "Border screening checks reported unified baseline figures"]
        })
        st.dataframe(timeline_events, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------
# MODULE 2: Surveillance Intelligence
# ---------------------------------------------------------------------
elif nav_category == "Surveillance Intelligence":
    st.markdown("### 📡 Surveillance Intelligence Module")
    
    tab_trends, tab_thresholds, tab_stratification = st.tabs(["Epidemic Trends & Forecasting", "Threshold Performance Alerts", "District Risk Classification"])
    
    with tab_trends:
        st.markdown("#### 📈 Epidemic Curves & Forecasting Engine")
        historical_df = get_historical_epi_data()
        
        # Interactive chart structure mapping Date-spacing, legends, annotations
        st.line_chart(historical_df, x='Date', y=['Alerts Received', 'Suspected'], color=["#2563EB", "#CE1126"])
        st.caption("Epi Curve Figure: Date metrics mapping tracking alerts context vs actual hospital suspected presentations.")
        
    with tab_thresholds:
        st.markdown("#### ⚠️ Real-Time Threshold Cross Monitoring")
        st.warning("Automated trigger systems detecting critical sentinel indicators or unusual biological activity.")
        
        threshold_logs = pd.DataFrame({
            "Indicator Metric": ["Cholera Threshold", "Meningitis Alert Line", "Unusual Mortality Cluster"],
            "Location Zone": ["Greater Accra (Coastal)", "Upper West Districts", "Eastern Region Sector Delta"],
            "Status Flag": ["Threshold Exceeded Line Crossed", "Alert Level Passed Threshold", "Statistical Anomaly Detected"],
            "Response Code": ["🔴 CRITICAL RESPONSE ACTIVE", "🟠 HEIGHTENED MONITORING", "🔴 INVESTIGATION TRIGGERED"]
        })
        st.table(threshold_logs)
        
    with tab_stratification:
        st.markdown("#### 🗺️ District Risk Classification Matrix")
        st.info("A map-linked sortable matrix categorizing active zones based on epidemiological score equations.")
        
        risk_data = pd.DataFrame({
            "District Unit Name": ["Bawku Central", "Accra Metropolitan", "Tema West", "Ketuan Border Delta", "Tamale Metro"],
            "Surveillance Weight Score": [88.5, 74.2, 61.0, 58.4, 34.1],
            "Risk Band Classification": ["🔴 High Risk Status", "🔴 High Risk Status", "🟠 Medium Assessment", "🟠 Medium Assessment", "🟢 Low/Stable Base"],
            "Mobility Density Indicator": ["Severe Cross-Border", "High Intranational", "High Hub Logistics", "Moderate Interface", "Low Stable Flow"]
        })
        st.dataframe(risk_data.sort_values(by="Surveillance Weight Score", ascending=False), use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------
# MODULE 3: Laboratory Intelligence
# ---------------------------------------------------------------------
elif nav_category == "Laboratory Intelligence":
    st.markdown("### 🔬 Laboratory Intelligence Module")
    
    st.markdown("#### 🏢 Laboratory Network Status Framework")
    lab_status_df = pd.DataFrame({
        "Laboratory Network Entity": ["Noguchi Memorial Institute for Medical Research (NMIMR)", "Kumasi Centre for Collaborative Research (KCCR)", "National Public Health Reference Laboratory (NPHRL)"],
        "Operational Status Indicator": ["🟢 FULLY ACTIVE", "🟢 FULLY ACTIVE", "🟢 FULLY ACTIVE"],
        "Turnaround Time (TAT Record)": ["18 Hours Certified", "24 Hours Certified", "12 Hours Certified"],
        "Specimen Processing Safe Backlogs": ["0 Packages", "2 Packages Pending", "0 Packages"]
    })
    st.dataframe(lab_status_df, use_container_width=True, hide_index=True)
    
    st.markdown("#### 📦 Specimen Transport Tracking Grid")
    col_tracking_info, col_pos_trends = st.columns([1.2, 1])
    
    with col_tracking_info:
        st.info("Live Courier tracking logs via regional hubs to central reference nodes.")
        transit_df = pd.DataFrame({
            "Sample ID": ["EVD-GH-024", "BDBV-GH-005", "VHF-GH-089"],
            "Origin Hub": ["Upper East Regional Hospital", "Volta Border Checkpoint Clinic", "Tema General Isolation Ward"],
            "Destination Center": ["NMIMR Accra", "NPHRL Accra", "NMIMR Accra"],
            "Transit Lifecycle Status": ["🚚 In-Transit via Air Link", "🔬 Under Processing Stage", "🟢 Safely Logged & Verified Completed"]
        })
        st.dataframe(transit_df, use_container_width=True, hide_index=True)
        
    with col_pos_trends:
        st.markdown("##### 📊 Pathogen Positivity Tracking Vectors")
        # Displaying zero-positivity state required for active Ebola verification baseline
        st.metric(label="Ebola Virus (Zaire Baseline Strain)", value="0 / 24 Samples Checked", delta="0% Positive")
        st.metric(label="Bundibugyo Disease Strain Baseline", value="0 / 24 Samples Checked", delta="0% Positive")

# ---------------------------------------------------------------------
# MODULE 4: Emergency Coordination
# ---------------------------------------------------------------------
elif nav_category == "Emergency Coordination":
    st.markdown("### 🏢 Incident Management System (IMS) & Emergency Coordination")
    
    st.markdown("#### ⚡ Active Incident Management Structure")
    
    # Render exactly matching specific table values from the revision documentation
    ims_data = pd.DataFrame({
        "Section Pillar Component": ["Operations Section", "Planning Section", "Logistics Section", "Finance/Administration Section"],
        "Activation Lifecycle Status": ["🟢 ACTIVE STATUS", "🟢 ACTIVE STATUS", "🟠 PARTIAL ACTIVATION MODALITY", "⚪ STANDBY STRUCTURAL DEPLOYMENT"],
        "Section Appointed Lead Officer": ["Dr. Emergency Lead Operations", "Senior Epidem. Coordination Officer", "Director Supply Chains Modalities", "Finance Control Supervisor"]
    })
    st.table(ims_data)
    
    st.markdown("#### 🛠️ Operational Component Trackers")
    col_rrt, col_res = st.columns(2)
    
    with col_rrt:
        st.markdown("##### 🚀 Rapid Response Teams (RRT) Deployment Hub")
        rrt_log = pd.DataFrame({
            "Deployment RRT ID": ["RRT-Alpha-01", "RRT-Beta-04"],
            "Assigned Destination Target": ["Upper East Watch Zone", "Volta Border Point Terminal"],
            "Current Assignment Status": ["Active Field Investigations Underway", "Deployment En-Route Transit Phase"]
        })
        st.dataframe(rrt_log, use_container_width=True, hide_index=True)
        
    with col_res:
        st.markdown("##### 📊 Critical Emergency Resource Levels")
        st.progress(0.85, text="Available Holding Isolation Beds: 85% Buffer Capacity Safe")
        st.progress(0.62, text="PPE Logistics Reserves: 62% Stock Level Verification")
        st.progress(0.90, text="Assigned Fleet Vehicle Assets Readiness: 90% High Profile Alert Ready")

# ---------------------------------------------------------------------
# MODULE 5: Contact Tracing
# ---------------------------------------------------------------------
elif nav_category == "Contact Tracing":
    st.markdown("### 👥 Operational DHIS2 Contact Tracing Interface")
    st.success("Synchronized workflows connected via local mobile networks data updates to backend registry records.")
    
    col_ct1, col_ct2, col_ct3 = st.columns(3)
    with col_ct1:
        st.metric(label="Total Linked Contacts Registered", value="42 Profiles", delta="Active Monitoring")
    with col_ct2:
        st.metric(label="Successful 24h Daily Follow-up Rate", value="100%", delta="Threshold Achieved")
    with col_ct3:
        st.metric(label="Symptom Flags Triggered Log", value="0 Alerts", delta="0 Critical Status")
        
    st.markdown("#### 🗂️ Active Case-Contact Association Ledger")
    contact_registry = pd.DataFrame({
        "Associated Index Case ID": ["EVD-SUSP-004", "EVD-SUSP-004", "EVD-SUSP-011"],
        "Contact Tracking ID": ["CT-ACC-901", "CT-ACC-902", "CT-BOL-145"],
        "Relationship Vectors": ["Immediate Household Member", "Primary Clinical Responder", "Transport Logistics Contact"],
        "Daily Follow-up Checklist status": ["🟢 Checked - Normal Temperature", "🟢 Checked - Normal Temperature", "⏳ Field Visit Schedule Set"]
    })
    st.dataframe(contact_registry, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------
# MODULE 6: Risk Assessment & Forecasting
# ---------------------------------------------------------------------
elif nav_category == "Risk Assessment & Forecasting":
    st.markdown("### 🧠 Risk Assessment Engine, Predictive Modeling & Early Warning System")
    
    col_risk1, col_risk2 = st.columns(2)
    with col_risk1:
        st.markdown("#### 🔀 Population Mobility Vector Overlays")
        st.info("Tracking public transport network nodes, commercial corridors, and marketplace flows from active alert zones to high-density hubs.")
        st.caption("Forecasting Models show an elevated risk vector trending towards regional transport terminals if primary clusters confirm positive.")
        
    with col_risk2:
        st.markdown("#### 🌧️ Environmental & Meteorological Signals Integration")
        st.info("Correlating live rainfall statistics and flood-risk vector indicators against local healthcare facility infrastructure access paths.")
        st.markdown("⚠️ **Weather/Flood Warning:** Southern coastal sectors display elevated logistical risk profiles which could slow vehicle response timelines.")

# ---------------------------------------------------------------------
# MODULE 7: SitRep & Reporting
# ---------------------------------------------------------------------
elif nav_category == "SitRep & Reporting":
    st.markdown("### 📄 Automated SitRep & Reporting Framework")
    st.info("System integration converts internal operational tracking analytics into standard WHO AFRO compliance documentation formats.")
    
    st.markdown("#### 🖨️ Situation Report (SitRep) Builder Suite")
    st.write("Generate and download regional and national bulletin summaries automatically:")
    
    col_actions1, col_actions2 = st.columns(2)
    with col_actions1:
        st.selectbox("Select Template Structure Compliance Target:", ["WHO AFRO Standard Standard Template v4", "National PHEOC Executive Brief Outline", "GHS External Stakeholders Bulletin Summary"])
        st.text_input("Enter Document Summary Reference ID Code:", "PHEOC-EVD-2026-SR-01")
    with col_actions2:
        st.write("")
        st.write("")
        st.button("⚙️ Trigger Automated Synthesis Compile Engine", use_container_width=True)
        
    st.write("---")
    st.markdown("#### 💾 Integrated Export Center Hub")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📥 Download Compiled National Flash SitRep (PDF Format Documentation)",
            data="Sample Content Generated from Streamlit Public Health Emergency Operational Export Core.",
            file_name="GIPHEOP_National_EVD_SitRep_2026-05-23.pdf",
            mime="application/pdf"
        )
    with col_dl2:
        st.download_button(
            label="📥 Export Live Laboratory Data Vectors (CSV Format)",
            data="Lab_ID,Status,TAT\nNMIMR,Active,18h\nKCCR,Active,24h\nNPHRL,Active,12h",
            file_name="GIPHEOP_Lab_Metrics.csv",
            mime="text/csv"
        )

# =====================================================================
# SYSTEM FOOTER DATA & DISCLOSURES
# =====================================================================
st.markdown("---")
col_foot1, col_foot2 = st.columns(2)
with col_foot1:
    st.markdown("<small style='color:gray;'>System Security Level: Protected Emergency Communication Interface Layer.</small>", unsafe_allow_html=True)
with col_foot2:
    st.markdown("<p style='text-align: right;'><small style='color:gray;'>Ghana National Public Health Emergency Operations Platform © 2026 All Rights Reserved.</small></p>", unsafe_allow_html=True)
