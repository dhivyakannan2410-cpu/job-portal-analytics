# # # # # # # # """
# # # # # # # # ================================================================================
# # # # # # # # JOB MARKET ANALYTICS — DRILL-DOWN DASHBOARD (Real Data Analyst Version)
# # # # # # # # Click any skill / role / company / location → see where the openings are
# # # # # # # # Tech Stack: Python | Pandas | NumPy | Plotly | Streamlit
# # # # # # # # Run: python -m streamlit run dashboard.py
# # # # # # # # ================================================================================
# # # # # # # # """

# # # # # # # # import streamlit as st
# # # # # # # # import pandas as pd
# # # # # # # # import numpy as np
# # # # # # # # import plotly.express as px
# # # # # # # # import plotly.graph_objects as go
# # # # # # # # from collections import Counter
# # # # # # # # from datetime import datetime
# # # # # # # # import warnings
# # # # # # # # import logging

# # # # # # # # warnings.filterwarnings('ignore')
# # # # # # # # logging.getLogger('streamlit').setLevel(logging.ERROR)

# # # # # # # # # ============================================================================
# # # # # # # # # PAGE CONFIG
# # # # # # # # # ============================================================================
# # # # # # # # st.set_page_config(
# # # # # # # #     page_title="Job Market Drill-Down Analytics",
# # # # # # # #     page_icon="🎯",
# # # # # # # #     layout="wide",
# # # # # # # #     initial_sidebar_state="expanded"
# # # # # # # # )

# # # # # # # # # CSS
# # # # # # # # st.markdown("""
# # # # # # # # <style>
    /* ========== FORCE DARK TEXT EVERYWHERE ========== */
    .stApp, .stApp * {
        color: #1a1a1a !important;
    }
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricLabel"] > div {
        color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stDataFrame"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
    }
# # # # # # # #     div[data-testid="stMarkdownContainer"] div,
# # # # # # # #     div[data-testid="stMarkdownContainer"] p,
# # # # # # # #     div[data-testid="stMarkdownContainer"] span,
# # # # # # # #     div[data-testid="stMarkdownContainer"] strong { color: #1a1a1a; }

# # # # # # # #     .main-header {
# # # # # # # #         font-size: 2.2rem; font-weight: bold;
# # # # # # # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # # # # # # #         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
# # # # # # # #         text-align: center; padding: 0.5rem 0;
# # # # # # # #     }
# # # # # # # #     .sub-header { text-align: center; color: #666; margin-bottom: 1rem; }
# # # # # # # #     .metric-card {
# # # # # # # #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# # # # # # # #         padding: 1rem; border-radius: 12px; color: #FFFFFF !important;
# # # # # # # #         text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
# # # # # # # #     }
# # # # # # # #     .metric-value { font-size: 1.8rem; font-weight: bold; margin: 0.3rem 0; color: #FFFFFF !important; }
# # # # # # # #     .metric-label { font-size: 0.8rem; opacity: 0.95; color: #FFFFFF !important; }
# # # # # # # #     .problem-header {
# # # # # # # #         background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
# # # # # # # #         padding: 0.7rem 1rem; border-radius: 8px;
# # # # # # # #         color: #FFFFFF !important; font-weight: bold;
# # # # # # # #         margin-bottom: 1rem; font-size: 1rem;
# # # # # # # #     }
# # # # # # # #     .insight-box {
# # # # # # # #         background: #f0f7ff; padding: 0.8rem;
# # # # # # # #         border-left: 4px solid #667eea; border-radius: 5px;
# # # # # # # #         margin: 0.6rem 0; font-size: 0.9rem; color: #1a1a1a !important;
# # # # # # # #     }
# # # # # # # #     .insight-box strong { color: #2c3e50 !important; font-weight: 700; }
# # # # # # # #     .drill-header {
# # # # # # # #         background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
# # # # # # # #         padding: 0.8rem 1rem; border-radius: 8px;
# # # # # # # #         color: #1a1a1a !important; font-weight: bold;
# # # # # # # #         margin: 1rem 0; font-size: 1.1rem;
# # # # # # # #         border: 2px solid #43e97b;
# # # # # # # #     }
# # # # # # # #     .stTabs [data-baseweb="tab-list"] { gap: 6px; flex-wrap: wrap; }
# # # # # # # #     .stTabs [data-baseweb="tab"] {
# # # # # # # #         background-color: #f0f2f6; border-radius: 6px;
# # # # # # # #         padding: 8px 12px; font-weight: 600; font-size: 0.78rem;
# # # # # # # #     }
# # # # # # # #     .stTabs [aria-selected="true"] {
# # # # # # # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # # # # # # #         color: #FFFFFF !important;
# # # # # # # #     }
# # # # # # # # </style>
# # # # # # # # """, unsafe_allow_html=True)

# # # # # # # # # ============================================================================
# # # # # # # # # DATA LOADING
# # # # # # # # # ============================================================================

# # # # # # # # @st.cache_data
# # # # # # # # def load_data():
# # # # # # # #     df = pd.read_csv("job_data_clean.csv")
# # # # # # # #     df['posted_date'] = pd.to_datetime(df['posted_date'], errors='coerce')
# # # # # # # #     return df

# # # # # # # # def extract_skills(text):
# # # # # # # #     if pd.isna(text):
# # # # # # # #         return []
# # # # # # # #     text = str(text).lower()
# # # # # # # #     skill_list = [
# # # # # # # #         'python', 'java', 'sql', 'javascript', 'typescript', 'react', 'angular',
# # # # # # # #         'node.js', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
# # # # # # # #         'jenkins', 'spark', 'kafka', 'airflow', 'snowflake', 'tableau', 'power bi',
# # # # # # # #         'machine learning', 'deep learning', 'nlp', 'llm', 'genai', 'rag',
# # # # # # # #         'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
# # # # # # # #         'excel', 'git', 'linux', 'agile', 'scrum', 'jira'
# # # # # # # #     ]
# # # # # # # #     return list(set([s for s in skill_list if s in text]))

# # # # # # # # try:
# # # # # # # #     df = load_data()
# # # # # # # #     df['skills'] = df['description'].apply(extract_skills)
# # # # # # # #     df['skill_count'] = df['skills'].apply(len)
# # # # # # # # except Exception as e:
# # # # # # # #     st.error(f"❌ Error loading 'job_data_clean.csv': {e}")
# # # # # # # #     st.stop()

# # # # # # # # # ============================================================================
# # # # # # # # # HEADER
# # # # # # # # # ============================================================================
# # # # # # # # st.markdown('<h1 class="main-header">🎯 Job Market Drill-Down Analytics</h1>', unsafe_allow_html=True)
# # # # # # # # st.markdown('<p class="sub-header">Click any skill, role, company or location → see where all the openings are</p>', unsafe_allow_html=True)

# # # # # # # # # ============================================================================
# # # # # # # # # SESSION STATE
# # # # # # # # # ============================================================================
# # # # # # # # for key in ['drill_type', 'drill_value']:
# # # # # # # #     if key not in st.session_state:
# # # # # # # #         st.session_state[key] = None

# # # # # # # # # ============================================================================
# # # # # # # # # SIDEBAR
# # # # # # # # # ============================================================================
# # # # # # # # st.sidebar.markdown("## 🔍 Filters")
# # # # # # # # st.sidebar.markdown("---")

# # # # # # # # if st.sidebar.button("🔄 Reset All"):
# # # # # # # #     st.session_state.drill_type = None
# # # # # # # #     st.session_state.drill_value = None
# # # # # # # #     st.rerun()

# # # # # # # # # Show active drill
# # # # # # # # if st.session_state.drill_type:
# # # # # # # #     st.sidebar.markdown("### 🎯 Active Drill-Down")
# # # # # # # #     st.sidebar.success(f"**{st.session_state.drill_type}:** {st.session_state.drill_value}")
# # # # # # # #     st.sidebar.caption("Click Reset to clear")

# # # # # # # # st.sidebar.markdown("---")
# # # # # # # # st.sidebar.markdown(f"**📊 Total Jobs:** {len(df)}")

# # # # # # # # # ============================================================================
# # # # # # # # # MAIN DASHBOARD — 4 SECTIONS
# # # # # # # # # ============================================================================
# # # # # # # # st.markdown("## 📊 Overview")

# # # # # # # # # KPI Cards
# # # # # # # # c1, c2, c3, c4, c5 = st.columns(5)

# # # # # # # # with c1:
# # # # # # # #     st.markdown(f"""<div class="metric-card">
# # # # # # # #         <div class="metric-label">Total Jobs</div>
# # # # # # # #         <div class="metric-value">{len(df)}</div>
# # # # # # # #         <div class="metric-label">in dataset</div></div>""", unsafe_allow_html=True)

# # # # # # # # with c2:
# # # # # # # #     st.markdown(f"""<div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
# # # # # # # #         <div class="metric-label">Companies</div>
# # # # # # # #         <div class="metric-value">{df['company'].nunique()}</div>
# # # # # # # #         <div class="metric-label">hiring</div></div>""", unsafe_allow_html=True)

# # # # # # # # with c3:
# # # # # # # #     st.markdown(f"""<div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
# # # # # # # #         <div class="metric-label">Job Roles</div>
# # # # # # # #         <div class="metric-value">{df['title'].nunique()}</div>
# # # # # # # #         <div class="metric-label">unique</div></div>""", unsafe_allow_html=True)

# # # # # # # # with c4:
# # # # # # # #     st.markdown(f"""<div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
# # # # # # # #         <div class="metric-label">Portals</div>
# # # # # # # #         <div class="metric-value">{df['platform'].nunique()}</div>
# # # # # # # #         <div class="metric-label">sources</div></div>""", unsafe_allow_html=True)

# # # # # # # # with c5:
# # # # # # # #     st.markdown(f"""<div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
# # # # # # # #         <div class="metric-label">Locations</div>
# # # # # # # #         <div class="metric-value">{df['location'].nunique()}</div>
# # # # # # # #         <div class="metric-label">cities</div></div>""", unsafe_allow_html=True)

# # # # # # # # st.markdown("---")

# # # # # # # # # ============================================================================
# # # # # # # # # DRILL-DOWN RESULTS (Shown only if user clicked something)
# # # # # # # # # ============================================================================
# # # # # # # # if st.session_state.drill_type and st.session_state.drill_value:
# # # # # # # #     drill_val = st.session_state.drill_value
# # # # # # # #     drill_type = st.session_state.drill_type

# # # # # # # #     st.markdown(f'<div class="drill-header">🎯 Drill-Down: {drill_type} = "{drill_val}"</div>', unsafe_allow_html=True)

# # # # # # # #     # Apply drill filter
# # # # # # # #     if drill_type == "Skill":
# # # # # # # #         drill_df = df[df['skills'].apply(lambda x: drill_val in x)]
# # # # # # # #     elif drill_type == "Job Role":
# # # # # # # #         drill_df = df[df['title'] == drill_val]
# # # # # # # #     elif drill_type == "Company":
# # # # # # # #         drill_df = df[df['company'] == drill_val]
# # # # # # # #     elif drill_type == "Location":
# # # # # # # #         drill_df = df[df['location'] == drill_val]
# # # # # # # #     elif drill_type == "Portal":
# # # # # # # #         drill_df = df[df['platform'] == drill_val]
# # # # # # # #     else:
# # # # # # # #         drill_df = df.copy()

# # # # # # # #     # ---- KPI for drill ----
# # # # # # # #     d1, d2, d3, d4 = st.columns(4)
# # # # # # # #     with d1:
# # # # # # # #         st.metric("🎯 Total Openings", len(drill_df))
# # # # # # # #     with d2:
# # # # # # # #         st.metric("🏢 Companies Hiring", drill_df['company'].nunique())
# # # # # # # #     with d3:
# # # # # # # #         st.metric("📍 Locations", drill_df['location'].nunique())
# # # # # # # #     with d4:
# # # # # # # #         rp = (drill_df['is_remote'] == 'Yes').sum() / len(drill_df) * 100 if len(drill_df) > 0 else 0
# # # # # # # #         st.metric("🏠 Remote %", f"{rp:.1f}%")

# # # # # # # #     # ---- 2x2 Grid of Drill Charts ----
# # # # # # # #     st.markdown("### 📊 Where Are These Openings?")

# # # # # # # #     g1, g2 = st.columns(2)

# # # # # # # #     # Chart 1: Openings by Portal
# # # # # # # #     with g1:
# # # # # # # #         portal_counts = drill_df['platform'].value_counts().reset_index()
# # # # # # # #         portal_counts.columns = ['Portal', 'Openings']

# # # # # # # #         fig = px.bar(
# # # # # # # #             portal_counts, x='Openings', y='Portal', orientation='h',
# # # # # # # #             title=f'Openings by Portal',
# # # # # # # #             color='Openings', color_continuous_scale='Blues', text='Openings'
# # # # # # # #         )
# # # # # # # #         fig.update_layout(height=350, showlegend=False,
# # # # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # # # #                           title_font_size=13)
# # # # # # # #         fig.update_traces(textposition='outside')
# # # # # # # #         st.plotly_chart(fig, use_container_width=True, key=f"drill_portal_{drill_val}")

# # # # # # # #     # Chart 2: Openings by Company
# # # # # # # #     with g2:
# # # # # # # #         comp_counts = drill_df['company'].value_counts().head(10).reset_index()
# # # # # # # #         comp_counts.columns = ['Company', 'Openings']

# # # # # # # #         fig = px.bar(
# # # # # # # #             comp_counts, x='Openings', y='Company', orientation='h',
# # # # # # # #             title=f'Top 10 Companies Hiring',
# # # # # # # #             color='Openings', color_continuous_scale='Viridis', text='Openings'
# # # # # # # #         )
# # # # # # # #         fig.update_layout(height=350, showlegend=False,
# # # # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # # # #                           title_font_size=13)
# # # # # # # #         fig.update_traces(textposition='outside')
# # # # # # # #         st.plotly_chart(fig, use_container_width=True, key=f"drill_comp_{drill_val}")

# # # # # # # #     # Chart 3: Openings by Location
# # # # # # # #     g3, g4 = st.columns(2)

# # # # # # # #     with g3:
# # # # # # # #         loc_counts = drill_df['location'].value_counts().head(10).reset_index()
# # # # # # # #         loc_counts.columns = ['Location', 'Openings']

# # # # # # # #         fig = px.bar(
# # # # # # # #             loc_counts, x='Location', y='Openings',
# # # # # # # #             title='Top Locations',
# # # # # # # #             color='Openings', color_continuous_scale='Magma', text='Openings'
# # # # # # # #         )
# # # # # # # #         fig.update_layout(height=350, showlegend=False,
# # # # # # # #                           xaxis_tickangle=-30, title_font_size=13)
# # # # # # # #         fig.update_traces(textposition='outside')
# # # # # # # #         st.plotly_chart(fig, use_container_width=True, key=f"drill_loc_{drill_val}")

# # # # # # # #     with g4:
# # # # # # # #         # Employment type breakdown
# # # # # # # #         emp_counts = drill_df['employment_type'].value_counts().reset_index()
# # # # # # # #         emp_counts.columns = ['Type', 'Count']

# # # # # # # #         fig = px.pie(
# # # # # # # #             emp_counts, values='Count', names='Type',
# # # # # # # #             title='Employment Type Breakdown',
# # # # # # # #             hole=0.4,
# # # # # # # #             color_discrete_sequence=px.colors.qualitative.Set2
# # # # # # # #         )
# # # # # # # #         fig.update_traces(
# # # # # # # #             textinfo='percent+label',
# # # # # # # #             textposition='outside',
# # # # # # # #             textfont_size=11,
# # # # # # # #             pull=[0.03] * len(emp_counts)
# # # # # # # #         )
# # # # # # # #         fig.update_layout(height=350, title_font_size=13)
# # # # # # # #         st.plotly_chart(fig, use_container_width=True, key=f"drill_emp_{drill_val}")

# # # # # # # #     # ---- Full Job List ----
# # # # # # # #     st.markdown("### 📋 All Job Openings (Filtered)")

# # # # # # # #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # # # # # # #                  'employment_type', 'posted_date']
# # # # # # # #     display_df = drill_df[show_cols].copy()
# # # # # # # #     display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # # # # # #                           'Remote', 'Type', 'Posted']

# # # # # # # #     st.dataframe(display_df, use_container_width=True, height=400)

# # # # # # # #     # Download
# # # # # # # #     csv = drill_df.to_csv(index=False)
# # # # # # # #     st.download_button(
# # # # # # # #         label="📥 Download These Jobs as CSV",
# # # # # # # #         data=csv,
# # # # # # # #         file_name=f"drilldown_{drill_type}_{drill_val}_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # # # #         mime="text/csv"
# # # # # # # #     )

# # # # # # # #     st.markdown("---")

# # # # # # # # # ============================================================================
# # # # # # # # # MAIN TABS — 5 EXPLORATION VIEWS
# # # # # # # # # ============================================================================
# # # # # # # # st.markdown("## 🔎 Explore the Data")
# # # # # # # # st.caption("👆 Click any bar or pie slice to drill down and see all openings")

# # # # # # # # tabs = st.tabs([
# # # # # # # #     "🛠️ By Skill",
# # # # # # # #     "💼 By Job Role",
# # # # # # # #     "🏢 By Company",
# # # # # # # #     "📍 By Location",
# # # # # # # #     "🌐 By Portal"
# # # # # # # # ])

# # # # # # # # # ----------------------------------------------------------------------------
# # # # # # # # # TAB 1: DRILL BY SKILL
# # # # # # # # # ----------------------------------------------------------------------------
# # # # # # # # with tabs[0]:
# # # # # # # #     st.markdown('<div class="problem-header">🛠️ Which Skills Are In Demand? (Click to drill down)</div>', unsafe_allow_html=True)

# # # # # # # #     all_sk = [s for skills in df['skills'] for s in skills]
# # # # # # # #     skill_counts = Counter(all_sk).most_common(20)

# # # # # # # #     if skill_counts:
# # # # # # # #         sdf = pd.DataFrame(skill_counts, columns=['Skill', 'Jobs'])
# # # # # # # #         sdf['Percentage'] = (sdf['Jobs'] / len(df) * 100).round(1)

# # # # # # # #         fig = px.bar(
# # # # # # # #             sdf, x='Jobs', y='Skill', orientation='h',
# # # # # # # #             title='Top 20 Skills — Click a bar to see all openings',
# # # # # # # #             color='Jobs', color_continuous_scale='RdYlGn',
# # # # # # # #             text='Jobs',
# # # # # # # #             hover_data={'Percentage': ':.1f'}
# # # # # # # #         )
# # # # # # # #         fig.update_layout(height=650, showlegend=False,
# # # # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # # # #                           title_font_size=14,
# # # # # # # #                           clickmode='event+select')
# # # # # # # #         fig.update_traces(textposition='outside', marker_line_width=1)

# # # # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # # # #                                 on_select="rerun", key="skill_drill")

# # # # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # # # # #             if clicked and (st.session_state.drill_type != "Skill" or st.session_state.drill_value != clicked):
# # # # # # # #                 st.session_state.drill_type = "Skill"
# # # # # # # #                 st.session_state.drill_value = clicked
# # # # # # # #                 st.rerun()

# # # # # # # #         st.markdown(f"""<div class="insight-box">
# # # # # # # #             <strong>Top Skill:</strong> {skill_counts[0][0].upper()} ({skill_counts[0][1]} jobs)<br>
# # # # # # # #             <strong>Total Unique Skills:</strong> {len(skill_counts)}<br>
# # # # # # # #             <strong>💡 Action:</strong> Click any skill bar above to see <strong>where all these jobs are posted</strong>
# # # # # # # #         </div>""", unsafe_allow_html=True)

# # # # # # # # # ----------------------------------------------------------------------------
# # # # # # # # # TAB 2: DRILL BY JOB ROLE
# # # # # # # # # ----------------------------------------------------------------------------
# # # # # # # # with tabs[1]:
# # # # # # # #     st.markdown('<div class="problem-header">💼 Job Roles — Click to see all openings & portals</div>', unsafe_allow_html=True)

# # # # # # # #     title_counts = df['title'].value_counts().head(20).reset_index()
# # # # # # # #     title_counts.columns = ['Job Role', 'Openings']

# # # # # # # #     fig = px.bar(
# # # # # # # #         title_counts, x='Openings', y='Job Role', orientation='h',
# # # # # # # #         title='Top 20 Job Roles — Click a bar to see all openings',
# # # # # # # #         color='Openings', color_continuous_scale='Viridis', text='Openings'
# # # # # # # #     )
# # # # # # # #     fig.update_layout(height=650, showlegend=False,
# # # # # # # #                       yaxis=dict(autorange="reversed"),
# # # # # # # #                       title_font_size=14,
# # # # # # # #                       clickmode='event+select')
# # # # # # # #     fig.update_traces(textposition='outside')

# # # # # # # #     event = st.plotly_chart(fig, use_container_width=True,
# # # # # # # #                             on_select="rerun", key="role_drill")

# # # # # # # #     if event and event.get("selection") and event["selection"].get("points"):
# # # # # # # #         clicked = event["selection"]["points"][0].get("y")
# # # # # # # #         if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
# # # # # # # #             st.session_state.drill_type = "Job Role"
# # # # # # # #             st.session_state.drill_value = clicked
# # # # # # # #             st.rerun()

# # # # # # # #     st.markdown(f"""<div class="insight-box">
# # # # # # # #         <strong>Top Role:</strong> {title_counts.iloc[0]['Job Role']} ({title_counts.iloc[0]['Openings']} openings)<br>
# # # # # # # #         <strong>Total Unique Roles:</strong> {df['title'].nunique()}<br>
# # # # # # # #         <strong>💡 Action:</strong> Click a job role to see <strong>every company hiring for it and on which portal</strong>
# # # # # # # #     </div>""", unsafe_allow_html=True)

# # # # # # # # # ----------------------------------------------------------------------------
# # # # # # # # # TAB 3: DRILL BY COMPANY
# # # # # # # # # ----------------------------------------------------------------------------
# # # # # # # # with tabs[2]:
# # # # # # # #     st.markdown('<div class="problem-header">🏢 Companies — Click to see their openings</div>', unsafe_allow_html=True)

# # # # # # # #     comp_counts = df['company'].value_counts().head(20).reset_index()
# # # # # # # #     comp_counts.columns = ['Company', 'Openings']

# # # # # # # #     fig = px.bar(
# # # # # # # #         comp_counts, x='Openings', y='Company', orientation='h',
# # # # # # # #         title='Top 20 Companies — Click a bar',
# # # # # # # #         color='Openings', color_continuous_scale='Cividis', text='Openings'
# # # # # # # #     )
# # # # # # # #     fig.update_layout(height=650, showlegend=False,
# # # # # # # #                       yaxis=dict(autorange="reversed"),
# # # # # # # #                       title_font_size=14,
# # # # # # # #                       clickmode='event+select')
# # # # # # # #     fig.update_traces(textposition='outside')

# # # # # # # #     event = st.plotly_chart(fig, use_container_width=True,
# # # # # # # #                             on_select="rerun", key="company_drill")

# # # # # # # #     if event and event.get("selection") and event["selection"].get("points"):
# # # # # # # #         clicked = event["selection"]["points"][0].get("y")
# # # # # # # #         if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
# # # # # # # #             st.session_state.drill_type = "Company"
# # # # # # # #             st.session_state.drill_value = clicked
# # # # # # # #             st.rerun()

# # # # # # # #     st.markdown(f"""<div class="insight-box">
# # # # # # # #         <strong>Top Employer:</strong> {comp_counts.iloc[0]['Company']} ({comp_counts.iloc[0]['Openings']} jobs)<br>
# # # # # # # #         <strong>💡 Action:</strong> Click a company to see <strong>all their job openings across portals</strong>
# # # # # # # #     </div>""", unsafe_allow_html=True)

# # # # # # # # # ----------------------------------------------------------------------------
# # # # # # # # # TAB 4: DRILL BY LOCATION
# # # # # # # # # ----------------------------------------------------------------------------
# # # # # # # # with tabs[3]:
# # # # # # # #     st.markdown('<div class="problem-header">📍 Locations — Click to see all openings in that city</div>', unsafe_allow_html=True)

# # # # # # # #     loc_counts = df['location'].value_counts().head(20).reset_index()
# # # # # # # #     loc_counts.columns = ['Location', 'Openings']

# # # # # # # #     fig = px.bar(
# # # # # # # #         loc_counts, x='Location', y='Openings',
# # # # # # # #         title='Top 20 Locations — Click a bar',
# # # # # # # #         color='Openings', color_continuous_scale='Turbo', text='Openings'
# # # # # # # #     )
# # # # # # # #     fig.update_layout(height=500, showlegend=False,
# # # # # # # #                       xaxis_tickangle=-40, title_font_size=14,
# # # # # # # #                       clickmode='event+select')
# # # # # # # #     fig.update_traces(textposition='outside')

# # # # # # # #     event = st.plotly_chart(fig, use_container_width=True,
# # # # # # # #                             on_select="rerun", key="loc_drill")

# # # # # # # #     if event and event.get("selection") and event["selection"].get("points"):
# # # # # # # #         clicked = event["selection"]["points"][0].get("x")
# # # # # # # #         if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
# # # # # # # #             st.session_state.drill_type = "Location"
# # # # # # # #             st.session_state.drill_value = clicked
# # # # # # # #             st.rerun()

# # # # # # # #     st.markdown(f"""<div class="insight-box">
# # # # # # # #         <strong>Top City:</strong> {loc_counts.iloc[0]['Location']} ({loc_counts.iloc[0]['Openings']} jobs)<br>
# # # # # # # #         <strong>💡 Action:</strong> Click a city to see <strong>all jobs, companies, and portals there</strong>
# # # # # # # #     </div>""", unsafe_allow_html=True)

# # # # # # # # # ----------------------------------------------------------------------------
# # # # # # # # # TAB 5: DRILL BY PORTAL
# # # # # # # # # ----------------------------------------------------------------------------
# # # # # # # # with tabs[4]:
# # # # # # # #     st.markdown('<div class="problem-header">🌐 Portals — Click to see all jobs from that portal</div>', unsafe_allow_html=True)

# # # # # # # #     portal_counts = df['platform'].value_counts().reset_index()
# # # # # # # #     portal_counts.columns = ['Portal', 'Openings']

# # # # # # # #     c1, c2 = st.columns(2)

# # # # # # # #     with c1:
# # # # # # # #         fig = px.bar(
# # # # # # # #             portal_counts, x='Portal', y='Openings',
# # # # # # # #             title='Jobs by Portal — Click a bar',
# # # # # # # #             color='Openings', color_continuous_scale='Plasma', text='Openings'
# # # # # # # #         )
# # # # # # # #         fig.update_layout(height=450, showlegend=False,
# # # # # # # #                           xaxis_tickangle=-30, title_font_size=13,
# # # # # # # #                           clickmode='event+select')
# # # # # # # #         fig.update_traces(textposition='outside')

# # # # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # # # #                                 on_select="rerun", key="portal_drill_bar")

# # # # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # # # #             clicked = event["selection"]["points"][0].get("x")
# # # # # # # #             if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
# # # # # # # #                 st.session_state.drill_type = "Portal"
# # # # # # # #                 st.session_state.drill_value = clicked
# # # # # # # #                 st.rerun()

# # # # # # # #     with c2:
# # # # # # # #         fig = px.pie(
# # # # # # # #             portal_counts, values='Openings', names='Portal',
# # # # # # # #             title='Portal Distribution — Click a slice',
# # # # # # # #             hole=0.4,
# # # # # # # #             color_discrete_sequence=px.colors.qualitative.Set3
# # # # # # # #         )
# # # # # # # #         fig.update_traces(
# # # # # # # #             textinfo='percent+label',
# # # # # # # #             textposition='outside',
# # # # # # # #             textfont_size=11,
# # # # # # # #             pull=[0.03] * len(portal_counts)
# # # # # # # #         )
# # # # # # # #         fig.update_layout(height=450, title_font_size=13)

# # # # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # # # #                                 on_select="rerun", key="portal_drill_pie")

# # # # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # # # #             pt = event["selection"]["points"][0]
# # # # # # # #             clicked = pt.get("label") or pt.get("legendgroup")
# # # # # # # #             if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
# # # # # # # #                 st.session_state.drill_type = "Portal"
# # # # # # # #                 st.session_state.drill_value = clicked
# # # # # # # #                 st.rerun()

# # # # # # # #     st.markdown(f"""<div class="insight-box">
# # # # # # # #         <strong>Top Portal:</strong> {portal_counts.iloc[0]['Portal']} ({portal_counts.iloc[0]['Openings']} jobs)<br>
# # # # # # # #         <strong>💡 Action:</strong> Click a portal to see <strong>all jobs, skills, and companies on that portal</strong>
# # # # # # # #     </div>""", unsafe_allow_html=True)

# # # # # # # # # ============================================================================
# # # # # # # # # FOOTER
# # # # # # # # # ============================================================================
# # # # # # # # st.markdown("---")
# # # # # # # # st.markdown(f"""<div style='text-align:center; color:#666; font-size:12px;'>
# # # # # # # #     Job Market Drill-Down Analytics | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
# # # # # # # #     {len(df)} total jobs | {df['company'].nunique()} companies | {df['platform'].nunique()} portals
# # # # # # # # </div>""", unsafe_allow_html=True)





















# # # # # # # """
# # # # # # # ================================================================================
# # # # # # # JOB MARKET ANALYTICS — CLICKABLE KPI DASHBOARD
# # # # # # # Click KPI cards to see detailed lists + Drill-down on charts
# # # # # # # Tech Stack: Python | Pandas | NumPy | Plotly | Streamlit
# # # # # # # Run: python -m streamlit run dashboard.py
# # # # # # # ================================================================================
# # # # # # # """

# # # # # # # import streamlit as st
# # # # # # # import pandas as pd
# # # # # # # import numpy as np
# # # # # # # import plotly.express as px
# # # # # # # import plotly.graph_objects as go
# # # # # # # from collections import Counter
# # # # # # # from datetime import datetime
# # # # # # # import warnings
# # # # # # # import logging

# # # # # # # warnings.filterwarnings('ignore')
# # # # # # # logging.getLogger('streamlit').setLevel(logging.ERROR)

# # # # # # # # ============================================================================
# # # # # # # # PAGE CONFIG
# # # # # # # # ============================================================================
# # # # # # # st.set_page_config(
# # # # # # #     page_title="Job Market Analytics",
# # # # # # #     page_icon="🎯",
# # # # # # #     layout="wide",
# # # # # # #     initial_sidebar_state="expanded"
# # # # # # # )

# # # # # # # # CSS
# # # # # # # st.markdown("""
# # # # # # # <style>
    /* ========== FORCE DARK TEXT EVERYWHERE ========== */
    .stApp, .stApp * {
        color: #1a1a1a !important;
    }
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricLabel"] > div {
        color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stDataFrame"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
    }
# # # # # # #     div[data-testid="stMarkdownContainer"] div,
# # # # # # #     div[data-testid="stMarkdownContainer"] p,
# # # # # # #     div[data-testid="stMarkdownContainer"] span,
# # # # # # #     div[data-testid="stMarkdownContainer"] strong { color: #1a1a1a; }

# # # # # # #     .main-header {
# # # # # # #         font-size: 2.2rem; font-weight: bold;
# # # # # # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # # # # # #         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
# # # # # # #         text-align: center; padding: 0.5rem 0;
# # # # # # #     }
# # # # # # #     .sub-header { text-align: center; color: #666; margin-bottom: 1rem; }
# # # # # # #     .problem-header {
# # # # # # #         background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
# # # # # # #         padding: 0.7rem 1rem; border-radius: 8px;
# # # # # # #         color: #FFFFFF !important; font-weight: bold;
# # # # # # #         margin-bottom: 1rem; font-size: 1rem;
# # # # # # #     }
# # # # # # #     .insight-box {
# # # # # # #         background: #f0f7ff; padding: 0.8rem;
# # # # # # #         border-left: 4px solid #667eea; border-radius: 5px;
# # # # # # #         margin: 0.6rem 0; font-size: 0.9rem; color: #1a1a1a !important;
# # # # # # #     }
# # # # # # #     .insight-box strong { color: #2c3e50 !important; font-weight: 700; }
# # # # # # #     .drill-header {
# # # # # # #         background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
# # # # # # #         padding: 0.8rem 1rem; border-radius: 8px;
# # # # # # #         color: #1a1a1a !important; font-weight: bold;
# # # # # # #         margin: 1rem 0; font-size: 1.1rem;
# # # # # # #         border: 2px solid #43e97b;
# # # # # # #     }
# # # # # # #     .stTabs [data-baseweb="tab-list"] { gap: 6px; flex-wrap: wrap; }
# # # # # # #     .stTabs [data-baseweb="tab"] {
# # # # # # #         background-color: #f0f2f6; border-radius: 6px;
# # # # # # #         padding: 8px 12px; font-weight: 600; font-size: 0.78rem;
# # # # # # #     }
# # # # # # #     .stTabs [aria-selected="true"] {
# # # # # # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # # # # # #         color: #FFFFFF !important;
# # # # # # #     }
# # # # # # #     /* KPI Button styling */
# # # # # # #     div[data-testid="stButton"] button {
# # # # # # #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# # # # # # #         color: white !important;
# # # # # # #         border: none;
# # # # # # #         padding: 1.5rem 1rem;
# # # # # # #         border-radius: 12px;
# # # # # # #         width: 100%;
# # # # # # #         min-height: 120px;
# # # # # # #         font-size: 1rem;
# # # # # # #         font-weight: bold;
# # # # # # #         box-shadow: 0 4px 12px rgba(0,0,0,0.1);
# # # # # # #         transition: transform 0.2s;
# # # # # # #     }
# # # # # # #     div[data-testid="stButton"] button:hover {
# # # # # # #         transform: translateY(-3px);
# # # # # # #         box-shadow: 0 6px 16px rgba(0,0,0,0.2);
# # # # # # #     }
# # # # # # #     div[data-testid="stButton"] button p {
# # # # # # #         color: white !important;
# # # # # # #         font-size: 1rem;
# # # # # # #         font-weight: bold;
# # # # # # #     }
# # # # # # # </style>
# # # # # # # """, unsafe_allow_html=True)

# # # # # # # # ============================================================================
# # # # # # # # DATA LOADING
# # # # # # # # ============================================================================

# # # # # # # @st.cache_data
# # # # # # # def load_data():
# # # # # # #     df = pd.read_csv("job_data_clean.csv")
# # # # # # #     df['posted_date'] = pd.to_datetime(df['posted_date'], errors='coerce')
# # # # # # #     return df

# # # # # # # def extract_skills(text):
# # # # # # #     if pd.isna(text):
# # # # # # #         return []
# # # # # # #     text = str(text).lower()
# # # # # # #     skill_list = [
# # # # # # #         'python', 'java', 'sql', 'javascript', 'typescript', 'react', 'angular',
# # # # # # #         'node.js', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
# # # # # # #         'jenkins', 'spark', 'kafka', 'airflow', 'snowflake', 'tableau', 'power bi',
# # # # # # #         'machine learning', 'deep learning', 'nlp', 'llm', 'genai', 'rag',
# # # # # # #         'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
# # # # # # #         'excel', 'git', 'linux', 'agile', 'scrum', 'jira'
# # # # # # #     ]
# # # # # # #     return list(set([s for s in skill_list if s in text]))

# # # # # # # try:
# # # # # # #     df = load_data()
# # # # # # #     df['skills'] = df['description'].apply(extract_skills)
# # # # # # #     df['skill_count'] = df['skills'].apply(len)
# # # # # # # except Exception as e:
# # # # # # #     st.error(f"❌ Error loading 'job_data_clean.csv': {e}")
# # # # # # #     st.stop()

# # # # # # # # ============================================================================
# # # # # # # # HEADER
# # # # # # # # ============================================================================
# # # # # # # st.markdown('<h1 class="main-header">🎯 Job Market Analytics</h1>', unsafe_allow_html=True)
# # # # # # # st.markdown('<p class="sub-header">Click any KPI card to see the detailed list • Click charts to drill down</p>', unsafe_allow_html=True)

# # # # # # # # ============================================================================
# # # # # # # # SESSION STATE
# # # # # # # # ============================================================================
# # # # # # # for key in ['view', 'drill_type', 'drill_value']:
# # # # # # #     if key not in st.session_state:
# # # # # # #         st.session_state[key] = None

# # # # # # # # Reset button in sidebar
# # # # # # # st.sidebar.markdown("## 🔍 Navigation")
# # # # # # # if st.sidebar.button("🏠 Home (Clear View)"):
# # # # # # #     st.session_state.view = None
# # # # # # #     st.session_state.drill_type = None
# # # # # # #     st.session_state.drill_value = None
# # # # # # #     st.rerun()

# # # # # # # if st.session_state.view:
# # # # # # #     st.sidebar.success(f"**Viewing:** {st.session_state.view}")

# # # # # # # if st.session_state.drill_type:
# # # # # # #     st.sidebar.info(f"**Drill:** {st.session_state.drill_type} = {st.session_state.drill_value}")
# # # # # # #     if st.sidebar.button("❌ Clear Drill"):
# # # # # # #         st.session_state.drill_type = None
# # # # # # #         st.session_state.drill_value = None
# # # # # # #         st.rerun()

# # # # # # # st.sidebar.markdown("---")
# # # # # # # st.sidebar.markdown(f"**📊 Total Jobs:** {len(df)}")

# # # # # # # # ============================================================================
# # # # # # # # KPI CARDS — CLICKABLE BUTTONS
# # # # # # # # ============================================================================
# # # # # # # st.markdown("## 📈 Overview — Click to Explore")

# # # # # # # k1, k2, k3, k4, k5 = st.columns(5)

# # # # # # # with k1:
# # # # # # #     if st.button(f"📊\n\n**Total Jobs**\n\n{len(df)}\n\n_in dataset_",
# # # # # # #                  key="kpi_total", use_container_width=True):
# # # # # # #         st.session_state.view = "Total Jobs"
# # # # # # #         st.session_state.drill_type = None
# # # # # # #         st.rerun()

# # # # # # # with k2:
# # # # # # #     if st.button(f"🏢\n\n**Companies**\n\n{df['company'].nunique()}\n\n_hiring_",
# # # # # # #                  key="kpi_company", use_container_width=True):
# # # # # # #         st.session_state.view = "Companies"
# # # # # # #         st.session_state.drill_type = None
# # # # # # #         st.rerun()

# # # # # # # with k3:
# # # # # # #     if st.button(f"💼\n\n**Job Roles**\n\n{df['title'].nunique()}\n\n_unique_",
# # # # # # #                  key="kpi_title", use_container_width=True):
# # # # # # #         st.session_state.view = "Job Roles"
# # # # # # #         st.session_state.drill_type = None
# # # # # # #         st.rerun()

# # # # # # # with k4:
# # # # # # #     if st.button(f"🌐\n\n**Portals**\n\n{df['platform'].nunique()}\n\n_sources_",
# # # # # # #                  key="kpi_portal", use_container_width=True):
# # # # # # #         st.session_state.view = "Portals"
# # # # # # #         st.session_state.drill_type = None
# # # # # # #         st.rerun()

# # # # # # # with k5:
# # # # # # #     if st.button(f"📍\n\n**Locations**\n\n{df['location'].nunique()}\n\n_cities_",
# # # # # # #                  key="kpi_location", use_container_width=True):
# # # # # # #         st.session_state.view = "Locations"
# # # # # # #         st.session_state.drill_type = None
# # # # # # #         st.rerun()

# # # # # # # st.markdown("---")

# # # # # # # # ============================================================================
# # # # # # # # VIEW: COMPANIES — FULL LIST
# # # # # # # # ============================================================================
# # # # # # # if st.session_state.view == "Companies":
# # # # # # #     st.markdown('<div class="drill-header">🏢 All Companies Hiring — Click any company to drill down</div>', unsafe_allow_html=True)

# # # # # # #     comp_df = df['company'].value_counts().reset_index()
# # # # # # #     comp_df.columns = ['Company', 'Openings']
# # # # # # #     comp_df['Share %'] = (comp_df['Openings'] / len(df) * 100).round(2)

# # # # # # #     c1, c2 = st.columns([3, 2])

# # # # # # #     with c1:
# # # # # # #         fig = px.bar(
# # # # # # #             comp_df.head(30), x='Openings', y='Company', orientation='h',
# # # # # # #             title=f'All {len(comp_df)} Companies (Top 30 shown) — Click a bar',
# # # # # # #             color='Openings', color_continuous_scale='Viridis', text='Openings'
# # # # # # #         )
# # # # # # #         fig.update_layout(height=800, showlegend=False,
# # # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # # #                           title_font_size=14,
# # # # # # #                           clickmode='event+select')
# # # # # # #         fig.update_traces(textposition='outside')

# # # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # # #                                 on_select="rerun", key="comp_list_drill")

# # # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # # # #             if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
# # # # # # #                 st.session_state.drill_type = "Company"
# # # # # # #                 st.session_state.drill_value = clicked
# # # # # # #                 st.rerun()

# # # # # # #     with c2:
# # # # # # #         st.markdown("### 📋 Complete Company List")
# # # # # # #         st.dataframe(comp_df, use_container_width=True, height=750, hide_index=True)

# # # # # # #     # Download
# # # # # # #     csv = comp_df.to_csv(index=False)
# # # # # # #     st.download_button(
# # # # # # #         label="📥 Download Full Company List (CSV)",
# # # # # # #         data=csv,
# # # # # # #         file_name=f"all_companies_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # # #         mime="text/csv",
# # # # # # #         key="dl_companies"
# # # # # # #     )

# # # # # # # # ============================================================================
# # # # # # # # VIEW: LOCATIONS — FULL LIST
# # # # # # # # ============================================================================
# # # # # # # elif st.session_state.view == "Locations":
# # # # # # #     st.markdown('<div class="drill-header">📍 All Locations — Click any city to drill down</div>', unsafe_allow_html=True)

# # # # # # #     loc_df = df['location'].value_counts().reset_index()
# # # # # # #     loc_df.columns = ['Location', 'Openings']
# # # # # # #     loc_df['Share %'] = (loc_df['Openings'] / len(df) * 100).round(2)

# # # # # # #     c1, c2 = st.columns([3, 2])

# # # # # # #     with c1:
# # # # # # #         fig = px.bar(
# # # # # # #             loc_df, x='Openings', y='Location', orientation='h',
# # # # # # #             title=f'All {len(loc_df)} Locations — Click a bar',
# # # # # # #             color='Openings', color_continuous_scale='Magma', text='Openings'
# # # # # # #         )
# # # # # # #         fig.update_layout(height=max(600, len(loc_df)*22), showlegend=False,
# # # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # # #                           title_font_size=14,
# # # # # # #                           clickmode='event+select')
# # # # # # #         fig.update_traces(textposition='outside')

# # # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # # #                                 on_select="rerun", key="loc_list_drill")

# # # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # # # #             if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
# # # # # # #                 st.session_state.drill_type = "Location"
# # # # # # #                 st.session_state.drill_value = clicked
# # # # # # #                 st.rerun()

# # # # # # #     with c2:
# # # # # # #         st.markdown("### 📋 Complete Location List")
# # # # # # #         st.dataframe(loc_df, use_container_width=True, height=750, hide_index=True)

# # # # # # #     csv = loc_df.to_csv(index=False)
# # # # # # #     st.download_button(
# # # # # # #         label="📥 Download Full Location List (CSV)",
# # # # # # #         data=csv,
# # # # # # #         file_name=f"all_locations_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # # #         mime="text/csv",
# # # # # # #         key="dl_locations"
# # # # # # #     )

# # # # # # # # ============================================================================
# # # # # # # # VIEW: JOB ROLES — FULL LIST
# # # # # # # # ============================================================================
# # # # # # # elif st.session_state.view == "Job Roles":
# # # # # # #     st.markdown('<div class="drill-header">💼 All Job Roles — Click any role to drill down</div>', unsafe_allow_html=True)

# # # # # # #     role_df = df['title'].value_counts().reset_index()
# # # # # # #     role_df.columns = ['Job Role', 'Openings']
# # # # # # #     role_df['Share %'] = (role_df['Openings'] / len(df) * 100).round(2)

# # # # # # #     c1, c2 = st.columns([3, 2])

# # # # # # #     with c1:
# # # # # # #         fig = px.bar(
# # # # # # #             role_df.head(40), x='Openings', y='Job Role', orientation='h',
# # # # # # #             title=f'All {len(role_df)} Job Roles (Top 40 shown) — Click a bar',
# # # # # # #             color='Openings', color_continuous_scale='Plasma', text='Openings'
# # # # # # #         )
# # # # # # #         fig.update_layout(height=1000, showlegend=False,
# # # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # # #                           title_font_size=14,
# # # # # # #                           clickmode='event+select')
# # # # # # #         fig.update_traces(textposition='outside')

# # # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # # #                                 on_select="rerun", key="role_list_drill")

# # # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # # # #             if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
# # # # # # #                 st.session_state.drill_type = "Job Role"
# # # # # # #                 st.session_state.drill_value = clicked
# # # # # # #                 st.rerun()

# # # # # # #     with c2:
# # # # # # #         st.markdown("### 📋 Complete Job Roles List")
# # # # # # #         st.dataframe(role_df, use_container_width=True, height=950, hide_index=True)

# # # # # # #     csv = role_df.to_csv(index=False)
# # # # # # #     st.download_button(
# # # # # # #         label="📥 Download Full Job Roles (CSV)",
# # # # # # #         data=csv,
# # # # # # #         file_name=f"all_roles_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # # #         mime="text/csv",
# # # # # # #         key="dl_roles"
# # # # # # #     )

# # # # # # # # ============================================================================
# # # # # # # # VIEW: PORTALS — FULL LIST
# # # # # # # # ============================================================================
# # # # # # # elif st.session_state.view == "Portals":
# # # # # # #     st.markdown('<div class="drill-header">🌐 All Portals — Click any portal to drill down</div>', unsafe_allow_html=True)

# # # # # # #     portal_df = df['platform'].value_counts().reset_index()
# # # # # # #     portal_df.columns = ['Portal', 'Openings']
# # # # # # #     portal_df['Share %'] = (portal_df['Openings'] / len(df) * 100).round(2)

# # # # # # #     c1, c2 = st.columns([2, 2])

# # # # # # #     with c1:
# # # # # # #         fig = px.bar(
# # # # # # #             portal_df, x='Portal', y='Openings',
# # # # # # #             title='All Portals — Click a bar',
# # # # # # #             color='Openings', color_continuous_scale='Turbo', text='Openings'
# # # # # # #         )
# # # # # # #         fig.update_layout(height=500, showlegend=False,
# # # # # # #                           xaxis_tickangle=-30, title_font_size=14,
# # # # # # #                           clickmode='event+select')
# # # # # # #         fig.update_traces(textposition='outside')

# # # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # # #                                 on_select="rerun", key="portal_list_drill")

# # # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # # #             clicked = event["selection"]["points"][0].get("x")
# # # # # # #             if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
# # # # # # #                 st.session_state.drill_type = "Portal"
# # # # # # #                 st.session_state.drill_value = clicked
# # # # # # #                 st.rerun()

# # # # # # #     with c2:
# # # # # # #         st.markdown("### 📋 Complete Portal List")
# # # # # # #         st.dataframe(portal_df, use_container_width=True, hide_index=True)

# # # # # # #         # Show jobs per portal visually
# # # # # # #         fig = px.pie(
# # # # # # #             portal_df, values='Openings', names='Portal',
# # # # # # #             title='Portal Distribution',
# # # # # # #             hole=0.4,
# # # # # # #             color_discrete_sequence=px.colors.qualitative.Set3
# # # # # # #         )
# # # # # # #         fig.update_traces(
# # # # # # #             textinfo='percent+label',
# # # # # # #             textposition='outside',
# # # # # # #             textfont_size=11,
# # # # # # #             pull=[0.03] * len(portal_df)
# # # # # # #         )
# # # # # # #         fig.update_layout(height=400, title_font_size=14)
# # # # # # #         st.plotly_chart(fig, use_container_width=True)

# # # # # # #     csv = portal_df.to_csv(index=False)
# # # # # # #     st.download_button(
# # # # # # #         label="📥 Download Full Portal List (CSV)",
# # # # # # #         data=csv,
# # # # # # #         file_name=f"all_portals_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # # #         mime="text/csv",
# # # # # # #         key="dl_portals"
# # # # # # #     )

# # # # # # # # ============================================================================
# # # # # # # # VIEW: TOTAL JOBS — FULL LIST
# # # # # # # # ============================================================================
# # # # # # # elif st.session_state.view == "Total Jobs":
# # # # # # #     st.markdown('<div class="drill-header">📊 All Jobs in Dataset</div>', unsafe_allow_html=True)

# # # # # # #     st.markdown(f"### 📋 Showing all {len(df)} jobs")

# # # # # # #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # # # # # #                  'employment_type', 'posted_date']
# # # # # # #     display_df = df[show_cols].copy()
# # # # # # #     display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # # # # #                           'Remote', 'Type', 'Posted']

# # # # # # #     st.dataframe(display_df, use_container_width=True, height=600)

# # # # # # #     csv = df.to_csv(index=False)
# # # # # # #     st.download_button(
# # # # # # #         label="📥 Download All Jobs (CSV)",
# # # # # # #         data=csv,
# # # # # # #         file_name=f"all_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # # #         mime="text/csv",
# # # # # # #         key="dl_all_jobs"
# # # # # # #     )

# # # # # # # # ============================================================================
# # # # # # # # DRILL-DOWN DETAIL PANEL (when user clicks a specific item)
# # # # # # # # ============================================================================
# # # # # # # if st.session_state.drill_type and st.session_state.drill_value:
# # # # # # #     st.markdown("---")
# # # # # # #     drill_val = st.session_state.drill_value
# # # # # # #     drill_type = st.session_state.drill_type

# # # # # # #     st.markdown(f'<div class="drill-header">🎯 Drill-Down: {drill_type} = "{drill_val}"</div>', unsafe_allow_html=True)

# # # # # # #     # Apply filter
# # # # # # #     if drill_type == "Skill":
# # # # # # #         drill_df = df[df['skills'].apply(lambda x: drill_val in x)]
# # # # # # #     elif drill_type == "Job Role":
# # # # # # #         drill_df = df[df['title'] == drill_val]
# # # # # # #     elif drill_type == "Company":
# # # # # # #         drill_df = df[df['company'] == drill_val]
# # # # # # #     elif drill_type == "Location":
# # # # # # #         drill_df = df[df['location'] == drill_val]
# # # # # # #     elif drill_type == "Portal":
# # # # # # #         drill_df = df[df['platform'] == drill_val]
# # # # # # #     else:
# # # # # # #         drill_df = df.copy()

# # # # # # #     # KPI for drill
# # # # # # #     d1, d2, d3, d4 = st.columns(4)
# # # # # # #     with d1:
# # # # # # #         st.metric("🎯 Total Openings", len(drill_df))
# # # # # # #     with d2:
# # # # # # #         st.metric("🏢 Companies Hiring", drill_df['company'].nunique())
# # # # # # #     with d3:
# # # # # # #         st.metric("📍 Locations", drill_df['location'].nunique())
# # # # # # #     with d4:
# # # # # # #         rp = (drill_df['is_remote'] == 'Yes').sum() / len(drill_df) * 100 if len(drill_df) > 0 else 0
# # # # # # #         st.metric("🏠 Remote %", f"{rp:.1f}%")

# # # # # # #     # Charts
# # # # # # #     st.markdown("### 📊 Where Are These Openings?")

# # # # # # #     g1, g2 = st.columns(2)
# # # # # # #     with g1:
# # # # # # #         portal_counts = drill_df['platform'].value_counts().reset_index()
# # # # # # #         portal_counts.columns = ['Portal', 'Openings']
# # # # # # #         fig = px.bar(portal_counts, x='Openings', y='Portal', orientation='h',
# # # # # # #                      title='Openings by Portal',
# # # # # # #                      color='Openings', color_continuous_scale='Blues', text='Openings')
# # # # # # #         fig.update_layout(height=350, showlegend=False,
# # # # # # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # # # # # #         fig.update_traces(textposition='outside')
# # # # # # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_portal_{drill_val}")

# # # # # # #     with g2:
# # # # # # #         comp_counts = drill_df['company'].value_counts().head(10).reset_index()
# # # # # # #         comp_counts.columns = ['Company', 'Openings']
# # # # # # #         fig = px.bar(comp_counts, x='Openings', y='Company', orientation='h',
# # # # # # #                      title='Top 10 Companies',
# # # # # # #                      color='Openings', color_continuous_scale='Viridis', text='Openings')
# # # # # # #         fig.update_layout(height=350, showlegend=False,
# # # # # # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # # # # # #         fig.update_traces(textposition='outside')
# # # # # # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_comp_{drill_val}")

# # # # # # #     g3, g4 = st.columns(2)
# # # # # # #     with g3:
# # # # # # #         loc_counts = drill_df['location'].value_counts().head(10).reset_index()
# # # # # # #         loc_counts.columns = ['Location', 'Openings']
# # # # # # #         fig = px.bar(loc_counts, x='Location', y='Openings',
# # # # # # #                      title='Top Locations',
# # # # # # #                      color='Openings', color_continuous_scale='Magma', text='Openings')
# # # # # # #         fig.update_layout(height=350, showlegend=False,
# # # # # # #                           xaxis_tickangle=-30, title_font_size=13)
# # # # # # #         fig.update_traces(textposition='outside')
# # # # # # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_loc_{drill_val}")

# # # # # # #     with g4:
# # # # # # #         emp_counts = drill_df['employment_type'].value_counts().reset_index()
# # # # # # #         emp_counts.columns = ['Type', 'Count']
# # # # # # #         fig = px.pie(emp_counts, values='Count', names='Type',
# # # # # # #                      title='Employment Type',
# # # # # # #                      hole=0.4,
# # # # # # #                      color_discrete_sequence=px.colors.qualitative.Set2)
# # # # # # #         fig.update_traces(textinfo='percent+label', textposition='outside',
# # # # # # #                           textfont_size=11, pull=[0.03] * len(emp_counts))
# # # # # # #         fig.update_layout(height=350, title_font_size=13)
# # # # # # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_emp_{drill_val}")

# # # # # # #     # Full list
# # # # # # #     st.markdown("### 📋 All Job Openings")
# # # # # # #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # # # # # #                  'employment_type', 'posted_date']
# # # # # # #     display_df = drill_df[show_cols].copy()
# # # # # # #     display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # # # # #                           'Remote', 'Type', 'Posted']
# # # # # # #     st.dataframe(display_df, use_container_width=True, height=400)

# # # # # # #     csv = drill_df.to_csv(index=False)
# # # # # # #     st.download_button(
# # # # # # #         label="📥 Download These Jobs (CSV)",
# # # # # # #         data=csv,
# # # # # # #         file_name=f"drilldown_{drill_type}_{drill_val}_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # # #         mime="text/csv",
# # # # # # #         key=f"dl_drill_{drill_val}"
# # # # # # #     )

# # # # # # # # ============================================================================
# # # # # # # # MAIN TABS (only show when no view is active)
# # # # # # # # ============================================================================
# # # # # # # if st.session_state.view is None:
# # # # # # #     st.markdown("---")
# # # # # # #     st.markdown("## 🔎 Explore Charts — Click to drill down")
# # # # # # #     st.caption("👆 Click any bar or pie slice to see all openings")

# # # # # # #     tabs = st.tabs([
# # # # # # #         "🛠️ By Skill",
# # # # # # #         "💼 By Job Role",
# # # # # # #         "🏢 By Company",
# # # # # # #         "📍 By Location",
# # # # # # #         "🌐 By Portal"
# # # # # # #     ])

# # # # # # #     # TAB 1: SKILL
# # # # # # #     with tabs[0]:
# # # # # # #         st.markdown('<div class="problem-header">🛠️ In-Demand Skills — Click a bar</div>', unsafe_allow_html=True)
# # # # # # #         all_sk = [s for skills in df['skills'] for s in skills]
# # # # # # #         skill_counts = Counter(all_sk).most_common(20)

# # # # # # #         if skill_counts:
# # # # # # #             sdf = pd.DataFrame(skill_counts, columns=['Skill', 'Jobs'])
# # # # # # #             fig = px.bar(sdf, x='Jobs', y='Skill', orientation='h',
# # # # # # #                          title='Top 20 Skills — Click a bar to drill down',
# # # # # # #                          color='Jobs', color_continuous_scale='RdYlGn', text='Jobs')
# # # # # # #             fig.update_layout(height=650, showlegend=False,
# # # # # # #                               yaxis=dict(autorange="reversed"),
# # # # # # #                               title_font_size=14, clickmode='event+select')
# # # # # # #             fig.update_traces(textposition='outside')

# # # # # # #             event = st.plotly_chart(fig, use_container_width=True,
# # # # # # #                                     on_select="rerun", key="skill_drill_main")

# # # # # # #             if event and event.get("selection") and event["selection"].get("points"):
# # # # # # #                 clicked = event["selection"]["points"][0].get("y")
# # # # # # #                 if clicked and (st.session_state.drill_type != "Skill" or st.session_state.drill_value != clicked):
# # # # # # #                     st.session_state.drill_type = "Skill"
# # # # # # #                     st.session_state.drill_value = clicked
# # # # # # #                     st.rerun()

# # # # # # #     # TAB 2: JOB ROLE
# # # # # # #     with tabs[1]:
# # # # # # #         st.markdown('<div class="problem-header">💼 Job Roles — Click a bar</div>', unsafe_allow_html=True)
# # # # # # #         title_counts = df['title'].value_counts().head(20).reset_index()
# # # # # # #         title_counts.columns = ['Job Role', 'Openings']

# # # # # # #         fig = px.bar(title_counts, x='Openings', y='Job Role', orientation='h',
# # # # # # #                      title='Top 20 Job Roles — Click a bar to drill down',
# # # # # # #                      color='Openings', color_continuous_scale='Viridis', text='Openings')
# # # # # # #         fig.update_layout(height=650, showlegend=False,
# # # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # # #                           title_font_size=14, clickmode='event+select')
# # # # # # #         fig.update_traces(textposition='outside')

# # # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # # #                                 on_select="rerun", key="role_drill_main")

# # # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # # # #             if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
# # # # # # #                 st.session_state.drill_type = "Job Role"
# # # # # # #                 st.session_state.drill_value = clicked
# # # # # # #                 st.rerun()

# # # # # # #     # TAB 3: COMPANY
# # # # # # #     with tabs[2]:
# # # # # # #         st.markdown('<div class="problem-header">🏢 Companies — Click a bar</div>', unsafe_allow_html=True)
# # # # # # #         comp_counts = df['company'].value_counts().head(20).reset_index()
# # # # # # #         comp_counts.columns = ['Company', 'Openings']

# # # # # # #         fig = px.bar(comp_counts, x='Openings', y='Company', orientation='h',
# # # # # # #                      title='Top 20 Companies — Click a bar to drill down',
# # # # # # #                      color='Openings', color_continuous_scale='Cividis', text='Openings')
# # # # # # #         fig.update_layout(height=650, showlegend=False,
# # # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # # #                           title_font_size=14, clickmode='event+select')
# # # # # # #         fig.update_traces(textposition='outside')

# # # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # # #                                 on_select="rerun", key="company_drill_main")

# # # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # # # #             if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
# # # # # # #                 st.session_state.drill_type = "Company"
# # # # # # #                 st.session_state.drill_value = clicked
# # # # # # #                 st.rerun()

# # # # # # #     # TAB 4: LOCATION
# # # # # # #     with tabs[3]:
# # # # # # #         st.markdown('<div class="problem-header">📍 Locations — Click a bar</div>', unsafe_allow_html=True)
# # # # # # #         loc_counts = df['location'].value_counts().head(20).reset_index()
# # # # # # #         loc_counts.columns = ['Location', 'Openings']

# # # # # # #         fig = px.bar(loc_counts, x='Location', y='Openings',
# # # # # # #                      title='Top 20 Locations — Click a bar to drill down',
# # # # # # #                      color='Openings', color_continuous_scale='Turbo', text='Openings')
# # # # # # #         fig.update_layout(height=500, showlegend=False,
# # # # # # #                           xaxis_tickangle=-40, title_font_size=14,
# # # # # # #                           clickmode='event+select')
# # # # # # #         fig.update_traces(textposition='outside')

# # # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # # #                                 on_select="rerun", key="loc_drill_main")

# # # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # # #             clicked = event["selection"]["points"][0].get("x")
# # # # # # #             if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
# # # # # # #                 st.session_state.drill_type = "Location"
# # # # # # #                 st.session_state.drill_value = clicked
# # # # # # #                 st.rerun()

# # # # # # #     # TAB 5: PORTAL
# # # # # # #     with tabs[4]:
# # # # # # #         st.markdown('<div class="problem-header">🌐 Portals — Click a bar or slice</div>', unsafe_allow_html=True)
# # # # # # #         portal_counts = df['platform'].value_counts().reset_index()
# # # # # # #         portal_counts.columns = ['Portal', 'Openings']

# # # # # # #         c1, c2 = st.columns(2)

# # # # # # #         with c1:
# # # # # # #             fig = px.bar(portal_counts, x='Portal', y='Openings',
# # # # # # #                          title='Jobs by Portal — Click a bar',
# # # # # # #                          color='Openings', color_continuous_scale='Plasma', text='Openings')
# # # # # # #             fig.update_layout(height=450, showlegend=False,
# # # # # # #                               xaxis_tickangle=-30, title_font_size=13,
# # # # # # #                               clickmode='event+select')
# # # # # # #             fig.update_traces(textposition='outside')

# # # # # # #             event = st.plotly_chart(fig, use_container_width=True,
# # # # # # #                                     on_select="rerun", key="portal_drill_bar_main")

# # # # # # #             if event and event.get("selection") and event["selection"].get("points"):
# # # # # # #                 clicked = event["selection"]["points"][0].get("x")
# # # # # # #                 if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
# # # # # # #                     st.session_state.drill_type = "Portal"
# # # # # # #                     st.session_state.drill_value = clicked
# # # # # # #                     st.rerun()

# # # # # # #         with c2:
# # # # # # #             fig = px.pie(portal_counts, values='Openings', names='Portal',
# # # # # # #                          title='Portal Distribution — Click a slice',
# # # # # # #                          hole=0.4,
# # # # # # #                          color_discrete_sequence=px.colors.qualitative.Set3)
# # # # # # #             fig.update_traces(textinfo='percent+label', textposition='outside',
# # # # # # #                               textfont_size=11, pull=[0.03] * len(portal_counts))
# # # # # # #             fig.update_layout(height=450, title_font_size=13)

# # # # # # #             event = st.plotly_chart(fig, use_container_width=True,
# # # # # # #                                     on_select="rerun", key="portal_drill_pie_main")

# # # # # # #             if event and event.get("selection") and event["selection"].get("points"):
# # # # # # #                 pt = event["selection"]["points"][0]
# # # # # # #                 clicked = pt.get("label") or pt.get("legendgroup")
# # # # # # #                 if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
# # # # # # #                     st.session_state.drill_type = "Portal"
# # # # # # #                     st.session_state.drill_value = clicked
# # # # # # #                     st.rerun()

# # # # # # # # ============================================================================
# # # # # # # # FOOTER
# # # # # # # # ============================================================================
# # # # # # # st.markdown("---")
# # # # # # # st.markdown(f"""<div style='text-align:center; color:#666; font-size:12px;'>
# # # # # # #     Job Market Analytics Dashboard | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
# # # # # # #     {len(df)} total jobs
# # # # # # # </div>""", unsafe_allow_html=True)









# # # # # # """
# # # # # # ================================================================================
# # # # # # JOB MARKET ANALYTICS — CLICKABLE KPI + REMOTE DRILL-DOWN
# # # # # # Click "Remote" → see all remote companies, areas, portals, skills
# # # # # # Tech Stack: Python | Pandas | NumPy | Plotly | Streamlit
# # # # # # Run: python -m streamlit run dashboard.py
# # # # # # ================================================================================
# # # # # # """

# # # # # # import streamlit as st
# # # # # # import pandas as pd
# # # # # # import numpy as np
# # # # # # import plotly.express as px
# # # # # # import plotly.graph_objects as go
# # # # # # from collections import Counter
# # # # # # from datetime import datetime
# # # # # # import warnings
# # # # # # import logging

# # # # # # warnings.filterwarnings('ignore')
# # # # # # logging.getLogger('streamlit').setLevel(logging.ERROR)

# # # # # # # ============================================================================
# # # # # # # PAGE CONFIG
# # # # # # # ============================================================================
# # # # # # st.set_page_config(
# # # # # #     page_title="Job Market Analytics",
# # # # # #     page_icon="🎯",
# # # # # #     layout="wide",
# # # # # #     initial_sidebar_state="expanded"
# # # # # # )

# # # # # # # CSS
# # # # # # st.markdown("""
# # # # # # <style>
    /* ========== FORCE DARK TEXT EVERYWHERE ========== */
    .stApp, .stApp * {
        color: #1a1a1a !important;
    }
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricLabel"] > div {
        color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stDataFrame"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
    }
# # # # # #     div[data-testid="stMarkdownContainer"] div,
# # # # # #     div[data-testid="stMarkdownContainer"] p,
# # # # # #     div[data-testid="stMarkdownContainer"] span,
# # # # # #     div[data-testid="stMarkdownContainer"] strong { color: #1a1a1a; }

# # # # # #     .main-header {
# # # # # #         font-size: 2.2rem; font-weight: bold;
# # # # # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # # # # #         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
# # # # # #         text-align: center; padding: 0.5rem 0;
# # # # # #     }
# # # # # #     .sub-header { text-align: center; color: #666; margin-bottom: 1rem; }
# # # # # #     .problem-header {
# # # # # #         background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
# # # # # #         padding: 0.7rem 1rem; border-radius: 8px;
# # # # # #         color: #FFFFFF !important; font-weight: bold;
# # # # # #         margin-bottom: 1rem; font-size: 1rem;
# # # # # #     }
# # # # # #     .insight-box {
# # # # # #         background: #f0f7ff; padding: 0.8rem;
# # # # # #         border-left: 4px solid #667eea; border-radius: 5px;
# # # # # #         margin: 0.6rem 0; font-size: 0.9rem; color: #1a1a1a !important;
# # # # # #     }
# # # # # #     .insight-box strong { color: #2c3e50 !important; font-weight: 700; }
# # # # # #     .drill-header {
# # # # # #         background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
# # # # # #         padding: 0.8rem 1rem; border-radius: 8px;
# # # # # #         color: #1a1a1a !important; font-weight: bold;
# # # # # #         margin: 1rem 0; font-size: 1.1rem;
# # # # # #         border: 2px solid #43e97b;
# # # # # #     }
# # # # # #     .stTabs [data-baseweb="tab-list"] { gap: 6px; flex-wrap: wrap; }
# # # # # #     .stTabs [data-baseweb="tab"] {
# # # # # #         background-color: #f0f2f6; border-radius: 6px;
# # # # # #         padding: 8px 12px; font-weight: 600; font-size: 0.78rem;
# # # # # #     }
# # # # # #     .stTabs [aria-selected="true"] {
# # # # # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # # # # #         color: #FFFFFF !important;
# # # # # #     }
# # # # # #     div[data-testid="stButton"] button {
# # # # # #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# # # # # #         color: white !important;
# # # # # #         border: none;
# # # # # #         padding: 1.5rem 1rem;
# # # # # #         border-radius: 12px;
# # # # # #         width: 100%;
# # # # # #         min-height: 120px;
# # # # # #         font-size: 1rem;
# # # # # #         font-weight: bold;
# # # # # #         box-shadow: 0 4px 12px rgba(0,0,0,0.1);
# # # # # #         transition: transform 0.2s;
# # # # # #     }
# # # # # #     div[data-testid="stButton"] button:hover {
# # # # # #         transform: translateY(-3px);
# # # # # #         box-shadow: 0 6px 16px rgba(0,0,0,0.2);
# # # # # #     }
# # # # # #     div[data-testid="stButton"] button p {
# # # # # #         color: white !important;
# # # # # #         font-size: 1rem;
# # # # # #         font-weight: bold;
# # # # # #     }
# # # # # # </style>
# # # # # # """, unsafe_allow_html=True)

# # # # # # # ============================================================================
# # # # # # # DATA LOADING
# # # # # # # ============================================================================

# # # # # # @st.cache_data
# # # # # # def load_data():
# # # # # #     df = pd.read_csv("job_data_clean.csv")
# # # # # #     df['posted_date'] = pd.to_datetime(df['posted_date'], errors='coerce')
# # # # # #     return df

# # # # # # def extract_skills(text):
# # # # # #     if pd.isna(text):
# # # # # #         return []
# # # # # #     text = str(text).lower()
# # # # # #     skill_list = [
# # # # # #         'python', 'java', 'sql', 'javascript', 'typescript', 'react', 'angular',
# # # # # #         'node.js', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
# # # # # #         'jenkins', 'spark', 'kafka', 'airflow', 'snowflake', 'tableau', 'power bi',
# # # # # #         'machine learning', 'deep learning', 'nlp', 'llm', 'genai', 'rag',
# # # # # #         'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
# # # # # #         'excel', 'git', 'linux', 'agile', 'scrum', 'jira'
# # # # # #     ]
# # # # # #     return list(set([s for s in skill_list if s in text]))

# # # # # # try:
# # # # # #     df = load_data()
# # # # # #     df['skills'] = df['description'].apply(extract_skills)
# # # # # #     df['skill_count'] = df['skills'].apply(len)
# # # # # # except Exception as e:
# # # # # #     st.error(f"❌ Error loading 'job_data_clean.csv': {e}")
# # # # # #     st.stop()

# # # # # # # ============================================================================
# # # # # # # HEADER
# # # # # # # ============================================================================
# # # # # # st.markdown('<h1 class="main-header">🎯 Job Market Analytics</h1>', unsafe_allow_html=True)
# # # # # # st.markdown('<p class="sub-header">Click any KPI card → see detailed breakdown</p>', unsafe_allow_html=True)

# # # # # # # ============================================================================
# # # # # # # SESSION STATE
# # # # # # # ============================================================================
# # # # # # for key in ['view', 'drill_type', 'drill_value']:
# # # # # #     if key not in st.session_state:
# # # # # #         st.session_state[key] = None

# # # # # # # Sidebar
# # # # # # st.sidebar.markdown("## 🔍 Navigation")
# # # # # # if st.sidebar.button("🏠 Home (Clear View)"):
# # # # # #     st.session_state.view = None
# # # # # #     st.session_state.drill_type = None
# # # # # #     st.session_state.drill_value = None
# # # # # #     st.rerun()

# # # # # # if st.session_state.view:
# # # # # #     st.sidebar.success(f"**Viewing:** {st.session_state.view}")

# # # # # # if st.session_state.drill_type:
# # # # # #     st.sidebar.info(f"**Drill:** {st.session_state.drill_type} = {st.session_state.drill_value}")
# # # # # #     if st.sidebar.button("❌ Clear Drill"):
# # # # # #         st.session_state.drill_type = None
# # # # # #         st.session_state.drill_value = None
# # # # # #         st.rerun()

# # # # # # st.sidebar.markdown("---")
# # # # # # st.sidebar.markdown(f"**📊 Total Jobs:** {len(df)}")
# # # # # # st.sidebar.markdown(f"**🏠 Remote Jobs:** {(df['is_remote']=='Yes').sum()}")

# # # # # # # ============================================================================
# # # # # # # KPI CARDS — CLICKABLE
# # # # # # # ============================================================================
# # # # # # st.markdown("## 📈 Overview — Click to Explore")

# # # # # # k1, k2, k3, k4, k5, k6 = st.columns(6)

# # # # # # with k1:
# # # # # #     if st.button(f"📊\n\n**Total Jobs**\n\n{len(df)}\n\n_in dataset_",
# # # # # #                  key="kpi_total", use_container_width=True):
# # # # # #         st.session_state.view = "Total Jobs"
# # # # # #         st.session_state.drill_type = None
# # # # # #         st.rerun()

# # # # # # with k2:
# # # # # #     if st.button(f"🏢\n\n**Companies**\n\n{df['company'].nunique()}\n\n_hiring_",
# # # # # #                  key="kpi_company", use_container_width=True):
# # # # # #         st.session_state.view = "Companies"
# # # # # #         st.session_state.drill_type = None
# # # # # #         st.rerun()

# # # # # # with k3:
# # # # # #     if st.button(f"💼\n\n**Job Roles**\n\n{df['title'].nunique()}\n\n_unique_",
# # # # # #                  key="kpi_title", use_container_width=True):
# # # # # #         st.session_state.view = "Job Roles"
# # # # # #         st.session_state.drill_type = None
# # # # # #         st.rerun()

# # # # # # with k4:
# # # # # #     if st.button(f"🌐\n\n**Portals**\n\n{df['platform'].nunique()}\n\n_sources_",
# # # # # #                  key="kpi_portal", use_container_width=True):
# # # # # #         st.session_state.view = "Portals"
# # # # # #         st.session_state.drill_type = None
# # # # # #         st.rerun()

# # # # # # with k5:
# # # # # #     if st.button(f"📍\n\n**Locations**\n\n{df['location'].nunique()}\n\n_cities_",
# # # # # #                  key="kpi_location", use_container_width=True):
# # # # # #         st.session_state.view = "Locations"
# # # # # #         st.session_state.drill_type = None
# # # # # #         st.rerun()

# # # # # # with k6:
# # # # # #     remote_count = (df['is_remote'] == 'Yes').sum()
# # # # # #     if st.button(f"🏠\n\n**Remote Jobs**\n\n{remote_count}\n\n_of {len(df)}_",
# # # # # #                  key="kpi_remote", use_container_width=True):
# # # # # #         st.session_state.view = "Remote Jobs"
# # # # # #         st.session_state.drill_type = None
# # # # # #         st.rerun()

# # # # # # st.markdown("---")

# # # # # # # ============================================================================
# # # # # # # VIEW: REMOTE JOBS — DETAILED BREAKDOWN
# # # # # # # ============================================================================
# # # # # # if st.session_state.view == "Remote Jobs":
# # # # # #     st.markdown('<div class="drill-header">🏠 Remote Jobs — Complete Breakdown</div>', unsafe_allow_html=True)

# # # # # #     # Get remote jobs
# # # # # #     remote_df = df[df['is_remote'] == 'Yes']

# # # # # #     if len(remote_df) == 0:
# # # # # #         st.warning("No remote jobs found in the dataset.")
# # # # # #     else:
# # # # # #         # ---- Top KPIs ----
# # # # # #         d1, d2, d3, d4, d5 = st.columns(5)
# # # # # #         with d1:
# # # # # #             st.metric("🏠 Total Remote Jobs", len(remote_df))
# # # # # #         with d2:
# # # # # #             st.metric("🏢 Companies", remote_df['company'].nunique())
# # # # # #         with d3:
# # # # # #             st.metric("📍 Locations", remote_df['location'].nunique())
# # # # # #         with d4:
# # # # # #             st.metric("💼 Job Roles", remote_df['title'].nunique())
# # # # # #         with d5:
# # # # # #             st.metric("🌐 Portals", remote_df['platform'].nunique())

# # # # # #         st.markdown("---")

# # # # # #         # ================================================================
# # # # # #         # SECTION 1: Remote Companies
# # # # # #         # ================================================================
# # # # # #         st.markdown("### 🏢 Companies Hiring Remote")

# # # # # #         c1, c2 = st.columns([3, 2])

# # # # # #         with c1:
# # # # # #             remote_companies = remote_df['company'].value_counts().reset_index()
# # # # # #             remote_companies.columns = ['Company', 'Remote Jobs']

# # # # # #             fig = px.bar(
# # # # # #                 remote_companies, x='Remote Jobs', y='Company', orientation='h',
# # # # # #                 title=f'All {len(remote_companies)} Companies Hiring Remote — Click a bar',
# # # # # #                 color='Remote Jobs', color_continuous_scale='Greens', text='Remote Jobs'
# # # # # #             )
# # # # # #             fig.update_layout(
# # # # # #                 height=max(400, len(remote_companies)*35),
# # # # # #                 showlegend=False,
# # # # # #                 yaxis=dict(autorange="reversed"),
# # # # # #                 title_font_size=14,
# # # # # #                 clickmode='event+select'
# # # # # #             )
# # # # # #             fig.update_traces(textposition='outside')

# # # # # #             event = st.plotly_chart(fig, use_container_width=True,
# # # # # #                                     on_select="rerun", key="remote_company_drill")

# # # # # #             if event and event.get("selection") and event["selection"].get("points"):
# # # # # #                 clicked = event["selection"]["points"][0].get("y")
# # # # # #                 if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
# # # # # #                     st.session_state.drill_type = "Company"
# # # # # #                     st.session_state.drill_value = clicked
# # # # # #                     st.rerun()

# # # # # #         with c2:
# # # # # #             st.markdown("#### 📋 Company List (Remote)")
# # # # # #             st.dataframe(remote_companies, use_container_width=True,
# # # # # #                          height=400, hide_index=True)

# # # # # #         # ================================================================
# # # # # #         # SECTION 2: Remote Locations / Areas
# # # # # #         # ================================================================
# # # # # #         st.markdown("### 📍 Remote Jobs by Location / Area")

# # # # # #         c3, c4 = st.columns([3, 2])

# # # # # #         with c3:
# # # # # #             remote_locs = remote_df['location'].value_counts().reset_index()
# # # # # #             remote_locs.columns = ['Location', 'Remote Jobs']

# # # # # #             fig = px.bar(
# # # # # #                 remote_locs, x='Remote Jobs', y='Location', orientation='h',
# # # # # #                 title=f'Remote Jobs by Location — Click a bar',
# # # # # #                 color='Remote Jobs', color_continuous_scale='Teal', text='Remote Jobs'
# # # # # #             )
# # # # # #             fig.update_layout(
# # # # # #                 height=max(400, len(remote_locs)*35),
# # # # # #                 showlegend=False,
# # # # # #                 yaxis=dict(autorange="reversed"),
# # # # # #                 title_font_size=14,
# # # # # #                 clickmode='event+select'
# # # # # #             )
# # # # # #             fig.update_traces(textposition='outside')

# # # # # #             event = st.plotly_chart(fig, use_container_width=True,
# # # # # #                                     on_select="rerun", key="remote_loc_drill")

# # # # # #             if event and event.get("selection") and event["selection"].get("points"):
# # # # # #                 clicked = event["selection"]["points"][0].get("y")
# # # # # #                 if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
# # # # # #                     st.session_state.drill_type = "Location"
# # # # # #                     st.session_state.drill_value = clicked
# # # # # #                     st.rerun()

# # # # # #         with c4:
# # # # # #             st.markdown("#### 📋 Location List (Remote)")
# # # # # #             st.dataframe(remote_locs, use_container_width=True,
# # # # # #                          height=400, hide_index=True)

# # # # # #         # ================================================================
# # # # # #         # SECTION 3: Remote Portals
# # # # # #         # ================================================================
# # # # # #         st.markdown("### 🌐 Which Portals Post Remote Jobs?")

# # # # # #         c5, c6 = st.columns([2, 2])

# # # # # #         with c5:
# # # # # #             remote_portals = remote_df['platform'].value_counts().reset_index()
# # # # # #             remote_portals.columns = ['Portal', 'Remote Jobs']

# # # # # #             fig = px.bar(
# # # # # #                 remote_portals, x='Portal', y='Remote Jobs',
# # # # # #                 title='Remote Jobs by Portal — Click a bar',
# # # # # #                 color='Remote Jobs', color_continuous_scale='Blues', text='Remote Jobs'
# # # # # #             )
# # # # # #             fig.update_layout(height=400, showlegend=False,
# # # # # #                               xaxis_tickangle=-30, title_font_size=13,
# # # # # #                               clickmode='event+select')
# # # # # #             fig.update_traces(textposition='outside')

# # # # # #             event = st.plotly_chart(fig, use_container_width=True,
# # # # # #                                     on_select="rerun", key="remote_portal_drill")

# # # # # #             if event and event.get("selection") and event["selection"].get("points"):
# # # # # #                 clicked = event["selection"]["points"][0].get("x")
# # # # # #                 if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
# # # # # #                     st.session_state.drill_type = "Portal"
# # # # # #                     st.session_state.drill_value = clicked
# # # # # #                     st.rerun()

# # # # # #         with c6:
# # # # # #             fig = px.pie(
# # # # # #                 remote_portals, values='Remote Jobs', names='Portal',
# # # # # #                 title='Remote Jobs — Portal Share',
# # # # # #                 hole=0.4,
# # # # # #                 color_discrete_sequence=px.colors.qualitative.Set3
# # # # # #             )
# # # # # #             fig.update_traces(textinfo='percent+label', textposition='outside',
# # # # # #                               textfont_size=11, pull=[0.03] * len(remote_portals))
# # # # # #             fig.update_layout(height=400, title_font_size=13)
# # # # # #             st.plotly_chart(fig, use_container_width=True, key="remote_portal_pie")

# # # # # #         # ================================================================
# # # # # #         # SECTION 4: Remote Job Roles
# # # # # #         # ================================================================
# # # # # #         st.markdown("### 💼 What Job Roles Are Remote?")

# # # # # #         remote_roles = remote_df['title'].value_counts().reset_index()
# # # # # #         remote_roles.columns = ['Job Role', 'Remote Jobs']

# # # # # #         fig = px.bar(
# # # # # #             remote_roles, x='Remote Jobs', y='Job Role', orientation='h',
# # # # # #             title=f'Remote Job Roles — Click a bar',
# # # # # #             color='Remote Jobs', color_continuous_scale='Purples', text='Remote Jobs'
# # # # # #         )
# # # # # #         fig.update_layout(
# # # # # #             height=max(400, len(remote_roles)*35),
# # # # # #             showlegend=False,
# # # # # #             yaxis=dict(autorange="reversed"),
# # # # # #             title_font_size=14,
# # # # # #             clickmode='event+select'
# # # # # #         )
# # # # # #         fig.update_traces(textposition='outside')

# # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # #                                 on_select="rerun", key="remote_role_drill")

# # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # # #             if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
# # # # # #                 st.session_state.drill_type = "Job Role"
# # # # # #                 st.session_state.drill_value = clicked
# # # # # #                 st.rerun()

# # # # # #         # ================================================================
# # # # # #         # SECTION 5: Skills Required for Remote Jobs
# # # # # #         # ================================================================
# # # # # #         st.markdown("### 🛠️ Top Skills Required for Remote Jobs")

# # # # # #         all_remote_skills = [s for skills in remote_df['skills'] for s in skills]
# # # # # #         remote_skill_counts = Counter(all_remote_skills).most_common(15)

# # # # # #         if remote_skill_counts:
# # # # # #             rs_df = pd.DataFrame(remote_skill_counts, columns=['Skill', 'Jobs'])
# # # # # #             rs_df['% of Remote'] = (rs_df['Jobs'] / len(remote_df) * 100).round(1)

# # # # # #             fig = px.bar(
# # # # # #                 rs_df, x='Jobs', y='Skill', orientation='h',
# # # # # #                 title='Top Skills for Remote Jobs',
# # # # # #                 color='Jobs', color_continuous_scale='Greens', text='Jobs'
# # # # # #             )
# # # # # #             fig.update_layout(height=500, showlegend=False,
# # # # # #                               yaxis=dict(autorange="reversed"),
# # # # # #                               title_font_size=14)
# # # # # #             fig.update_traces(textposition='outside')
# # # # # #             st.plotly_chart(fig, use_container_width=True, key="remote_skills")

# # # # # #         # ================================================================
# # # # # #         # SECTION 6: Full Remote Job List
# # # # # #         # ================================================================
# # # # # #         st.markdown("### 📋 All Remote Job Openings")

# # # # # #         show_cols = ['title', 'company', 'location', 'platform',
# # # # # #                      'employment_type', 'posted_date']
# # # # # #         display_remote = remote_df[show_cols].copy()
# # # # # #         display_remote.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # # # #                                   'Type', 'Posted']

# # # # # #         st.dataframe(display_remote, use_container_width=True, height=500)

# # # # # #         csv = remote_df.to_csv(index=False)
# # # # # #         st.download_button(
# # # # # #             label="📥 Download All Remote Jobs (CSV)",
# # # # # #             data=csv,
# # # # # #             file_name=f"remote_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # #             mime="text/csv",
# # # # # #             key="dl_remote"
# # # # # #         )

# # # # # #         # ---- Insight ----
# # # # # #         top_comp = remote_df['company'].value_counts().index[0]
# # # # # #         top_loc = remote_df['location'].value_counts().index[0]
# # # # # #         top_portal = remote_df['platform'].value_counts().index[0]

# # # # # #         st.markdown(f"""<div class="insight-box">
# # # # # #             <strong>📊 Remote Job Summary:</strong><br>
# # # # # #             🏢 <strong>Top Remote Employer:</strong> {top_comp}<br>
# # # # # #             📍 <strong>Top Remote Location:</strong> {top_loc}<br>
# # # # # #             🌐 <strong>Top Portal for Remote:</strong> {top_portal}<br>
# # # # # #             🛠️ <strong>Top Skill for Remote:</strong> {remote_skill_counts[0][0] if remote_skill_counts else 'N/A'}<br>
# # # # # #             📊 <strong>Remote % of Total:</strong> {len(remote_df)/len(df)*100:.1f}%
# # # # # #         </div>""", unsafe_allow_html=True)

# # # # # # # ============================================================================
# # # # # # # OTHER VIEWS (Companies, Locations, etc.)
# # # # # # # ============================================================================
# # # # # # elif st.session_state.view == "Companies":
# # # # # #     st.markdown('<div class="drill-header">🏢 All Companies Hiring</div>', unsafe_allow_html=True)
# # # # # #     comp_df = df['company'].value_counts().reset_index()
# # # # # #     comp_df.columns = ['Company', 'Openings']
# # # # # #     comp_df['Share %'] = (comp_df['Openings'] / len(df) * 100).round(2)

# # # # # #     c1, c2 = st.columns([3, 2])
# # # # # #     with c1:
# # # # # #         fig = px.bar(comp_df.head(30), x='Openings', y='Company', orientation='h',
# # # # # #                      title=f'All {len(comp_df)} Companies (Top 30) — Click a bar',
# # # # # #                      color='Openings', color_continuous_scale='Viridis', text='Openings')
# # # # # #         fig.update_layout(height=800, showlegend=False,
# # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # #                           title_font_size=14, clickmode='event+select')
# # # # # #         fig.update_traces(textposition='outside')
# # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # #                                 on_select="rerun", key="comp_view_drill")
# # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # # #             if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
# # # # # #                 st.session_state.drill_type = "Company"
# # # # # #                 st.session_state.drill_value = clicked
# # # # # #                 st.rerun()

# # # # # #     with c2:
# # # # # #         st.markdown("### 📋 Complete List")
# # # # # #         st.dataframe(comp_df, use_container_width=True, height=750, hide_index=True)

# # # # # #     csv = comp_df.to_csv(index=False)
# # # # # #     st.download_button("📥 Download CSV", csv,
# # # # # #                        file_name=f"companies_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # #                        mime="text/csv", key="dl_comp_view")

# # # # # # elif st.session_state.view == "Locations":
# # # # # #     st.markdown('<div class="drill-header">📍 All Locations</div>', unsafe_allow_html=True)
# # # # # #     loc_df = df['location'].value_counts().reset_index()
# # # # # #     loc_df.columns = ['Location', 'Openings']
# # # # # #     loc_df['Share %'] = (loc_df['Openings'] / len(df) * 100).round(2)

# # # # # #     c1, c2 = st.columns([3, 2])
# # # # # #     with c1:
# # # # # #         fig = px.bar(loc_df, x='Openings', y='Location', orientation='h',
# # # # # #                      title=f'All {len(loc_df)} Locations — Click a bar',
# # # # # #                      color='Openings', color_continuous_scale='Magma', text='Openings')
# # # # # #         fig.update_layout(height=max(600, len(loc_df)*22), showlegend=False,
# # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # #                           title_font_size=14, clickmode='event+select')
# # # # # #         fig.update_traces(textposition='outside')
# # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # #                                 on_select="rerun", key="loc_view_drill")
# # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # # #             if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
# # # # # #                 st.session_state.drill_type = "Location"
# # # # # #                 st.session_state.drill_value = clicked
# # # # # #                 st.rerun()

# # # # # #     with c2:
# # # # # #         st.markdown("### 📋 Complete List")
# # # # # #         st.dataframe(loc_df, use_container_width=True, height=750, hide_index=True)

# # # # # #     csv = loc_df.to_csv(index=False)
# # # # # #     st.download_button("📥 Download CSV", csv,
# # # # # #                        file_name=f"locations_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # #                        mime="text/csv", key="dl_loc_view")

# # # # # # elif st.session_state.view == "Job Roles":
# # # # # #     st.markdown('<div class="drill-header">💼 All Job Roles</div>', unsafe_allow_html=True)
# # # # # #     role_df = df['title'].value_counts().reset_index()
# # # # # #     role_df.columns = ['Job Role', 'Openings']
# # # # # #     role_df['Share %'] = (role_df['Openings'] / len(df) * 100).round(2)

# # # # # #     c1, c2 = st.columns([3, 2])
# # # # # #     with c1:
# # # # # #         fig = px.bar(role_df.head(40), x='Openings', y='Job Role', orientation='h',
# # # # # #                      title=f'All {len(role_df)} Job Roles (Top 40) — Click a bar',
# # # # # #                      color='Openings', color_continuous_scale='Plasma', text='Openings')
# # # # # #         fig.update_layout(height=1000, showlegend=False,
# # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # #                           title_font_size=14, clickmode='event+select')
# # # # # #         fig.update_traces(textposition='outside')
# # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # #                                 on_select="rerun", key="role_view_drill")
# # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # # #             if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
# # # # # #                 st.session_state.drill_type = "Job Role"
# # # # # #                 st.session_state.drill_value = clicked
# # # # # #                 st.rerun()

# # # # # #     with c2:
# # # # # #         st.markdown("### 📋 Complete List")
# # # # # #         st.dataframe(role_df, use_container_width=True, height=950, hide_index=True)

# # # # # #     csv = role_df.to_csv(index=False)
# # # # # #     st.download_button("📥 Download CSV", csv,
# # # # # #                        file_name=f"roles_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # #                        mime="text/csv", key="dl_role_view")

# # # # # # elif st.session_state.view == "Portals":
# # # # # #     st.markdown('<div class="drill-header">🌐 All Portals</div>', unsafe_allow_html=True)
# # # # # #     portal_df = df['platform'].value_counts().reset_index()
# # # # # #     portal_df.columns = ['Portal', 'Openings']
# # # # # #     portal_df['Share %'] = (portal_df['Openings'] / len(df) * 100).round(2)

# # # # # #     c1, c2 = st.columns(2)
# # # # # #     with c1:
# # # # # #         fig = px.bar(portal_df, x='Portal', y='Openings',
# # # # # #                      title='Portals — Click a bar',
# # # # # #                      color='Openings', color_continuous_scale='Turbo', text='Openings')
# # # # # #         fig.update_layout(height=450, showlegend=False,
# # # # # #                           xaxis_tickangle=-30, title_font_size=13,
# # # # # #                           clickmode='event+select')
# # # # # #         fig.update_traces(textposition='outside')
# # # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # # #                                 on_select="rerun", key="portal_view_drill")
# # # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # # #             clicked = event["selection"]["points"][0].get("x")
# # # # # #             if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
# # # # # #                 st.session_state.drill_type = "Portal"
# # # # # #                 st.session_state.drill_value = clicked
# # # # # #                 st.rerun()

# # # # # #     with c2:
# # # # # #         st.markdown("### 📋 Complete List")
# # # # # #         st.dataframe(portal_df, use_container_width=True, hide_index=True)

# # # # # #     csv = portal_df.to_csv(index=False)
# # # # # #     st.download_button("📥 Download CSV", csv,
# # # # # #                        file_name=f"portals_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # #                        mime="text/csv", key="dl_portal_view")

# # # # # # elif st.session_state.view == "Total Jobs":
# # # # # #     st.markdown('<div class="drill-header">📊 All Jobs in Dataset</div>', unsafe_allow_html=True)
# # # # # #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # # # # #                  'employment_type', 'posted_date']
# # # # # #     display_df = df[show_cols].copy()
# # # # # #     display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # # # #                           'Remote', 'Type', 'Posted']
# # # # # #     st.dataframe(display_df, use_container_width=True, height=600)
# # # # # #     csv = df.to_csv(index=False)
# # # # # #     st.download_button("📥 Download All Jobs (CSV)", csv,
# # # # # #                        file_name=f"all_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # # #                        mime="text/csv", key="dl_total_view")

# # # # # # # ============================================================================
# # # # # # # DRILL-DOWN PANEL
# # # # # # # ============================================================================
# # # # # # if st.session_state.drill_type and st.session_state.drill_value:
# # # # # #     st.markdown("---")
# # # # # #     drill_val = st.session_state.drill_value
# # # # # #     drill_type = st.session_state.drill_type

# # # # # #     st.markdown(f'<div class="drill-header">🎯 Drill-Down: {drill_type} = "{drill_val}"</div>', unsafe_allow_html=True)

# # # # # #     if drill_type == "Skill":
# # # # # #         drill_df = df[df['skills'].apply(lambda x: drill_val in x)]
# # # # # #     elif drill_type == "Job Role":
# # # # # #         drill_df = df[df['title'] == drill_val]
# # # # # #     elif drill_type == "Company":
# # # # # #         drill_df = df[df['company'] == drill_val]
# # # # # #     elif drill_type == "Location":
# # # # # #         drill_df = df[df['location'] == drill_val]
# # # # # #     elif drill_type == "Portal":
# # # # # #         drill_df = df[df['platform'] == drill_val]
# # # # # #     else:
# # # # # #         drill_df = df.copy()

# # # # # #     d1, d2, d3, d4 = st.columns(4)
# # # # # #     with d1: st.metric("🎯 Total Openings", len(drill_df))
# # # # # #     with d2: st.metric("🏢 Companies", drill_df['company'].nunique())
# # # # # #     with d3: st.metric("📍 Locations", drill_df['location'].nunique())
# # # # # #     with d4:
# # # # # #         rp = (drill_df['is_remote'] == 'Yes').sum() / len(drill_df) * 100 if len(drill_df) > 0 else 0
# # # # # #         st.metric("🏠 Remote %", f"{rp:.1f}%")

# # # # # #     g1, g2 = st.columns(2)
# # # # # #     with g1:
# # # # # #         pc = drill_df['platform'].value_counts().reset_index()
# # # # # #         pc.columns = ['Portal', 'Openings']
# # # # # #         fig = px.bar(pc, x='Openings', y='Portal', orientation='h',
# # # # # #                      title='By Portal', color='Openings',
# # # # # #                      color_continuous_scale='Blues', text='Openings')
# # # # # #         fig.update_layout(height=350, showlegend=False,
# # # # # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # # # # #         fig.update_traces(textposition='outside')
# # # # # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_p_{drill_val}")

# # # # # #     with g2:
# # # # # #         cc = drill_df['company'].value_counts().head(10).reset_index()
# # # # # #         cc.columns = ['Company', 'Openings']
# # # # # #         fig = px.bar(cc, x='Openings', y='Company', orientation='h',
# # # # # #                      title='By Company', color='Openings',
# # # # # #                      color_continuous_scale='Viridis', text='Openings')
# # # # # #         fig.update_layout(height=350, showlegend=False,
# # # # # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # # # # #         fig.update_traces(textposition='outside')
# # # # # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_c_{drill_val}")

# # # # # #     st.markdown("### 📋 All Job Openings")
# # # # # #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # # # # #                  'employment_type', 'posted_date']
# # # # # #     ddf = drill_df[show_cols].copy()
# # # # # #     ddf.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # # # #                    'Remote', 'Type', 'Posted']
# # # # # #     st.dataframe(ddf, use_container_width=True, height=400)

# # # # # #     csv = drill_df.to_csv(index=False)
# # # # # #     st.download_button("📥 Download (CSV)", csv,
# # # # # #                        file_name=f"drill_{drill_type}_{drill_val}.csv",
# # # # # #                        mime="text/csv", key=f"dl_dd_{drill_val}")

# # # # # # # ============================================================================
# # # # # # # MAIN TABS (when no view is active)
# # # # # # # ============================================================================
# # # # # # if st.session_state.view is None:
# # # # # #     st.markdown("---")
# # # # # #     st.markdown("## 🔎 Explore Charts — Click to drill down")

# # # # # #     tabs = st.tabs(["🛠️ By Skill", "💼 By Role", "🏢 By Company",
# # # # # #                     "📍 By Location", "🌐 By Portal"])

# # # # # #     with tabs[0]:
# # # # # #         all_sk = [s for skills in df['skills'] for s in skills]
# # # # # #         sc = Counter(all_sk).most_common(20)
# # # # # #         if sc:
# # # # # #             sdf = pd.DataFrame(sc, columns=['Skill', 'Jobs'])
# # # # # #             fig = px.bar(sdf, x='Jobs', y='Skill', orientation='h',
# # # # # #                          title='Top 20 Skills', color='Jobs',
# # # # # #                          color_continuous_scale='RdYlGn', text='Jobs')
# # # # # #             fig.update_layout(height=650, showlegend=False,
# # # # # #                               yaxis=dict(autorange="reversed"),
# # # # # #                               clickmode='event+select')
# # # # # #             fig.update_traces(textposition='outside')
# # # # # #             ev = st.plotly_chart(fig, use_container_width=True,
# # # # # #                                  on_select="rerun", key="main_skill")
# # # # # #             if ev and ev.get("selection") and ev["selection"].get("points"):
# # # # # #                 c = ev["selection"]["points"][0].get("y")
# # # # # #                 if c and (st.session_state.drill_type != "Skill" or st.session_state.drill_value != c):
# # # # # #                     st.session_state.drill_type = "Skill"
# # # # # #                     st.session_state.drill_value = c
# # # # # #                     st.rerun()

# # # # # #     with tabs[1]:
# # # # # #         tc = df['title'].value_counts().head(20).reset_index()
# # # # # #         tc.columns = ['Job Role', 'Openings']
# # # # # #         fig = px.bar(tc, x='Openings', y='Job Role', orientation='h',
# # # # # #                      title='Top 20 Roles', color='Openings',
# # # # # #                      color_continuous_scale='Viridis', text='Openings')
# # # # # #         fig.update_layout(height=650, showlegend=False,
# # # # # #                           yaxis=dict(autorange="reversed"),
# # # # # #                           clickmode='event+select')
# # # # # #         fig.update_traces(textposition='outside')
# # # # # #         ev = st.plotly_chart(fig, use_container_width=True,
# # # # # #                              on_select="rerun", key="main_role")
# # # # # #         if ev and ev.get("selection") and ev["selection"].get("points"):
# # # # # #             c = ev["selection"]["points"][0].get("y")
# # # # # #             if c and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != c):
# # # # # #                 st.session_state.drill_type = "Job Role"
# # # # # #                 st.session_state.drill_value = c
# # # # # #                 st.rerun()

# # # # # #     with tabs[2]:
# # # # # #         cc = df['company'].value_counts().head(20).reset_index()
# # # # # #         cc.columns = ['Company', 'Openings']
# # # # # #         fig = px.bar(cc, x='Openings', y='Company', orientation='h',
# # # # # #                      title='Top 20 Companies', color='




# # # # # """
# # # # # ================================================================================
# # # # # JOB MARKET ANALYTICS — CLICKABLE KPI + REMOTE DRILL-DOWN
# # # # # Click "Remote" → see all remote companies, areas, portals, skills
# # # # # Tech Stack: Python | Pandas | NumPy | Plotly | Streamlit
# # # # # Run: python -m streamlit run dashboard.py
# # # # # ================================================================================
# # # # # """

# # # # # import streamlit as st
# # # # # import pandas as pd
# # # # # import numpy as np
# # # # # import plotly.express as px
# # # # # import plotly.graph_objects as go
# # # # # from collections import Counter
# # # # # from datetime import datetime
# # # # # import warnings
# # # # # import logging

# # # # # warnings.filterwarnings('ignore')
# # # # # logging.getLogger('streamlit').setLevel(logging.ERROR)

# # # # # # ============================================================================
# # # # # # PAGE CONFIG
# # # # # # ============================================================================
# # # # # st.set_page_config(
# # # # #     page_title="Job Market Analytics",
# # # # #     page_icon="🎯",
# # # # #     layout="wide",
# # # # #     initial_sidebar_state="expanded"
# # # # # )

# # # # # # CSS
# # # # # st.markdown("""
# # # # # <style>
    /* ========== FORCE DARK TEXT EVERYWHERE ========== */
    .stApp, .stApp * {
        color: #1a1a1a !important;
    }
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricLabel"] > div {
        color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stDataFrame"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
    }
# # # # #     div[data-testid="stMarkdownContainer"] div,
# # # # #     div[data-testid="stMarkdownContainer"] p,
# # # # #     div[data-testid="stMarkdownContainer"] span,
# # # # #     div[data-testid="stMarkdownContainer"] strong { color: #1a1a1a; }

# # # # #     .main-header {
# # # # #         font-size: 2.2rem; font-weight: bold;
# # # # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # # # #         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
# # # # #         text-align: center; padding: 0.5rem 0;
# # # # #     }
# # # # #     .sub-header { text-align: center; color: #666; margin-bottom: 1rem; }
# # # # #     .problem-header {
# # # # #         background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
# # # # #         padding: 0.7rem 1rem; border-radius: 8px;
# # # # #         color: #FFFFFF !important; font-weight: bold;
# # # # #         margin-bottom: 1rem; font-size: 1rem;
# # # # #     }
# # # # #     .insight-box {
# # # # #         background: #f0f7ff; padding: 0.8rem;
# # # # #         border-left: 4px solid #667eea; border-radius: 5px;
# # # # #         margin: 0.6rem 0; font-size: 0.9rem; color: #1a1a1a !important;
# # # # #     }
# # # # #     .insight-box strong { color: #2c3e50 !important; font-weight: 700; }
# # # # #     .drill-header {
# # # # #         background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
# # # # #         padding: 0.8rem 1rem; border-radius: 8px;
# # # # #         color: #1a1a1a !important; font-weight: bold;
# # # # #         margin: 1rem 0; font-size: 1.1rem;
# # # # #         border: 2px solid #43e97b;
# # # # #     }
# # # # #     .stTabs [data-baseweb="tab-list"] { gap: 6px; flex-wrap: wrap; }
# # # # #     .stTabs [data-baseweb="tab"] {
# # # # #         background-color: #f0f2f6; border-radius: 6px;
# # # # #         padding: 8px 12px; font-weight: 600; font-size: 0.78rem;
# # # # #     }
# # # # #     .stTabs [aria-selected="true"] {
# # # # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # # # #         color: #FFFFFF !important;
# # # # #     }
# # # # #     div[data-testid="stButton"] button {
# # # # #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# # # # #         color: white !important;
# # # # #         border: none;
# # # # #         padding: 1.5rem 1rem;
# # # # #         border-radius: 12px;
# # # # #         width: 100%;
# # # # #         min-height: 120px;
# # # # #         font-size: 1rem;
# # # # #         font-weight: bold;
# # # # #         box-shadow: 0 4px 12px rgba(0,0,0,0.1);
# # # # #         transition: transform 0.2s;
# # # # #     }
# # # # #     div[data-testid="stButton"] button:hover {
# # # # #         transform: translateY(-3px);
# # # # #         box-shadow: 0 6px 16px rgba(0,0,0,0.2);
# # # # #     }
# # # # #     div[data-testid="stButton"] button p {
# # # # #         color: white !important;
# # # # #         font-size: 1rem;
# # # # #         font-weight: bold;
# # # # #     }
# # # # # </style>
# # # # # """, unsafe_allow_html=True)

# # # # # # ============================================================================
# # # # # # DATA LOADING
# # # # # # ============================================================================

# # # # # @st.cache_data
# # # # # def load_data():
# # # # #     df = pd.read_csv("job_data_clean.csv")
# # # # #     df['posted_date'] = pd.to_datetime(df['posted_date'], errors='coerce')
# # # # #     return df

# # # # # def extract_skills(text):
# # # # #     if pd.isna(text):
# # # # #         return []
# # # # #     text = str(text).lower()
# # # # #     skill_list = [
# # # # #         'python', 'java', 'sql', 'javascript', 'typescript', 'react', 'angular',
# # # # #         'node.js', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
# # # # #         'jenkins', 'spark', 'kafka', 'airflow', 'snowflake', 'tableau', 'power bi',
# # # # #         'machine learning', 'deep learning', 'nlp', 'llm', 'genai', 'rag',
# # # # #         'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
# # # # #         'excel', 'git', 'linux', 'agile', 'scrum', 'jira'
# # # # #     ]
# # # # #     return list(set([s for s in skill_list if s in text]))

# # # # # try:
# # # # #     df = load_data()
# # # # #     df['skills'] = df['description'].apply(extract_skills)
# # # # #     df['skill_count'] = df['skills'].apply(len)
# # # # # except Exception as e:
# # # # #     st.error(f"❌ Error loading 'job_data_clean.csv': {e}")
# # # # #     st.stop()

# # # # # # ============================================================================
# # # # # # HEADER
# # # # # # ============================================================================
# # # # # st.markdown('<h1 class="main-header">🎯 Job Market Analytics</h1>', unsafe_allow_html=True)
# # # # # st.markdown('<p class="sub-header">Click any KPI card → see detailed breakdown</p>', unsafe_allow_html=True)

# # # # # # ============================================================================
# # # # # # SESSION STATE
# # # # # # ============================================================================
# # # # # for key in ['view', 'drill_type', 'drill_value']:
# # # # #     if key not in st.session_state:
# # # # #         st.session_state[key] = None

# # # # # # Sidebar
# # # # # st.sidebar.markdown("## 🔍 Navigation")
# # # # # if st.sidebar.button("🏠 Home (Clear View)"):
# # # # #     st.session_state.view = None
# # # # #     st.session_state.drill_type = None
# # # # #     st.session_state.drill_value = None
# # # # #     st.rerun()

# # # # # if st.session_state.view:
# # # # #     st.sidebar.success(f"**Viewing:** {st.session_state.view}")

# # # # # if st.session_state.drill_type:
# # # # #     st.sidebar.info(f"**Drill:** {st.session_state.drill_type} = {st.session_state.drill_value}")
# # # # #     if st.sidebar.button("❌ Clear Drill"):
# # # # #         st.session_state.drill_type = None
# # # # #         st.session_state.drill_value = None
# # # # #         st.rerun()

# # # # # st.sidebar.markdown("---")
# # # # # st.sidebar.markdown(f"**📊 Total Jobs:** {len(df)}")
# # # # # st.sidebar.markdown(f"**🏠 Remote Jobs:** {(df['is_remote']=='Yes').sum()}")

# # # # # # ============================================================================
# # # # # # KPI CARDS — CLICKABLE
# # # # # # ============================================================================
# # # # # st.markdown("## 📈 Overview — Click to Explore")

# # # # # k1, k2, k3, k4, k5, k6 = st.columns(6)

# # # # # with k1:
# # # # #     if st.button(f"📊\n\n**Total Jobs**\n\n{len(df)}\n\n_in dataset_",
# # # # #                  key="kpi_total", use_container_width=True):
# # # # #         st.session_state.view = "Total Jobs"
# # # # #         st.session_state.drill_type = None
# # # # #         st.rerun()

# # # # # with k2:
# # # # #     if st.button(f"🏢\n\n**Companies**\n\n{df['company'].nunique()}\n\n_hiring_",
# # # # #                  key="kpi_company", use_container_width=True):
# # # # #         st.session_state.view = "Companies"
# # # # #         st.session_state.drill_type = None
# # # # #         st.rerun()

# # # # # with k3:
# # # # #     if st.button(f"💼\n\n**Job Roles**\n\n{df['title'].nunique()}\n\n_unique_",
# # # # #                  key="kpi_title", use_container_width=True):
# # # # #         st.session_state.view = "Job Roles"
# # # # #         st.session_state.drill_type = None
# # # # #         st.rerun()

# # # # # with k4:
# # # # #     if st.button(f"🌐\n\n**Portals**\n\n{df['platform'].nunique()}\n\n_sources_",
# # # # #                  key="kpi_portal", use_container_width=True):
# # # # #         st.session_state.view = "Portals"
# # # # #         st.session_state.drill_type = None
# # # # #         st.rerun()

# # # # # with k5:
# # # # #     if st.button(f"📍\n\n**Locations**\n\n{df['location'].nunique()}\n\n_cities_",
# # # # #                  key="kpi_location", use_container_width=True):
# # # # #         st.session_state.view = "Locations"
# # # # #         st.session_state.drill_type = None
# # # # #         st.rerun()

# # # # # with k6:
# # # # #     remote_count = (df['is_remote'] == 'Yes').sum()
# # # # #     if st.button(f"🏠\n\n**Remote Jobs**\n\n{remote_count}\n\n_of {len(df)}_",
# # # # #                  key="kpi_remote", use_container_width=True):
# # # # #         st.session_state.view = "Remote Jobs"
# # # # #         st.session_state.drill_type = None
# # # # #         st.rerun()

# # # # # st.markdown("---")

# # # # # # ============================================================================
# # # # # # VIEW: REMOTE JOBS — DETAILED BREAKDOWN
# # # # # # ============================================================================
# # # # # if st.session_state.view == "Remote Jobs":
# # # # #     st.markdown('<div class="drill-header">🏠 Remote Jobs — Complete Breakdown</div>', unsafe_allow_html=True)

# # # # #     # Get remote jobs
# # # # #     remote_df = df[df['is_remote'] == 'Yes']

# # # # #     if len(remote_df) == 0:
# # # # #         st.warning("No remote jobs found in the dataset.")
# # # # #     else:
# # # # #         # ---- Top KPIs ----
# # # # #         d1, d2, d3, d4, d5 = st.columns(5)
# # # # #         with d1:
# # # # #             st.metric("🏠 Total Remote Jobs", len(remote_df))
# # # # #         with d2:
# # # # #             st.metric("🏢 Companies", remote_df['company'].nunique())
# # # # #         with d3:
# # # # #             st.metric("📍 Locations", remote_df['location'].nunique())
# # # # #         with d4:
# # # # #             st.metric("💼 Job Roles", remote_df['title'].nunique())
# # # # #         with d5:
# # # # #             st.metric("🌐 Portals", remote_df['platform'].nunique())

# # # # #         st.markdown("---")

# # # # #         # ================================================================
# # # # #         # SECTION 1: Remote Companies
# # # # #         # ================================================================
# # # # #         st.markdown("### 🏢 Companies Hiring Remote")

# # # # #         c1, c2 = st.columns([3, 2])

# # # # #         with c1:
# # # # #             remote_companies = remote_df['company'].value_counts().reset_index()
# # # # #             remote_companies.columns = ['Company', 'Remote Jobs']

# # # # #             fig = px.bar(
# # # # #                 remote_companies, x='Remote Jobs', y='Company', orientation='h',
# # # # #                 title=f'All {len(remote_companies)} Companies Hiring Remote — Click a bar',
# # # # #                 color='Remote Jobs', color_continuous_scale='Greens', text='Remote Jobs'
# # # # #             )
# # # # #             fig.update_layout(
# # # # #                 height=max(400, len(remote_companies)*35),
# # # # #                 showlegend=False,
# # # # #                 yaxis=dict(autorange="reversed"),
# # # # #                 title_font_size=14,
# # # # #                 clickmode='event+select'
# # # # #             )
# # # # #             fig.update_traces(textposition='outside')

# # # # #             event = st.plotly_chart(fig, use_container_width=True,
# # # # #                                     on_select="rerun", key="remote_company_drill")

# # # # #             if event and event.get("selection") and event["selection"].get("points"):
# # # # #                 clicked = event["selection"]["points"][0].get("y")
# # # # #                 if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
# # # # #                     st.session_state.drill_type = "Company"
# # # # #                     st.session_state.drill_value = clicked
# # # # #                     st.rerun()

# # # # #         with c2:
# # # # #             st.markdown("#### 📋 Company List (Remote)")
# # # # #             st.dataframe(remote_companies, use_container_width=True,
# # # # #                          height=400, hide_index=True)

# # # # #         # ================================================================
# # # # #         # SECTION 2: Remote Locations / Areas
# # # # #         # ================================================================
# # # # #         st.markdown("### 📍 Remote Jobs by Location / Area")

# # # # #         c3, c4 = st.columns([3, 2])

# # # # #         with c3:
# # # # #             remote_locs = remote_df['location'].value_counts().reset_index()
# # # # #             remote_locs.columns = ['Location', 'Remote Jobs']

# # # # #             fig = px.bar(
# # # # #                 remote_locs, x='Remote Jobs', y='Location', orientation='h',
# # # # #                 title=f'Remote Jobs by Location — Click a bar',
# # # # #                 color='Remote Jobs', color_continuous_scale='Teal', text='Remote Jobs'
# # # # #             )
# # # # #             fig.update_layout(
# # # # #                 height=max(400, len(remote_locs)*35),
# # # # #                 showlegend=False,
# # # # #                 yaxis=dict(autorange="reversed"),
# # # # #                 title_font_size=14,
# # # # #                 clickmode='event+select'
# # # # #             )
# # # # #             fig.update_traces(textposition='outside')

# # # # #             event = st.plotly_chart(fig, use_container_width=True,
# # # # #                                     on_select="rerun", key="remote_loc_drill")

# # # # #             if event and event.get("selection") and event["selection"].get("points"):
# # # # #                 clicked = event["selection"]["points"][0].get("y")
# # # # #                 if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
# # # # #                     st.session_state.drill_type = "Location"
# # # # #                     st.session_state.drill_value = clicked
# # # # #                     st.rerun()

# # # # #         with c4:
# # # # #             st.markdown("#### 📋 Location List (Remote)")
# # # # #             st.dataframe(remote_locs, use_container_width=True,
# # # # #                          height=400, hide_index=True)

# # # # #         # ================================================================
# # # # #         # SECTION 3: Remote Portals
# # # # #         # ================================================================
# # # # #         st.markdown("### 🌐 Which Portals Post Remote Jobs?")

# # # # #         c5, c6 = st.columns([2, 2])

# # # # #         with c5:
# # # # #             remote_portals = remote_df['platform'].value_counts().reset_index()
# # # # #             remote_portals.columns = ['Portal', 'Remote Jobs']

# # # # #             fig = px.bar(
# # # # #                 remote_portals, x='Portal', y='Remote Jobs',
# # # # #                 title='Remote Jobs by Portal — Click a bar',
# # # # #                 color='Remote Jobs', color_continuous_scale='Blues', text='Remote Jobs'
# # # # #             )
# # # # #             fig.update_layout(height=400, showlegend=False,
# # # # #                               xaxis_tickangle=-30, title_font_size=13,
# # # # #                               clickmode='event+select')
# # # # #             fig.update_traces(textposition='outside')

# # # # #             event = st.plotly_chart(fig, use_container_width=True,
# # # # #                                     on_select="rerun", key="remote_portal_drill")

# # # # #             if event and event.get("selection") and event["selection"].get("points"):
# # # # #                 clicked = event["selection"]["points"][0].get("x")
# # # # #                 if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
# # # # #                     st.session_state.drill_type = "Portal"
# # # # #                     st.session_state.drill_value = clicked
# # # # #                     st.rerun()

# # # # #         with c6:
# # # # #             fig = px.pie(
# # # # #                 remote_portals, values='Remote Jobs', names='Portal',
# # # # #                 title='Remote Jobs — Portal Share',
# # # # #                 hole=0.4,
# # # # #                 color_discrete_sequence=px.colors.qualitative.Set3
# # # # #             )
# # # # #             fig.update_traces(textinfo='percent+label', textposition='outside',
# # # # #                               textfont_size=11, pull=[0.03] * len(remote_portals))
# # # # #             fig.update_layout(height=400, title_font_size=13)
# # # # #             st.plotly_chart(fig, use_container_width=True, key="remote_portal_pie")

# # # # #         # ================================================================
# # # # #         # SECTION 4: Remote Job Roles
# # # # #         # ================================================================
# # # # #         st.markdown("### 💼 What Job Roles Are Remote?")

# # # # #         remote_roles = remote_df['title'].value_counts().reset_index()
# # # # #         remote_roles.columns = ['Job Role', 'Remote Jobs']

# # # # #         fig = px.bar(
# # # # #             remote_roles, x='Remote Jobs', y='Job Role', orientation='h',
# # # # #             title=f'Remote Job Roles — Click a bar',
# # # # #             color='Remote Jobs', color_continuous_scale='Purples', text='Remote Jobs'
# # # # #         )
# # # # #         fig.update_layout(
# # # # #             height=max(400, len(remote_roles)*35),
# # # # #             showlegend=False,
# # # # #             yaxis=dict(autorange="reversed"),
# # # # #             title_font_size=14,
# # # # #             clickmode='event+select'
# # # # #         )
# # # # #         fig.update_traces(textposition='outside')

# # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # #                                 on_select="rerun", key="remote_role_drill")

# # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # #             if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
# # # # #                 st.session_state.drill_type = "Job Role"
# # # # #                 st.session_state.drill_value = clicked
# # # # #                 st.rerun()

# # # # #         # ================================================================
# # # # #         # SECTION 5: Skills Required for Remote Jobs
# # # # #         # ================================================================
# # # # #         st.markdown("### 🛠️ Top Skills Required for Remote Jobs")

# # # # #         all_remote_skills = [s for skills in remote_df['skills'] for s in skills]
# # # # #         remote_skill_counts = Counter(all_remote_skills).most_common(15)

# # # # #         if remote_skill_counts:
# # # # #             rs_df = pd.DataFrame(remote_skill_counts, columns=['Skill', 'Jobs'])
# # # # #             rs_df['% of Remote'] = (rs_df['Jobs'] / len(remote_df) * 100).round(1)

# # # # #             fig = px.bar(
# # # # #                 rs_df, x='Jobs', y='Skill', orientation='h',
# # # # #                 title='Top Skills for Remote Jobs',
# # # # #                 color='Jobs', color_continuous_scale='Greens', text='Jobs'
# # # # #             )
# # # # #             fig.update_layout(height=500, showlegend=False,
# # # # #                               yaxis=dict(autorange="reversed"),
# # # # #                               title_font_size=14)
# # # # #             fig.update_traces(textposition='outside')
# # # # #             st.plotly_chart(fig, use_container_width=True, key="remote_skills")

# # # # #         # ================================================================
# # # # #         # SECTION 6: Full Remote Job List
# # # # #         # ================================================================
# # # # #         st.markdown("### 📋 All Remote Job Openings")

# # # # #         show_cols = ['title', 'company', 'location', 'platform',
# # # # #                      'employment_type', 'posted_date']
# # # # #         display_remote = remote_df[show_cols].copy()
# # # # #         display_remote.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # # #                                   'Type', 'Posted']

# # # # #         st.dataframe(display_remote, use_container_width=True, height=500)

# # # # #         csv = remote_df.to_csv(index=False)
# # # # #         st.download_button(
# # # # #             label="📥 Download All Remote Jobs (CSV)",
# # # # #             data=csv,
# # # # #             file_name=f"remote_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # #             mime="text/csv",
# # # # #             key="dl_remote"
# # # # #         )

# # # # #         # ---- Insight ----
# # # # #         top_comp = remote_df['company'].value_counts().index[0]
# # # # #         top_loc = remote_df['location'].value_counts().index[0]
# # # # #         top_portal = remote_df['platform'].value_counts().index[0]

# # # # #         st.markdown(f"""<div class="insight-box">
# # # # #             <strong>📊 Remote Job Summary:</strong><br>
# # # # #             🏢 <strong>Top Remote Employer:</strong> {top_comp}<br>
# # # # #             📍 <strong>Top Remote Location:</strong> {top_loc}<br>
# # # # #             🌐 <strong>Top Portal for Remote:</strong> {top_portal}<br>
# # # # #             🛠️ <strong>Top Skill for Remote:</strong> {remote_skill_counts[0][0] if remote_skill_counts else 'N/A'}<br>
# # # # #             📊 <strong>Remote % of Total:</strong> {len(remote_df)/len(df)*100:.1f}%
# # # # #         </div>""", unsafe_allow_html=True)

# # # # # # ============================================================================
# # # # # # OTHER VIEWS (Companies, Locations, etc.)
# # # # # # ============================================================================
# # # # # elif st.session_state.view == "Companies":
# # # # #     st.markdown('<div class="drill-header">🏢 All Companies Hiring</div>', unsafe_allow_html=True)
# # # # #     comp_df = df['company'].value_counts().reset_index()
# # # # #     comp_df.columns = ['Company', 'Openings']
# # # # #     comp_df['Share %'] = (comp_df['Openings'] / len(df) * 100).round(2)

# # # # #     c1, c2 = st.columns([3, 2])
# # # # #     with c1:
# # # # #         fig = px.bar(comp_df.head(30), x='Openings', y='Company', orientation='h',
# # # # #                      title=f'All {len(comp_df)} Companies (Top 30) — Click a bar',
# # # # #                      color='Openings', color_continuous_scale='Viridis', text='Openings')
# # # # #         fig.update_layout(height=800, showlegend=False,
# # # # #                           yaxis=dict(autorange="reversed"),
# # # # #                           title_font_size=14, clickmode='event+select')
# # # # #         fig.update_traces(textposition='outside')
# # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # #                                 on_select="rerun", key="comp_view_drill")
# # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # #             if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
# # # # #                 st.session_state.drill_type = "Company"
# # # # #                 st.session_state.drill_value = clicked
# # # # #                 st.rerun()

# # # # #     with c2:
# # # # #         st.markdown("### 📋 Complete List")
# # # # #         st.dataframe(comp_df, use_container_width=True, height=750, hide_index=True)

# # # # #     csv = comp_df.to_csv(index=False)
# # # # #     st.download_button("📥 Download CSV", csv,
# # # # #                        file_name=f"companies_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # #                        mime="text/csv", key="dl_comp_view")

# # # # # elif st.session_state.view == "Locations":
# # # # #     st.markdown('<div class="drill-header">📍 All Locations</div>', unsafe_allow_html=True)
# # # # #     loc_df = df['location'].value_counts().reset_index()
# # # # #     loc_df.columns = ['Location', 'Openings']
# # # # #     loc_df['Share %'] = (loc_df['Openings'] / len(df) * 100).round(2)

# # # # #     c1, c2 = st.columns([3, 2])
# # # # #     with c1:
# # # # #         fig = px.bar(loc_df, x='Openings', y='Location', orientation='h',
# # # # #                      title=f'All {len(loc_df)} Locations — Click a bar',
# # # # #                      color='Openings', color_continuous_scale='Magma', text='Openings')
# # # # #         fig.update_layout(height=max(600, len(loc_df)*22), showlegend=False,
# # # # #                           yaxis=dict(autorange="reversed"),
# # # # #                           title_font_size=14, clickmode='event+select')
# # # # #         fig.update_traces(textposition='outside')
# # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # #                                 on_select="rerun", key="loc_view_drill")
# # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # #             if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
# # # # #                 st.session_state.drill_type = "Location"
# # # # #                 st.session_state.drill_value = clicked
# # # # #                 st.rerun()

# # # # #     with c2:
# # # # #         st.markdown("### 📋 Complete List")
# # # # #         st.dataframe(loc_df, use_container_width=True, height=750, hide_index=True)

# # # # #     csv = loc_df.to_csv(index=False)
# # # # #     st.download_button("📥 Download CSV", csv,
# # # # #                        file_name=f"locations_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # #                        mime="text/csv", key="dl_loc_view")

# # # # # elif st.session_state.view == "Job Roles":
# # # # #     st.markdown('<div class="drill-header">💼 All Job Roles</div>', unsafe_allow_html=True)
# # # # #     role_df = df['title'].value_counts().reset_index()
# # # # #     role_df.columns = ['Job Role', 'Openings']
# # # # #     role_df['Share %'] = (role_df['Openings'] / len(df) * 100).round(2)

# # # # #     c1, c2 = st.columns([3, 2])
# # # # #     with c1:
# # # # #         fig = px.bar(role_df.head(40), x='Openings', y='Job Role', orientation='h',
# # # # #                      title=f'All {len(role_df)} Job Roles (Top 40) — Click a bar',
# # # # #                      color='Openings', color_continuous_scale='Plasma', text='Openings')
# # # # #         fig.update_layout(height=1000, showlegend=False,
# # # # #                           yaxis=dict(autorange="reversed"),
# # # # #                           title_font_size=14, clickmode='event+select')
# # # # #         fig.update_traces(textposition='outside')
# # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # #                                 on_select="rerun", key="role_view_drill")
# # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # #             clicked = event["selection"]["points"][0].get("y")
# # # # #             if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
# # # # #                 st.session_state.drill_type = "Job Role"
# # # # #                 st.session_state.drill_value = clicked
# # # # #                 st.rerun()

# # # # #     with c2:
# # # # #         st.markdown("### 📋 Complete List")
# # # # #         st.dataframe(role_df, use_container_width=True, height=950, hide_index=True)

# # # # #     csv = role_df.to_csv(index=False)
# # # # #     st.download_button("📥 Download CSV", csv,
# # # # #                        file_name=f"roles_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # #                        mime="text/csv", key="dl_role_view")

# # # # # elif st.session_state.view == "Portals":
# # # # #     st.markdown('<div class="drill-header">🌐 All Portals</div>', unsafe_allow_html=True)
# # # # #     portal_df = df['platform'].value_counts().reset_index()
# # # # #     portal_df.columns = ['Portal', 'Openings']
# # # # #     portal_df['Share %'] = (portal_df['Openings'] / len(df) * 100).round(2)

# # # # #     c1, c2 = st.columns(2)
# # # # #     with c1:
# # # # #         fig = px.bar(portal_df, x='Portal', y='Openings',
# # # # #                      title='Portals — Click a bar',
# # # # #                      color='Openings', color_continuous_scale='Turbo', text='Openings')
# # # # #         fig.update_layout(height=450, showlegend=False,
# # # # #                           xaxis_tickangle=-30, title_font_size=13,
# # # # #                           clickmode='event+select')
# # # # #         fig.update_traces(textposition='outside')
# # # # #         event = st.plotly_chart(fig, use_container_width=True,
# # # # #                                 on_select="rerun", key="portal_view_drill")
# # # # #         if event and event.get("selection") and event["selection"].get("points"):
# # # # #             clicked = event["selection"]["points"][0].get("x")
# # # # #             if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
# # # # #                 st.session_state.drill_type = "Portal"
# # # # #                 st.session_state.drill_value = clicked
# # # # #                 st.rerun()

# # # # #     with c2:
# # # # #         st.markdown("### 📋 Complete List")
# # # # #         st.dataframe(portal_df, use_container_width=True, hide_index=True)

# # # # #     csv = portal_df.to_csv(index=False)
# # # # #     st.download_button("📥 Download CSV", csv,
# # # # #                        file_name=f"portals_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # #                        mime="text/csv", key="dl_portal_view")

# # # # # elif st.session_state.view == "Total Jobs":
# # # # #     st.markdown('<div class="drill-header">📊 All Jobs in Dataset</div>', unsafe_allow_html=True)
# # # # #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # # # #                  'employment_type', 'posted_date']
# # # # #     display_df = df[show_cols].copy()
# # # # #     display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # # #                           'Remote', 'Type', 'Posted']
# # # # #     st.dataframe(display_df, use_container_width=True, height=600)
# # # # #     csv = df.to_csv(index=False)
# # # # #     st.download_button("📥 Download All Jobs (CSV)", csv,
# # # # #                        file_name=f"all_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
# # # # #                        mime="text/csv", key="dl_total_view")

# # # # # # ============================================================================
# # # # # # DRILL-DOWN PANEL
# # # # # # ============================================================================
# # # # # if st.session_state.drill_type and st.session_state.drill_value:
# # # # #     st.markdown("---")
# # # # #     drill_val = st.session_state.drill_value
# # # # #     drill_type = st.session_state.drill_type

# # # # #     st.markdown(f'<div class="drill-header">🎯 Drill-Down: {drill_type} = "{drill_val}"</div>', unsafe_allow_html=True)

# # # # #     if drill_type == "Skill":
# # # # #         drill_df = df[df['skills'].apply(lambda x: drill_val in x)]
# # # # #     elif drill_type == "Job Role":
# # # # #         drill_df = df[df['title'] == drill_val]
# # # # #     elif drill_type == "Company":
# # # # #         drill_df = df[df['company'] == drill_val]
# # # # #     elif drill_type == "Location":
# # # # #         drill_df = df[df['location'] == drill_val]
# # # # #     elif drill_type == "Portal":
# # # # #         drill_df = df[df['platform'] == drill_val]
# # # # #     else:
# # # # #         drill_df = df.copy()

# # # # #     d1, d2, d3, d4 = st.columns(4)
# # # # #     with d1: st.metric("🎯 Total Openings", len(drill_df))
# # # # #     with d2: st.metric("🏢 Companies", drill_df['company'].nunique())
# # # # #     with d3: st.metric("📍 Locations", drill_df['location'].nunique())
# # # # #     with d4:
# # # # #         rp = (drill_df['is_remote'] == 'Yes').sum() / len(drill_df) * 100 if len(drill_df) > 0 else 0
# # # # #         st.metric("🏠 Remote %", f"{rp:.1f}%")

# # # # #     g1, g2 = st.columns(2)
# # # # #     with g1:
# # # # #         pc = drill_df['platform'].value_counts().reset_index()
# # # # #         pc.columns = ['Portal', 'Openings']
# # # # #         fig = px.bar(pc, x='Openings', y='Portal', orientation='h',
# # # # #                      title='By Portal', color='Openings',
# # # # #                      color_continuous_scale='Blues', text='Openings')
# # # # #         fig.update_layout(height=350, showlegend=False,
# # # # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # # # #         fig.update_traces(textposition='outside')
# # # # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_p_{drill_val}")

# # # # #     with g2:
# # # # #         cc = drill_df['company'].value_counts().head(10).reset_index()
# # # # #         cc.columns = ['Company', 'Openings']
# # # # #         fig = px.bar(cc, x='Openings', y='Company', orientation='h',
# # # # #                      title='By Company', color='Openings',
# # # # #                      color_continuous_scale='Viridis', text='Openings')
# # # # #         fig.update_layout(height=350, showlegend=False,
# # # # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # # # #         fig.update_traces(textposition='outside')
# # # # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_c_{drill_val}")

# # # # #     st.markdown("### 📋 All Job Openings")
# # # # #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # # # #                  'employment_type', 'posted_date']
# # # # #     ddf = drill_df[show_cols].copy()
# # # # #     ddf.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # # #                    'Remote', 'Type', 'Posted']
# # # # #     st.dataframe(ddf, use_container_width=True, height=400)

# # # # #     csv = drill_df.to_csv(index=False)
# # # # #     st.download_button("📥 Download (CSV)", csv,
# # # # #                        file_name=f"drill_{drill_type}_{drill_val}.csv",
# # # # #                        mime="text/csv", key=f"dl_dd_{drill_val}")

# # # # # # ============================================================================
# # # # # # MAIN TABS (when no view is active)
# # # # # # ============================================================================
# # # # # if st.session_state.view is None:
# # # # #     st.markdown("---")
# # # # #     st.markdown("## 🔎 Explore Charts — Click to drill down")

# # # # #     tabs = st.tabs(["🛠️ By Skill", "💼 By Role", "🏢 By Company",
# # # # #                     "📍 By Location", "🌐 By Portal"])

# # # # #     with tabs[0]:
# # # # #         all_sk = [s for skills in df['skills'] for s in skills]
# # # # #         sc = Counter(all_sk).most_common(20)
# # # # #         if sc:
# # # # #             sdf = pd.DataFrame(sc, columns=['Skill', 'Jobs'])
# # # # #             fig = px.bar(sdf, x='Jobs', y='Skill', orientation='h',
# # # # #                          title='Top 20 Skills', color='Jobs',
# # # # #                          color_continuous_scale='RdYlGn', text='Jobs')
# # # # #             fig.update_layout(height=650, showlegend=False,
# # # # #                               yaxis=dict(autorange="reversed"),
# # # # #                               clickmode='event+select')
# # # # #             fig.update_traces(textposition='outside')
# # # # #             ev = st.plotly_chart(fig, use_container_width=True,
# # # # #                                  on_select="rerun", key="main_skill")
# # # # #             if ev and ev.get("selection") and ev["selection"].get("points"):
# # # # #                 c = ev["selection"]["points"][0].get("y")
# # # # #                 if c and (st.session_state.drill_type != "Skill" or st.session_state.drill_value != c):
# # # # #                     st.session_state.drill_type = "Skill"
# # # # #                     st.session_state.drill_value = c
# # # # #                     st.rerun()

# # # # #     with tabs[1]:
# # # # #         tc = df['title'].value_counts().head(20).reset_index()
# # # # #         tc.columns = ['Job Role', 'Openings']
# # # # #         fig = px.bar(tc, x='Openings', y='Job Role', orientation='h',
# # # # #                      title='Top 20 Roles', color='Openings',
# # # # #                      color_continuous_scale='Viridis', text='Openings')
# # # # #         fig.update_layout(height=650, showlegend=False,
# # # # #                           yaxis=dict(autorange="reversed"),
# # # # #                           clickmode='event+select')
# # # # #         fig.update_traces(textposition='outside')
# # # # #         ev = st.plotly_chart(fig, use_container_width=True,
# # # # #                              on_select="rerun", key="main_role")
# # # # #         if ev and ev.get("selection") and ev["selection"].get("points"):
# # # # #             c = ev["selection"]["points"][0].get("y")
# # # # #             if c and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != c):
# # # # #                 st.session_state.drill_type = "Job Role"
# # # # #                 st.session_state.drill_value = c
# # # # #                 st.rerun()

# # # # #     with tabs[2]:
# # # # #         cc = df['company'].value_counts().head(20).reset_index()
# # # # #         cc.columns = ['Company', 'Openings']
# # # # #         fig = px.bar(cc, x='Openings', y='Company', orientation='h',
# # # # #                      title='Top 20 Companies', color='Openings',
# # # # #                      color_continuous_scale='Cividis', text='Openings')
# # # # #         fig.update_layout(height=650, showlegend=False,
# # # # #                           yaxis=dict(autorange="reversed"),
# # # # #                           clickmode='event+select')
# # # # #         fig.update_traces(textposition='outside')
# # # # #         ev = st.plotly_chart(fig, use_container_width=True,
# # # # #                              on_select="rerun", key="main_company")
# # # # #         if ev and ev.get("selection") and ev["selection"].get("points"):
# # # # #             c = ev["selection"]["points"][0].get("y")
# # # # #             if c and (st.session_state.drill_type != "Company" or st.session_state.drill_value != c):
# # # # #                 st.session_state.drill_type = "Company"
# # # # #                 st.session_state.drill_value = c
# # # # #                 st.rerun()

# # # # #     with tabs[3]:
# # # # #         lc = df['location'].value_counts().head(20).reset_index()
# # # # #         lc.columns = ['Location', 'Openings']
# # # # #         fig = px.bar(lc, x='Location', y='Openings',
# # # # #                      title='Top 20 Locations', color='Openings',
# # # # #                      color_continuous_scale='Turbo', text='Openings')
# # # # #         fig.update_layout(height=500, showlegend=False,
# # # # #                           xaxis_tickangle=-40, clickmode='event+select')
# # # # #         fig.update_traces(textposition='outside')
# # # # #         ev = st.plotly_chart(fig, use_container_width=True,
# # # # #                              on_select="rerun", key="main_loc")
# # # # #         if ev and ev.get("selection") and ev["selection"].get("points"):
# # # # #             c = ev["selection"]["points"][0].get("x")
# # # # #             if c and (st.session_state.drill_type != "Location" or st.session_state.drill_value != c):
# # # # #                 st.session_state.drill_type = "Location"
# # # # #                 st.session_state.drill_value = c
# # # # #                 st.rerun()

# # # # #     with tabs[4]:
# # # # #         pc = df['platform'].value_counts().reset_index()
# # # # #         pc.columns = ['Portal', 'Openings']
# # # # #         c1, c2 = st.columns(2)
# # # # #         with c1:
# # # # #             fig = px.bar(pc, x='Portal', y='Openings',
# # # # #                          title='Portals', color='Openings',
# # # # #                          color_continuous_scale='Plasma', text='Openings')
# # # # #             fig.update_layout(height=450, showlegend=False,
# # # # #                               xaxis_tickangle=-30, clickmode='event+select')
# # # # #             fig.update_traces(textposition='outside')
# # # # #             ev = st.plotly_chart(fig, use_container_width=True,
# # # # #                                  on_select="rerun", key="main_portal")
# # # # #             if ev and ev.get("selection") and ev["selection"].get("points"):
# # # # #                 c = ev["selection"]["points"][0].get("x")
# # # # #                 if c and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != c):
# # # # #                     st.session_state.drill_type = "Portal"
# # # # #                     st.session_state.drill_value = c
# # # # #                     st.rerun()

# # # # #         with c2:
# # # # #             fig = px.pie(pc, values='Openings', names='Portal',
# # # # #                          title='Distribution', hole=0.4,
# # # # #                          color_discrete_sequence=px.colors.qualitative.Set3)
# # # # #             fig.update_traces(textinfo='percent+label',
# # # # #                               textposition='outside', textfont_size=11,
# # # # #                               pull=[0.03] * len(pc))
# # # # #             fig.update_layout(height=450)
# # # # #             st.plotly_chart(fig, use_container_width=True, key="main_portal_pie")

# # # # # # ============================================================================
# # # # # # FOOTER
# # # # # # ============================================================================
# # # # # st.markdown("---")
# # # # # st.markdown(f"""<div style='text-align:center; color:#666; font-size:12px;'>
# # # # #     Job Market Analytics | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
# # # # #     {len(df)} total jobs | {(df['is_remote']=='Yes').sum()} remote
# # # # # </div>""", unsafe_allow_html=True)

















































# # # # """
# # # # ================================================================================
# # # # JOB MARKET ANALYTICS — WITH LIVE SEARCH
# # # # Type any keyword → see all matching openings instantly
# # # # Tech Stack: Python | Pandas | NumPy | Plotly | Streamlit
# # # # Run: python -m streamlit run dashboard.py
# # # # ================================================================================
# # # # """

# # # # import streamlit as st
# # # # import pandas as pd
# # # # import numpy as np
# # # # import plotly.express as px
# # # # import plotly.graph_objects as go
# # # # from collections import Counter
# # # # from datetime import datetime
# # # # import warnings
# # # # import logging

# # # # warnings.filterwarnings('ignore')
# # # # logging.getLogger('streamlit').setLevel(logging.ERROR)

# # # # # ============================================================================
# # # # # PAGE CONFIG
# # # # # ============================================================================
# # # # st.set_page_config(
# # # #     page_title="Job Market Analytics",
# # # #     page_icon="🎯",
# # # #     layout="wide",
# # # #     initial_sidebar_state="expanded"
# # # # )

# # # # # CSS
# # # # st.markdown("""
# # # # <style>
    /* ========== FORCE DARK TEXT EVERYWHERE ========== */
    .stApp, .stApp * {
        color: #1a1a1a !important;
    }
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricLabel"] > div {
        color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stDataFrame"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
    }
# # # #     div[data-testid="stMarkdownContainer"] div,
# # # #     div[data-testid="stMarkdownContainer"] p,
# # # #     div[data-testid="stMarkdownContainer"] span,
# # # #     div[data-testid="stMarkdownContainer"] strong { color: #1a1a1a; }

# # # #     .main-header {
# # # #         font-size: 2.2rem; font-weight: bold;
# # # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # # #         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
# # # #         text-align: center; padding: 0.5rem 0;
# # # #     }
# # # #     .sub-header { text-align: center; color: #666; margin-bottom: 1rem; }
# # # #     .problem-header {
# # # #         background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
# # # #         padding: 0.7rem 1rem; border-radius: 8px;
# # # #         color: #FFFFFF !important; font-weight: bold;
# # # #         margin-bottom: 1rem; font-size: 1rem;
# # # #     }
# # # #     .insight-box {
# # # #         background: #f0f7ff; padding: 0.8rem;
# # # #         border-left: 4px solid #667eea; border-radius: 5px;
# # # #         margin: 0.6rem 0; font-size: 0.9rem; color: #1a1a1a !important;
# # # #     }
# # # #     .insight-box strong { color: #2c3e50 !important; font-weight: 700; }
# # # #     .drill-header {
# # # #         background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
# # # #         padding: 0.8rem 1rem; border-radius: 8px;
# # # #         color: #1a1a1a !important; font-weight: bold;
# # # #         margin: 1rem 0; font-size: 1.1rem;
# # # #         border: 2px solid #43e97b;
# # # #     }
# # # #     .search-header {
# # # #         background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
# # # #         padding: 1rem 1.2rem; border-radius: 10px;
# # # #         color: #1a1a1a !important; font-weight: bold;
# # # #         margin: 1rem 0; font-size: 1.15rem;
# # # #         border: 2px solid #4facfe;
# # # #     }
# # # #     .stTabs [data-baseweb="tab-list"] { gap: 6px; flex-wrap: wrap; }
# # # #     .stTabs [data-baseweb="tab"] {
# # # #         background-color: #f0f2f6; border-radius: 6px;
# # # #         padding: 8px 12px; font-weight: 600; font-size: 0.78rem;
# # # #     }
# # # #     .stTabs [aria-selected="true"] {
# # # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # # #         color: #FFFFFF !important;
# # # #     }
# # # #     div[data-testid="stButton"] button {
# # # #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# # # #         color: white !important; border: none;
# # # #         padding: 1.5rem 1rem; border-radius: 12px;
# # # #         width: 100%; min-height: 120px;
# # # #         font-size: 1rem; font-weight: bold;
# # # #         box-shadow: 0 4px 12px rgba(0,0,0,0.1);
# # # #         transition: transform 0.2s;
# # # #     }
# # # #     div[data-testid="stButton"] button:hover {
# # # #         transform: translateY(-3px);
# # # #         box-shadow: 0 6px 16px rgba(0,0,0,0.2);
# # # #     }
# # # #     div[data-testid="stButton"] button p {
# # # #         color: white !important; font-size: 1rem; font-weight: bold;
# # # #     }
# # # # </style>
# # # # """, unsafe_allow_html=True)

# # # # # ============================================================================
# # # # # DATA LOADING
# # # # # ============================================================================

# # # # @st.cache_data
# # # # def load_data():
# # # #     df = pd.read_csv("job_data_clean.csv")
# # # #     df['posted_date'] = pd.to_datetime(df['posted_date'], errors='coerce')
# # # #     return df

# # # # def extract_skills(text):
# # # #     if pd.isna(text):
# # # #         return []
# # # #     text = str(text).lower()
# # # #     skill_list = [
# # # #         'python', 'java', 'sql', 'javascript', 'typescript', 'react', 'angular',
# # # #         'node.js', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
# # # #         'jenkins', 'spark', 'kafka', 'airflow', 'snowflake', 'tableau', 'power bi',
# # # #         'machine learning', 'deep learning', 'nlp', 'llm', 'genai', 'rag',
# # # #         'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
# # # #         'excel', 'git', 'linux', 'agile', 'scrum', 'jira'
# # # #     ]
# # # #     return list(set([s for s in skill_list if s in text]))

# # # # try:
# # # #     df = load_data()
# # # #     df['skills'] = df['description'].apply(extract_skills)
# # # #     df['skill_count'] = df['skills'].apply(len)
# # # #     # Build a searchable text column (title + company + location + description)
# # # #     df['search_text'] = (
# # # #         df['title'].fillna('') + ' ' +
# # # #         df['company'].fillna('') + ' ' +
# # # #         df['location'].fillna('') + ' ' +
# # # #         df['description'].fillna('')
# # # #     ).str.lower()
# # # # except Exception as e:
# # # #     st.error(f"❌ Error loading 'job_data_clean.csv': {e}")
# # # #     st.stop()

# # # # # ============================================================================
# # # # # HEADER
# # # # # ============================================================================
# # # # st.markdown('<h1 class="main-header">🎯 Job Market Analytics</h1>', unsafe_allow_html=True)
# # # # st.markdown('<p class="sub-header">🔍 Search any keyword • 🎯 Click KPI cards • 📊 Click charts to drill down</p>', unsafe_allow_html=True)

# # # # # ============================================================================
# # # # # SESSION STATE
# # # # # ============================================================================
# # # # for key in ['view', 'drill_type', 'drill_value', 'search_query']:
# # # #     if key not in st.session_state:
# # # #         st.session_state[key] = None

# # # # # ============================================================================
# # # # # SEARCH BAR (THE STAR FEATURE)
# # # # # ============================================================================
# # # # st.markdown("### 🔍 Search Job Openings")
# # # # search_col1, search_col2, search_col3 = st.columns([4, 1, 1])

# # # # with search_col1:
# # # #     search_query = st.text_input(
# # # #         "Type any keyword (e.g., data analyst, python, remote, bangalore):",
# # # #         value=st.session_state.search_query if st.session_state.search_query else "",
# # # #         placeholder="🔍 Try: data analyst, python, mastercard, remote, bangalore...",
# # # #         key="search_input",
# # # #         label_visibility="collapsed"
# # # #     )

# # # # with search_col2:
# # # #     if st.button("🔍 Search", use_container_width=True, key="search_btn"):
# # # #         st.session_state.search_query = search_query
# # # #         st.session_state.view = "Search Results"
# # # #         st.session_state.drill_type = None
# # # #         st.rerun()

# # # # with search_col3:
# # # #     if st.button("❌ Clear", use_container_width=True, key="clear_search"):
# # # #         st.session_state.search_query = None
# # # #         st.session_state.view = None
# # # #         st.rerun()

# # # # # Quick search suggestion chips
# # # # st.markdown("**Popular searches:**")
# # # # chip_cols = st.columns(8)
# # # # quick_searches = ["data analyst", "data scientist", "python", "remote", "mastercard", "bangalore", "sql", "engineer"]
# # # # for i, term in enumerate(quick_searches):
# # # #     with chip_cols[i]:
# # # #         if st.button(f"🔎 {term}", key=f"quick_{term}", use_container_width=True):
# # # #             st.session_state.search_query = term
# # # #             st.session_state.view = "Search Results"
# # # #             st.session_state.drill_type = None
# # # #             st.rerun()

# # # # # Auto-search when user types
# # # # if search_query and search_query != st.session_state.search_query and search_query.strip():
# # # #     st.session_state.search_query = search_query
# # # #     st.session_state.view = "Search Results"
# # # #     st.session_state.drill_type = None

# # # # # ============================================================================
# # # # # SEARCH RESULTS VIEW
# # # # # ============================================================================
# # # # if st.session_state.view == "Search Results" and st.session_state.search_query:
# # # #     query = st.session_state.search_query.strip().lower()

# # # #     # Filter using search_text
# # # #     search_results = df[df['search_text'].str.contains(query, na=False, regex=False)]

# # # #     st.markdown(f'<div class="search-header">🔍 Search Results for: "{st.session_state.search_query}" — {len(search_results)} jobs found</div>', unsafe_allow_html=True)

# # # #     if len(search_results) == 0:
# # # #         st.warning(f"❌ No jobs found matching **'{st.session_state.search_query}'**. Try another keyword.")
# # # #     else:
# # # #         # ---- KPI Cards for search ----
# # # #         s1, s2, s3, s4, s5 = st.columns(5)
# # # #         with s1:
# # # #             st.metric("🎯 Matching Jobs", len(search_results))
# # # #         with s2:
# # # #             st.metric("🏢 Companies", search_results['company'].nunique())
# # # #         with s3:
# # # #             st.metric("📍 Locations", search_results['location'].nunique())
# # # #         with s4:
# # # #             st.metric("🌐 Portals", search_results['platform'].nunique())
# # # #         with s5:
# # # #             rp = (search_results['is_remote'] == 'Yes').sum() / len(search_results) * 100
# # # #             st.metric("🏠 Remote %", f"{rp:.1f}%")

# # # #         st.markdown("---")

# # # #         # ---- Charts for search results ----
# # # #         c1, c2 = st.columns(2)

# # # #         with c1:
# # # #             pc = search_results['platform'].value_counts().reset_index()
# # # #             pc.columns = ['Portal', 'Jobs']
# # # #             fig = px.bar(pc, x='Jobs', y='Portal', orientation='h',
# # # #                          title='Where These Jobs Are Posted',
# # # #                          color='Jobs', color_continuous_scale='Blues', text='Jobs')
# # # #             fig.update_layout(height=400, showlegend=False,
# # # #                               yaxis=dict(autorange="reversed"),
# # # #                               title_font_size=13)
# # # #             fig.update_traces(textposition='outside')
# # # #             st.plotly_chart(fig, use_container_width=True, key="search_portals")

# # # #         with c2:
# # # #             cc = search_results['company'].value_counts().head(10).reset_index()
# # # #             cc.columns = ['Company', 'Jobs']
# # # #             fig = px.bar(cc, x='Jobs', y='Company', orientation='h',
# # # #                          title='Top Companies Hiring',
# # # #                          color='Jobs', color_continuous_scale='Viridis', text='Jobs')
# # # #             fig.update_layout(height=400, showlegend=False,
# # # #                               yaxis=dict(autorange="reversed"),
# # # #                               title_font_size=13)
# # # #             fig.update_traces(textposition='outside')
# # # #             st.plotly_chart(fig, use_container_width=True, key="search_companies")

# # # #         c3, c4 = st.columns(2)

# # # #         with c3:
# # # #             lc = search_results['location'].value_counts().head(10).reset_index()
# # # #             lc.columns = ['Location', 'Jobs']
# # # #             fig = px.bar(lc, x='Jobs', y='Location', orientation='h',
# # # #                          title='Top Locations',
# # # #                          color='Jobs', color_continuous_scale='Magma', text='Jobs')
# # # #             fig.update_layout(height=400, showlegend=False,
# # # #                               yaxis=dict(autorange="reversed"),
# # # #                               title_font_size=13)
# # # #             fig.update_traces(textposition='outside')
# # # #             st.plotly_chart(fig, use_container_width=True, key="search_locations")

# # # #         with c4:
# # # #             all_sk = [s for skills in search_results['skills'] for s in skills]
# # # #             sk_counts = Counter(all_sk).most_common(10)
# # # #             if sk_counts:
# # # #                 sk_df = pd.DataFrame(sk_counts, columns=['Skill', 'Jobs'])
# # # #                 fig = px.bar(sk_df, x='Jobs', y='Skill', orientation='h',
# # # #                              title='Top Skills Required',
# # # #                              color='Jobs', color_continuous_scale='RdYlGn', text='Jobs')
# # # #                 fig.update_layout(height=400, showlegend=False,
# # # #                                   yaxis=dict(autorange="reversed"),
# # # #                                   title_font_size=13)
# # # #                 fig.update_traces(textposition='outside')
# # # #                 st.plotly_chart(fig, use_container_width=True, key="search_skills")

# # # #         # ---- Full Table ----
# # # #         st.markdown(f"### 📋 All {len(search_results)} Matching Jobs")

# # # #         show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # # #                      'employment_type', 'posted_date']
# # # #         display_df = search_results[show_cols].copy()
# # # #         display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # #                               'Remote', 'Type', 'Posted']
# # # #         st.dataframe(display_df, use_container_width=True, height=500)

# # # #         # ---- Download ----
# # # #         csv = search_results.to_csv(index=False)
# # # #         st.download_button(
# # # #             label=f"📥 Download {len(search_results)} Jobs (CSV)",
# # # #             data=csv,
# # # #             file_name=f"search_{st.session_state.search_query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
# # # #             mime="text/csv",
# # # #             key="dl_search"
# # # #         )

# # # #         # ---- Insight ----
# # # #         top_comp = search_results['company'].value_counts().index[0]
# # # #         top_portal = search_results['platform'].value_counts().index[0]
# # # #         top_loc = search_results['location'].value_counts().index[0]

# # # #         st.markdown(f"""<div class="insight-box">
# # # #             <strong>📊 Search Summary for "{st.session_state.search_query}":</strong><br>
# # # #             🎯 <strong>Matching Jobs:</strong> {len(search_results)}<br>
# # # #             🏢 <strong>Top Company:</strong> {top_comp}<br>
# # # #             🌐 <strong>Top Portal:</strong> {top_portal}<br>
# # # #             📍 <strong>Top Location:</strong> {top_loc}<br>
# # # #             🛠️ <strong>Top Skill:</strong> {sk_counts[0][0] if sk_counts else 'N/A'}
# # # #         </div>""", unsafe_allow_html=True)

# # # #     st.markdown("---")

# # # # # ============================================================================
# # # # # KPI CARDS (shown when NOT in search results)
# # # # # ============================================================================
# # # # if st.session_state.view != "Search Results":
# # # #     st.markdown("## 📈 Overview — Click to Explore")
# # # #     k1, k2, k3, k4, k5, k6 = st.columns(6)

# # # #     with k1:
# # # #         if st.button(f"📊\n\n**Total Jobs**\n\n{len(df)}\n\n_in dataset_",
# # # #                      key="kpi_total", use_container_width=True):
# # # #             st.session_state.view = "Total Jobs"
# # # #             st.session_state.drill_type = None
# # # #             st.rerun()

# # # #     with k2:
# # # #         if st.button(f"🏢\n\n**Companies**\n\n{df['company'].nunique()}\n\n_hiring_",
# # # #                      key="kpi_company", use_container_width=True):
# # # #             st.session_state.view = "Companies"
# # # #             st.session_state.drill_type = None
# # # #             st.rerun()

# # # #     with k3:
# # # #         if st.button(f"💼\n\n**Job Roles**\n\n{df['title'].nunique()}\n\n_unique_",
# # # #                      key="kpi_title", use_container_width=True):
# # # #             st.session_state.view = "Job Roles"
# # # #             st.session_state.drill_type = None
# # # #             st.rerun()

# # # #     with k4:
# # # #         if st.button(f"🌐\n\n**Portals**\n\n{df['platform'].nunique()}\n\n_sources_",
# # # #                      key="kpi_portal", use_container_width=True):
# # # #             st.session_state.view = "Portals"
# # # #             st.session_state.drill_type = None
# # # #             st.rerun()

# # # #     with k5:
# # # #         if st.button(f"📍\n\n**Locations**\n\n{df['location'].nunique()}\n\n_cities_",
# # # #                      key="kpi_location", use_container_width=True):
# # # #             st.session_state.view = "Locations"
# # # #             st.session_state.drill_type = None
# # # #             st.rerun()

# # # #     with k6:
# # # #         remote_count = (df['is_remote'] == 'Yes').sum()
# # # #         if st.button(f"🏠\n\n**Remote Jobs**\n\n{remote_count}\n\n_of {len(df)}_",
# # # #                      key="kpi_remote", use_container_width=True):
# # # #             st.session_state.view = "Remote Jobs"
# # # #             st.session_state.drill_type = None
# # # #             st.rerun()

# # # #     st.markdown("---")

# # # # # ============================================================================
# # # # # VIEW: REMOTE JOBS
# # # # # ============================================================================
# # # # if st.session_state.view == "Remote Jobs":
# # # #     st.markdown('<div class="drill-header">🏠 Remote Jobs — Complete Breakdown</div>', unsafe_allow_html=True)
# # # #     remote_df = df[df['is_remote'] == 'Yes']

# # # #     if len(remote_df) == 0:
# # # #         st.warning("No remote jobs found.")
# # # #     else:
# # # #         d1, d2, d3, d4, d5 = st.columns(5)
# # # #         with d1: st.metric("🏠 Total Remote", len(remote_df))
# # # #         with d2: st.metric("🏢 Companies", remote_df['company'].nunique())
# # # #         with d3: st.metric("📍 Locations", remote_df['location'].nunique())
# # # #         with d4: st.metric("💼 Roles", remote_df['title'].nunique())
# # # #         with d5: st.metric("🌐 Portals", remote_df['platform'].nunique())

# # # #         st.markdown("---")

# # # #         c1, c2 = st.columns([3, 2])
# # # #         with c1:
# # # #             rc = remote_df['company'].value_counts().reset_index()
# # # #             rc.columns = ['Company', 'Remote Jobs']
# # # #             fig = px.bar(rc, x='Remote Jobs', y='Company', orientation='h',
# # # #                          title=f'Companies Hiring Remote ({len(rc)} total)',
# # # #                          color='Remote Jobs', color_continuous_scale='Greens',
# # # #                          text='Remote Jobs')
# # # #             fig.update_layout(height=max(400, len(rc)*35), showlegend=False,
# # # #                               yaxis=dict(autorange="reversed"), title_font_size=13)
# # # #             fig.update_traces(textposition='outside')
# # # #             st.plotly_chart(fig, use_container_width=True, key="rem_companies")

# # # #         with c2:
# # # #             st.markdown("#### 📋 Company List")
# # # #             st.dataframe(rc, use_container_width=True, height=400, hide_index=True)

# # # #         c3, c4 = st.columns([3, 2])
# # # #         with c3:
# # # #             rl = remote_df['location'].value_counts().reset_index()
# # # #             rl.columns = ['Location', 'Remote Jobs']
# # # #             fig = px.bar(rl, x='Remote Jobs', y='Location', orientation='h',
# # # #                          title='Remote Jobs by Location',
# # # #                          color='Remote Jobs', color_continuous_scale='Teal',
# # # #                          text='Remote Jobs')
# # # #             fig.update_layout(height=max(400, len(rl)*35), showlegend=False,
# # # #                               yaxis=dict(autorange="reversed"), title_font_size=13)
# # # #             fig.update_traces(textposition='outside')
# # # #             st.plotly_chart(fig, use_container_width=True, key="rem_locations")

# # # #         with c4:
# # # #             st.markdown("#### 📋 Location List")
# # # #             st.dataframe(rl, use_container_width=True, height=400, hide_index=True)

# # # #         c5, c6 = st.columns(2)
# # # #         with c5:
# # # #             rp = remote_df['platform'].value_counts().reset_index()
# # # #             rp.columns = ['Portal', 'Remote Jobs']
# # # #             fig = px.bar(rp, x='Portal', y='Remote Jobs',
# # # #                          title='Remote Jobs by Portal',
# # # #                          color='Remote Jobs', color_continuous_scale='Blues',
# # # #                          text='Remote Jobs')
# # # #             fig.update_layout(height=400, showlegend=False,
# # # #                               xaxis_tickangle=-30, title_font_size=13)
# # # #             fig.update_traces(textposition='outside')
# # # #             st.plotly_chart(fig, use_container_width=True, key="rem_portals")

# # # #         with c6:
# # # #             fig = px.pie(rp, values='Remote Jobs', names='Portal',
# # # #                          title='Portal Share (Remote)', hole=0.4,
# # # #                          color_discrete_sequence=px.colors.qualitative.Set3)
# # # #             fig.update_traces(textinfo='percent+label', textposition='outside',
# # # #                               textfont_size=11, pull=[0.03] * len(rp))
# # # #             fig.update_layout(height=400, title_font_size=13)
# # # #             st.plotly_chart(fig, use_container_width=True, key="rem_pie")

# # # #         # Skills
# # # #         st.markdown("### 🛠️ Top Skills for Remote Jobs")
# # # #         all_rs = [s for skills in remote_df['skills'] for s in skills]
# # # #         rs = Counter(all_rs).most_common(15)
# # # #         if rs:
# # # #             rs_df = pd.DataFrame(rs, columns=['Skill', 'Jobs'])
# # # #             fig = px.bar(rs_df, x='Jobs', y='Skill', orientation='h',
# # # #                          title='Top Skills (Remote)', color='Jobs',
# # # #                          color_continuous_scale='Greens', text='Jobs')
# # # #             fig.update_layout(height=500, showlegend=False,
# # # #                               yaxis=dict(autorange="reversed"), title_font_size=13)
# # # #             fig.update_traces(textposition='outside')
# # # #             st.plotly_chart(fig, use_container_width=True, key="rem_skills")

# # # #         # Full list
# # # #         st.markdown("### 📋 All Remote Jobs")
# # # #         show_cols = ['title', 'company', 'location', 'platform',
# # # #                      'employment_type', 'posted_date']
# # # #         display_remote = remote_df[show_cols].copy()
# # # #         display_remote.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # #                                   'Type', 'Posted']
# # # #         st.dataframe(display_remote, use_container_width=True, height=500)

# # # #         csv = remote_df.to_csv(index=False)
# # # #         st.download_button("📥 Download All Remote Jobs (CSV)", csv,
# # # #                            file_name=f"remote_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
# # # #                            mime="text/csv", key="dl_remote_all")

# # # # # ============================================================================
# # # # # OTHER VIEWS
# # # # # ============================================================================
# # # # elif st.session_state.view == "Companies":
# # # #     st.markdown('<div class="drill-header">🏢 All Companies Hiring</div>', unsafe_allow_html=True)
# # # #     comp_df = df['company'].value_counts().reset_index()
# # # #     comp_df.columns = ['Company', 'Openings']
# # # #     comp_df['Share %'] = (comp_df['Openings'] / len(df) * 100).round(2)

# # # #     c1, c2 = st.columns([3, 2])
# # # #     with c1:
# # # #         fig = px.bar(comp_df.head(30), x='Openings', y='Company', orientation='h',
# # # #                      title=f'All {len(comp_df)} Companies (Top 30)',
# # # #                      color='Openings', color_continuous_scale='Viridis', text='Openings')
# # # #         fig.update_layout(height=800, showlegend=False,
# # # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # # #         fig.update_traces(textposition='outside')
# # # #         st.plotly_chart(fig, use_container_width=True, key="all_comp")
# # # #     with c2:
# # # #         st.dataframe(comp_df, use_container_width=True, height=750, hide_index=True)
# # # #     csv = comp_df.to_csv(index=False)
# # # #     st.download_button("📥 Download CSV", csv,
# # # #                        file_name=f"companies_{datetime.now().strftime('%Y%m%d')}.csv",
# # # #                        mime="text/csv", key="dl_comp")

# # # # elif st.session_state.view == "Locations":
# # # #     st.markdown('<div class="drill-header">📍 All Locations</div>', unsafe_allow_html=True)
# # # #     loc_df = df['location'].value_counts().reset_index()
# # # #     loc_df.columns = ['Location', 'Openings']

# # # #     c1, c2 = st.columns([3, 2])
# # # #     with c1:
# # # #         fig = px.bar(loc_df, x='Openings', y='Location', orientation='h',
# # # #                      title=f'All {len(loc_df)} Locations',
# # # #                      color='Openings', color_continuous_scale='Magma', text='Openings')
# # # #         fig.update_layout(height=max(600, len(loc_df)*22), showlegend=False,
# # # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # # #         fig.update_traces(textposition='outside')
# # # #         st.plotly_chart(fig, use_container_width=True, key="all_loc")
# # # #     with c2:
# # # #         st.dataframe(loc_df, use_container_width=True, height=750, hide_index=True)
# # # #     csv = loc_df.to_csv(index=False)
# # # #     st.download_button("📥 Download CSV", csv,
# # # #                        file_name=f"locations_{datetime.now().strftime('%Y%m%d')}.csv",
# # # #                        mime="text/csv", key="dl_loc")

# # # # elif st.session_state.view == "Job Roles":
# # # #     st.markdown('<div class="drill-header">💼 All Job Roles</div>', unsafe_allow_html=True)
# # # #     role_df = df['title'].value_counts().reset_index()
# # # #     role_df.columns = ['Job Role', 'Openings']

# # # #     c1, c2 = st.columns([3, 2])
# # # #     with c1:
# # # #         fig = px.bar(role_df.head(40), x='Openings', y='Job Role', orientation='h',
# # # #                      title=f'All {len(role_df)} Roles (Top 40)',
# # # #                      color='Openings', color_continuous_scale='Plasma', text='Openings')
# # # #         fig.update_layout(height=1000, showlegend=False,
# # # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # # #         fig.update_traces(textposition='outside')
# # # #         st.plotly_chart(fig, use_container_width=True, key="all_role")
# # # #     with c2:
# # # #         st.dataframe(role_df, use_container_width=True, height=950, hide_index=True)
# # # #     csv = role_df.to_csv(index=False)
# # # #     st.download_button("📥 Download CSV", csv,
# # # #                        file_name=f"roles_{datetime.now().strftime('%Y%m%d')}.csv",
# # # #                        mime="text/csv", key="dl_role")

# # # # elif st.session_state.view == "Portals":
# # # #     st.markdown('<div class="drill-header">🌐 All Portals</div>', unsafe_allow_html=True)
# # # #     portal_df = df['platform'].value_counts().reset_index()
# # # #     portal_df.columns = ['Portal', 'Openings']

# # # #     c1, c2 = st.columns(2)
# # # #     with c1:
# # # #         fig = px.bar(portal_df, x='Portal', y='Openings',
# # # #                      title='Portals', color='Openings',
# # # #                      color_continuous_scale='Turbo', text='Openings')
# # # #         fig.update_layout(height=450, showlegend=False,
# # # #                           xaxis_tickangle=-30, title_font_size=13)
# # # #         fig.update_traces(textposition='outside')
# # # #         st.plotly_chart(fig, use_container_width=True, key="all_portal")
# # # #     with c2:
# # # #         st.dataframe(portal_df, use_container_width=True, hide_index=True)
# # # #     csv = portal_df.to_csv(index=False)
# # # #     st.download_button("📥 Download CSV", csv,
# # # #                        file_name=f"portals_{datetime.now().strftime('%Y%m%d')}.csv",
# # # #                        mime="text/csv", key="dl_portal")

# # # # elif st.session_state.view == "Total Jobs":
# # # #     st.markdown('<div class="drill-header">📊 All Jobs in Dataset</div>', unsafe_allow_html=True)
# # # #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # # #                  'employment_type', 'posted_date']
# # # #     display_df = df[show_cols].copy()
# # # #     display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # #                           'Remote', 'Type', 'Posted']
# # # #     st.dataframe(display_df, use_container_width=True, height=600)
# # # #     csv = df.to_csv(index=False)
# # # #     st.download_button("📥 Download All Jobs (CSV)", csv,
# # # #                        file_name=f"all_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
# # # #                        mime="text/csv", key="dl_total")

# # # # # ============================================================================
# # # # # DRILL-DOWN PANEL
# # # # # ============================================================================
# # # # if st.session_state.drill_type and st.session_state.drill_value:
# # # #     st.markdown("---")
# # # #     dv = st.session_state.drill_value
# # # #     dt = st.session_state.drill_type
# # # #     st.markdown(f'<div class="drill-header">🎯 Drill-Down: {dt} = "{dv}"</div>', unsafe_allow_html=True)

# # # #     if dt == "Skill":
# # # #         ddf = df[df['skills'].apply(lambda x: dv in x)]
# # # #     elif dt == "Job Role":
# # # #         ddf = df[df['title'] == dv]
# # # #     elif dt == "Company":
# # # #         ddf = df[df['company'] == dv]
# # # #     elif dt == "Location":
# # # #         ddf = df[df['location'] == dv]
# # # #     elif dt == "Portal":
# # # #         ddf = df[df['platform'] == dv]
# # # #     else:
# # # #         ddf = df.copy()

# # # #     d1, d2, d3, d4 = st.columns(4)
# # # #     with d1: st.metric("🎯 Openings", len(ddf))
# # # #     with d2: st.metric("🏢 Companies", ddf['company'].nunique())
# # # #     with d3: st.metric("📍 Locations", ddf['location'].nunique())
# # # #     with d4:
# # # #         rp = (ddf['is_remote'] == 'Yes').sum() / len(ddf) * 100 if len(ddf) > 0 else 0
# # # #         st.metric("🏠 Remote %", f"{rp:.1f}%")

# # # #     g1, g2 = st.columns(2)
# # # #     with g1:
# # # #         pc = ddf['platform'].value_counts().reset_index()
# # # #         pc.columns = ['Portal', 'Openings']
# # # #         fig = px.bar(pc, x='Openings', y='Portal', orientation='h',
# # # #                      title='By Portal', color='Openings',
# # # #                      color_continuous_scale='Blues', text='Openings')
# # # #         fig.update_layout(height=350, showlegend=False,
# # # #                           yaxis=dict(autorange="reversed"))
# # # #         fig.update_traces(textposition='outside')
# # # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_p_{dv}")
# # # #     with g2:
# # # #         cc = ddf['company'].value_counts().head(10).reset_index()
# # # #         cc.columns = ['Company', 'Openings']
# # # #         fig = px.bar(cc, x='Openings', y='Company', orientation='h',
# # # #                      title='By Company', color='Openings',
# # # #                      color_continuous_scale='Viridis', text='Openings')
# # # #         fig.update_layout(height=350, showlegend=False,
# # # #                           yaxis=dict(autorange="reversed"))
# # # #         fig.update_traces(textposition='outside')
# # # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_c_{dv}")

# # # #     st.markdown("### 📋 All Job Openings")
# # # #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # # #                  'employment_type', 'posted_date']
# # # #     disp = ddf[show_cols].copy()
# # # #     disp.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # # #                     'Remote', 'Type', 'Posted']
# # # #     st.dataframe(disp, use_container_width=True, height=400)

# # # #     csv = ddf.to_csv(index=False)
# # # #     st.download_button("📥 Download (CSV)", csv,
# # # #                        file_name=f"drill_{dt}_{dv}.csv",
# # # #                        mime="text/csv", key=f"dl_dd_{dv}")

# # # # # ============================================================================
# # # # # FOOTER
# # # # # ============================================================================
# # # # st.markdown("---")
# # # # st.markdown(f"""<div style='text-align:center; color:#666; font-size:12px;'>
# # # #     Job Market Analytics | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
# # # #     {len(df)} total jobs | {(df['is_remote']=='Yes').sum()} remote
# # # # </div>""", unsafe_allow_html=True)








# # # """
# # # ================================================================================
# # # JOB MARKET ANALYTICS — WITH LIVE SEARCH
# # # Type any keyword → see all matching openings instantly
# # # Tech Stack: Python | Pandas | NumPy | Plotly | Streamlit
# # # Run: python -m streamlit run dashboard.py
# # # ================================================================================
# # # """

# # # import streamlit as st
# # # import pandas as pd
# # # import numpy as np
# # # import plotly.express as px
# # # import plotly.graph_objects as go
# # # from collections import Counter
# # # from datetime import datetime
# # # import warnings
# # # import logging

# # # warnings.filterwarnings('ignore')
# # # logging.getLogger('streamlit').setLevel(logging.ERROR)

# # # # ============================================================================
# # # # PAGE CONFIG
# # # # ============================================================================
# # # st.set_page_config(
# # #     page_title="Job Market Analytics",
# # #     page_icon="🎯",
# # #     layout="wide",
# # #     initial_sidebar_state="expanded"
# # # )

# # # # CSS
# # # st.markdown("""
# # # <style>
    /* ========== FORCE DARK TEXT EVERYWHERE ========== */
    .stApp, .stApp * {
        color: #1a1a1a !important;
    }
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricLabel"] > div {
        color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stDataFrame"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
    }
# # #     div[data-testid="stMarkdownContainer"] div,
# # #     div[data-testid="stMarkdownContainer"] p,
# # #     div[data-testid="stMarkdownContainer"] span,
# # #     div[data-testid="stMarkdownContainer"] strong { color: #1a1a1a; }

# # #     .main-header {
# # #         font-size: 2.2rem; font-weight: bold;
# # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # #         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
# # #         text-align: center; padding: 0.5rem 0;
# # #     }
# # #     .sub-header { text-align: center; color: #666; margin-bottom: 1rem; }
# # #     .problem-header {
# # #         background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
# # #         padding: 0.7rem 1rem; border-radius: 8px;
# # #         color: #FFFFFF !important; font-weight: bold;
# # #         margin-bottom: 1rem; font-size: 1rem;
# # #     }
# # #     .insight-box {
# # #         background: #f0f7ff; padding: 0.8rem;
# # #         border-left: 4px solid #667eea; border-radius: 5px;
# # #         margin: 0.6rem 0; font-size: 0.9rem; color: #1a1a1a !important;
# # #     }
# # #     .insight-box strong { color: #2c3e50 !important; font-weight: 700; }
# # #     .drill-header {
# # #         background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
# # #         padding: 0.8rem 1rem; border-radius: 8px;
# # #         color: #1a1a1a !important; font-weight: bold;
# # #         margin: 1rem 0; font-size: 1.1rem;
# # #         border: 2px solid #43e97b;
# # #     }
# # #     .search-header {
# # #         background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
# # #         padding: 1rem 1.2rem; border-radius: 10px;
# # #         color: #1a1a1a !important; font-weight: bold;
# # #         margin: 1rem 0; font-size: 1.15rem;
# # #         border: 2px solid #4facfe;
# # #     }
# # #     .stTabs [data-baseweb="tab-list"] { gap: 6px; flex-wrap: wrap; }
# # #     .stTabs [data-baseweb="tab"] {
# # #         background-color: #f0f2f6; border-radius: 6px;
# # #         padding: 8px 12px; font-weight: 600; font-size: 0.78rem;
# # #     }
# # #     .stTabs [aria-selected="true"] {
# # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # #         color: #FFFFFF !important;
# # #     }
# # #     div[data-testid="stButton"] button {
# # #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# # #         color: white !important; border: none;
# # #         padding: 1.5rem 1rem; border-radius: 12px;
# # #         width: 100%; min-height: 120px;
# # #         font-size: 1rem; font-weight: bold;
# # #         box-shadow: 0 4px 12px rgba(0,0,0,0.1);
# # #         transition: transform 0.2s;
# # #     }
# # #     div[data-testid="stButton"] button:hover {
# # #         transform: translateY(-3px);
# # #         box-shadow: 0 6px 16px rgba(0,0,0,0.2);
# # #     }
# # #     div[data-testid="stButton"] button p {
# # #         color: white !important; font-size: 1rem; font-weight: bold;
# # #     }
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # ============================================================================
# # # # DATA LOADING
# # # # ============================================================================

# # # @st.cache_data
# # # def load_data():
# # #     df = pd.read_csv("job_data_clean.csv")
# # #     df['posted_date'] = pd.to_datetime(df['posted_date'], errors='coerce')
# # #     return df

# # # def extract_skills(text):
# # #     if pd.isna(text):
# # #         return []
# # #     text = str(text).lower()
# # #     skill_list = [
# # #         'python', 'java', 'sql', 'javascript', 'typescript', 'react', 'angular',
# # #         'node.js', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
# # #         'jenkins', 'spark', 'kafka', 'airflow', 'snowflake', 'tableau', 'power bi',
# # #         'machine learning', 'deep learning', 'nlp', 'llm', 'genai', 'rag',
# # #         'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
# # #         'excel', 'git', 'linux', 'agile', 'scrum', 'jira'
# # #     ]
# # #     return list(set([s for s in skill_list if s in text]))

# # # try:
# # #     df = load_data()
# # #     df['skills'] = df['description'].apply(extract_skills)
# # #     df['skill_count'] = df['skills'].apply(len)
# # #     # Build a searchable text column (title + company + location + description)
# # #     df['search_text'] = (
# # #         df['title'].fillna('') + ' ' +
# # #         df['company'].fillna('') + ' ' +
# # #         df['location'].fillna('') + ' ' +
# # #         df['description'].fillna('')
# # #     ).str.lower()
# # # except Exception as e:
# # #     st.error(f"❌ Error loading 'job_data_clean.csv': {e}")
# # #     st.stop()

# # # # ============================================================================
# # # # HEADER
# # # # ============================================================================
# # # st.markdown('<h1 class="main-header">🎯 Job Market Analytics</h1>', unsafe_allow_html=True)
# # # st.markdown('<p class="sub-header">🔍 Search any keyword • 🎯 Click KPI cards • 📊 Click charts to drill down</p>', unsafe_allow_html=True)

# # # # ============================================================================
# # # # SESSION STATE
# # # # ============================================================================
# # # for key in ['view', 'drill_type', 'drill_value', 'search_query']:
# # #     if key not in st.session_state:
# # #         st.session_state[key] = None

# # # # ============================================================================
# # # # SEARCH BAR (THE STAR FEATURE)
# # # # ============================================================================
# # # st.markdown("### 🔍 Search Job Openings")
# # # search_col1, search_col2, search_col3 = st.columns([4, 1, 1])

# # # with search_col1:
# # #     search_query = st.text_input(
# # #         "Type any keyword (e.g., data analyst, python, remote, bangalore):",
# # #         value=st.session_state.search_query if st.session_state.search_query else "",
# # #         placeholder="🔍 Try: data analyst, python, mastercard, remote, bangalore...",
# # #         key="search_input",
# # #         label_visibility="collapsed"
# # #     )

# # # with search_col2:
# # #     if st.button("🔍 Search", use_container_width=True, key="search_btn"):
# # #         st.session_state.search_query = search_query
# # #         st.session_state.view = "Search Results"
# # #         st.session_state.drill_type = None
# # #         st.rerun()

# # # with search_col3:
# # #     if st.button("❌ Clear", use_container_width=True, key="clear_search"):
# # #         st.session_state.search_query = None
# # #         st.session_state.view = None
# # #         st.rerun()

# # # # Quick search suggestion chips
# # # st.markdown("**Popular searches:**")
# # # chip_cols = st.columns(8)
# # # quick_searches = ["data analyst", "data scientist", "python", "remote", "mastercard", "bangalore", "sql", "engineer"]
# # # for i, term in enumerate(quick_searches):
# # #     with chip_cols[i]:
# # #         if st.button(f"🔎 {term}", key=f"quick_{term}", use_container_width=True):
# # #             st.session_state.search_query = term
# # #             st.session_state.view = "Search Results"
# # #             st.session_state.drill_type = None
# # #             st.rerun()

# # # # Auto-search when user types
# # # if search_query and search_query != st.session_state.search_query and search_query.strip():
# # #     st.session_state.search_query = search_query
# # #     st.session_state.view = "Search Results"
# # #     st.session_state.drill_type = None

# # # # ============================================================================
# # # # SEARCH RESULTS VIEW
# # # # ============================================================================
# # # if st.session_state.view == "Search Results" and st.session_state.search_query:
# # #     query = st.session_state.search_query.strip().lower()

# # #     # Filter using search_text
# # #     search_results = df[df['search_text'].str.contains(query, na=False, regex=False)]

# # #     st.markdown(f'<div class="search-header">🔍 Search Results for: "{st.session_state.search_query}" — {len(search_results)} jobs found</div>', unsafe_allow_html=True)

# # #     if len(search_results) == 0:
# # #         st.warning(f"❌ No jobs found matching **'{st.session_state.search_query}'**. Try another keyword.")
# # #     else:
# # #         # ---- KPI Cards for search ----
# # #         s1, s2, s3, s4, s5 = st.columns(5)
# # #         with s1:
# # #             st.metric("🎯 Matching Jobs", len(search_results))
# # #         with s2:
# # #             st.metric("🏢 Companies", search_results['company'].nunique())
# # #         with s3:
# # #             st.metric("📍 Locations", search_results['location'].nunique())
# # #         with s4:
# # #             st.metric("🌐 Portals", search_results['platform'].nunique())
# # #         with s5:
# # #             rp = (search_results['is_remote'] == 'Yes').sum() / len(search_results) * 100
# # #             st.metric("🏠 Remote %", f"{rp:.1f}%")

# # #         st.markdown("---")

# # #         # ---- Charts for search results ----
# # #         c1, c2 = st.columns(2)

# # #         with c1:
# # #             pc = search_results['platform'].value_counts().reset_index()
# # #             pc.columns = ['Portal', 'Jobs']
# # #             fig = px.bar(pc, x='Jobs', y='Portal', orientation='h',
# # #                          title='Where These Jobs Are Posted',
# # #                          color='Jobs', color_continuous_scale='Blues', text='Jobs')
# # #             fig.update_layout(height=400, showlegend=False,
# # #                               yaxis=dict(autorange="reversed"),
# # #                               title_font_size=13)
# # #             fig.update_traces(textposition='outside')
# # #             st.plotly_chart(fig, use_container_width=True, key="search_portals")

# # #         with c2:
# # #             cc = search_results['company'].value_counts().head(10).reset_index()
# # #             cc.columns = ['Company', 'Jobs']
# # #             fig = px.bar(cc, x='Jobs', y='Company', orientation='h',
# # #                          title='Top Companies Hiring',
# # #                          color='Jobs', color_continuous_scale='Viridis', text='Jobs')
# # #             fig.update_layout(height=400, showlegend=False,
# # #                               yaxis=dict(autorange="reversed"),
# # #                               title_font_size=13)
# # #             fig.update_traces(textposition='outside')
# # #             st.plotly_chart(fig, use_container_width=True, key="search_companies")

# # #         c3, c4 = st.columns(2)

# # #         with c3:
# # #             lc = search_results['location'].value_counts().head(10).reset_index()
# # #             lc.columns = ['Location', 'Jobs']
# # #             fig = px.bar(lc, x='Jobs', y='Location', orientation='h',
# # #                          title='Top Locations',
# # #                          color='Jobs', color_continuous_scale='Magma', text='Jobs')
# # #             fig.update_layout(height=400, showlegend=False,
# # #                               yaxis=dict(autorange="reversed"),
# # #                               title_font_size=13)
# # #             fig.update_traces(textposition='outside')
# # #             st.plotly_chart(fig, use_container_width=True, key="search_locations")

# # #         with c4:
# # #             all_sk = [s for skills in search_results['skills'] for s in skills]
# # #             sk_counts = Counter(all_sk).most_common(10)
# # #             if sk_counts:
# # #                 sk_df = pd.DataFrame(sk_counts, columns=['Skill', 'Jobs'])
# # #                 fig = px.bar(sk_df, x='Jobs', y='Skill', orientation='h',
# # #                              title='Top Skills Required',
# # #                              color='Jobs', color_continuous_scale='RdYlGn', text='Jobs')
# # #                 fig.update_layout(height=400, showlegend=False,
# # #                                   yaxis=dict(autorange="reversed"),
# # #                                   title_font_size=13)
# # #                 fig.update_traces(textposition='outside')
# # #                 st.plotly_chart(fig, use_container_width=True, key="search_skills")

# # #         # ---- Full Table ----
# # #         st.markdown(f"### 📋 All {len(search_results)} Matching Jobs")

# # #         show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # #                      'employment_type', 'posted_date']
# # #         display_df = search_results[show_cols].copy()
# # #         display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # #                               'Remote', 'Type', 'Posted']
# # #         st.dataframe(display_df, use_container_width=True, height=500)

# # #         # ---- Download ----
# # #         csv = search_results.to_csv(index=False)
# # #         st.download_button(
# # #             label=f"📥 Download {len(search_results)} Jobs (CSV)",
# # #             data=csv,
# # #             file_name=f"search_{st.session_state.search_query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
# # #             mime="text/csv",
# # #             key="dl_search"
# # #         )

# # #         # ---- Insight ----
# # #         top_comp = search_results['company'].value_counts().index[0]
# # #         top_portal = search_results['platform'].value_counts().index[0]
# # #         top_loc = search_results['location'].value_counts().index[0]

# # #         st.markdown(f"""<div class="insight-box">
# # #             <strong>📊 Search Summary for "{st.session_state.search_query}":</strong><br>
# # #             🎯 <strong>Matching Jobs:</strong> {len(search_results)}<br>
# # #             🏢 <strong>Top Company:</strong> {top_comp}<br>
# # #             🌐 <strong>Top Portal:</strong> {top_portal}<br>
# # #             📍 <strong>Top Location:</strong> {top_loc}<br>
# # #             🛠️ <strong>Top Skill:</strong> {sk_counts[0][0] if sk_counts else 'N/A'}
# # #         </div>""", unsafe_allow_html=True)

# # #     st.markdown("---")

# # # # ============================================================================
# # # # KPI CARDS (shown when NOT in search results)
# # # # ============================================================================
# # # if st.session_state.view != "Search Results":
# # #     st.markdown("## 📈 Overview — Click to Explore")
# # #     k1, k2, k3, k4, k5, k6 = st.columns(6)

# # #     with k1:
# # #         if st.button(f"📊\n\n**Total Jobs**\n\n{len(df)}\n\n_in dataset_",
# # #                      key="kpi_total", use_container_width=True):
# # #             st.session_state.view = "Total Jobs"
# # #             st.session_state.drill_type = None
# # #             st.rerun()

# # #     with k2:
# # #         if st.button(f"🏢\n\n**Companies**\n\n{df['company'].nunique()}\n\n_hiring_",
# # #                      key="kpi_company", use_container_width=True):
# # #             st.session_state.view = "Companies"
# # #             st.session_state.drill_type = None
# # #             st.rerun()

# # #     with k3:
# # #         if st.button(f"💼\n\n**Job Roles**\n\n{df['title'].nunique()}\n\n_unique_",
# # #                      key="kpi_title", use_container_width=True):
# # #             st.session_state.view = "Job Roles"
# # #             st.session_state.drill_type = None
# # #             st.rerun()

# # #     with k4:
# # #         if st.button(f"🌐\n\n**Portals**\n\n{df['platform'].nunique()}\n\n_sources_",
# # #                      key="kpi_portal", use_container_width=True):
# # #             st.session_state.view = "Portals"
# # #             st.session_state.drill_type = None
# # #             st.rerun()

# # #     with k5:
# # #         if st.button(f"📍\n\n**Locations**\n\n{df['location'].nunique()}\n\n_cities_",
# # #                      key="kpi_location", use_container_width=True):
# # #             st.session_state.view = "Locations"
# # #             st.session_state.drill_type = None
# # #             st.rerun()

# # #     with k6:
# # #         remote_count = (df['is_remote'] == 'Yes').sum()
# # #         if st.button(f"🏠\n\n**Remote Jobs**\n\n{remote_count}\n\n_of {len(df)}_",
# # #                      key="kpi_remote", use_container_width=True):
# # #             st.session_state.view = "Remote Jobs"
# # #             st.session_state.drill_type = None
# # #             st.rerun()

# # #     st.markdown("---")

# # # # ============================================================================
# # # # VIEW: REMOTE JOBS
# # # # ============================================================================
# # # if st.session_state.view == "Remote Jobs":
# # #     st.markdown('<div class="drill-header">🏠 Remote Jobs — Complete Breakdown</div>', unsafe_allow_html=True)
# # #     remote_df = df[df['is_remote'] == 'Yes']

# # #     if len(remote_df) == 0:
# # #         st.warning("No remote jobs found.")
# # #     else:
# # #         d1, d2, d3, d4, d5 = st.columns(5)
# # #         with d1: st.metric("🏠 Total Remote", len(remote_df))
# # #         with d2: st.metric("🏢 Companies", remote_df['company'].nunique())
# # #         with d3: st.metric("📍 Locations", remote_df['location'].nunique())
# # #         with d4: st.metric("💼 Roles", remote_df['title'].nunique())
# # #         with d5: st.metric("🌐 Portals", remote_df['platform'].nunique())

# # #         st.markdown("---")

# # #         c1, c2 = st.columns([3, 2])
# # #         with c1:
# # #             rc = remote_df['company'].value_counts().reset_index()
# # #             rc.columns = ['Company', 'Remote Jobs']
# # #             fig = px.bar(rc, x='Remote Jobs', y='Company', orientation='h',
# # #                          title=f'Companies Hiring Remote ({len(rc)} total)',
# # #                          color='Remote Jobs', color_continuous_scale='Greens',
# # #                          text='Remote Jobs')
# # #             fig.update_layout(height=max(400, len(rc)*35), showlegend=False,
# # #                               yaxis=dict(autorange="reversed"), title_font_size=13)
# # #             fig.update_traces(textposition='outside')
# # #             st.plotly_chart(fig, use_container_width=True, key="rem_companies")

# # #         with c2:
# # #             st.markdown("#### 📋 Company List")
# # #             st.dataframe(rc, use_container_width=True, height=400, hide_index=True)

# # #         c3, c4 = st.columns([3, 2])
# # #         with c3:
# # #             rl = remote_df['location'].value_counts().reset_index()
# # #             rl.columns = ['Location', 'Remote Jobs']
# # #             fig = px.bar(rl, x='Remote Jobs', y='Location', orientation='h',
# # #                          title='Remote Jobs by Location',
# # #                          color='Remote Jobs', color_continuous_scale='Teal',
# # #                          text='Remote Jobs')
# # #             fig.update_layout(height=max(400, len(rl)*35), showlegend=False,
# # #                               yaxis=dict(autorange="reversed"), title_font_size=13)
# # #             fig.update_traces(textposition='outside')
# # #             st.plotly_chart(fig, use_container_width=True, key="rem_locations")

# # #         with c4:
# # #             st.markdown("#### 📋 Location List")
# # #             st.dataframe(rl, use_container_width=True, height=400, hide_index=True)

# # #         c5, c6 = st.columns(2)
# # #         with c5:
# # #             rp = remote_df['platform'].value_counts().reset_index()
# # #             rp.columns = ['Portal', 'Remote Jobs']
# # #             fig = px.bar(rp, x='Portal', y='Remote Jobs',
# # #                          title='Remote Jobs by Portal',
# # #                          color='Remote Jobs', color_continuous_scale='Blues',
# # #                          text='Remote Jobs')
# # #             fig.update_layout(height=400, showlegend=False,
# # #                               xaxis_tickangle=-30, title_font_size=13)
# # #             fig.update_traces(textposition='outside')
# # #             st.plotly_chart(fig, use_container_width=True, key="rem_portals")

# # #         with c6:
# # #             fig = px.pie(rp, values='Remote Jobs', names='Portal',
# # #                          title='Portal Share (Remote)', hole=0.4,
# # #                          color_discrete_sequence=px.colors.qualitative.Set3)
# # #             fig.update_traces(textinfo='percent+label', textposition='outside',
# # #                               textfont_size=11, pull=[0.03] * len(rp))
# # #             fig.update_layout(height=400, title_font_size=13)
# # #             st.plotly_chart(fig, use_container_width=True, key="rem_pie")

# # #         # Skills
# # #         st.markdown("### 🛠️ Top Skills for Remote Jobs")
# # #         all_rs = [s for skills in remote_df['skills'] for s in skills]
# # #         rs = Counter(all_rs).most_common(15)
# # #         if rs:
# # #             rs_df = pd.DataFrame(rs, columns=['Skill', 'Jobs'])
# # #             fig = px.bar(rs_df, x='Jobs', y='Skill', orientation='h',
# # #                          title='Top Skills (Remote)', color='Jobs',
# # #                          color_continuous_scale='Greens', text='Jobs')
# # #             fig.update_layout(height=500, showlegend=False,
# # #                               yaxis=dict(autorange="reversed"), title_font_size=13)
# # #             fig.update_traces(textposition='outside')
# # #             st.plotly_chart(fig, use_container_width=True, key="rem_skills")

# # #         # Full list
# # #         st.markdown("### 📋 All Remote Jobs")
# # #         show_cols = ['title', 'company', 'location', 'platform',
# # #                      'employment_type', 'posted_date']
# # #         display_remote = remote_df[show_cols].copy()
# # #         display_remote.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # #                                   'Type', 'Posted']
# # #         st.dataframe(display_remote, use_container_width=True, height=500)

# # #         csv = remote_df.to_csv(index=False)
# # #         st.download_button("📥 Download All Remote Jobs (CSV)", csv,
# # #                            file_name=f"remote_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
# # #                            mime="text/csv", key="dl_remote_all")

# # # # ============================================================================
# # # # OTHER VIEWS
# # # # ============================================================================
# # # elif st.session_state.view == "Companies":
# # #     st.markdown('<div class="drill-header">🏢 All Companies Hiring</div>', unsafe_allow_html=True)
# # #     comp_df = df['company'].value_counts().reset_index()
# # #     comp_df.columns = ['Company', 'Openings']
# # #     comp_df['Share %'] = (comp_df['Openings'] / len(df) * 100).round(2)

# # #     c1, c2 = st.columns([3, 2])
# # #     with c1:
# # #         fig = px.bar(comp_df.head(30), x='Openings', y='Company', orientation='h',
# # #                      title=f'All {len(comp_df)} Companies (Top 30)',
# # #                      color='Openings', color_continuous_scale='Viridis', text='Openings')
# # #         fig.update_layout(height=800, showlegend=False,
# # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # #         fig.update_traces(textposition='outside')
# # #         st.plotly_chart(fig, use_container_width=True, key="all_comp")
# # #     with c2:
# # #         st.dataframe(comp_df, use_container_width=True, height=750, hide_index=True)
# # #     csv = comp_df.to_csv(index=False)
# # #     st.download_button("📥 Download CSV", csv,
# # #                        file_name=f"companies_{datetime.now().strftime('%Y%m%d')}.csv",
# # #                        mime="text/csv", key="dl_comp")

# # # elif st.session_state.view == "Locations":
# # #     st.markdown('<div class="drill-header">📍 All Locations</div>', unsafe_allow_html=True)
# # #     loc_df = df['location'].value_counts().reset_index()
# # #     loc_df.columns = ['Location', 'Openings']

# # #     c1, c2 = st.columns([3, 2])
# # #     with c1:
# # #         fig = px.bar(loc_df, x='Openings', y='Location', orientation='h',
# # #                      title=f'All {len(loc_df)} Locations',
# # #                      color='Openings', color_continuous_scale='Magma', text='Openings')
# # #         fig.update_layout(height=max(600, len(loc_df)*22), showlegend=False,
# # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # #         fig.update_traces(textposition='outside')
# # #         st.plotly_chart(fig, use_container_width=True, key="all_loc")
# # #     with c2:
# # #         st.dataframe(loc_df, use_container_width=True, height=750, hide_index=True)
# # #     csv = loc_df.to_csv(index=False)
# # #     st.download_button("📥 Download CSV", csv,
# # #                        file_name=f"locations_{datetime.now().strftime('%Y%m%d')}.csv",
# # #                        mime="text/csv", key="dl_loc")

# # # elif st.session_state.view == "Job Roles":
# # #     st.markdown('<div class="drill-header">💼 All Job Roles</div>', unsafe_allow_html=True)
# # #     role_df = df['title'].value_counts().reset_index()
# # #     role_df.columns = ['Job Role', 'Openings']

# # #     c1, c2 = st.columns([3, 2])
# # #     with c1:
# # #         fig = px.bar(role_df.head(40), x='Openings', y='Job Role', orientation='h',
# # #                      title=f'All {len(role_df)} Roles (Top 40)',
# # #                      color='Openings', color_continuous_scale='Plasma', text='Openings')
# # #         fig.update_layout(height=1000, showlegend=False,
# # #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# # #         fig.update_traces(textposition='outside')
# # #         st.plotly_chart(fig, use_container_width=True, key="all_role")
# # #     with c2:
# # #         st.dataframe(role_df, use_container_width=True, height=950, hide_index=True)
# # #     csv = role_df.to_csv(index=False)
# # #     st.download_button("📥 Download CSV", csv,
# # #                        file_name=f"roles_{datetime.now().strftime('%Y%m%d')}.csv",
# # #                        mime="text/csv", key="dl_role")

# # # elif st.session_state.view == "Portals":
# # #     st.markdown('<div class="drill-header">🌐 All Portals</div>', unsafe_allow_html=True)
# # #     portal_df = df['platform'].value_counts().reset_index()
# # #     portal_df.columns = ['Portal', 'Openings']

# # #     c1, c2 = st.columns(2)
# # #     with c1:
# # #         fig = px.bar(portal_df, x='Portal', y='Openings',
# # #                      title='Portals', color='Openings',
# # #                      color_continuous_scale='Turbo', text='Openings')
# # #         fig.update_layout(height=450, showlegend=False,
# # #                           xaxis_tickangle=-30, title_font_size=13)
# # #         fig.update_traces(textposition='outside')
# # #         st.plotly_chart(fig, use_container_width=True, key="all_portal")
# # #     with c2:
# # #         st.dataframe(portal_df, use_container_width=True, hide_index=True)
# # #     csv = portal_df.to_csv(index=False)
# # #     st.download_button("📥 Download CSV", csv,
# # #                        file_name=f"portals_{datetime.now().strftime('%Y%m%d')}.csv",
# # #                        mime="text/csv", key="dl_portal")

# # # elif st.session_state.view == "Total Jobs":
# # #     st.markdown('<div class="drill-header">📊 All Jobs in Dataset</div>', unsafe_allow_html=True)
# # #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # #                  'employment_type', 'posted_date']
# # #     display_df = df[show_cols].copy()
# # #     display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # #                           'Remote', 'Type', 'Posted']
# # #     st.dataframe(display_df, use_container_width=True, height=600)
# # #     csv = df.to_csv(index=False)
# # #     st.download_button("📥 Download All Jobs (CSV)", csv,
# # #                        file_name=f"all_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
# # #                        mime="text/csv", key="dl_total")

# # # # ============================================================================
# # # # DRILL-DOWN PANEL
# # # # ============================================================================
# # # if st.session_state.drill_type and st.session_state.drill_value:
# # #     st.markdown("---")
# # #     dv = st.session_state.drill_value
# # #     dt = st.session_state.drill_type
# # #     st.markdown(f'<div class="drill-header">🎯 Drill-Down: {dt} = "{dv}"</div>', unsafe_allow_html=True)

# # #     if dt == "Skill":
# # #         ddf = df[df['skills'].apply(lambda x: dv in x)]
# # #     elif dt == "Job Role":
# # #         ddf = df[df['title'] == dv]
# # #     elif dt == "Company":
# # #         ddf = df[df['company'] == dv]
# # #     elif dt == "Location":
# # #         ddf = df[df['location'] == dv]
# # #     elif dt == "Portal":
# # #         ddf = df[df['platform'] == dv]
# # #     else:
# # #         ddf = df.copy()

# # #     d1, d2, d3, d4 = st.columns(4)
# # #     with d1: st.metric("🎯 Openings", len(ddf))
# # #     with d2: st.metric("🏢 Companies", ddf['company'].nunique())
# # #     with d3: st.metric("📍 Locations", ddf['location'].nunique())
# # #     with d4:
# # #         rp = (ddf['is_remote'] == 'Yes').sum() / len(ddf) * 100 if len(ddf) > 0 else 0
# # #         st.metric("🏠 Remote %", f"{rp:.1f}%")

# # #     g1, g2 = st.columns(2)
# # #     with g1:
# # #         pc = ddf['platform'].value_counts().reset_index()
# # #         pc.columns = ['Portal', 'Openings']
# # #         fig = px.bar(pc, x='Openings', y='Portal', orientation='h',
# # #                      title='By Portal', color='Openings',
# # #                      color_continuous_scale='Blues', text='Openings')
# # #         fig.update_layout(height=350, showlegend=False,
# # #                           yaxis=dict(autorange="reversed"))
# # #         fig.update_traces(textposition='outside')
# # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_p_{dv}")
# # #     with g2:
# # #         cc = ddf['company'].value_counts().head(10).reset_index()
# # #         cc.columns = ['Company', 'Openings']
# # #         fig = px.bar(cc, x='Openings', y='Company', orientation='h',
# # #                      title='By Company', color='Openings',
# # #                      color_continuous_scale='Viridis', text='Openings')
# # #         fig.update_layout(height=350, showlegend=False,
# # #                           yaxis=dict(autorange="reversed"))
# # #         fig.update_traces(textposition='outside')
# # #         st.plotly_chart(fig, use_container_width=True, key=f"dd_c_{dv}")

# # #     st.markdown("### 📋 All Job Openings")
# # #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# # #                  'employment_type', 'posted_date']
# # #     disp = ddf[show_cols].copy()
# # #     disp.columns = ['Job Title', 'Company', 'Location', 'Portal',
# # #                     'Remote', 'Type', 'Posted']
# # #     st.dataframe(disp, use_container_width=True, height=400)

# # #     csv = ddf.to_csv(index=False)
# # #     st.download_button("📥 Download (CSV)", csv,
# # #                        file_name=f"drill_{dt}_{dv}.csv",
# # #                        mime="text/csv", key=f"dl_dd_{dv}")

# # # # ============================================================================
# # # # FOOTER
# # # # ============================================================================
# # # st.markdown("---")
# # # st.markdown(f"""<div style='text-align:center; color:#666; font-size:12px;'>
# # #     Job Market Analytics | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
# # #     {len(df)} total jobs | {(df['is_remote']=='Yes').sum()} remote
# # # </div>""", unsafe_allow_html=True)










# # """
# # ================================================================================
# # JOB MARKET ANALYTICS — CLICKABLE KPI + REMOTE DRILL-DOWN
# # Click KPI cards to see detailed lists + Drill-down on charts
# # Tech Stack: Python | Pandas | NumPy | Plotly | Streamlit
# # Run: python -m streamlit run dashboard.py
# # ================================================================================
# # """

# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # import plotly.express as px
# # import plotly.graph_objects as go
# # from collections import Counter
# # from datetime import datetime
# # import warnings
# # import logging

# # warnings.filterwarnings('ignore')
# # logging.getLogger('streamlit').setLevel(logging.ERROR)

# # # ============================================================================
# # # PAGE CONFIG
# # # ============================================================================
# # st.set_page_config(
# #     page_title="Job Market Analytics",
# #     page_icon="🎯",
# #     layout="wide",
# #     initial_sidebar_state="expanded"
# # )

# # # CSS
# # st.markdown("""
# # <style>
    /* ========== FORCE DARK TEXT EVERYWHERE ========== */
    .stApp, .stApp * {
        color: #1a1a1a !important;
    }
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricLabel"] > div {
        color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stDataFrame"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
    }
# #     div[data-testid="stMarkdownContainer"] div,
# #     div[data-testid="stMarkdownContainer"] p,
# #     div[data-testid="stMarkdownContainer"] span,
# #     div[data-testid="stMarkdownContainer"] strong { color: #1a1a1a; }

# #     .main-header {
# #         font-size: 2.2rem; font-weight: bold;
# #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# #         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
# #         text-align: center; padding: 0.5rem 0;
# #     }
# #     .sub-header { text-align: center; color: #666; margin-bottom: 1rem; }
# #     .problem-header {
# #         background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
# #         padding: 0.7rem 1rem; border-radius: 8px;
# #         color: #FFFFFF !important; font-weight: bold;
# #         margin-bottom: 1rem; font-size: 1rem;
# #     }
# #     .insight-box {
# #         background: #f0f7ff; padding: 0.8rem;
# #         border-left: 4px solid #667eea; border-radius: 5px;
# #         margin: 0.6rem 0; font-size: 0.9rem; color: #1a1a1a !important;
# #     }
# #     .insight-box strong { color: #2c3e50 !important; font-weight: 700; }
# #     .drill-header {
# #         background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
# #         padding: 0.8rem 1rem; border-radius: 8px;
# #         color: #1a1a1a !important; font-weight: bold;
# #         margin: 1rem 0; font-size: 1.1rem;
# #         border: 2px solid #43e97b;
# #     }
# #     .stTabs [data-baseweb="tab-list"] { gap: 6px; flex-wrap: wrap; }
# #     .stTabs [data-baseweb="tab"] {
# #         background-color: #f0f2f6; border-radius: 6px;
# #         padding: 8px 12px; font-weight: 600; font-size: 0.78rem;
# #     }
# #     .stTabs [aria-selected="true"] {
# #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# #         color: #FFFFFF !important;
# #     }
# #     div[data-testid="stButton"] button {
# #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #         color: white !important;
# #         border: none;
# #         padding: 1.5rem 1rem;
# #         border-radius: 12px;
# #         width: 100%;
# #         min-height: 120px;
# #         font-size: 1rem;
# #         font-weight: bold;
# #         box-shadow: 0 4px 12px rgba(0,0,0,0.1);
# #         transition: transform 0.2s;
# #     }
# #     div[data-testid="stButton"] button:hover {
# #         transform: translateY(-3px);
# #         box-shadow: 0 6px 16px rgba(0,0,0,0.2);
# #     }
# #     div[data-testid="stButton"] button p {
# #         color: white !important;
# #         font-size: 1rem;
# #         font-weight: bold;
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # # ============================================================================
# # # DATA LOADING
# # # ============================================================================

# # @st.cache_data
# # def load_data():
# #     df = pd.read_csv("job_data_clean.csv")
# #     df['posted_date'] = pd.to_datetime(df['posted_date'], errors='coerce')
# #     return df

# # def extract_skills(text):
# #     if pd.isna(text):
# #         return []
# #     text = str(text).lower()
# #     skill_list = [
# #         'python', 'java', 'sql', 'javascript', 'typescript', 'react', 'angular',
# #         'node.js', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
# #         'jenkins', 'spark', 'kafka', 'airflow', 'snowflake', 'tableau', 'power bi',
# #         'machine learning', 'deep learning', 'nlp', 'llm', 'genai', 'rag',
# #         'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
# #         'excel', 'git', 'linux', 'agile', 'scrum', 'jira'
# #     ]
# #     return list(set([s for s in skill_list if s in text]))

# # try:
# #     df = load_data()
# #     df['skills'] = df['description'].apply(extract_skills)
# #     df['skill_count'] = df['skills'].apply(len)
# # except Exception as e:
# #     st.error(f"❌ Error loading 'job_data_clean.csv': {e}")
# #     st.stop()

# # # ============================================================================
# # # HEADER
# # # ============================================================================
# # st.markdown('<h1 class="main-header">🎯 Job Market Analytics</h1>', unsafe_allow_html=True)
# # st.markdown('<p class="sub-header">Click any KPI card → see detailed breakdown</p>', unsafe_allow_html=True)

# # # ============================================================================
# # # SESSION STATE
# # # ============================================================================
# # for key in ['view', 'drill_type', 'drill_value']:
# #     if key not in st.session_state:
# #         st.session_state[key] = None

# # # Sidebar
# # st.sidebar.markdown("## 🔍 Navigation")
# # if st.sidebar.button("🏠 Home (Clear View)"):
# #     st.session_state.view = None
# #     st.session_state.drill_type = None
# #     st.session_state.drill_value = None
# #     st.rerun()

# # if st.session_state.view:
# #     st.sidebar.success(f"**Viewing:** {st.session_state.view}")

# # if st.session_state.drill_type:
# #     st.sidebar.info(f"**Drill:** {st.session_state.drill_type} = {st.session_state.drill_value}")
# #     if st.sidebar.button("❌ Clear Drill"):
# #         st.session_state.drill_type = None
# #         st.session_state.drill_value = None
# #         st.rerun()

# # st.sidebar.markdown("---")
# # st.sidebar.markdown(f"**📊 Total Jobs:** {len(df)}")
# # st.sidebar.markdown(f"**🏠 Remote Jobs:** {(df['is_remote']=='Yes').sum()}")

# # # ============================================================================
# # # KPI CARDS — CLICKABLE
# # # ============================================================================
# # st.markdown("## 📈 Overview — Click to Explore")

# # k1, k2, k3, k4, k5, k6 = st.columns(6)

# # with k1:
# #     if st.button(f"📊\n\n**Total Jobs**\n\n{len(df)}\n\n_in dataset_",
# #                  key="kpi_total", use_container_width=True):
# #         st.session_state.view = "Total Jobs"
# #         st.session_state.drill_type = None
# #         st.rerun()

# # with k2:
# #     if st.button(f"🏢\n\n**Companies**\n\n{df['company'].nunique()}\n\n_hiring_",
# #                  key="kpi_company", use_container_width=True):
# #         st.session_state.view = "Companies"
# #         st.session_state.drill_type = None
# #         st.rerun()

# # with k3:
# #     if st.button(f"💼\n\n**Job Roles**\n\n{df['title'].nunique()}\n\n_unique_",
# #                  key="kpi_title", use_container_width=True):
# #         st.session_state.view = "Job Roles"
# #         st.session_state.drill_type = None
# #         st.rerun()

# # with k4:
# #     if st.button(f"🌐\n\n**Portals**\n\n{df['platform'].nunique()}\n\n_sources_",
# #                  key="kpi_portal", use_container_width=True):
# #         st.session_state.view = "Portals"
# #         st.session_state.drill_type = None
# #         st.rerun()

# # with k5:
# #     if st.button(f"📍\n\n**Locations**\n\n{df['location'].nunique()}\n\n_cities_",
# #                  key="kpi_location", use_container_width=True):
# #         st.session_state.view = "Locations"
# #         st.session_state.drill_type = None
# #         st.rerun()

# # with k6:
# #     remote_count = (df['is_remote'] == 'Yes').sum()
# #     if st.button(f"🏠\n\n**Remote Jobs**\n\n{remote_count}\n\n_of {len(df)}_",
# #                  key="kpi_remote", use_container_width=True):
# #         st.session_state.view = "Remote Jobs"
# #         st.session_state.drill_type = None
# #         st.rerun()

# # st.markdown("---")

# # # ============================================================================
# # # VIEW: REMOTE JOBS — DETAILED BREAKDOWN
# # # ============================================================================
# # if st.session_state.view == "Remote Jobs":
# #     st.markdown('<div class="drill-header">🏠 Remote Jobs — Complete Breakdown</div>', unsafe_allow_html=True)

# #     remote_df = df[df['is_remote'] == 'Yes']

# #     if len(remote_df) == 0:
# #         st.warning("No remote jobs found in the dataset.")
# #     else:
# #         d1, d2, d3, d4, d5 = st.columns(5)
# #         with d1: st.metric("🏠 Total Remote Jobs", len(remote_df))
# #         with d2: st.metric("🏢 Companies", remote_df['company'].nunique())
# #         with d3: st.metric("📍 Locations", remote_df['location'].nunique())
# #         with d4: st.metric("💼 Job Roles", remote_df['title'].nunique())
# #         with d5: st.metric("🌐 Portals", remote_df['platform'].nunique())

# #         st.markdown("---")

# #         # Section 1: Remote Companies
# #         st.markdown("### 🏢 Companies Hiring Remote")
# #         c1, c2 = st.columns([3, 2])

# #         with c1:
# #             rc = remote_df['company'].value_counts().reset_index()
# #             rc.columns = ['Company', 'Remote Jobs']
# #             fig = px.bar(
# #                 rc, x='Remote Jobs', y='Company', orientation='h',
# #                 title=f'All {len(rc)} Companies Hiring Remote — Click a bar',
# #                 color='Remote Jobs', color_continuous_scale='Greens', text='Remote Jobs'
# #             )
# #             fig.update_layout(
# #                 height=max(400, len(rc)*35), showlegend=False,
# #                 yaxis=dict(autorange="reversed"), title_font_size=14,
# #                 clickmode='event+select'
# #             )
# #             fig.update_traces(textposition='outside')

# #             event = st.plotly_chart(fig, use_container_width=True,
# #                                     on_select="rerun", key="remote_company_drill")

# #             if event and event.get("selection") and event["selection"].get("points"):
# #                 clicked = event["selection"]["points"][0].get("y")
# #                 if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
# #                     st.session_state.drill_type = "Company"
# #                     st.session_state.drill_value = clicked
# #                     st.rerun()

# #         with c2:
# #             st.markdown("#### 📋 Company List (Remote)")
# #             st.dataframe(rc, use_container_width=True, height=400, hide_index=True)

# #         # Section 2: Remote Locations
# #         st.markdown("### 📍 Remote Jobs by Location / Area")
# #         c3, c4 = st.columns([3, 2])

# #         with c3:
# #             rl = remote_df['location'].value_counts().reset_index()
# #             rl.columns = ['Location', 'Remote Jobs']
# #             fig = px.bar(
# #                 rl, x='Remote Jobs', y='Location', orientation='h',
# #                 title='Remote Jobs by Location — Click a bar',
# #                 color='Remote Jobs', color_continuous_scale='Teal', text='Remote Jobs'
# #             )
# #             fig.update_layout(
# #                 height=max(400, len(rl)*35), showlegend=False,
# #                 yaxis=dict(autorange="reversed"), title_font_size=14,
# #                 clickmode='event+select'
# #             )
# #             fig.update_traces(textposition='outside')

# #             event = st.plotly_chart(fig, use_container_width=True,
# #                                     on_select="rerun", key="remote_loc_drill")

# #             if event and event.get("selection") and event["selection"].get("points"):
# #                 clicked = event["selection"]["points"][0].get("y")
# #                 if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
# #                     st.session_state.drill_type = "Location"
# #                     st.session_state.drill_value = clicked
# #                     st.rerun()

# #         with c4:
# #             st.markdown("#### 📋 Location List (Remote)")
# #             st.dataframe(rl, use_container_width=True, height=400, hide_index=True)

# #         # Section 3: Portals
# #         st.markdown("### 🌐 Which Portals Post Remote Jobs?")
# #         c5, c6 = st.columns([2, 2])

# #         with c5:
# #             rp = remote_df['platform'].value_counts().reset_index()
# #             rp.columns = ['Portal', 'Remote Jobs']
# #             fig = px.bar(
# #                 rp, x='Portal', y='Remote Jobs',
# #                 title='Remote Jobs by Portal — Click a bar',
# #                 color='Remote Jobs', color_continuous_scale='Blues', text='Remote Jobs'
# #             )
# #             fig.update_layout(height=400, showlegend=False,
# #                               xaxis_tickangle=-30, title_font_size=13,
# #                               clickmode='event+select')
# #             fig.update_traces(textposition='outside')

# #             event = st.plotly_chart(fig, use_container_width=True,
# #                                     on_select="rerun", key="remote_portal_drill")

# #             if event and event.get("selection") and event["selection"].get("points"):
# #                 clicked = event["selection"]["points"][0].get("x")
# #                 if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
# #                     st.session_state.drill_type = "Portal"
# #                     st.session_state.drill_value = clicked
# #                     st.rerun()

# #         with c6:
# #             fig = px.pie(
# #                 rp, values='Remote Jobs', names='Portal',
# #                 title='Remote Jobs — Portal Share',
# #                 hole=0.4,
# #                 color_discrete_sequence=px.colors.qualitative.Set3
# #             )
# #             fig.update_traces(textinfo='percent+label', textposition='outside',
# #                               textfont_size=11, pull=[0.03] * len(rp))
# #             fig.update_layout(height=400, title_font_size=13)
# #             st.plotly_chart(fig, use_container_width=True, key="remote_portal_pie")

# #         # Section 4: Roles
# #         st.markdown("### 💼 What Job Roles Are Remote?")
# #         rr = remote_df['title'].value_counts().reset_index()
# #         rr.columns = ['Job Role', 'Remote Jobs']
# #         fig = px.bar(
# #             rr, x='Remote Jobs', y='Job Role', orientation='h',
# #             title='Remote Job Roles — Click a bar',
# #             color='Remote Jobs', color_continuous_scale='Purples', text='Remote Jobs'
# #         )
# #         fig.update_layout(
# #             height=max(400, len(rr)*35), showlegend=False,
# #             yaxis=dict(autorange="reversed"), title_font_size=14,
# #             clickmode='event+select'
# #         )
# #         fig.update_traces(textposition='outside')

# #         event = st.plotly_chart(fig, use_container_width=True,
# #                                 on_select="rerun", key="remote_role_drill")

# #         if event and event.get("selection") and event["selection"].get("points"):
# #             clicked = event["selection"]["points"][0].get("y")
# #             if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
# #                 st.session_state.drill_type = "Job Role"
# #                 st.session_state.drill_value = clicked
# #                 st.rerun()

# #         # Section 5: Skills
# #         st.markdown("### 🛠️ Top Skills Required for Remote Jobs")
# #         all_rs = [s for skills in remote_df['skills'] for s in skills]
# #         rs = Counter(all_rs).most_common(15)

# #         if rs:
# #             rs_df = pd.DataFrame(rs, columns=['Skill', 'Jobs'])
# #             rs_df['% of Remote'] = (rs_df['Jobs'] / len(remote_df) * 100).round(1)
# #             fig = px.bar(
# #                 rs_df, x='Jobs', y='Skill', orientation='h',
# #                 title='Top Skills for Remote Jobs',
# #                 color='Jobs', color_continuous_scale='Greens', text='Jobs'
# #             )
# #             fig.update_layout(height=500, showlegend=False,
# #                               yaxis=dict(autorange="reversed"), title_font_size=14)
# #             fig.update_traces(textposition='outside')
# #             st.plotly_chart(fig, use_container_width=True, key="remote_skills")

# #         # Section 6: Full List
# #         st.markdown("### 📋 All Remote Job Openings")
# #         show_cols = ['title', 'company', 'location', 'platform',
# #                      'employment_type', 'posted_date']
# #         display_remote = remote_df[show_cols].copy()
# #         display_remote.columns = ['Job Title', 'Company', 'Location', 'Portal',
# #                                   'Type', 'Posted']
# #         st.dataframe(display_remote, use_container_width=True, height=500)

# #         csv = remote_df.to_csv(index=False)
# #         st.download_button(
# #             label="📥 Download All Remote Jobs (CSV)",
# #             data=csv,
# #             file_name=f"remote_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
# #             mime="text/csv",
# #             key="dl_remote"
# #         )

# #         # Insight
# #         top_comp = remote_df['company'].value_counts().index[0]
# #         top_loc = remote_df['location'].value_counts().index[0]
# #         top_portal = remote_df['platform'].value_counts().index[0]

# #         st.markdown(f"""<div class="insight-box">
# #             <strong>📊 Remote Job Summary:</strong><br>
# #             🏢 <strong>Top Remote Employer:</strong> {top_comp}<br>
# #             📍 <strong>Top Remote Location:</strong> {top_loc}<br>
# #             🌐 <strong>Top Portal for Remote:</strong> {top_portal}<br>
# #             🛠️ <strong>Top Skill for Remote:</strong> {rs[0][0] if rs else 'N/A'}<br>
# #             📊 <strong>Remote % of Total:</strong> {len(remote_df)/len(df)*100:.1f}%
# #         </div>""", unsafe_allow_html=True)

# # # ============================================================================
# # # OTHER VIEWS
# # # ============================================================================
# # elif st.session_state.view == "Companies":
# #     st.markdown('<div class="drill-header">🏢 All Companies Hiring</div>', unsafe_allow_html=True)
# #     comp_df = df['company'].value_counts().reset_index()
# #     comp_df.columns = ['Company', 'Openings']
# #     comp_df['Share %'] = (comp_df['Openings'] / len(df) * 100).round(2)

# #     c1, c2 = st.columns([3, 2])
# #     with c1:
# #         fig = px.bar(comp_df.head(30), x='Openings', y='Company', orientation='h',
# #                      title=f'All {len(comp_df)} Companies (Top 30) — Click a bar',
# #                      color='Openings', color_continuous_scale='Viridis', text='Openings')
# #         fig.update_layout(height=800, showlegend=False,
# #                           yaxis=dict(autorange="reversed"),
# #                           title_font_size=14, clickmode='event+select')
# #         fig.update_traces(textposition='outside')
# #         event = st.plotly_chart(fig, use_container_width=True,
# #                                 on_select="rerun", key="comp_view_drill")
# #         if event and event.get("selection") and event["selection"].get("points"):
# #             clicked = event["selection"]["points"][0].get("y")
# #             if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
# #                 st.session_state.drill_type = "Company"
# #                 st.session_state.drill_value = clicked
# #                 st.rerun()

# #     with c2:
# #         st.markdown("### 📋 Complete List")
# #         st.dataframe(comp_df, use_container_width=True, height=750, hide_index=True)

# #     csv = comp_df.to_csv(index=False)
# #     st.download_button("📥 Download CSV", csv,
# #                        file_name=f"companies_{datetime.now().strftime('%Y%m%d')}.csv",
# #                        mime="text/csv", key="dl_comp_view")

# # elif st.session_state.view == "Locations":
# #     st.markdown('<div class="drill-header">📍 All Locations</div>', unsafe_allow_html=True)
# #     loc_df = df['location'].value_counts().reset_index()
# #     loc_df.columns = ['Location', 'Openings']
# #     loc_df['Share %'] = (loc_df['Openings'] / len(df) * 100).round(2)

# #     c1, c2 = st.columns([3, 2])
# #     with c1:
# #         fig = px.bar(loc_df, x='Openings', y='Location', orientation='h',
# #                      title=f'All {len(loc_df)} Locations — Click a bar',
# #                      color='Openings', color_continuous_scale='Magma', text='Openings')
# #         fig.update_layout(height=max(600, len(loc_df)*22), showlegend=False,
# #                           yaxis=dict(autorange="reversed"),
# #                           title_font_size=14, clickmode='event+select')
# #         fig.update_traces(textposition='outside')
# #         event = st.plotly_chart(fig, use_container_width=True,
# #                                 on_select="rerun", key="loc_view_drill")
# #         if event and event.get("selection") and event["selection"].get("points"):
# #             clicked = event["selection"]["points"][0].get("y")
# #             if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
# #                 st.session_state.drill_type = "Location"
# #                 st.session_state.drill_value = clicked
# #                 st.rerun()

# #     with c2:
# #         st.markdown("### 📋 Complete List")
# #         st.dataframe(loc_df, use_container_width=True, height=750, hide_index=True)

# #     csv = loc_df.to_csv(index=False)
# #     st.download_button("📥 Download CSV", csv,
# #                        file_name=f"locations_{datetime.now().strftime('%Y%m%d')}.csv",
# #                        mime="text/csv", key="dl_loc_view")

# # elif st.session_state.view == "Job Roles":
# #     st.markdown('<div class="drill-header">💼 All Job Roles</div>', unsafe_allow_html=True)
# #     role_df = df['title'].value_counts().reset_index()
# #     role_df.columns = ['Job Role', 'Openings']
# #     role_df['Share %'] = (role_df['Openings'] / len(df) * 100).round(2)

# #     c1, c2 = st.columns([3, 2])
# #     with c1:
# #         fig = px.bar(role_df.head(40), x='Openings', y='Job Role', orientation='h',
# #                      title=f'All {len(role_df)} Job Roles (Top 40) — Click a bar',
# #                      color='Openings', color_continuous_scale='Plasma', text='Openings')
# #         fig.update_layout(height=1000, showlegend=False,
# #                           yaxis=dict(autorange="reversed"),
# #                           title_font_size=14, clickmode='event+select')
# #         fig.update_traces(textposition='outside')
# #         event = st.plotly_chart(fig, use_container_width=True,
# #                                 on_select="rerun", key="role_view_drill")
# #         if event and event.get("selection") and event["selection"].get("points"):
# #             clicked = event["selection"]["points"][0].get("y")
# #             if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
# #                 st.session_state.drill_type = "Job Role"
# #                 st.session_state.drill_value = clicked
# #                 st.rerun()

# #     with c2:
# #         st.markdown("### 📋 Complete List")
# #         st.dataframe(role_df, use_container_width=True, height=950, hide_index=True)

# #     csv = role_df.to_csv(index=False)
# #     st.download_button("📥 Download CSV", csv,
# #                        file_name=f"roles_{datetime.now().strftime('%Y%m%d')}.csv",
# #                        mime="text/csv", key="dl_role_view")

# # elif st.session_state.view == "Portals":
# #     st.markdown('<div class="drill-header">🌐 All Portals</div>', unsafe_allow_html=True)
# #     portal_df = df['platform'].value_counts().reset_index()
# #     portal_df.columns = ['Portal', 'Openings']
# #     portal_df['Share %'] = (portal_df['Openings'] / len(df) * 100).round(2)

# #     c1, c2 = st.columns(2)
# #     with c1:
# #         fig = px.bar(portal_df, x='Portal', y='Openings',
# #                      title='Portals — Click a bar',
# #                      color='Openings', color_continuous_scale='Turbo', text='Openings')
# #         fig.update_layout(height=450, showlegend=False,
# #                           xaxis_tickangle=-30, title_font_size=13,
# #                           clickmode='event+select')
# #         fig.update_traces(textposition='outside')
# #         event = st.plotly_chart(fig, use_container_width=True,
# #                                 on_select="rerun", key="portal_view_drill")
# #         if event and event.get("selection") and event["selection"].get("points"):
# #             clicked = event["selection"]["points"][0].get("x")
# #             if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
# #                 st.session_state.drill_type = "Portal"
# #                 st.session_state.drill_value = clicked
# #                 st.rerun()

# #     with c2:
# #         st.markdown("### 📋 Complete List")
# #         st.dataframe(portal_df, use_container_width=True, hide_index=True)

# #     csv = portal_df.to_csv(index=False)
# #     st.download_button("📥 Download CSV", csv,
# #                        file_name=f"portals_{datetime.now().strftime('%Y%m%d')}.csv",
# #                        mime="text/csv", key="dl_portal_view")

# # elif st.session_state.view == "Total Jobs":
# #     st.markdown('<div class="drill-header">📊 All Jobs in Dataset</div>', unsafe_allow_html=True)
# #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# #                  'employment_type', 'posted_date']
# #     display_df = df[show_cols].copy()
# #     display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
# #                           'Remote', 'Type', 'Posted']
# #     st.dataframe(display_df, use_container_width=True, height=600)
# #     csv = df.to_csv(index=False)
# #     st.download_button("📥 Download All Jobs (CSV)", csv,
# #                        file_name=f"all_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
# #                        mime="text/csv", key="dl_total_view")

# # # ============================================================================
# # # DRILL-DOWN PANEL
# # # ============================================================================
# # if st.session_state.drill_type and st.session_state.drill_value:
# #     st.markdown("---")
# #     drill_val = st.session_state.drill_value
# #     drill_type = st.session_state.drill_type

# #     st.markdown(f'<div class="drill-header">🎯 Drill-Down: {drill_type} = "{drill_val}"</div>', unsafe_allow_html=True)

# #     if drill_type == "Skill":
# #         drill_df = df[df['skills'].apply(lambda x: drill_val in x)]
# #     elif drill_type == "Job Role":
# #         drill_df = df[df['title'] == drill_val]
# #     elif drill_type == "Company":
# #         drill_df = df[df['company'] == drill_val]
# #     elif drill_type == "Location":
# #         drill_df = df[df['location'] == drill_val]
# #     elif drill_type == "Portal":
# #         drill_df = df[df['platform'] == drill_val]
# #     else:
# #         drill_df = df.copy()

# #     d1, d2, d3, d4 = st.columns(4)
# #     with d1: st.metric("🎯 Total Openings", len(drill_df))
# #     with d2: st.metric("🏢 Companies", drill_df['company'].nunique())
# #     with d3: st.metric("📍 Locations", drill_df['location'].nunique())
# #     with d4:
# #         rp = (drill_df['is_remote'] == 'Yes').sum() / len(drill_df) * 100 if len(drill_df) > 0 else 0
# #         st.metric("🏠 Remote %", f"{rp:.1f}%")

# #     g1, g2 = st.columns(2)
# #     with g1:
# #         pc = drill_df['platform'].value_counts().reset_index()
# #         pc.columns = ['Portal', 'Openings']
# #         fig = px.bar(pc, x='Openings', y='Portal', orientation='h',
# #                      title='By Portal', color='Openings',
# #                      color_continuous_scale='Blues', text='Openings')
# #         fig.update_layout(height=350, showlegend=False,
# #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# #         fig.update_traces(textposition='outside')
# #         st.plotly_chart(fig, use_container_width=True, key=f"dd_p_{drill_val}")

# #     with g2:
# #         cc = drill_df['company'].value_counts().head(10).reset_index()
# #         cc.columns = ['Company', 'Openings']
# #         fig = px.bar(cc, x='Openings', y='Company', orientation='h',
# #                      title='By Company', color='Openings',
# #                      color_continuous_scale='Viridis', text='Openings')
# #         fig.update_layout(height=350, showlegend=False,
# #                           yaxis=dict(autorange="reversed"), title_font_size=13)
# #         fig.update_traces(textposition='outside')
# #         st.plotly_chart(fig, use_container_width=True, key=f"dd_c_{drill_val}")

# #     st.markdown("### 📋 All Job Openings")
# #     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
# #                  'employment_type', 'posted_date']
# #     ddf = drill_df[show_cols].copy()
# #     ddf.columns = ['Job Title', 'Company', 'Location', 'Portal',
# #                    'Remote', 'Type', 'Posted']
# #     st.dataframe(ddf, use_container_width=True, height=400)

# #     csv = drill_df.to_csv(index=False)
# #     st.download_button("📥 Download (CSV)", csv,
# #                        file_name=f"drill_{drill_type}_{drill_val}.csv",
# #                        mime="text/csv", key=f"dl_dd_{drill_val}")

# # # ============================================================================
# # # MAIN TABS (when no view is active)
# # # ============================================================================
# # if st.session_state.view is None:
# #     st.markdown("---")
# #     st.markdown("## 🔎 Explore Charts — Click to drill down")

# #     tabs = st.tabs(["🛠️ By Skill", "💼 By Role", "🏢 By Company",
# #                     "📍 By Location", "🌐 By Portal"])

# #     with tabs[0]:
# #         all_sk = [s for skills in df['skills'] for s in skills]
# #         sc = Counter(all_sk).most_common(20)
# #         if sc:
# #             sdf = pd.DataFrame(sc, columns=['Skill', 'Jobs'])
# #             fig = px.bar(sdf, x='Jobs', y='Skill', orientation='h',
# #                          title='Top 20 Skills', color='Jobs',
# #                          color_continuous_scale='RdYlGn', text='Jobs')
# #             fig.update_layout(height=650, showlegend=False,
# #                               yaxis=dict(autorange="reversed"),
# #                               clickmode='event+select')
# #             fig.update_traces(textposition='outside')
# #             ev = st.plotly_chart(fig, use_container_width=True,
# #                                  on_select="rerun", key="main_skill")
# #             if ev and ev.get("selection") and ev["selection"].get("points"):
# #                 c = ev["selection"]["points"][0].get("y")
# #                 if c and (st.session_state.drill_type != "Skill" or st.session_state.drill_value != c):
# #                     st.session_state.drill_type = "Skill"
# #                     st.session_state.drill_value = c
# #                     st.rerun()

# #     with tabs[1]:
# #         tc = df['title'].value_counts().head(20).reset_index()
# #         tc.columns = ['Job Role', 'Openings']
# #         fig = px.bar(tc, x='Openings', y='Job Role', orientation='h',
# #                      title='Top 20 Roles', color='Openings',
# #                      color_continuous_scale='Viridis', text='Openings')
# #         fig.update_layout(height=650, showlegend=False,
# #                           yaxis=dict(autorange="reversed"),
# #                           clickmode='event+select')
# #         fig.update_traces(textposition='outside')
# #         ev = st.plotly_chart(fig, use_container_width=True,
# #                              on_select="rerun", key="main_role")
# #         if ev and ev.get("selection") and ev["selection"].get("points"):
# #             c = ev["selection"]["points"][0].get("y")
# #             if c and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != c):
# #                 st.session_state.drill_type = "Job Role"
# #                 st.session_state.drill_value = c
# #                 st.rerun()

# #     with tabs[2]:
# #         cc = df['company'].value_counts().head(20).reset_index()
# #         cc.columns = ['Company', 'Openings']
# #         fig = px.bar(cc, x='Openings', y='Company', orientation='h',
# #                      title='Top 20 Companies', color='Openings',
# #                      color_continuous_scale='Cividis', text='Openings')
# #         fig.update_layout(height=650, showlegend=False,
# #                           yaxis=dict(autorange="reversed"),
# #                           clickmode='event+select')
# #         fig.update_traces(textposition='outside')
# #         ev = st.plotly_chart(fig, use_container_width=True,
# #                              on_select="rerun", key="main_company")
# #         if ev and ev.get("selection") and ev["selection"].get("points"):
# #             c = ev["selection"]["points"][0].get("y")
# #             if c and (st.session_state.drill_type != "Company" or st.session_state.drill_value != c):
# #                 st.session_state.drill_type = "Company"
# #                 st.session_state.drill_value = c
# #                 st.rerun()

# #     with tabs[3]:
# #         lc = df['location'].value_counts().head(20).reset_index()
# #         lc.columns = ['Location', 'Openings']
# #         fig = px.bar(lc, x='Location', y='Openings',
# #                      title='Top 20 Locations', color='Openings',
# #                      color_continuous_scale='Turbo', text='Openings')
# #         fig.update_layout(height=500, showlegend=False,
# #                           xaxis_tickangle=-40, clickmode='event+select')
# #         fig.update_traces(textposition='outside')
# #         ev = st.plotly_chart(fig, use_container_width=True,
# #                              on_select="rerun", key="main_loc")
# #         if ev and ev.get("selection") and ev["selection"].get("points"):
# #             c = ev["selection"]["points"][0].get("x")
# #             if c and (st.session_state.drill_type != "Location" or st.session_state.drill_value != c):
# #                 st.session_state.drill_type = "Location"
# #                 st.session_state.drill_value = c
# #                 st.rerun()

# #     with tabs[4]:
# #         pc = df['platform'].value_counts().reset_index()
# #         pc.columns = ['Portal', 'Openings']
# #         c1, c2 = st.columns(2)
# #         with c1:
# #             fig = px.bar(pc, x='Portal', y='Openings',
# #                          title='Portals', color='Openings',
# #                          color_continuous_scale='Plasma', text='Openings')
# #             fig.update_layout(height=450, showlegend=False,
# #                               xaxis_tickangle=-30, clickmode='event+select')
# #             fig.update_traces(textposition='outside')
# #             ev = st.plotly_chart(fig, use_container_width=True,
# #                                  on_select="rerun", key="main_portal")
# #             if ev and ev.get("selection") and ev["selection"].get("points"):
# #                 c = ev["selection"]["points"][0].get("x")
# #                 if c and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != c):
# #                     st.session_state.drill_type = "Portal"
# #                     st.session_state.drill_value = c
# #                     st.rerun()

# #         with c2:
# #             fig = px.pie(pc, values='Openings', names='Portal',
# #                          title='Distribution', hole=0.4,
# #                          color_discrete_sequence=px.colors.qualitative.Set3)
# #             fig.update_traces(textinfo='percent+label',
# #                               textposition='outside', textfont_size=11,
# #                               pull=[0.03] * len(pc))
# #             fig.update_layout(height=450)
# #             st.plotly_chart(fig, use_container_width=True, key="main_portal_pie")

# # # ============================================================================
# # # FOOTER
# # # ============================================================================
# # st.markdown("---")
# # st.markdown(f"""<div style='text-align:center; color:#666; font-size:12px;'>
# #     Job Market Analytics | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
# #     {len(df)} total jobs | {(df['is_remote']=='Yes').sum()} remote
# # </div>""", unsafe_allow_html=True)


















# """
# ================================================================================
# JOB MARKET ANALYTICS — CLICKABLE KPI + REMOTE DRILL-DOWN (FIXED TEXT)
# Run: python -m streamlit run dashboard.py
# ================================================================================
# """

# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# from collections import Counter
# from datetime import datetime
# import warnings
# import logging

# warnings.filterwarnings('ignore')
# logging.getLogger('streamlit').setLevel(logging.ERROR)

# # ============================================================================
# # PAGE CONFIG
# # ============================================================================
# st.set_page_config(
#     page_title="Job Market Analytics",
#     page_icon="🎯",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ============================================================================
# # CSS — FORCES DARK TEXT EVERYWHERE
# # ============================================================================
# st.markdown("""
# <style>
    /* ========== FORCE DARK TEXT EVERYWHERE ========== */
    .stApp, .stApp * {
        color: #1a1a1a !important;
    }
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricLabel"] > div {
        color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stDataFrame"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
    }
#     /* ========== FORCE DARK TEXT ON EVERYTHING ========== */
#     .stApp, .stApp * {
#         color: #1a1a1a !important;
#     }

#     /* Metric values (numbers) */
#     div[data-testid="stMetricValue"] > div,
#     div[data-testid="stMetricLabel"] > div {
#         color: #1a1a1a !important;
#     }

#     /* Dataframe text */
#     div[data-testid="stDataFrame"] * {
#         color: #1a1a1a !important;
#     }

#     /* Sidebar text */
#     section[data-testid="stSidebar"] * {
#         color: #1a1a1a !important;
#     }

#     /* Buttons — keep white text */
#     div[data-testid="stButton"] button,
#     div[data-testid="stButton"] button *,
#     div[data-testid="stButton"] button p {
#         color: #FFFFFF !important;
#     }

#     /* ========== HEADERS ========== */
#     .main-header {
#         font-size: 2.2rem; font-weight: bold;
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         text-align: center; padding: 0.5rem 0;
#     }
#     .sub-header {
#         text-align: center; color: #555 !important;
#         margin-bottom: 1.2rem; font-size: 0.95rem;
#     }

#     /* ========== PROBLEM HEADER ========== */
#     .problem-header {
#         background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
#         padding: 0.7rem 1rem; border-radius: 8px;
#         color: #FFFFFF !important; font-weight: bold;
#         margin-bottom: 1rem; font-size: 0.95rem;
#     }
#     .problem-header * { color: #FFFFFF !important; }

#     /* ========== INSIGHT BOX ========== */
#     .insight-box {
#         background: #f0f7ff; padding: 0.8rem;
#         border-left: 4px solid #667eea; border-radius: 5px;
#         margin: 0.6rem 0; font-size: 0.88rem;
#         color: #1a1a1a !important;
#     }
#     .insight-box * { color: #1a1a1a !important; }
#     .insight-box strong { color: #2c3e50 !important; font-weight: 700; }

#     /* ========== DRILL HEADER ========== */
#     .drill-header {
#         background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
#         padding: 0.8rem 1rem; border-radius: 8px;
#         color: #0d3d2c !important; font-weight: bold;
#         margin: 1rem 0; font-size: 1.05rem;
#         border: 2px solid #43e97b;
#     }
#     .drill-header * { color: #0d3d2c !important; }

#     /* ========== TABS ========== */
#     .stTabs [data-baseweb="tab-list"] { gap: 6px; flex-wrap: wrap; }
#     .stTabs [data-baseweb="tab"] {
#         background-color: #f0f2f6; border-radius: 6px;
#         padding: 8px 12px; font-weight: 600; font-size: 0.78rem;
#         color: #1a1a1a !important;
#     }
#     .stTabs [aria-selected="true"] {
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#     }
#     .stTabs [aria-selected="true"] * { color: #FFFFFF !important; }

#     /* ========== KPI BUTTON CARDS — SHORT & CLEAN ========== */
#     div[data-testid="stButton"] button {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: #FFFFFF !important;
#         border: none;
#         padding: 0.8rem 0.4rem;
#         border-radius: 10px;
#         width: 100%;
#         min-height: 95px;
#         box-shadow: 0 3px 10px rgba(0,0,0,0.15);
#         transition: transform 0.2s;
#         white-space: normal;
#         word-wrap: break-word;
#     }
#     div[data-testid="stButton"] button:hover {
#         transform: translateY(-3px);
#         box-shadow: 0 6px 16px rgba(0,0,0,0.25);
#     }
#     div[data-testid="stButton"] button p {
#         color: #FFFFFF !important;
#         font-size: 0.82rem !important;
#         font-weight: 700 !important;
#         line-height: 1.35 !important;
#         margin: 0 !important;
#         text-align: center;
#     }

#     /* Force dark on everything else */
#     h1, h2, h3, h4, h5, h6, p, span, div, label {
#         color: #1a1a1a;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ============================================================================
# # DATA LOADING
# # ============================================================================

# @st.cache_data
# def load_data():
#     df = pd.read_csv("job_data_clean.csv")
#     df['posted_date'] = pd.to_datetime(df['posted_date'], errors='coerce')
#     return df

# def extract_skills(text):
#     if pd.isna(text):
#         return []
#     text = str(text).lower()
#     skill_list = [
#         'python', 'java', 'sql', 'javascript', 'typescript', 'react', 'angular',
#         'node.js', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
#         'jenkins', 'spark', 'kafka', 'airflow', 'snowflake', 'tableau', 'power bi',
#         'machine learning', 'deep learning', 'nlp', 'llm', 'genai', 'rag',
#         'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
#         'excel', 'git', 'linux', 'agile', 'scrum', 'jira'
#     ]
#     return list(set([s for s in skill_list if s in text]))

# try:
#     df = load_data()
#     df['skills'] = df['description'].apply(extract_skills)
#     df['skill_count'] = df['skills'].apply(len)
# except Exception as e:
#     st.error(f"❌ Error loading 'job_data_clean.csv': {e}")
#     st.stop()

# # ============================================================================
# # HEADER
# # ============================================================================
# st.markdown('<h1 class="main-header">🎯 Job Market Analytics</h1>', unsafe_allow_html=True)
# st.markdown('<p class="sub-header">Click any KPI card → see detailed breakdown</p>', unsafe_allow_html=True)

# # ============================================================================
# # SESSION STATE
# # ============================================================================
# for key in ['view', 'drill_type', 'drill_value']:
#     if key not in st.session_state:
#         st.session_state[key] = None

# # Sidebar
# st.sidebar.markdown("## 🔍 Navigation")
# if st.sidebar.button("🏠 Home (Clear View)"):
#     st.session_state.view = None
#     st.session_state.drill_type = None
#     st.session_state.drill_value = None
#     st.rerun()

# if st.session_state.view:
#     st.sidebar.success(f"**Viewing:** {st.session_state.view}")

# if st.session_state.drill_type:
#     st.sidebar.info(f"**Drill:** {st.session_state.drill_type} = {st.session_state.drill_value}")
#     if st.sidebar.button("❌ Clear Drill"):
#         st.session_state.drill_type = None
#         st.session_state.drill_value = None
#         st.rerun()

# st.sidebar.markdown("---")
# st.sidebar.markdown(f"**📊 Total Jobs:** {len(df)}")
# st.sidebar.markdown(f"**🏠 Remote Jobs:** {(df['is_remote']=='Yes').sum()}")

# # ============================================================================
# # KPI CARDS — SHORT NAMES, CLEAN LAYOUT
# # ============================================================================
# st.markdown("## 📈 Overview — Click to Explore")

# k1, k2, k3, k4, k5, k6 = st.columns(6)

# with k1:
#     if st.button(f"📊 Jobs\n\n{len(df)}",
#                  key="kpi_total", use_container_width=True):
#         st.session_state.view = "Total Jobs"
#         st.session_state.drill_type = None
#         st.rerun()

# with k2:
#     if st.button(f"🏢 Companies\n\n{df['company'].nunique()}",
#                  key="kpi_company", use_container_width=True):
#         st.session_state.view = "Companies"
#         st.session_state.drill_type = None
#         st.rerun()

# with k3:
#     if st.button(f"💼 Roles\n\n{df['title'].nunique()}",
#                  key="kpi_title", use_container_width=True):
#         st.session_state.view = "Job Roles"
#         st.session_state.drill_type = None
#         st.rerun()

# with k4:
#     if st.button(f"🌐 Portals\n\n{df['platform'].nunique()}",
#                  key="kpi_portal", use_container_width=True):
#         st.session_state.view = "Portals"
#         st.session_state.drill_type = None
#         st.rerun()

# with k5:
#     if st.button(f"📍 Cities\n\n{df['location'].nunique()}",
#                  key="kpi_location", use_container_width=True):
#         st.session_state.view = "Locations"
#         st.session_state.drill_type = None
#         st.rerun()

# with k6:
#     remote_count = (df['is_remote'] == 'Yes').sum()
#     if st.button(f"🏠 Remote\n\n{remote_count}",
#                  key="kpi_remote", use_container_width=True):
#         st.session_state.view = "Remote Jobs"
#         st.session_state.drill_type = None
#         st.rerun()

# st.markdown("---")

# # ============================================================================
# # VIEW: REMOTE JOBS — DETAILED BREAKDOWN
# # ============================================================================
# if st.session_state.view == "Remote Jobs":
#     st.markdown('<div class="drill-header">🏠 Remote Jobs — Complete Breakdown</div>', unsafe_allow_html=True)

#     remote_df = df[df['is_remote'] == 'Yes']

#     if len(remote_df) == 0:
#         st.warning("No remote jobs found in the dataset.")
#     else:
#         d1, d2, d3, d4, d5 = st.columns(5)
#         with d1: st.metric("🏠 Total Remote Jobs", len(remote_df))
#         with d2: st.metric("🏢 Companies", remote_df['company'].nunique())
#         with d3: st.metric("📍 Locations", remote_df['location'].nunique())
#         with d4: st.metric("💼 Job Roles", remote_df['title'].nunique())
#         with d5: st.metric("🌐 Portals", remote_df['platform'].nunique())

#         st.markdown("---")

#         # Section 1: Remote Companies
#         st.markdown("### 🏢 Companies Hiring Remote")
#         c1, c2 = st.columns([3, 2])

#         with c1:
#             rc = remote_df['company'].value_counts().reset_index()
#             rc.columns = ['Company', 'Remote Jobs']
#             fig = px.bar(
#                 rc, x='Remote Jobs', y='Company', orientation='h',
#                 title=f'All {len(rc)} Companies Hiring Remote — Click a bar',
#                 color='Remote Jobs', color_continuous_scale='Greens', text='Remote Jobs'
#             )
#             fig.update_layout(
#                 height=max(400, len(rc)*35), showlegend=False,
#                 yaxis=dict(autorange="reversed"), title_font_size=14,
#                 clickmode='event+select'
#             )
#             fig.update_traces(textposition='outside')

#             event = st.plotly_chart(fig, use_container_width=True,
#                                     on_select="rerun", key="remote_company_drill")

#             if event and event.get("selection") and event["selection"].get("points"):
#                 clicked = event["selection"]["points"][0].get("y")
#                 if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
#                     st.session_state.drill_type = "Company"
#                     st.session_state.drill_value = clicked
#                     st.rerun()

#         with c2:
#             st.markdown("#### 📋 Company List (Remote)")
#             st.dataframe(rc, use_container_width=True, height=400, hide_index=True)

#         # Section 2: Remote Locations
#         st.markdown("### 📍 Remote Jobs by Location / Area")
#         c3, c4 = st.columns([3, 2])

#         with c3:
#             rl = remote_df['location'].value_counts().reset_index()
#             rl.columns = ['Location', 'Remote Jobs']
#             fig = px.bar(
#                 rl, x='Remote Jobs', y='Location', orientation='h',
#                 title='Remote Jobs by Location — Click a bar',
#                 color='Remote Jobs', color_continuous_scale='Teal', text='Remote Jobs'
#             )
#             fig.update_layout(
#                 height=max(400, len(rl)*35), showlegend=False,
#                 yaxis=dict(autorange="reversed"), title_font_size=14,
#                 clickmode='event+select'
#             )
#             fig.update_traces(textposition='outside')

#             event = st.plotly_chart(fig, use_container_width=True,
#                                     on_select="rerun", key="remote_loc_drill")

#             if event and event.get("selection") and event["selection"].get("points"):
#                 clicked = event["selection"]["points"][0].get("y")
#                 if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
#                     st.session_state.drill_type = "Location"
#                     st.session_state.drill_value = clicked
#                     st.rerun()

#         with c4:
#             st.markdown("#### 📋 Location List (Remote)")
#             st.dataframe(rl, use_container_width=True, height=400, hide_index=True)

#         # Section 3: Portals
#         st.markdown("### 🌐 Which Portals Post Remote Jobs?")
#         c5, c6 = st.columns([2, 2])

#         with c5:
#             rp = remote_df['platform'].value_counts().reset_index()
#             rp.columns = ['Portal', 'Remote Jobs']
#             fig = px.bar(
#                 rp, x='Portal', y='Remote Jobs',
#                 title='Remote Jobs by Portal — Click a bar',
#                 color='Remote Jobs', color_continuous_scale='Blues', text='Remote Jobs'
#             )
#             fig.update_layout(height=400, showlegend=False,
#                               xaxis_tickangle=-30, title_font_size=13,
#                               clickmode='event+select')
#             fig.update_traces(textposition='outside')

#             event = st.plotly_chart(fig, use_container_width=True,
#                                     on_select="rerun", key="remote_portal_drill")

#             if event and event.get("selection") and event["selection"].get("points"):
#                 clicked = event["selection"]["points"][0].get("x")
#                 if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
#                     st.session_state.drill_type = "Portal"
#                     st.session_state.drill_value = clicked
#                     st.rerun()

#         with c6:
#             fig = px.pie(
#                 rp, values='Remote Jobs', names='Portal',
#                 title='Remote Jobs — Portal Share',
#                 hole=0.4,
#                 color_discrete_sequence=px.colors.qualitative.Set3
#             )
#             fig.update_traces(textinfo='percent+label', textposition='outside',
#                               textfont_size=11, pull=[0.03] * len(rp))
#             fig.update_layout(height=400, title_font_size=13)
#             st.plotly_chart(fig, use_container_width=True, key="remote_portal_pie")

#         # Section 4: Roles
#         st.markdown("### 💼 What Job Roles Are Remote?")
#         rr = remote_df['title'].value_counts().reset_index()
#         rr.columns = ['Job Role', 'Remote Jobs']
#         fig = px.bar(
#             rr, x='Remote Jobs', y='Job Role', orientation='h',
#             title='Remote Job Roles — Click a bar',
#             color='Remote Jobs', color_continuous_scale='Purples', text='Remote Jobs'
#         )
#         fig.update_layout(
#             height=max(400, len(rr)*35), showlegend=False,
#             yaxis=dict(autorange="reversed"), title_font_size=14,
#             clickmode='event+select'
#         )
#         fig.update_traces(textposition='outside')

#         event = st.plotly_chart(fig, use_container_width=True,
#                                 on_select="rerun", key="remote_role_drill")

#         if event and event.get("selection") and event["selection"].get("points"):
#             clicked = event["selection"]["points"][0].get("y")
#             if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
#                 st.session_state.drill_type = "Job Role"
#                 st.session_state.drill_value = clicked
#                 st.rerun()

#         # Section 5: Skills
#         st.markdown("### 🛠️ Top Skills Required for Remote Jobs")
#         all_rs = [s for skills in remote_df['skills'] for s in skills]
#         rs = Counter(all_rs).most_common(15)

#         if rs:
#             rs_df = pd.DataFrame(rs, columns=['Skill', 'Jobs'])
#             rs_df['% of Remote'] = (rs_df['Jobs'] / len(remote_df) * 100).round(1)
#             fig = px.bar(
#                 rs_df, x='Jobs', y='Skill', orientation='h',
#                 title='Top Skills for Remote Jobs',
#                 color='Jobs', color_continuous_scale='Greens', text='Jobs'
#             )
#             fig.update_layout(height=500, showlegend=False,
#                               yaxis=dict(autorange="reversed"), title_font_size=14)
#             fig.update_traces(textposition='outside')
#             st.plotly_chart(fig, use_container_width=True, key="remote_skills")

#         # Section 6: Full List
#         st.markdown("### 📋 All Remote Job Openings")
#         show_cols = ['title', 'company', 'location', 'platform',
#                      'employment_type', 'posted_date']
#         display_remote = remote_df[show_cols].copy()
#         display_remote.columns = ['Job Title', 'Company', 'Location', 'Portal',
#                                   'Type', 'Posted']
#         st.dataframe(display_remote, use_container_width=True, height=500)

#         csv = remote_df.to_csv(index=False)
#         st.download_button(
#             label="📥 Download All Remote Jobs (CSV)",
#             data=csv,
#             file_name=f"remote_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
#             mime="text/csv",
#             key="dl_remote"
#         )

#         # Insight
#         top_comp = remote_df['company'].value_counts().index[0]
#         top_loc = remote_df['location'].value_counts().index[0]
#         top_portal = remote_df['platform'].value_counts().index[0]

#         st.markdown(f"""<div class="insight-box">
#             <strong>📊 Remote Job Summary:</strong><br>
#             🏢 <strong>Top Remote Employer:</strong> {top_comp}<br>
#             📍 <strong>Top Remote Location:</strong> {top_loc}<br>
#             🌐 <strong>Top Portal for Remote:</strong> {top_portal}<br>
#             🛠️ <strong>Top Skill for Remote:</strong> {rs[0][0] if rs else 'N/A'}<br>
#             📊 <strong>Remote % of Total:</strong> {len(remote_df)/len(df)*100:.1f}%
#         </div>""", unsafe_allow_html=True)

# # ============================================================================
# # OTHER VIEWS
# # ============================================================================
# elif st.session_state.view == "Companies":
#     st.markdown('<div class="drill-header">🏢 All Companies Hiring</div>', unsafe_allow_html=True)
#     comp_df = df['company'].value_counts().reset_index()
#     comp_df.columns = ['Company', 'Openings']
#     comp_df['Share %'] = (comp_df['Openings'] / len(df) * 100).round(2)

#     c1, c2 = st.columns([3, 2])
#     with c1:
#         fig = px.bar(comp_df.head(30), x='Openings', y='Company', orientation='h',
#                      title=f'All {len(comp_df)} Companies (Top 30) — Click a bar',
#                      color='Openings', color_continuous_scale='Viridis', text='Openings')
#         fig.update_layout(height=800, showlegend=False,
#                           yaxis=dict(autorange="reversed"),
#                           title_font_size=14, clickmode='event+select')
#         fig.update_traces(textposition='outside')
#         event = st.plotly_chart(fig, use_container_width=True,
#                                 on_select="rerun", key="comp_view_drill")
#         if event and event.get("selection") and event["selection"].get("points"):
#             clicked = event["selection"]["points"][0].get("y")
#             if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
#                 st.session_state.drill_type = "Company"
#                 st.session_state.drill_value = clicked
#                 st.rerun()

#     with c2:
#         st.markdown("### 📋 Complete List")
#         st.dataframe(comp_df, use_container_width=True, height=750, hide_index=True)

#     csv = comp_df.to_csv(index=False)
#     st.download_button("📥 Download CSV", csv,
#                        file_name=f"companies_{datetime.now().strftime('%Y%m%d')}.csv",
#                        mime="text/csv", key="dl_comp_view")

# elif st.session_state.view == "Locations":
#     st.markdown('<div class="drill-header">📍 All Locations</div>', unsafe_allow_html=True)
#     loc_df = df['location'].value_counts().reset_index()
#     loc_df.columns = ['Location', 'Openings']
#     loc_df['Share %'] = (loc_df['Openings'] / len(df) * 100).round(2)

#     c1, c2 = st.columns([3, 2])
#     with c1:
#         fig = px.bar(loc_df, x='Openings', y='Location', orientation='h',
#                      title=f'All {len(loc_df)} Locations — Click a bar',
#                      color='Openings', color_continuous_scale='Magma', text='Openings')
#         fig.update_layout(height=max(600, len(loc_df)*22), showlegend=False,
#                           yaxis=dict(autorange="reversed"),
#                           title_font_size=14, clickmode='event+select')
#         fig.update_traces(textposition='outside')
#         event = st.plotly_chart(fig, use_container_width=True,
#                                 on_select="rerun", key="loc_view_drill")
#         if event and event.get("selection") and event["selection"].get("points"):
#             clicked = event["selection"]["points"][0].get("y")
#             if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
#                 st.session_state.drill_type = "Location"
#                 st.session_state.drill_value = clicked
#                 st.rerun()

#     with c2:
#         st.markdown("### 📋 Complete List")
#         st.dataframe(loc_df, use_container_width=True, height=750, hide_index=True)

#     csv = loc_df.to_csv(index=False)
#     st.download_button("📥 Download CSV", csv,
#                        file_name=f"locations_{datetime.now().strftime('%Y%m%d')}.csv",
#                        mime="text/csv", key="dl_loc_view")

# elif st.session_state.view == "Job Roles":
#     st.markdown('<div class="drill-header">💼 All Job Roles</div>', unsafe_allow_html=True)
#     role_df = df['title'].value_counts().reset_index()
#     role_df.columns = ['Job Role', 'Openings']
#     role_df['Share %'] = (role_df['Openings'] / len(df) * 100).round(2)

#     c1, c2 = st.columns([3, 2])
#     with c1:
#         fig = px.bar(role_df.head(40), x='Openings', y='Job Role', orientation='h',
#                      title=f'All {len(role_df)} Job Roles (Top 40) — Click a bar',
#                      color='Openings', color_continuous_scale='Plasma', text='Openings')
#         fig.update_layout(height=1000, showlegend=False,
#                           yaxis=dict(autorange="reversed"),
#                           title_font_size=14, clickmode='event+select')
#         fig.update_traces(textposition='outside')
#         event = st.plotly_chart(fig, use_container_width=True,
#                                 on_select="rerun", key="role_view_drill")
#         if event and event.get("selection") and event["selection"].get("points"):
#             clicked = event["selection"]["points"][0].get("y")
#             if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
#                 st.session_state.drill_type = "Job Role"
#                 st.session_state.drill_value = clicked
#                 st.rerun()

#     with c2:
#         st.markdown("### 📋 Complete List")
#         st.dataframe(role_df, use_container_width=True, height=950, hide_index=True)

#     csv = role_df.to_csv(index=False)
#     st.download_button("📥 Download CSV", csv,
#                        file_name=f"roles_{datetime.now().strftime('%Y%m%d')}.csv",
#                        mime="text/csv", key="dl_role_view")

# elif st.session_state.view == "Portals":
#     st.markdown('<div class="drill-header">🌐 All Portals</div>', unsafe_allow_html=True)
#     portal_df = df['platform'].value_counts().reset_index()
#     portal_df.columns = ['Portal', 'Openings']
#     portal_df['Share %'] = (portal_df['Openings'] / len(df) * 100).round(2)

#     c1, c2 = st.columns(2)
#     with c1:
#         fig = px.bar(portal_df, x='Portal', y='Openings',
#                      title='Portals — Click a bar',
#                      color='Openings', color_continuous_scale='Turbo', text='Openings')
#         fig.update_layout(height=450, showlegend=False,
#                           xaxis_tickangle=-30, title_font_size=13,
#                           clickmode='event+select')
#         fig.update_traces(textposition='outside')
#         event = st.plotly_chart(fig, use_container_width=True,
#                                 on_select="rerun", key="portal_view_drill")
#         if event and event.get("selection") and event["selection"].get("points"):
#             clicked = event["selection"]["points"][0].get("x")
#             if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
#                 st.session_state.drill_type = "Portal"
#                 st.session_state.drill_value = clicked
#                 st.rerun()

#     with c2:
#         st.markdown("### 📋 Complete List")
#         st.dataframe(portal_df, use_container_width=True, hide_index=True)

#     csv = portal_df.to_csv(index=False)
#     st.download_button("📥 Download CSV", csv,
#                        file_name=f"portals_{datetime.now().strftime('%Y%m%d')}.csv",
#                        mime="text/csv", key="dl_portal_view")

# elif st.session_state.view == "Total Jobs":
#     st.markdown('<div class="drill-header">📊 All Jobs in Dataset</div>', unsafe_allow_html=True)
#     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
#                  'employment_type', 'posted_date']
#     display_df = df[show_cols].copy()
#     display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
#                           'Remote', 'Type', 'Posted']
#     st.dataframe(display_df, use_container_width=True, height=600)
#     csv = df.to_csv(index=False)
#     st.download_button("📥 Download All Jobs (CSV)", csv,
#                        file_name=f"all_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
#                        mime="text/csv", key="dl_total_view")

# # ============================================================================
# # DRILL-DOWN PANEL
# # ============================================================================
# if st.session_state.drill_type and st.session_state.drill_value:
#     st.markdown("---")
#     drill_val = st.session_state.drill_value
#     drill_type = st.session_state.drill_type

#     st.markdown(f'<div class="drill-header">🎯 Drill-Down: {drill_type} = "{drill_val}"</div>', unsafe_allow_html=True)

#     if drill_type == "Skill":
#         drill_df = df[df['skills'].apply(lambda x: drill_val in x)]
#     elif drill_type == "Job Role":
#         drill_df = df[df['title'] == drill_val]
#     elif drill_type == "Company":
#         drill_df = df[df['company'] == drill_val]
#     elif drill_type == "Location":
#         drill_df = df[df['location'] == drill_val]
#     elif drill_type == "Portal":
#         drill_df = df[df['platform'] == drill_val]
#     else:
#         drill_df = df.copy()

#     d1, d2, d3, d4 = st.columns(4)
#     with d1: st.metric("🎯 Total Openings", len(drill_df))
#     with d2: st.metric("🏢 Companies", drill_df['company'].nunique())
#     with d3: st.metric("📍 Locations", drill_df['location'].nunique())
#     with d4:
#         rp = (drill_df['is_remote'] == 'Yes').sum() / len(drill_df) * 100 if len(drill_df) > 0 else 0
#         st.metric("🏠 Remote %", f"{rp:.1f}%")

#     g1, g2 = st.columns(2)
#     with g1:
#         pc = drill_df['platform'].value_counts().reset_index()
#         pc.columns = ['Portal', 'Openings']
#         fig = px.bar(pc, x='Openings', y='Portal', orientation='h',
#                      title='By Portal', color='Openings',
#                      color_continuous_scale='Blues', text='Openings')
#         fig.update_layout(height=350, showlegend=False,
#                           yaxis=dict(autorange="reversed"), title_font_size=13)
#         fig.update_traces(textposition='outside')
#         st.plotly_chart(fig, use_container_width=True, key=f"dd_p_{drill_val}")

#     with g2:
#         cc = drill_df['company'].value_counts().head(10).reset_index()
#         cc.columns = ['Company', 'Openings']
#         fig = px.bar(cc, x='Openings', y='Company', orientation='h',
#                      title='By Company', color='Openings',
#                      color_continuous_scale='Viridis', text='Openings')
#         fig.update_layout(height=350, showlegend=False,
#                           yaxis=dict(autorange="reversed"), title_font_size=13)
#         fig.update_traces(textposition='outside')
#         st.plotly_chart(fig, use_container_width=True, key=f"dd_c_{drill_val}")

#     st.markdown("### 📋 All Job Openings")
#     show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
#                  'employment_type', 'posted_date']
#     ddf = drill_df[show_cols].copy()
#     ddf.columns = ['Job Title', 'Company', 'Location', 'Portal',
#                    'Remote', 'Type', 'Posted']
#     st.dataframe(ddf, use_container_width=True, height=400)

#     csv = drill_df.to_csv(index=False)
#     st.download_button("📥 Download (CSV)", csv,
#                        file_name=f"drill_{drill_type}_{drill_val}.csv",
#                        mime="text/csv", key=f"dl_dd_{drill_val}")

# # ============================================================================
# # MAIN TABS (when no view is active)
# # ============================================================================
# if st.session_state.view is None:
#     st.markdown("---")
#     st.markdown("## 🔎 Explore Charts — Click to drill down")

#     tabs = st.tabs(["🛠️ By Skill", "💼 By Role", "🏢 By Company",
#                     "📍 By Location", "🌐 By Portal"])

#     with tabs[0]:
#         all_sk = [s for skills in df['skills'] for s in skills]
#         sc = Counter(all_sk).most_common(20)
#         if sc:
#             sdf = pd.DataFrame(sc, columns=['Skill', 'Jobs'])
#             fig = px.bar(sdf, x='Jobs', y='Skill', orientation='h',
#                          title='Top 20 Skills', color='Jobs',
#                          color_continuous_scale='RdYlGn', text='Jobs')
#             fig.update_layout(height=650, showlegend=False,
#                               yaxis=dict(autorange="reversed"),
#                               clickmode='event+select')
#             fig.update_traces(textposition='outside')
#             ev = st.plotly_chart(fig, use_container_width=True,
#                                  on_select="rerun", key="main_skill")
#             if ev and ev.get("selection") and ev["selection"].get("points"):
#                 c = ev["selection"]["points"][0].get("y")
#                 if c and (st.session_state.drill_type != "Skill" or st.session_state.drill_value != c):
#                     st.session_state.drill_type = "Skill"
#                     st.session_state.drill_value = c
#                     st.rerun()

#     with tabs[1]:
#         tc = df['title'].value_counts().head(20).reset_index()
#         tc.columns = ['Job Role', 'Openings']
#         fig = px.bar(tc, x='Openings', y='Job Role', orientation='h',
#                      title='Top 20 Roles', color='Openings',
#                      color_continuous_scale='Viridis', text='Openings')
#         fig.update_layout(height=650, showlegend=False,
#                           yaxis=dict(autorange="reversed"),
#                           clickmode='event+select')
#         fig.update_traces(textposition='outside')
#         ev = st.plotly_chart(fig, use_container_width=True,
#                              on_select="rerun", key="main_role")
#         if ev and ev.get("selection") and ev["selection"].get("points"):
#             c = ev["selection"]["points"][

































"""
================================================================================
JOB MARKET ANALYTICS — CLICKABLE KPI + REMOTE DRILL-DOWN (FIXED TEXT)
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

warnings.filterwarnings('ignore')
logging.getLogger('streamlit').setLevel(logging.ERROR)

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
# CSS — FORCES DARK TEXT EVERYWHERE
# ============================================================================
st.markdown("""
<style>
    /* ========== FORCE DARK TEXT EVERYWHERE ========== */
    .stApp, .stApp * {
        color: #1a1a1a !important;
    }
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricLabel"] > div {
        color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stDataFrame"] * {
        color: #1a1a1a !important;
    }
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
    }
    /* ========== FORCE DARK TEXT ON EVERYTHING ========== */
    .stApp, .stApp * {
        color: #1a1a1a !important;
    }

    /* Metric values (numbers) */
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricLabel"] > div {
        color: #1a1a1a !important;
    }

    /* Dataframe text */
    div[data-testid="stDataFrame"] * {
        color: #1a1a1a !important;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }

    /* Buttons — keep white text */
    div[data-testid="stButton"] button,
    div[data-testid="stButton"] button *,
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
    }

    /* ========== HEADERS ========== */
    .main-header {
        font-size: 2.2rem; font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; padding: 0.5rem 0;
    }
    .sub-header {
        text-align: center; color: #555 !important;
        margin-bottom: 1.2rem; font-size: 0.95rem;
    }

    /* ========== PROBLEM HEADER ========== */
    .problem-header {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 0.7rem 1rem; border-radius: 8px;
        color: #FFFFFF !important; font-weight: bold;
        margin-bottom: 1rem; font-size: 0.95rem;
    }
    .problem-header * { color: #FFFFFF !important; }

    /* ========== INSIGHT BOX ========== */
    .insight-box {
        background: #f0f7ff; padding: 0.8rem;
        border-left: 4px solid #667eea; border-radius: 5px;
        margin: 0.6rem 0; font-size: 0.88rem;
        color: #1a1a1a !important;
    }
    .insight-box * { color: #1a1a1a !important; }
    .insight-box strong { color: #2c3e50 !important; font-weight: 700; }

    /* ========== DRILL HEADER ========== */
    .drill-header {
        background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
        padding: 0.8rem 1rem; border-radius: 8px;
        color: #0d3d2c !important; font-weight: bold;
        margin: 1rem 0; font-size: 1.05rem;
        border: 2px solid #43e97b;
    }
    .drill-header * { color: #0d3d2c !important; }

    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6; border-radius: 6px;
        padding: 8px 12px; font-weight: 600; font-size: 0.78rem;
        color: #1a1a1a !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    .stTabs [aria-selected="true"] * { color: #FFFFFF !important; }

    /* ========== KPI BUTTON CARDS — SHORT & CLEAN ========== */
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
        white-space: normal;
        word-wrap: break-word;
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

    /* Force dark on everything else */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    df = pd.read_csv("job_data_clean.csv")
    df['posted_date'] = pd.to_datetime(df['posted_date'], errors='coerce')
    return df

def extract_skills(text):
    if pd.isna(text):
        return []
    text = str(text).lower()
    skill_list = [
        'python', 'java', 'sql', 'javascript', 'typescript', 'react', 'angular',
        'node.js', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
        'jenkins', 'spark', 'kafka', 'airflow', 'snowflake', 'tableau', 'power bi',
        'machine learning', 'deep learning', 'nlp', 'llm', 'genai', 'rag',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
        'excel', 'git', 'linux', 'agile', 'scrum', 'jira'
    ]
    return list(set([s for s in skill_list if s in text]))

try:
    df = load_data()
    df['skills'] = df['description'].apply(extract_skills)
    df['skill_count'] = df['skills'].apply(len)
except Exception as e:
    st.error(f"❌ Error loading 'job_data_clean.csv': {e}")
    st.stop()

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<h1 class="main-header">🎯 Job Market Analytics</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Click any KPI card → see detailed breakdown</p>', unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
for key in ['view', 'drill_type', 'drill_value']:
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
    st.sidebar.success(f"**Viewing:** {st.session_state.view}")

if st.session_state.drill_type:
    st.sidebar.info(f"**Drill:** {st.session_state.drill_type} = {st.session_state.drill_value}")
    if st.sidebar.button("❌ Clear Drill"):
        st.session_state.drill_type = None
        st.session_state.drill_value = None
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**📊 Total Jobs:** {len(df)}")
st.sidebar.markdown(f"**🏠 Remote Jobs:** {(df['is_remote']=='Yes').sum()}")

# ============================================================================
# KPI CARDS — SHORT NAMES, CLEAN LAYOUT
# ============================================================================
st.markdown("## 📈 Overview — Click to Explore")

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    if st.button(f"📊 Jobs\n\n{len(df)}",
                 key="kpi_total", use_container_width=True):
        st.session_state.view = "Total Jobs"
        st.session_state.drill_type = None
        st.rerun()

with k2:
    if st.button(f"🏢 Companies\n\n{df['company'].nunique()}",
                 key="kpi_company", use_container_width=True):
        st.session_state.view = "Companies"
        st.session_state.drill_type = None
        st.rerun()

with k3:
    if st.button(f"💼 Roles\n\n{df['title'].nunique()}",
                 key="kpi_title", use_container_width=True):
        st.session_state.view = "Job Roles"
        st.session_state.drill_type = None
        st.rerun()

with k4:
    if st.button(f"🌐 Portals\n\n{df['platform'].nunique()}",
                 key="kpi_portal", use_container_width=True):
        st.session_state.view = "Portals"
        st.session_state.drill_type = None
        st.rerun()

with k5:
    if st.button(f"📍 Cities\n\n{df['location'].nunique()}",
                 key="kpi_location", use_container_width=True):
        st.session_state.view = "Locations"
        st.session_state.drill_type = None
        st.rerun()

with k6:
    remote_count = (df['is_remote'] == 'Yes').sum()
    if st.button(f"🏠 Remote\n\n{remote_count}",
                 key="kpi_remote", use_container_width=True):
        st.session_state.view = "Remote Jobs"
        st.session_state.drill_type = None
        st.rerun()

st.markdown("---")

# ============================================================================
# VIEW: REMOTE JOBS — DETAILED BREAKDOWN
# ============================================================================
if st.session_state.view == "Remote Jobs":
    st.markdown('<div class="drill-header">🏠 Remote Jobs — Complete Breakdown</div>', unsafe_allow_html=True)

    remote_df = df[df['is_remote'] == 'Yes']

    if len(remote_df) == 0:
        st.warning("No remote jobs found in the dataset.")
    else:
        d1, d2, d3, d4, d5 = st.columns(5)
        with d1: st.metric("🏠 Total Remote Jobs", len(remote_df))
        with d2: st.metric("🏢 Companies", remote_df['company'].nunique())
        with d3: st.metric("📍 Locations", remote_df['location'].nunique())
        with d4: st.metric("💼 Job Roles", remote_df['title'].nunique())
        with d5: st.metric("🌐 Portals", remote_df['platform'].nunique())

        st.markdown("---")

        # Section 1: Remote Companies
        st.markdown("### 🏢 Companies Hiring Remote")
        c1, c2 = st.columns([3, 2])

        with c1:
            rc = remote_df['company'].value_counts().reset_index()
            rc.columns = ['Company', 'Remote Jobs']
            fig = px.bar(
                rc, x='Remote Jobs', y='Company', orientation='h',
                title=f'All {len(rc)} Companies Hiring Remote — Click a bar',
                color='Remote Jobs', color_continuous_scale='Greens', text='Remote Jobs'
            )
            fig.update_layout(
                height=max(400, len(rc)*35), showlegend=False,
                yaxis=dict(autorange="reversed"), title_font_size=14,
                clickmode='event+select'
            )
            fig.update_traces(textposition='outside')

            event = st.plotly_chart(fig, use_container_width=True,
                                    on_select="rerun", key="remote_company_drill")

            if event and event.get("selection") and event["selection"].get("points"):
                clicked = event["selection"]["points"][0].get("y")
                if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
                    st.session_state.drill_type = "Company"
                    st.session_state.drill_value = clicked
                    st.rerun()

        with c2:
            st.markdown("#### 📋 Company List (Remote)")
            st.dataframe(rc, use_container_width=True, height=400, hide_index=True)

        # Section 2: Remote Locations
        st.markdown("### 📍 Remote Jobs by Location / Area")
        c3, c4 = st.columns([3, 2])

        with c3:
            rl = remote_df['location'].value_counts().reset_index()
            rl.columns = ['Location', 'Remote Jobs']
            fig = px.bar(
                rl, x='Remote Jobs', y='Location', orientation='h',
                title='Remote Jobs by Location — Click a bar',
                color='Remote Jobs', color_continuous_scale='Teal', text='Remote Jobs'
            )
            fig.update_layout(
                height=max(400, len(rl)*35), showlegend=False,
                yaxis=dict(autorange="reversed"), title_font_size=14,
                clickmode='event+select'
            )
            fig.update_traces(textposition='outside')

            event = st.plotly_chart(fig, use_container_width=True,
                                    on_select="rerun", key="remote_loc_drill")

            if event and event.get("selection") and event["selection"].get("points"):
                clicked = event["selection"]["points"][0].get("y")
                if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
                    st.session_state.drill_type = "Location"
                    st.session_state.drill_value = clicked
                    st.rerun()

        with c4:
            st.markdown("#### 📋 Location List (Remote)")
            st.dataframe(rl, use_container_width=True, height=400, hide_index=True)

        # Section 3: Portals
        st.markdown("### 🌐 Which Portals Post Remote Jobs?")
        c5, c6 = st.columns([2, 2])

        with c5:
            rp = remote_df['platform'].value_counts().reset_index()
            rp.columns = ['Portal', 'Remote Jobs']
            fig = px.bar(
                rp, x='Portal', y='Remote Jobs',
                title='Remote Jobs by Portal — Click a bar',
                color='Remote Jobs', color_continuous_scale='Blues', text='Remote Jobs'
            )
            fig.update_layout(height=400, showlegend=False,
                              xaxis_tickangle=-30, title_font_size=13,
                              clickmode='event+select')
            fig.update_traces(textposition='outside')

            event = st.plotly_chart(fig, use_container_width=True,
                                    on_select="rerun", key="remote_portal_drill")

            if event and event.get("selection") and event["selection"].get("points"):
                clicked = event["selection"]["points"][0].get("x")
                if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
                    st.session_state.drill_type = "Portal"
                    st.session_state.drill_value = clicked
                    st.rerun()

        with c6:
            fig = px.pie(
                rp, values='Remote Jobs', names='Portal',
                title='Remote Jobs — Portal Share',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textinfo='percent+label', textposition='outside',
                              textfont_size=11, pull=[0.03] * len(rp))
            fig.update_layout(height=400, title_font_size=13)
            st.plotly_chart(fig, use_container_width=True, key="remote_portal_pie")

        # Section 4: Roles
        st.markdown("### 💼 What Job Roles Are Remote?")
        rr = remote_df['title'].value_counts().reset_index()
        rr.columns = ['Job Role', 'Remote Jobs']
        fig = px.bar(
            rr, x='Remote Jobs', y='Job Role', orientation='h',
            title='Remote Job Roles — Click a bar',
            color='Remote Jobs', color_continuous_scale='Purples', text='Remote Jobs'
        )
        fig.update_layout(
            height=max(400, len(rr)*35), showlegend=False,
            yaxis=dict(autorange="reversed"), title_font_size=14,
            clickmode='event+select'
        )
        fig.update_traces(textposition='outside')

        event = st.plotly_chart(fig, use_container_width=True,
                                on_select="rerun", key="remote_role_drill")

        if event and event.get("selection") and event["selection"].get("points"):
            clicked = event["selection"]["points"][0].get("y")
            if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
                st.session_state.drill_type = "Job Role"
                st.session_state.drill_value = clicked
                st.rerun()

        # Section 5: Skills
        st.markdown("### 🛠️ Top Skills Required for Remote Jobs")
        all_rs = [s for skills in remote_df['skills'] for s in skills]
        rs = Counter(all_rs).most_common(15)

        if rs:
            rs_df = pd.DataFrame(rs, columns=['Skill', 'Jobs'])
            rs_df['% of Remote'] = (rs_df['Jobs'] / len(remote_df) * 100).round(1)
            fig = px.bar(
                rs_df, x='Jobs', y='Skill', orientation='h',
                title='Top Skills for Remote Jobs',
                color='Jobs', color_continuous_scale='Greens', text='Jobs'
            )
            fig.update_layout(height=500, showlegend=False,
                              yaxis=dict(autorange="reversed"), title_font_size=14)
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True, key="remote_skills")

        # Section 6: Full List
        st.markdown("### 📋 All Remote Job Openings")
        show_cols = ['title', 'company', 'location', 'platform',
                     'employment_type', 'posted_date']
        display_remote = remote_df[show_cols].copy()
        display_remote.columns = ['Job Title', 'Company', 'Location', 'Portal',
                                  'Type', 'Posted']
        st.dataframe(display_remote, use_container_width=True, height=500)

        csv = remote_df.to_csv(index=False)
        st.download_button(
            label="📥 Download All Remote Jobs (CSV)",
            data=csv,
            file_name=f"remote_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="dl_remote"
        )

        # Insight
        top_comp = remote_df['company'].value_counts().index[0]
        top_loc = remote_df['location'].value_counts().index[0]
        top_portal = remote_df['platform'].value_counts().index[0]

        st.markdown(f"""<div class="insight-box">
            <strong>📊 Remote Job Summary:</strong><br>
            🏢 <strong>Top Remote Employer:</strong> {top_comp}<br>
            📍 <strong>Top Remote Location:</strong> {top_loc}<br>
            🌐 <strong>Top Portal for Remote:</strong> {top_portal}<br>
            🛠️ <strong>Top Skill for Remote:</strong> {rs[0][0] if rs else 'N/A'}<br>
            📊 <strong>Remote % of Total:</strong> {len(remote_df)/len(df)*100:.1f}%
        </div>""", unsafe_allow_html=True)

# ============================================================================
# OTHER VIEWS
# ============================================================================
elif st.session_state.view == "Companies":
    st.markdown('<div class="drill-header">🏢 All Companies Hiring</div>', unsafe_allow_html=True)
    comp_df = df['company'].value_counts().reset_index()
    comp_df.columns = ['Company', 'Openings']
    comp_df['Share %'] = (comp_df['Openings'] / len(df) * 100).round(2)

    c1, c2 = st.columns([3, 2])
    with c1:
        fig = px.bar(comp_df.head(30), x='Openings', y='Company', orientation='h',
                     title=f'All {len(comp_df)} Companies (Top 30) — Click a bar',
                     color='Openings', color_continuous_scale='Viridis', text='Openings')
        fig.update_layout(height=800, showlegend=False,
                          yaxis=dict(autorange="reversed"),
                          title_font_size=14, clickmode='event+select')
        fig.update_traces(textposition='outside')
        event = st.plotly_chart(fig, use_container_width=True,
                                on_select="rerun", key="comp_view_drill")
        if event and event.get("selection") and event["selection"].get("points"):
            clicked = event["selection"]["points"][0].get("y")
            if clicked and (st.session_state.drill_type != "Company" or st.session_state.drill_value != clicked):
                st.session_state.drill_type = "Company"
                st.session_state.drill_value = clicked
                st.rerun()

    with c2:
        st.markdown("### 📋 Complete List")
        st.dataframe(comp_df, use_container_width=True, height=750, hide_index=True)

    csv = comp_df.to_csv(index=False)
    st.download_button("📥 Download CSV", csv,
                       file_name=f"companies_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv", key="dl_comp_view")

elif st.session_state.view == "Locations":
    st.markdown('<div class="drill-header">📍 All Locations</div>', unsafe_allow_html=True)
    loc_df = df['location'].value_counts().reset_index()
    loc_df.columns = ['Location', 'Openings']
    loc_df['Share %'] = (loc_df['Openings'] / len(df) * 100).round(2)

    c1, c2 = st.columns([3, 2])
    with c1:
        fig = px.bar(loc_df, x='Openings', y='Location', orientation='h',
                     title=f'All {len(loc_df)} Locations — Click a bar',
                     color='Openings', color_continuous_scale='Magma', text='Openings')
        fig.update_layout(height=max(600, len(loc_df)*22), showlegend=False,
                          yaxis=dict(autorange="reversed"),
                          title_font_size=14, clickmode='event+select')
        fig.update_traces(textposition='outside')
        event = st.plotly_chart(fig, use_container_width=True,
                                on_select="rerun", key="loc_view_drill")
        if event and event.get("selection") and event["selection"].get("points"):
            clicked = event["selection"]["points"][0].get("y")
            if clicked and (st.session_state.drill_type != "Location" or st.session_state.drill_value != clicked):
                st.session_state.drill_type = "Location"
                st.session_state.drill_value = clicked
                st.rerun()

    with c2:
        st.markdown("### 📋 Complete List")
        st.dataframe(loc_df, use_container_width=True, height=750, hide_index=True)

    csv = loc_df.to_csv(index=False)
    st.download_button("📥 Download CSV", csv,
                       file_name=f"locations_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv", key="dl_loc_view")

elif st.session_state.view == "Job Roles":
    st.markdown('<div class="drill-header">💼 All Job Roles</div>', unsafe_allow_html=True)
    role_df = df['title'].value_counts().reset_index()
    role_df.columns = ['Job Role', 'Openings']
    role_df['Share %'] = (role_df['Openings'] / len(df) * 100).round(2)

    c1, c2 = st.columns([3, 2])
    with c1:
        fig = px.bar(role_df.head(40), x='Openings', y='Job Role', orientation='h',
                     title=f'All {len(role_df)} Job Roles (Top 40) — Click a bar',
                     color='Openings', color_continuous_scale='Plasma', text='Openings')
        fig.update_layout(height=1000, showlegend=False,
                          yaxis=dict(autorange="reversed"),
                          title_font_size=14, clickmode='event+select')
        fig.update_traces(textposition='outside')
        event = st.plotly_chart(fig, use_container_width=True,
                                on_select="rerun", key="role_view_drill")
        if event and event.get("selection") and event["selection"].get("points"):
            clicked = event["selection"]["points"][0].get("y")
            if clicked and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != clicked):
                st.session_state.drill_type = "Job Role"
                st.session_state.drill_value = clicked
                st.rerun()

    with c2:
        st.markdown("### 📋 Complete List")
        st.dataframe(role_df, use_container_width=True, height=950, hide_index=True)

    csv = role_df.to_csv(index=False)
    st.download_button("📥 Download CSV", csv,
                       file_name=f"roles_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv", key="dl_role_view")

elif st.session_state.view == "Portals":
    st.markdown('<div class="drill-header">🌐 All Portals</div>', unsafe_allow_html=True)
    portal_df = df['platform'].value_counts().reset_index()
    portal_df.columns = ['Portal', 'Openings']
    portal_df['Share %'] = (portal_df['Openings'] / len(df) * 100).round(2)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(portal_df, x='Portal', y='Openings',
                     title='Portals — Click a bar',
                     color='Openings', color_continuous_scale='Turbo', text='Openings')
        fig.update_layout(height=450, showlegend=False,
                          xaxis_tickangle=-30, title_font_size=13,
                          clickmode='event+select')
        fig.update_traces(textposition='outside')
        event = st.plotly_chart(fig, use_container_width=True,
                                on_select="rerun", key="portal_view_drill")
        if event and event.get("selection") and event["selection"].get("points"):
            clicked = event["selection"]["points"][0].get("x")
            if clicked and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != clicked):
                st.session_state.drill_type = "Portal"
                st.session_state.drill_value = clicked
                st.rerun()

    with c2:
        st.markdown("### 📋 Complete List")
        st.dataframe(portal_df, use_container_width=True, hide_index=True)

    csv = portal_df.to_csv(index=False)
    st.download_button("📥 Download CSV", csv,
                       file_name=f"portals_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv", key="dl_portal_view")

elif st.session_state.view == "Total Jobs":
    st.markdown('<div class="drill-header">📊 All Jobs in Dataset</div>', unsafe_allow_html=True)
    show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
                 'employment_type', 'posted_date']
    display_df = df[show_cols].copy()
    display_df.columns = ['Job Title', 'Company', 'Location', 'Portal',
                          'Remote', 'Type', 'Posted']
    st.dataframe(display_df, use_container_width=True, height=600)
    csv = df.to_csv(index=False)
    st.download_button("📥 Download All Jobs (CSV)", csv,
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
        drill_df = df[df['skills'].apply(lambda x: drill_val in x)]
    elif drill_type == "Job Role":
        drill_df = df[df['title'] == drill_val]
    elif drill_type == "Company":
        drill_df = df[df['company'] == drill_val]
    elif drill_type == "Location":
        drill_df = df[df['location'] == drill_val]
    elif drill_type == "Portal":
        drill_df = df[df['platform'] == drill_val]
    else:
        drill_df = df.copy()

    d1, d2, d3, d4 = st.columns(4)
    with d1: st.metric("🎯 Total Openings", len(drill_df))
    with d2: st.metric("🏢 Companies", drill_df['company'].nunique())
    with d3: st.metric("📍 Locations", drill_df['location'].nunique())
    with d4:
        rp = (drill_df['is_remote'] == 'Yes').sum() / len(drill_df) * 100 if len(drill_df) > 0 else 0
        st.metric("🏠 Remote %", f"{rp:.1f}%")

    g1, g2 = st.columns(2)
    with g1:
        pc = drill_df['platform'].value_counts().reset_index()
        pc.columns = ['Portal', 'Openings']
        fig = px.bar(pc, x='Openings', y='Portal', orientation='h',
                     title='By Portal', color='Openings',
                     color_continuous_scale='Blues', text='Openings')
        fig.update_layout(height=350, showlegend=False,
                          yaxis=dict(autorange="reversed"), title_font_size=13)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True, key=f"dd_p_{drill_val}")

    with g2:
        cc = drill_df['company'].value_counts().head(10).reset_index()
        cc.columns = ['Company', 'Openings']
        fig = px.bar(cc, x='Openings', y='Company', orientation='h',
                     title='By Company', color='Openings',
                     color_continuous_scale='Viridis', text='Openings')
        fig.update_layout(height=350, showlegend=False,
                          yaxis=dict(autorange="reversed"), title_font_size=13)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True, key=f"dd_c_{drill_val}")

    st.markdown("### 📋 All Job Openings")
    show_cols = ['title', 'company', 'location', 'platform', 'is_remote',
                 'employment_type', 'posted_date']
    ddf = drill_df[show_cols].copy()
    ddf.columns = ['Job Title', 'Company', 'Location', 'Portal',
                   'Remote', 'Type', 'Posted']
    st.dataframe(ddf, use_container_width=True, height=400)

    csv = drill_df.to_csv(index=False)
    st.download_button("📥 Download (CSV)", csv,
                       file_name=f"drill_{drill_type}_{drill_val}.csv",
                       mime="text/csv", key=f"dl_dd_{drill_val}")

# ============================================================================
# MAIN TABS (when no view is active)
# ============================================================================
if st.session_state.view is None:
    st.markdown("---")
    st.markdown("## 🔎 Explore Charts — Click to drill down")

    tabs = st.tabs(["🛠️ By Skill", "💼 By Role", "🏢 By Company",
                    "📍 By Location", "🌐 By Portal"])

    with tabs[0]:
        all_sk = [s for skills in df['skills'] for s in skills]
        sc = Counter(all_sk).most_common(20)
        if sc:
            sdf = pd.DataFrame(sc, columns=['Skill', 'Jobs'])
            fig = px.bar(sdf, x='Jobs', y='Skill', orientation='h',
                         title='Top 20 Skills', color='Jobs',
                         color_continuous_scale='RdYlGn', text='Jobs')
            fig.update_layout(height=650, showlegend=False,
                              yaxis=dict(autorange="reversed"),
                              clickmode='event+select')
            fig.update_traces(textposition='outside')
            ev = st.plotly_chart(fig, use_container_width=True,
                                 on_select="rerun", key="main_skill")
            if ev and ev.get("selection") and ev["selection"].get("points"):
                c = ev["selection"]["points"][0].get("y")
                if c and (st.session_state.drill_type != "Skill" or st.session_state.drill_value != c):
                    st.session_state.drill_type = "Skill"
                    st.session_state.drill_value = c
                    st.rerun()

    with tabs[1]:
        tc = df['title'].value_counts().head(20).reset_index()
        tc.columns = ['Job Role', 'Openings']
        fig = px.bar(tc, x='Openings', y='Job Role', orientation='h',
                     title='Top 20 Roles', color='Openings',
                     color_continuous_scale='Viridis', text='Openings')
        fig.update_layout(height=650, showlegend=False,
                          yaxis=dict(autorange="reversed"),
                          clickmode='event+select')
        fig.update_traces(textposition='outside')
        ev = st.plotly_chart(fig, use_container_width=True,
                             on_select="rerun", key="main_role")
        if ev and ev.get("selection") and ev["selection"].get("points"):
            c = ev["selection"]["points"][0].get("y")
            if c and (st.session_state.drill_type != "Job Role" or st.session_state.drill_value != c):
                st.session_state.drill_type = "Job Role"
                st.session_state.drill_value = c
                st.rerun()

    with tabs[2]:
        cc = df['company'].value_counts().head(20).reset_index()
        cc.columns = ['Company', 'Openings']
        fig = px.bar(cc, x='Openings', y='Company', orientation='h',
                     title='Top 20 Companies', color='Openings',
                     color_continuous_scale='Cividis', text='Openings')
        fig.update_layout(height=650, showlegend=False,
                          yaxis=dict(autorange="reversed"),
                          clickmode='event+select')
        fig.update_traces(textposition='outside')
        ev = st.plotly_chart(fig, use_container_width=True,
                             on_select="rerun", key="main_company")
        if ev and ev.get("selection") and ev["selection"].get("points"):
            c = ev["selection"]["points"][0].get("y")
            if c and (st.session_state.drill_type != "Company" or st.session_state.drill_value != c):
                st.session_state.drill_type = "Company"
                st.session_state.drill_value = c
                st.rerun()

    with tabs[3]:
        lc = df['location'].value_counts().head(20).reset_index()
        lc.columns = ['Location', 'Openings']
        fig = px.bar(lc, x='Location', y='Openings',
                     title='Top 20 Locations', color='Openings',
                     color_continuous_scale='Turbo', text='Openings')
        fig.update_layout(height=500, showlegend=False,
                          xaxis_tickangle=-40, clickmode='event+select')
        fig.update_traces(textposition='outside')
        ev = st.plotly_chart(fig, use_container_width=True,
                             on_select="rerun", key="main_loc")
        if ev and ev.get("selection") and ev["selection"].get("points"):
            c = ev["selection"]["points"][0].get("x")
            if c and (st.session_state.drill_type != "Location" or st.session_state.drill_value != c):
                st.session_state.drill_type = "Location"
                st.session_state.drill_value = c
                st.rerun()

    with tabs[4]:
        pc = df['platform'].value_counts().reset_index()
        pc.columns = ['Portal', 'Openings']
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(pc, x='Portal', y='Openings',
                         title='Portals', color='Openings',
                         color_continuous_scale='Plasma', text='Openings')
            fig.update_layout(height=450, showlegend=False,
                              xaxis_tickangle=-30, clickmode='event+select')
            fig.update_traces(textposition='outside')
            ev = st.plotly_chart(fig, use_container_width=True,
                                 on_select="rerun", key="main_portal")
            if ev and ev.get("selection") and ev["selection"].get("points"):
                c = ev["selection"]["points"][0].get("x")
                if c and (st.session_state.drill_type != "Portal" or st.session_state.drill_value != c):
                    st.session_state.drill_type = "Portal"
                    st.session_state.drill_value = c
                    st.rerun()

        with c2:
            fig = px.pie(pc, values='Openings', names='Portal',
                         title='Distribution', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textinfo='percent+label',
                              textposition='outside', textfont_size=11,
                              pull=[0.03] * len(pc))
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True, key="main_portal_pie")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""<div style='text-align:center; color:#666; font-size:12px;'>
    Job Market Analytics | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
    {len(df)} total jobs | {(df['is_remote']=='Yes').sum()} remote
</div>""", unsafe_allow_html=True)
