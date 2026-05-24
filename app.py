import streamlit as st
import pandas as pd
import numpy as np
import datetime

# =====================================================================
# 1. PAGE LAYOUT & ORIGINAL CSS ARCHITECTURE PRESERVATION
# =====================================================================
st.set_page_config(
    page_title="Ghana Integrated Public Health Emergency Platform (GIPHEP)",
    page_icon="🇬🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injecting HTML headers and styling directly from your layout configuration
st.markdown("""
    <style>
        /* Exact color scheme variables from user code */
        :root {
            --green: #006B3F;
            --yellow: #FCD116;
            --red: #CE1126;
            --bg: #f4f7f6;
            --sidebar-dark: #004d2e;
            --text: #1f2937;
            --border: #e5e7eb;
        }
        
        /* Flag strip layout component */
        .flag-strip {
            height: 6px;
            display: flex;
            margin-bottom: 15px;
        }
        .flag-red { background: var(--red); flex: 1; }
        .flag-yellow { background: var(--yellow); flex: 1; }
        .flag-green { background: var(--green); flex: 1; }

        /* Banner ticker background */
        .ticker-box {
            background: #fff;
            padding: 12px 20px;
            border-bottom: 2px solid var(--red);
            font-size: 14px;
            margin-bottom: 20px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        /* KPI panel style structural mappings */
        .kpi-card-custom {
            background: #fff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            border-left: 4px solid var(--green);
            margin-bottom: 10px;
        }
        .kpi-card-custom h4 {
            font-size: 11px;
            color: #6b7280;
            text-transform: uppercase;
            margin-bottom: 8px;
            font-weight: 600;
        }
        .kpi-card-custom h2 {
            font-size: 28px;
            color: #111827;
            font-weight: 800;
            margin: 0;
        }

        /* Status panel boxes */
        .panel-container {
            background: #fff;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 20px;
            overflow: hidden;
        }
        .panel-head-custom {
            padding: 15px 20px;
            background: #f9fafb;
            border-bottom: 1px solid var(--border);
        }
        .panel-head-custom h3 {
            font-size: 14px;
            font-weight: 700;
            color: var(--green);
            text-transform: uppercase;
            margin: 0;
        }
        .panel-body-custom {
            padding: 20px;
        }

        /* Custom typography components */
        .topbar-title-custom {
            font-size: 22px;
            font-weight: 800;
            color: var(--green);
            line-height: 1.2;
            margin: 0;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. BRANDING TOPBAR INTEGRATION
# =====================================================================
st.markdown("""
    <div class="flag-strip">
        <div class="flag-red"></div>
        <div class="flag-yellow"></div>
        <div class="flag-green"></div>
    </div>
""", unsafe_allow_html=True)

col_top_left, col_top_right = st.columns([2, 1])

with col_top_left:
    # Combining the layout structure components into a single container row
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 20px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Coat_of_arms_of_Ghana.svg/1280px-Coat_of_arms_of_Ghana.svg.png" width="55">
            <div>
                <h2 class="topbar-title-custom">Ghana Integrated Public Health Emergency Operations Platform (GIPHEOP)</h2>
                <small style="color: #64748b; font-weight: 500;">Powered by Ghana National PHEOC & Ghana Health Service</small>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_top_right:
    # Real-time counter and the second agency brand logo
    now_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: flex-end; gap: 20px; text-align: right;">
            <div>
                <small style="color:#64748b;">Last updated</small><br>
                <strong style="font-size:13px; color:#111827;">{now_time}</strong>
            </div>
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpuQVNB3Y2X4GTxYETRwhMrTLqRJX3Iz7BeQ&s" width="50">
        </div>
    """, unsafe_allow_html=True)

st.write("")

# =====================================================================
# 3. REVISED TICKER LOGIC (HEIGHTENED SURVEILLANCE CRITERIA)
# =====================================================================
st.markdown("""
    <div class="ticker-box">
        <strong style="color:var(--red)">ALERT LEVEL:</strong> 
        <span style="font-weight: 600; color: #1f2937;">HEIGHTENED SURVEILLANCE & PREPAREDNESS — Event: Ebola Virus Disease (EVD) and Bundibugyo Disease Monitoring</span>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# 4. SIDEBAR SELECTION CONTROLS (MIGRATED TAXONOMY)
# =====================================================================
st.sidebar.markdown("<h4 style='color:#FCD116; font-weight:700; margin-bottom:15px;'>GIPHEOP ROOMS</h4>", unsafe_allow_html=True)

room_selection = st.sidebar.radio(
    "Select Component:",
    [
        "📊 National Situation Room",
        "📡 Surveillance Intelligence",
        "🔬 Laboratory Intelligence",
        "🏢 Emergency Coordination",
        "👥 Contact Tracing Room",
        "🧠 Risk Assessment & Forecasting",
        "📄 SitRep & Reporting Center"
    ]
)

# Dataset cache tool configurations
@st.cache_data
def load_surveillance_trends():
    dates = pd.date_range(start="2026-05-01", end="2026-05-23", freq="D")
    return pd.DataFrame({
        'Date': dates,
        'Suspected Clusters': np.random.randint(1, 6, size=len(dates)),
        'Alerts Resolved': np.random.randint(8, 22, size=len(dates))
    }).set_index('Date')

# =====================================================================
# 5. MODULAR STRUCTURAL ROUTING VIEWPORTS
# =====================================================================

# ---------------------------------------------------------------------
# ROOM 1: National Situation Room
# ---------------------------------------------------------------------
if "National Situation Room" in room_selection:
    st.markdown("### Executive Overview Room")
    
    # 9 Structural KPI Metric Elements defined in reference guidelines
    kpi_cols_1 = st.columns(5)
    with kpi_cols_1[0]:
        st.markdown('<div class="kpi-card-custom"><h4>Suspected Cases</h4><h2>14</h2></div>', unsafe_allow_html=True)
    with kpi_cols_1[1]:
        st.markdown('<div class="kpi-card-custom"><h4>Confirmed Cases</h4><h2>0</h2></div>', unsafe_allow_html=True)
    with kpi_cols_1[2]:
        st.markdown('<div class="kpi-card-custom"><h4>New Cases (24h)</h4><h2>+2</h2></div>', unsafe_allow_html=True)
    with kpi_cols_1[3]:
        st.markdown('<div class="kpi-card-custom" style="border-left-color: var(--red);"><h4>Deaths Reported</h4><h2>0</h2></div>', unsafe_allow_html=True)
    with kpi_cols_1[4]:
        st.markdown('<div class="kpi-card-custom"><h4>Case Fatality Rate</h4><h2>0.0%</h2></div>', unsafe_allow_html=True)

    kpi_cols_2 = st.columns(4)
    with kpi_cols_2[0]:
        st.markdown('<div class="kpi-card-custom"><h4>Regions Reporting</h4><h2>3 / 16</h2></div>', unsafe_allow_html=True)
    with kpi_cols_2[1]:
        st.markdown('<div class="kpi-card-custom"><h4>Districts Active</h4><h2>8</h2></div>', unsafe_allow_html=True)
    with kpi_cols_2[2]:
        st.markdown('<div class="kpi-card-custom"><h4>Lab Positivity Rate</h4><h2>0.0%</h2></div>', unsafe_allow_html=True)
    with kpi_cols_2[3]:
        st.markdown('<div class="kpi-card-custom"><h4>Alerts Investigated</h4><h2>100%</h2></div>', unsafe_allow_html=True)

    st.write("")
    
    layout_split_col1, layout_split_col2 = st.columns([1.6, 1])
    
    with layout_split_col1:
        st.markdown("""
            <div class="panel-container">
                <div class="panel-head-custom"><h3>🗺️ Geo-Spatial Situation Map View</h3></div>
                <div class="panel-body-custom">
                    <p style="font-size:13px; color:#64748b;">Live Monitoring Layer Toggles: Active Watch Clusters, Laboratory Sites, RRT Positions.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Real-time coordinate distributions matching tracking points across Ghana borders
        map_dataframe = pd.DataFrame({
            'lat': [10.985, 5.556, 6.666],
            'lon': [-1.030, -0.196, -1.616]
        })
        st.map(map_dataframe, zoom=6)
        
    with layout_split_col2:
        st.markdown("""
            <div class="panel-container">
                <div class="panel-head-custom"><h3>⚠️ Top Structural Risks & Critical Decisions Needed</h3></div>
                <div class="panel-body-custom">
                    <div style="border-left: 4px solid var(--red); background: #fff5f5; padding: 12px; font-size: 13px; margin-bottom:12px;">
                        <strong>DECISION REQUIRED:</strong> Deploy supplementary Rapid Response Team to Upper East sector to reconcile unresolved validation alerts.
                    </div>
                    <div style="border-left: 4px solid var(--yellow); background: #fffdf0; padding: 12px; font-size: 13px; margin-bottom:12px;">
                        <strong>SURVEILLANCE NOTICE:</strong> Strengthen cross-border inspection workflows inside Volta Region corridor tracking entries.
                    </div>
                    <div style="border-left: 4px solid #2563EB; background: #eff6ff; padding: 12px; font-size: 13px;">
                        <strong>LOGISTICS REQUEST:</strong> Release pre-positioned PPE equipment reserves to designated healthcare isolation units.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------
# ROOM 2: Surveillance Intelligence
# ---------------------------------------------------------------------
elif "Surveillance Intelligence" in room_selection:
    st.markdown("### Surveillance Intelligence Hub")
    
    st.markdown("""
        <div class="panel-container">
            <div class="panel-head-custom"><h3>📈 Epidemic Curve Trends & Predictive Modeling Analytics</h3></div>
            <div class="panel-body-custom">
    """, unsafe_allow_html=True)
    
    trend_data = load_surveillance_trends()
    st.line_chart(trend_data, color=["#CE1126", "#006B3F"])
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    col_surv_split1, col_surv_split2 = st.columns(2)
    with col_surv_split1:
        st.markdown("""
            <div class="panel-container">
                <div class="panel-head-custom"><h3>⚠️ Sentinel Threshold Exceedance Incidents</h3></div>
                <div class="panel-body-custom">
        """, unsafe_allow_html=True)
        exceed_table = pd.DataFrame({
            "Indicator Stream": ["EBS Unusual Mortality Tracking", "Meningitis Sentinel Base", "VHF Cluster Alerts"],
            "Location Zone": ["Upper West Sector", "Northern Territory", "Bawku Central District"],
            "Status Check": ["Normal Baseline", "Approaching Threshold", "Trigger Alert Line Met"]
        })
        st.table(exceed_table)
        st.markdown("</div></div>", unsafe_allow_html=True)
        
    with col_surv_split2:
        st.markdown("""
            <div class="panel-container">
                <div class="panel-head-custom"><h3>📋 District Risk Categorization Matrix</h3></div>
                <div class="panel-body-custom">
        """, unsafe_allow_html=True)
        risk_matrix = pd.DataFrame({
            "District Unit": ["Bawku Central", "Paga Border Sector", "Accra Metro", "Tamale Metropolitan"],
            "Epi Risk Grading": ["🔴 Severe Risk", "🔴 Severe Risk", "🟠 Medium Risk", "🟢 Control Base"]
        })
        st.dataframe(risk_matrix, use_container_width=True, hide_index=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# ROOM 3: Laboratory Intelligence
# ---------------------------------------------------------------------
elif "Laboratory Intelligence" in room_selection:
    st.markdown("### Laboratory Diagnostics Room")
    
    st.markdown("""
        <div class="panel-container">
            <div class="panel-head-custom"><h3>🔬 Diagnostic Reference Center Status Records</h3></div>
            <div class="panel-body-custom">
    """, unsafe_allow_html=True)
    
    lab_records = pd.DataFrame({
        "Reference Facility Hub": ["Noguchi Memorial Institute (NMIMR)", "Kumasi Centre for Collaborative Research (KCCR)", "National Public Health Reference Lab (NPHRL)"],
        "Operational Status": ["Active Monitoring Mode", "Active Monitoring Mode", "Active Monitoring Mode"],
        "Average TAT Metric": ["14 Hours Certified", "19 Hours Certified", "12 Hours Certified"],
        "Pending Sample Inflow": [2, 0, 1]
    })
    st.table(lab_records)
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="panel-container">
            <div class="panel-head-custom"><h3>🚚 Specimen Transportation Ledger & Tracking Systems</h3></div>
            <div class="panel-body-custom">
    """, unsafe_allow_html=True)
    specimen_ledger = pd.DataFrame({
        "Sample Batch ID": ["VHF-2026-089", "VHF-2026-090"],
        "Origin Outpost": ["Bawku Field Clinic", "Paga Boundary Station"],
        "Pathogen Assay Checked": ["Ebola Zaire / Bundibugyo", "Ebola Zaire / Bundibugyo"],
        "Current Routing Lifecycle": ["In-Transit (Courier Air Link)", "Logged - Processing Queue Active"]
    })
    st.dataframe(specimen_ledger, use_container_width=True, hide_index=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# ROOM 4: Emergency Coordination
# ---------------------------------------------------------------------
elif "Emergency Coordination" in room_selection:
    st.markdown("### Incident Management System & Pillar Command")
    
    col_ims_left, col_ims_right = st.columns([1.2, 1])
    
    with col_ims_left:
        st.markdown("""
            <div class="panel-container">
                <div class="panel-head-custom"><h3>⚡ Activated IMS Structure & Functional Command</h3></div>
                <div class="panel-body-custom">
        """, unsafe_allow_html=True)
        ims_matrix = pd.DataFrame({
            "IMS Command Section": ["Operations Section Pillar", "Planning Section Pillar", "Logistics Support Pillar", "Finance & Administration"],
            "Status Code": ["Active", "Active", "Partial Activation", "Standby Status Ready"]
        })
        st.table(ims_matrix)
        st.markdown("</div></div>", unsafe_allow_html=True)
        
    with col_ims_right:
        st.markdown("""
            <div class="panel-container">
                <div class="panel-head-custom"><h3>🚀 Rapid Response Teams (RRT) Active Logs</h3></div>
                <div class="panel-body-custom">
        """, unsafe_allow_html=True)
        rrt_deployment_data = pd.DataFrame({
            "Deployed Unit Team": ["RRT Squad Alpha", "RRT Squad Delta"],
            "Target Operational Area": ["Upper East Zone", "Volta Control Sector"],
            "Assignment Status": ["Field Investigation Setup", "En-Route Deployment Phase"]
        })
        st.dataframe(rrt_deployment_data, use_container_width=True, hide_index=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# ROOM 5: Contact Tracing Room
# ---------------------------------------------------------------------
elif "Contact Tracing Room" in room_selection:
    st.markdown("### Contact Tracing & Mobile DHIS2 Network Link")
    
    st.info("Mobile data synchronization engine actively pooling field telemetry updates from primary response networks.")
    
    col_ct_cards = st.columns(3)
    with col_ct_cards[0]:
        st.metric("Total Contacts Listed", "42 Cases Registered")
    with col_ct_cards[1]:
        st.metric("Daily Follow-up Threshold Completion", "100%")
    with col_ct_cards[2]:
        st.metric("Active Symptom Trigger Flags", "0 Signs Detected")
        
    st.markdown("""
        <div class="panel-container">
            <div class="panel-head-custom"><h3>📋 Contact Verification Ledger</h3></div>
            <div class="panel-body-custom">
    """, unsafe_allow_html=True)
    contact_ledger_df = pd.DataFrame({
        "Associated Index ID": ["EVD-SUSP-011", "EVD-SUSP-011", "EVD-SUSP-014"],
        "Contact Case Code": ["CT-BAW-401", "CT-BAW-402", "CT-ACC-119"],
        "Risk Link Pathway": ["Household Core", "Healthcare Contact Vectors", "Transit Network Contact"],
        "Last 24h Check Status": ["Checked - Normal Temp", "Checked - Normal Temp", "Pending Field Team Clearance"]
    })
    st.dataframe(contact_ledger_df, use_container_width=True, hide_index=True)
    st.markdown("</div></div>", unsafe_
