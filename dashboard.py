
"""
================================================================================
JOB MARKET ANALYTICS — CLICKABLE KPI + REMOTE DRILL-DOWN + PORTAL COMPARISON
Run: python -m streamlit run dashboard.py
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from datetime import datetime
import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger("streamlit").setLevel(logging.ERROR)

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Job Market Analytics",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS
# ============================================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem; font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; padding: 0.5rem 0;
    }
    .sub-header {
        text-align: center; color: #555;
        margin-bottom: 1.2rem; font-size: 0.95rem;
    }
    .problem-header {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 0.7rem 1rem; border-radius: 8px;
        color: #FFFFFF !important; font-weight: bold;
        margin-bottom: 1rem; font-size: 0.95rem;
    }
    .insight-box {
        background: #f0f7ff; padding: 0.8rem;
        border-left: 4px solid #667eea; border-radius: 5px;
        margin: 0.6rem 0; font-size: 0.88rem;
        color: #1a1a1a !important;
    }
    .insight-box strong { color: #2c3e50 !important; font-weight: 700; }
    .drill-header {
        background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
        padding: 0.8rem 1rem; border-radius: 8px;
        color: #0d3d2c !important; font-weight: bold;
        margin: 1rem 0; font-size: 1.05rem;
        border: 2px solid #43e97b;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6; border-radius: 6px;
        padding: 8px 12px; font-weight: 600; font-size: 0.78rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    .stTabs [aria-selected="true"] * { color: #FFFFFF !important; }

    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #FFFFFF !important;
        border: none;
        padding: 0.8rem 0.4rem;
        border-radius: 10px;
        width: 100%;
        min-height: 95px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
        transition: transform 0.2s;
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
    }
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        line-height: 1.35 !important;
        margin: 0 !important;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    df = pd.read_csv("job_data_clean.csv")
    df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
    return df


def extract_skills(text):
    if pd.isna(text):
        return []
    text = str(text).lower()
    skill_list = [
        "python", "java", "sql", "javascript", "typescript", "react", "angular",
        "node.js", "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "jenkins", "spark", "kafka", "airflow", "snowflake", "tableau", "power bi",
        "machine learning", "deep learning", "nlp", "llm", "genai", "rag",
        "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
        "excel", "git", "linux", "agile", "scrum", "jira"
    ]
    return list(set([s for s in skill_list if s in text]))


try:
    df = load_data()
    df["skills"] = df["description"].apply(extract_skills)
    df["skill_count"] = df["skills"].apply(len)
except Exception as e:
    st.error(f"Error loading job_data_clean.csv: {e}")
    st.stop()

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<h1 class="main-header">🎯 Job Market Analytics</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Click any KPI card → see detailed breakdown</p>', unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
for key in ["view", "drill_type", "drill_value"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Sidebar
st.sidebar.markdown("## 🔍 Navigation")
if st.sidebar.button("🏠 Home (Clear View)"):
    st.session_state.view = None
    st.session_state.drill_type = None
    st.session_state.drill_value = None
    st.rerun()

if st.session_state.view:
    st.sidebar.success(f"Viewing: {st.session_state.view}")

if st.session_state.drill_type:
    st.sidebar.info(f"Drill: {st.session_state.drill_type} = {st.session_state.drill_value}")
    if st.sidebar.button("❌ Clear Drill"):
        st.session_state.drill_type = None
        st.session_state.drill_value = None
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"Total Jobs: {len(df)}")
st.sidebar.markdown(f"Remote Jobs: {(df['is_remote']=='Yes').sum()}")

# ============================================================================
# KPI CARDS
# ============================================================================
st.markdown("## 📈 Overview — Click to Explore")

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    if st.button(f"📊 Jobs\n\n{len(df)}", key="kpi_total", use_container_width=True):
        st.session_state.view = "Total Jobs"
        st.session_state.drill_type = None
        st.rerun()

with k2:
    if st.button(f"🏢 Companies\n\n{df['company'].nunique()}", key="kpi_company", use_container_width=True):
        st.session_state.view = "Companies"
        st.session_state.drill_type = None
        st.rerun()

with k3:
    if st.button(f"💼 Roles\n\n{df['title'].nunique()}", key="kpi_title", use_container_width=True):
        st.session_state.view = "Job Roles"
        st.session_state.drill_type = None
        st.rerun()

with k4:
    if st.button(f"🌐 Portals\n\n{df['platform'].nunique()}", key="kpi_portal", use_container_width=True):
        st.session_state.view = "Portals"
        st.session_state.drill_type = None
        st.rerun()

with k5:
    if st.button(f"📍 Cities\n\n{df['location'].nunique()}", key="kpi_location", use_container_width=True):
        st.session_state.view = "Locations"
        st.session_state.drill_type = None
        st.rerun()

with k6:
    remote_count = (df["is_remote"] == "Yes").sum()
    if st.button(f"🏠 Remote\n\n{remote_count}", key="kpi_remote", use_container_width=True):
        st.session_state.view = "Remote Jobs"
        st.session_state.drill_type = None
        st.rerun()

st.markdown("---")

# ============================================================================
# VIEW: REMOTE JOBS
# ============================================================================
if st.session_state.view == "Remote Jobs":
    st.markdown('<div class="drill-header">🏠 Remote Jobs — Complete Breakdown</div>', unsafe_allow_html=True)
    remote_df = df[df["is_remote"] == "Yes"]

    if len(remote_df) == 0:
        st.warning("No remote jobs found.")
    else:
        d1, d2, d3, d4, d5 = st.columns(5)
        with d1: st.metric("Total Remote Jobs", len(remote_df))
        with d2: st.metric("Companies", remote_df["company"].nunique())
        with d3: st.metric("Locations", remote_df["location"].nunique())
        with d4: st.metric("Job Roles", remote_df["title"].nunique())
        with d5: st.metric("Portals", remote_df["platform"].nunique())

        st.markdown("---")
        st.markdown("### 🏢 Companies Hiring Remote")
        c1, c2 = st.columns([3, 2])
        with c1:
            rc = remote_df["company"].value_counts().reset_index()
            rc.columns = ["Company", "Remote Jobs"]
            fig = px.bar(rc, x="Remote Jobs", y="Company", orientation="h",
                         title=f"All {len(rc)} Companies Hiring Remote — Click a bar",
                         color="Remote Jobs", color_continuous_scale="Greens", text="Remote Jobs")
            fig.update_layout(height=max(400, len(rc)*35), showlegend=False,
                              yaxis=dict(autorange="reversed"), title_font_size=14,
                              clickmode="event+select")
            fig.update_traces(textposition="outside")
            event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="remote_company_drill")
            if event and event.get("selection") and event["selection"].get("points"):
                clicked = event["selection"]["points"][0].get("y")
                if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
                    st.session_state.drill_type = "Company"
                    st.session_state.drill_value = clicked
                    st.rerun()
        with c2:
            st.markdown("#### Company List (Remote)")
            st.dataframe(rc, use_container_width=True, height=400, hide_index=True)

        st.markdown("### 📍 Remote Jobs by Location / Area")
        c3, c4 = st.columns([3, 2])
        with c3:
            rl = remote_df["location"].value_counts().reset_index()
            rl.columns = ["Location", "Remote Jobs"]
            fig = px.bar(rl, x="Remote Jobs", y="Location", orientation="h",
                         title="Remote Jobs by Location — Click a bar",
                         color="Remote Jobs", color_continuous_scale="Teal", text="Remote Jobs")
            fig.update_layout(height=max(400, len(rl)*35), showlegend=False,
                              yaxis=dict(autorange="reversed"), title_font_size=14,
                              clickmode="event+select")
            fig.update_traces(textposition="outside")
            event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="remote_loc_drill")
            if event and event.get("selection") and event["selection"].get("points"):
                clicked = event["selection"]["points"][0].get("y")
                if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
                    st.session_state.drill_type = "Location"
                    st.session_state.drill_value = clicked
                    st.rerun()
        with c4:
            st.markdown("#### Location List (Remote)")
            st.dataframe(rl, use_container_width=True, height=400, hide_index=True)

        st.markdown("### 🌐 Which Portals Post Remote Jobs?")
        c5, c6 = st.columns([2, 2])
        with c5:
            rp = remote_df["platform"].value_counts().reset_index()
            rp.columns = ["Portal", "Remote Jobs"]
            fig = px.bar(rp, x="Portal", y="Remote Jobs",
                         title="Remote Jobs by Portal — Click a bar",
                         color="Remote Jobs", color_continuous_scale="Blues", text="Remote Jobs")
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-30,
                              title_font_size=13, clickmode="event+select")
            fig.update_traces(textposition="outside")
            event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="remote_portal_drill")
            if event and event.get("selection") and event["selection"].get("points"):
                clicked = event["selection"]["points"][0].get("x")
                if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
                    st.session_state.drill_type = "Portal"
                    st.session_state.drill_value = clicked
                    st.rerun()
        with c6:
            fig = px.pie(rp, values="Remote Jobs", names="Portal",
                         title="Remote Jobs — Portal Share", hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textinfo="percent+label", textposition="outside",
                              textfont_size=11, pull=[0.03] * len(rp))
            fig.update_layout(height=400, title_font_size=13)
            st.plotly_chart(fig, use_container_width=True, key="remote_portal_pie")

        st.markdown("### 💼 What Job Roles Are Remote?")
        rr = remote_df["title"].value_counts().reset_index()
        rr.columns = ["Job Role", "Remote Jobs"]
        fig = px.bar(rr, x="Remote Jobs", y="Job Role", orientation="h",
                     title="Remote Job Roles — Click a bar",
                     color="Remote Jobs", color_continuous_scale="Purples", text="Remote Jobs")
        fig.update_layout(height=max(400, len(rr)*35), showlegend=False,
                          yaxis=dict(autorange="reversed"), title_font_size=14,
                          clickmode="event+select")
        fig.update_traces(textposition="outside")
        event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="remote_role_drill")
        if event and event.get("selection") and event["selection"].get("points"):
            clicked = event["selection"]["points"][0].get("y")
            if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
                st.session_state.drill_type = "Job Role"
                st.session_state.drill_value = clicked
                st.rerun()

        st.markdown("### 🛠️ Top Skills Required for Remote Jobs")
        all_rs = [s for skills in remote_df["skills"] for s in skills]
        rs = Counter(all_rs).most_common(15)
        if rs:
            rs_df = pd.DataFrame(rs, columns=["Skill", "Jobs"])
            rs_df["% of Remote"] = (rs_df["Jobs"] / len(remote_df) * 100).round(1)
            fig = px.bar(rs_df, x="Jobs", y="Skill", orientation="h",
                         title="Top Skills for Remote Jobs", color="Jobs",
                         color_continuous_scale="Greens", text="Jobs")
            fig.update_layout(height=500, showlegend=False,
                              yaxis=dict(autorange="reversed"), title_font_size=14)
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True, key="remote_skills")

        st.markdown("### 📋 All Remote Job Openings")
        show_cols = ["title", "company", "location", "platform", "employment_type", "posted_date"]
        display_remote = remote_df[show_cols].copy()
        display_remote.columns = ["Job Title", "Company", "Location", "Portal", "Type", "Posted"]
        st.dataframe(display_remote, use_container_width=True, height=500)

        csv = remote_df.to_csv(index=False)
        st.download_button("Download All Remote Jobs (CSV)", data=csv,
                           file_name=f"remote_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime="text/csv", key="dl_remote")

        top_comp = remote_df["company"].value_counts().index[0]
        top_loc = remote_df["location"].value_counts().index[0]
        top_portal = remote_df["platform"].value_counts().index[0]

        st.markdown(f"""<div class="insight-box">
            <strong>Remote Job Summary:</strong><br>
            Top Remote Employer: {top_comp}<br>
            Top Remote Location: {top_loc}<br>
            Top Portal for Remote: {top_portal}<br>
            Top Skill for Remote: {rs[0][0] if rs else 'N/A'}<br>
            Remote % of Total: {len(remote_df)/len(df)*100:.1f}%
        </div>""", unsafe_allow_html=True)

# ============================================================================
# VIEW: COMPANIES
# ============================================================================
elif st.session_state.view == "Companies":
    st.markdown('<div class="drill-header">🏢 All Companies Hiring</div>', unsafe_allow_html=True)
    comp_df = df["company"].value_counts().reset_index()
    comp_df.columns = ["Company", "Openings"]
    comp_df["Share %"] = (comp_df["Openings"] / len(df) * 100).round(2)
    c1, c2 = st.columns([3, 2])
    with c1:
        fig = px.bar(comp_df.head(30), x="Openings", y="Company", orientation="h",
                     title=f"All {len(comp_df)} Companies (Top 30) — Click a bar",
                     color="Openings", color_continuous_scale="Viridis", text="Openings")
        fig.update_layout(height=800, showlegend=False, yaxis=dict(autorange="reversed"),
                          title_font_size=14, clickmode="event+select")
        fig.update_traces(textposition="outside")
        event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="comp_view_drill")
        if event and event.get("selection") and event["selection"].get("points"):
            clicked = event["selection"]["points"][0].get("y")
            if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
                st.session_state.drill_type = "Company"
                st.session_state.drill_value = clicked
                st.rerun()
    with c2:
        st.dataframe(comp_df, use_container_width=True, height=750, hide_index=True)
    csv = comp_df.to_csv(index=False)
    st.download_button("Download CSV", csv,
                       file_name=f"companies_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv", key="dl_comp_view")

# ============================================================================
# VIEW: LOCATIONS
# ============================================================================
elif st.session_state.view == "Locations":
    st.markdown('<div class="drill-header">📍 All Locations</div>', unsafe_allow_html=True)
    loc_df = df["location"].value_counts().reset_index()
    loc_df.columns = ["Location", "Openings"]
    loc_df["Share %"] = (loc_df["Openings"] / len(df) * 100).round(2)
    c1, c2 = st.columns([3, 2])
    with c1:
        fig = px.bar(loc_df, x="Openings", y="Location", orientation="h",
                     title=f"All {len(loc_df)} Locations — Click a bar",
                     color="Openings", color_continuous_scale="Magma", text="Openings")
        fig.update_layout(height=max(600, len(loc_df)*22), showlegend=False,
                          yaxis=dict(autorange="reversed"), title_font_size=14,
                          clickmode="event+select")
        fig.update_traces(textposition="outside")
        event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="loc_view_drill")
        if event and event.get("selection") and event["selection"].get("points"):
            clicked = event["selection"]["points"][0].get("y")
            if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
                st.session_state.drill_type = "Location"
                st.session_state.drill_value = clicked
                st.rerun()
    with c2:
        st.dataframe(loc_df, use_container_width=True, height=750, hide_index=True)
    csv = loc_df.to_csv(index=False)
    st.download_button("Download CSV", csv,
                       file_name=f"locations_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv", key="dl_loc_view")

# ============================================================================
# VIEW: JOB ROLES
# ============================================================================
elif st.session_state.view == "Job Roles":
    st.markdown('<div class="drill-header">💼 All Job Roles</div>', unsafe_allow_html=True)
    role_df = df["title"].value_counts().reset_index()
    role_df.columns = ["Job Role", "Openings"]
    role_df["Share %"] = (role_df["Openings"] / len(df) * 100).round(2)
    c1, c2 = st.columns([3, 2])
    with c1:
        fig = px.bar(role_df.head(40), x="Openings", y="Job Role", orientation="h",
                     title=f"All {len(role_df)} Job Roles (Top 40) — Click a bar",
                     color="Openings", color_continuous_scale="Plasma", text="Openings")
        fig.update_layout(height=1000, showlegend=False, yaxis=dict(autorange="reversed"),
                          title_font_size=14, clickmode="event+select")
        fig.update_traces(textposition="outside")
        event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="role_view_drill")
        if event and event.get("selection") and event["selection"].get("points"):
            clicked = event["selection"]["points"][0].get("y")
            if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
                st.session_state.drill_type = "Job Role"
                st.session_state.drill_value = clicked
                st.rerun()
    with c2:
        st.dataframe(role_df, use_container_width=True, height=950, hide_index=True)
    csv = role_df.to_csv(index=False)
    st.download_button("Download CSV", csv,
                       file_name=f"roles_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv", key="dl_role_view")

# ============================================================================
# VIEW: PORTALS
# ============================================================================
elif st.session_state.view == "Portals":
    st.markdown('<div class="drill-header">🌐 All Portals</div>', unsafe_allow_html=True)
    portal_df = df["platform"].value_counts().reset_index()
    portal_df.columns = ["Portal", "Openings"]
    portal_df["Share %"] = (portal_df["Openings"] / len(df) * 100).round(2)
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(portal_df, x="Portal", y="Openings",
                     title="Portals — Click a bar", color="Openings",
                     color_continuous_scale="Turbo", text="Openings")
        fig.update_layout(height=450, showlegend=False, xaxis_tickangle=-30,
                          title_font_size=13, clickmode="event+select")
        fig.update_traces(textposition="outside")
        event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="portal_view_drill")
        if event and event.get("selection") and event["selection"].get("points"):
            clicked = event["selection"]["points"][0].get("x")
            if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
                st.session_state.drill_type = "Portal"
                st.session_state.drill_value = clicked
                st.rerun()
    with c2:
        st.dataframe(portal_df, use_container_width=True, hide_index=True)
    csv = portal_df.to_csv(index=False)
    st.download_button("Download CSV", csv,
                       file_name=f"portals_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv", key="dl_portal_view")

# ============================================================================
# VIEW: TOTAL JOBS
# ============================================================================
elif st.session_state.view == "Total Jobs":
    st.markdown('<div class="drill-header">📊 All Jobs in Dataset</div>', unsafe_allow_html=True)
    show_cols = ["title", "company", "location", "platform", "is_remote", "employment_type", "posted_date"]
    display_df = df[show_cols].copy()
    display_df.columns = ["Job Title", "Company", "Location", "Portal", "Remote", "Type", "Posted"]
    st.dataframe(display_df, use_container_width=True, height=600)
    csv = df.to_csv(index=False)
    st.download_button("Download All Jobs (CSV)", csv,
                       file_name=f"all_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv", key="dl_total_view")

# ============================================================================
# DRILL-DOWN PANEL
# ============================================================================
if st.session_state.drill_type and st.session_state.drill_value:
    st.markdown("---")
    drill_val = st.session_state.drill_value
    drill_type = st.session_state.drill_type
    st.markdown(f'<div class="drill-header">🎯 Drill-Down: {drill_type} = "{drill_val}"</div>', unsafe_allow_html=True)

    if drill_type == "Skill":
        drill_df = df[df["skills"].apply(lambda x: drill_val in x)]
    elif drill_type == "Job Role":
        drill_df = df[df["title"] == drill_val]
    elif drill_type == "Company":
        drill_df = df[df["company"] == drill_val]
    elif drill_type == "Location":
        drill_df = df[df["location"] == drill_val]
    elif drill_type == "Portal":
        drill_df = df[df["platform"] == drill_val]
    else:
        drill_df = df.copy()

    d1, d2, d3, d4 = st.columns(4)
    with d1: st.metric("Total Openings", len(drill_df))
    with d2: st.metric("Companies", drill_df["company"].nunique())
    with d3: st.metric("Locations", drill_df["location"].nunique())
    with d4:
        rp = (drill_df["is_remote"] == "Yes").sum() / len(drill_df) * 100 if len(drill_df) > 0 else 0
        st.metric("Remote %", f"{rp:.1f}%")

    g1, g2 = st.columns(2)
    with g1:
        pc = drill_df["platform"].value_counts().reset_index()
        pc.columns = ["Portal", "Openings"]
        fig = px.bar(pc, x="Openings", y="Portal", orientation="h",
                     title="By Portal", color="Openings",
                     color_continuous_scale="Blues", text="Openings")
        fig.update_layout(height=350, showlegend=False, yaxis=dict(autorange="reversed"), title_font_size=13)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True, key=f"dd_p_{drill_val}")
    with g2:
        cc = drill_df["company"].value_counts().head(10).reset_index()
        cc.columns = ["Company", "Openings"]
        fig = px.bar(cc, x="Openings", y="Company", orientation="h",
                     title="By Company", color="Openings",
                     color_continuous_scale="Viridis", text="Openings")
        fig.update_layout(height=350, showlegend=False, yaxis=dict(autorange="reversed"), title_font_size=13)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True, key=f"dd_c_{drill_val}")

    st.markdown("### 📋 All Job Openings")
    show_cols = ["title", "company", "location", "platform", "is_remote", "employment_type", "posted_date"]
    ddf = drill_df[show_cols].copy()
    ddf.columns = ["Job Title", "Company", "Location", "Portal", "Remote", "Type", "Posted"]
    st.dataframe(ddf, use_container_width=True, height=400)
    csv = drill_df.to_csv(index=False)
    st.download_button("Download (CSV)", csv,
                       file_name=f"drill_{drill_type}_{drill_val}.csv",
                       mime="text/csv", key=f"dl_dd_{drill_val}")

# ============================================================================
# MAIN TABS
# ============================================================================
if st.session_state.view is None:
    st.markdown("---")
    st.markdown("## 🔎 Explore Charts — Click to drill down")

    tabs = st.tabs(["🛠️ By Skill", "💼 By Role", "🏢 By Company",
                    "📍 By Location", "🌐 By Portal", "⚖️ Portal Comparison"])

    # ---- TAB 0: By Skill ----
    with tabs[0]:
        all_sk = [s for skills in df["skills"] for s in skills]
        sc = Counter(all_sk).most_common(20)
        if sc:
            sdf = pd.DataFrame(sc, columns=["Skill", "Jobs"])
            fig = px.bar(sdf, x="Jobs", y="Skill", orientation="h",
                         title="Top 20 Skills", color="Jobs",
                         color_continuous_scale="RdYlGn", text="Jobs")
            fig.update_layout(height=650, showlegend=False,
                              yaxis=dict(autorange="reversed"), clickmode="event+select")
            fig.update_traces(textposition="outside")
            ev = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="main_skill")
            if ev and ev.get("selection") and ev["selection"].get("points"):
                c = ev["selection"]["points"][0].get("y")
                if c and (st.session_state.drill_type != "Skill" or st.session_state.drill_value != c):
                    st.session_state.drill_type = "Skill"
                    st.session_state.drill_value = c
                    st.rerun()

    # ---- TAB 1: By Role ----
    with tabs[1]:
        tc = df["title"].value_counts().head(20).reset_index()
        tc.columns = ["Job Role", "Openings"]
        fig = px.bar(tc, x="Openings", y="Job Role", orientation="h",
                     title="Top 20 Roles", color="Openings",
                     color_continuous_scale="Viridis", text="Openings")
        fig.update_layout(height=650, showlegend=False,
                          yaxis=dict(autorange="reversed"), clickmode="event+select")
        fig.update_traces(textposition="outside")
        ev = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="main_role")
        if ev and ev.get("selection") and ev["selection"].get("points"):
            c = ev["selection"]["points"][0].get("y")
            if c and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != c):
                st.session_state.drill_type = "Job Role"
                st.session_state.drill_value = c
                st.rerun()

    # ---- TAB 2: By Company ----
    with tabs[2]:
        cc = df["company"].value_counts().head(20).reset_index()
        cc.columns = ["Company", "Openings"]
        fig = px.bar(cc, x="Openings", y="Company", orientation="h",
                     title="Top 20 Companies", color="Openings",
                     color_continuous_scale="Cividis", text="Openings")
        fig.update_layout(height=650, showlegend=False,
                          yaxis=dict(autorange="reversed"), clickmode="event+select")
        fig.update_traces(textposition="outside")
        ev = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="main_company")
        if ev and ev.get("selection") and ev["selection"].get("points"):
            c = ev["selection"]["points"][0].get("y")
            if c and (st.session_state.drill_type != "Company" or st.session_state.drill_value != c):
                st.session_state.drill_type = "Company"
                st.session_state.drill_value = c
                st.rerun()

    # ---- TAB 3: By Location ----
    with tabs[3]:
        lc = df["location"].value_counts().head(20).reset_index()
        lc.columns = ["Location", "Openings"]
        fig = px.bar(lc, x="Location", y="Openings",
                     title="Top 20 Locations", color="Openings",
                     color_continuous_scale="Turbo", text="Openings")
        fig.update_layout(height=500, showlegend=False,
                          xaxis_tickangle=-40, clickmode="event+select")
        fig.update_traces(textposition="outside")
        ev = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="main_loc")
        if ev and ev.get("selection") and ev["selection"].get("points"):
            c = ev["selection"]["points"][0].get("x")
            if c and (st.session_state.drill_type != "Location" or st.session_state.drill_value != c):
                st.session_state.drill_type = "Location"
                st.session_state.drill_value = c
                st.rerun()

    # ---- TAB 4: By Portal ----
    with tabs[4]:
        pc = df["platform"].value_counts().reset_index()
        pc.columns = ["Portal", "Openings"]
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(pc, x="Portal", y="Openings", title="Portals",
                         color="Openings", color_continuous_scale="Plasma", text="Openings")
            fig.update_layout(height=450, showlegend=False,
                              xaxis_tickangle=-30, clickmode="event+select")
            fig.update_traces(textposition="outside")
            ev = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="main_portal")
            if ev and ev.get("selection") and ev["selection"].get("points"):
                c = ev["selection"]["points"][0].get("x")
                if c and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != c):
                    st.session_state.drill_type = "Portal"
                    st.session_state.drill_value = c
                    st.rerun()
        with c2:
            fig = px.pie(pc, values="Openings", names="Portal",
                         title="Distribution", hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textinfo="percent+label", textposition="outside",
                              textfont_size=11, pull=[0.03] * len(pc))
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True, key="main_portal_pie")

    # ========================================================================
    # TAB 5: PORTAL COMPARISON (NEW)
    # ========================================================================
    with tabs[5]:
        st.markdown('<div class="problem-header">⚖️ Portal Comparison — Which Portal Wins?</div>', unsafe_allow_html=True)

        portal_stats = []
        for portal in df['platform'].unique():
            pdf = df[df['platform'] == portal]
            all_skills_in_portal = [s for skills in pdf['skills'] for s in skills]
            portal_stats.append({
                'Portal': portal,
                'Total Jobs': len(pdf),
                'Companies': pdf['company'].nunique(),
                'Job Roles': pdf['title'].nunique(),
                'Locations': pdf['location'].nunique(),
                'Remote Jobs': (pdf['is_remote'] == 'Yes').sum(),
                'Remote %': round((pdf['is_remote'] == 'Yes').sum() / len(pdf) * 100, 1) if len(pdf) else 0,
                'Avg Skills': round(pdf['skill_count'].mean(), 1),
                'Unique Skills': len(set(all_skills_in_portal)),
            })

        comp_df = pd.DataFrame(portal_stats).sort_values('Total Jobs', ascending=False).reset_index(drop=True)

        # ---- Metric Cards per Portal ----
        st.markdown("### 📊 Portal Metrics at a Glance")
        metric_cols = st.columns(len(comp_df))
        for i, row in comp_df.iterrows():
            with metric_cols[i]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 1rem; border-radius: 10px; color: #FFFFFF;
                            text-align: center; margin-bottom: 0.5rem;">
                    <div style="font-size: 1.05rem; font-weight: bold; margin-bottom: 0.5rem;">{row['Portal']}</div>
                    <div style="font-size: 0.7rem; opacity: 0.9;">Jobs</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{row['Total Jobs']}</div>
                    <div style="font-size: 0.72rem; margin-top: 0.3rem;">
                        🏢 {row['Companies']} · 💼 {row['Job Roles']} · 📍 {row['Locations']}
                    </div>
                    <div style="font-size: 0.72rem; margin-top: 0.3rem;">
                        🏠 {row['Remote %']}% Remote
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # ---- Multi-Metric Bar Charts ----
        st.markdown("### 📈 Portal Performance Across Metrics")
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(comp_df, x='Portal', y='Total Jobs',
                         title='📊 Total Jobs by Portal',
                         color='Total Jobs', color_continuous_scale='Blues', text='Total Jobs')
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-30, title_font_size=14)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True, key="cmp_jobs")
        with c2:
            fig = px.bar(comp_df, x='Portal', y='Companies',
                         title='🏢 Company Diversity by Portal',
                         color='Companies', color_continuous_scale='Greens', text='Companies')
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-30, title_font_size=14)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True, key="cmp_companies")

        c3, c4 = st.columns(2)
        with c3:
            fig = px.bar(comp_df, x='Portal', y='Job Roles',
                         title='💼 Role Diversity by Portal',
                         color='Job Roles', color_continuous_scale='Purples', text='Job Roles')
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-30, title_font_size=14)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True, key="cmp_roles")
        with c4:
            fig = px.bar(comp_df, x='Portal', y='Locations',
                         title='📍 Location Coverage by Portal',
                         color='Locations', color_continuous_scale='Oranges', text='Locations')
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-30, title_font_size=14)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True, key="cmp_locations")

        st.markdown("---")

        # ---- Remote + Skills ----
        st.markdown("### 🏠 Remote Jobs & Skills by Portal")
        c5, c6 = st.columns(2)
        with c5:
            fig = px.bar(comp_df, x='Portal', y='Remote %',
                         title='🏠 Remote Job % by Portal',
                         color='Remote %', color_continuous_scale='Teal', text='Remote %')
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-30, title_font_size=14)
            fig.update_traces(textposition='outside', texttemplate='%{text}%')
            st.plotly_chart(fig, use_container_width=True, key="cmp_remote")
        with c6:
            fig = px.bar(comp_df, x='Portal', y='Avg Skills',
                         title='🛠️ Average Skills Required per Portal',
                         color='Avg Skills', color_continuous_scale='RdYlGn', text='Avg Skills')
            fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-30, title_font_size=14)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True, key="cmp_skills")

        st.markdown("---")

        # ---- Radar Chart ----
        st.markdown("### 🎯 Radar Chart — All Metrics Compared")
        radar_df = comp_df.copy()
        metrics = ['Total Jobs', 'Companies', 'Job Roles', 'Locations', 'Avg Skills']
        for m in metrics:
            max_val = radar_df[m].max()
            radar_df[m + '_norm'] = (radar_df[m] / max_val * 100).round(1) if max_val > 0 else 0

        fig = go.Figure()
        colors = ['#667eea', '#f5576c', '#43e97b', '#4facfe', '#fa709a', '#FFA500']
        for i, row in radar_df.iterrows():
            values = [row[m + '_norm'] for m in metrics]
            values.append(values[0])
            fig.add_trace(go.Scatterpolar(
                r=values, theta=metrics + [metrics[0]],
                fill='toself', name=row['Portal'],
                line=dict(color=colors[i % len(colors)], width=2), opacity=0.6
            ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100],
                                        showticklabels=True, ticksuffix='%')),
            showlegend=True, height=600,
            title='Portal Comparison (Normalized — bigger = better)',
            title_font_size=14
        )
        st.plotly_chart(fig, use_container_width=True, key="cmp_radar")

        st.markdown("""
        <div class="insight-box">
            <strong>How to read this:</strong> Each axis is normalized to 100% (the best portal per metric = 100%).<br>
            <strong>Bigger shape</strong> = More dominant portal across metrics
        </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # ---- Employment Type Stacked ----
        st.markdown("### 📋 Employment Type Breakdown by Portal")
        pe = df.groupby(['platform', 'employment_type']).size().reset_index(name='Jobs')
        fig = px.bar(pe, x='platform', y='Jobs', color='employment_type',
                     title='Employment Type Distribution Across Portals',
                     barmode='stack',
                     color_discrete_sequence=px.colors.qualitative.Set2, text='Jobs')
        fig.update_layout(height=450, title_font_size=14, xaxis_tickangle=-30,
                          legend_title='Employment Type')
        fig.update_traces(textposition='inside')
        st.plotly_chart(fig, use_container_width=True, key="cmp_emp_stacked")

        st.markdown("---")

        # ---- Full Table ----
        st.markdown("### 📊 Full Portal Comparison Table")
        display_table = comp_df.copy()
        display_table.index = range(1, len(display_table) + 1)
        st.dataframe(display_table, use_container_width=True,
                     height=min(400, (len(display_table) + 1) * 35 + 40))

        csv = comp_df.to_csv(index=False)
        st.download_button("📥 Download Portal Comparison (CSV)", data=csv,
                           file_name=f"portal_comparison_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime="text/csv", key="dl_portal_comparison")

        st.markdown("---")

        # ---- Auto Insights ----
        st.markdown("### 💡 Auto-Generated Insights")
        top_volume = comp_df.iloc[0]
        top_company_div = comp_df.loc[comp_df['Companies'].idxmax()]
        top_role_div = comp_df.loc[comp_df['Job Roles'].idxmax()]
        top_loc_cov = comp_df.loc[comp_df['Locations'].idxmax()]
        top_remote = comp_df.loc[comp_df['Remote %'].idxmax()]
        top_skills = comp_df.loc[comp_df['Avg Skills'].idxmax()]

        st.markdown(f"""
        <div class="insight-box">
            <strong>🏆 Best Portal by Total Jobs:</strong> {top_volume['Portal']} ({top_volume['Total Jobs']} jobs)<br>
            <strong>🏢 Best for Company Diversity:</strong> {top_company_div['Portal']} ({top_company_div['Companies']} companies)<br>
            <strong>💼 Best for Role Diversity:</strong> {top_role_div['Portal']} ({top_role_div['Job Roles']} roles)<br>
            <strong>📍 Best for Location Coverage:</strong> {top_loc_cov['Portal']} ({top_loc_cov['Locations']} cities)<br>
            <strong>🏠 Best for Remote Jobs:</strong> {top_remote['Portal']} ({top_remote['Remote %']}% remote)<br>
            <strong>🛠️ Highest Skill Demand:</strong> {top_skills['Portal']} ({top_skills['Avg Skills']} avg)
        </div>
        """, unsafe_allow_html=True)

        # ---- Recommendation ----
        st.markdown("### 🎯 Recommendation")
        score_df = comp_df.copy()
        for m in ['Total Jobs', 'Companies', 'Job Roles', 'Locations', 'Remote %']:
            max_val = score_df[m].max()
            score_df[m + '_score'] = (score_df[m] / max_val * 100) if max_val > 0 else 0

        score_df['Overall Score'] = (
            score_df['Total Jobs_score'] * 0.35 +
            score_df['Companies_score'] * 0.20 +
            score_df['Job Roles_score'] * 0.20 +
            score_df['Locations_score'] * 0.15 +
            score_df['Remote %_score'] * 0.10
        ).round(1)

        score_df = score_df.sort_values('Overall Score', ascending=False)
        best_portal = score_df.iloc[0]

        st.markdown(f"""
        <div class="insight-box" style="background: #e8f5e9; border-left: 4px solid #4caf50;">
            <strong style="font-size: 1.1rem;">🏆 RECOMMENDED PORTAL: {best_portal['Portal']}</strong><br>
            <strong>Overall Score:</strong> {best_portal['Overall Score']}/100<br>
            <strong>Why:</strong> Strongest combination of volume, diversity, and coverage<br>
            <br>
            <strong>🎯 For Job Seekers:</strong> Focus on <strong>{best_portal['Portal']}</strong><br>
            <strong>🎯 For Recruiters:</strong> Post on <strong>{top_volume['Portal']}</strong> for volume, <strong>{top_remote['Portal']}</strong> for remote roles
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏅 Portal Ranking (Weighted Score)")
        ranked = score_df[['Portal', 'Overall Score', 'Total Jobs', 'Companies',
                           'Job Roles', 'Locations', 'Remote %']].reset_index(drop=True)
        ranked.index = range(1, len(ranked) + 1)
        st.dataframe(ranked, use_container_width=True, hide_index=False)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""<div style='text-align:center; color:#666; font-size:12px;'>
    Job Market Analytics | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
    {len(df)} total jobs | {(df['is_remote']=='Yes').sum()} remote
</div>""", unsafe_allow_html=True)