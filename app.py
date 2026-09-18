"""
Job Portal Analytics — Interactive Dashboard with Filters
Runs on localhost with dynamic slicers and filters

Installation:
pip install streamlit pandas matplotlib seaborn

Usage:
streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Job Market Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("job_data_clean.csv")
    df['posted_date'] = pd.to_datetime(df['posted_date'])
    return df

def extract_skills(text):
    """Extract skills from description"""
    if pd.isna(text):
        return []
    
    text = str(text).lower()
    skills = []
    
    skill_list = [
        'python', 'java', 'sql', 'javascript', 'react', 'angular', 'vue', 'node',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins',
        'spark', 'kafka', 'airflow', 'snowflake', 'tableau', 'power bi',
        'machine learning', 'deep learning', 'nlp', 'llm', 'genai', 
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'
    ]
    
    for skill in skill_list:
        if skill in text:
            skills.append(skill)
    
    return list(set(skills))

# Load data
try:
    df = load_data()
    st.success(f"✅ Loaded {len(df)} job postings")
except:
    st.error("❌ File 'job_data_clean.csv' not found. Please run data_cleaning.py first.")
    st.stop()

# Extract skills
df['skills'] = df['description'].apply(extract_skills)

# ============================================================================
# SIDEBAR FILTERS (SLICERS)
# ============================================================================

st.sidebar.title("🔍 FILTERS")

# 1. Job Title Filter
st.sidebar.subheader("📌 Job Title")
title_options = ["All"] + sorted(df['title'].unique().tolist())
selected_title = st.sidebar.selectbox("Select Job Title", title_options)

# 2. Company Filter
st.sidebar.subheader("🏢 Company")
company_options = ["All"] + sorted(df['company'].unique().tolist())
selected_company = st.sidebar.selectbox("Select Company", company_options)

# 3. Location Filter
st.sidebar.subheader("📍 Location")
location_options = ["All"] + sorted(df['location'].unique().tolist())
selected_location = st.sidebar.selectbox("Select Location", location_options)

# 4. Platform Filter
st.sidebar.subheader("🌐 Platform")
platform_options = ["All"] + sorted(df['platform'].unique().tolist())
selected_platform = st.sidebar.selectbox("Select Platform", platform_options)

# 5. Remote Filter
st.sidebar.subheader("🏠 Remote")
remote_options = ["All", "Yes", "No"]
selected_remote = st.sidebar.selectbox("Remote Status", remote_options)

# 6. Employment Type Filter
st.sidebar.subheader("📋 Employment Type")
emp_options = ["All"] + sorted(df['employment_type'].unique().tolist())
selected_emp = st.sidebar.selectbox("Employment Type", emp_options)

# 7. Date Range Filter
st.sidebar.subheader("📅 Date Range")
if 'posted_date' in df.columns:
    min_date = df['posted_date'].min().date()
    max_date = df['posted_date'].max().date()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

# 8. Skills Filter
st.sidebar.subheader("🛠️ Skills")
all_skills = sorted(set([s for skills in df['skills'] for s in skills]))
selected_skills = st.sidebar.multiselect("Select Skills", all_skills)

# ============================================================================
# APPLY FILTERS
# ============================================================================

filtered_df = df.copy()

# Apply filters
if selected_title != "All":
    filtered_df = filtered_df[filtered_df['title'] == selected_title]

if selected_company != "All":
    filtered_df = filtered_df[filtered_df['company'] == selected_company]

if selected_location != "All":
    filtered_df = filtered_df[filtered_df['location'] == selected_location]

if selected_platform != "All":
    filtered_df = filtered_df[filtered_df['platform'] == selected_platform]

if selected_remote != "All":
    filtered_df = filtered_df[filtered_df['is_remote'] == selected_remote]

if selected_emp != "All":
    filtered_df = filtered_df[filtered_df['employment_type'] == selected_emp]

if 'posted_date' in df.columns and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['posted_date'].dt.date >= start_date) & 
        (filtered_df['posted_date'].dt.date <= end_date)
    ]

if selected_skills:
    filtered_df = filtered_df[
        filtered_df['skills'].apply(lambda x: any(skill in x for skill in selected_skills))
    ]

# ============================================================================
# DASHBOARD HEADER
# ============================================================================

st.title("📊 Job Market Analytics Dashboard")
st.markdown(f"**Filtered Results:** {len(filtered_df)} job postings (Total: {len(df)})")

# ============================================================================
# KPI CARDS (ROW 1)
# ============================================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Jobs", len(filtered_df))

with col2:
    st.metric("Companies", filtered_df['company'].nunique())

with col3:
    st.metric("Job Titles", filtered_df['title'].nunique())

with col4:
    if filtered_df['is_remote'].nunique() > 0:
        remote_pct = (filtered_df['is_remote'] == 'Yes').sum() / len(filtered_df) * 100
        st.metric("Remote Jobs", f"{remote_pct:.1f}%")

with col5:
    avg_skills = filtered_df['skills'].apply(len).mean()
    st.metric("Avg Skills/Job", f"{avg_skills:.1f}")

# ============================================================================
# CHARTS (ROW 2 - 2 Columns)
# ============================================================================

col1, col2 = st.columns(2)

# Chart 1: Top Job Titles
with col1:
    st.subheader("💼 Top Job Titles")
    if len(filtered_df) > 0:
        top_titles = filtered_df['title'].value_counts().head(8)
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = plt.cm.viridis(range(len(top_titles)))
        bars = ax.barh(range(len(top_titles)), top_titles.values, color=colors)
        ax.set_yticks(range(len(top_titles)))
        ax.set_yticklabels(top_titles.index, fontsize=9)
        ax.set_xlabel('Number of Jobs')
        ax.invert_yaxis()
        for i, (bar, val) in enumerate(zip(bars, top_titles.values)):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                    str(val), va='center', fontsize=9, fontweight='bold')
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No data for selected filters")

# Chart 2: Top Companies
with col2:
    st.subheader("🏢 Top Companies")
    if len(filtered_df) > 0:
        top_companies = filtered_df['company'].value_counts().head(8)
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = plt.cm.coolwarm(range(len(top_companies)))
        bars = ax.bar(range(len(top_companies)), top_companies.values, color=colors)
        ax.set_xticks(range(len(top_companies)))
        ax.set_xticklabels(top_companies.index, rotation=45, ha='right', fontsize=8)
        ax.set_ylabel('Number of Jobs')
        for bar, val in zip(bars, top_companies.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    str(val), ha='center', va='bottom', fontsize=9, fontweight='bold')
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No data for selected filters")

# ============================================================================
# CHARTS (ROW 3 - 3 Columns)
# ============================================================================

col1, col2, col3 = st.columns(3)

# Chart 3: Location Distribution
with col1:
    st.subheader("📍 Top Locations")
    if len(filtered_df) > 0:
        top_locs = filtered_df['location'].value_counts().head(6)
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = plt.cm.magma(range(len(top_locs)))
        bars = ax.bar(range(len(top_locs)), top_locs.values, color=colors)
        ax.set_xticks(range(len(top_locs)))
        ax.set_xticklabels(top_locs.index, rotation=45, ha='right', fontsize=8)
        ax.set_ylabel('Number of Jobs')
        for bar, val in zip(bars, top_locs.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    str(val), ha='center', va='bottom', fontsize=8, fontweight='bold')
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No data for selected filters")

# Chart 4: Remote Work Status
with col2:
    st.subheader("🏠 Remote Status")
    if len(filtered_df) > 0:
        remote_counts = filtered_df['is_remote'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#27ae60' if x=='Yes' else '#e74c3c' for x in remote_counts.index]
        bars = ax.bar(remote_counts.index, remote_counts.values, color=colors, width=0.4)
        ax.set_ylabel('Number of Jobs')
        for bar, val in zip(bars, remote_counts.values):
            pct = val/len(filtered_df)*100
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val}\n({pct:.0f}%)', ha='center', va='bottom', 
                    fontsize=8, fontweight='bold')
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No data for selected filters")

# Chart 5: Employment Type
with col3:
    st.subheader("📋 Employment Type")
    if len(filtered_df) > 0:
        emp_counts = filtered_df['employment_type'].value_counts().head(5)
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = plt.cm.Set3(range(len(emp_counts)))
        bars = ax.bar(range(len(emp_counts)), emp_counts.values, color=colors, width=0.4)
        ax.set_xticks(range(len(emp_counts)))
        ax.set_xticklabels(emp_counts.index, rotation=0, fontsize=9, ha='center')
        ax.set_ylabel('Number of Jobs')
        for bar, val in zip(bars, emp_counts.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    str(val), ha='center', va='bottom', fontsize=8, fontweight='bold')
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No data for selected filters")

# ============================================================================
# CHARTS (ROW 4 - 2 Columns)
# ============================================================================

col1, col2 = st.columns(2)

# Chart 6: Platform Distribution
with col1:
    st.subheader("🌐 Platform Distribution")
    if len(filtered_df) > 0:
        platform_counts = filtered_df['platform'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        wedges, texts, autotexts = ax.pie(
            platform_counts.values,
            labels=platform_counts.index,
            autopct=lambda pct: f'{pct:.0f}%',
            colors=colors[:len(platform_counts)],
            textprops={'fontsize': 9},
            labeldistance=1.1,
            pctdistance=0.7,
            startangle=90,
            explode=[0.02] * len(platform_counts),
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
        )
        for text in texts:
            text.set_fontsize(9)
            text.set_weight('bold')
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_color('white')
            autotext.set_weight('bold')
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No data for selected filters")

# Chart 7: Jobs Over Time
with col2:
    st.subheader("📅 Jobs Over Time")
    if len(filtered_df) > 0:
        daily = filtered_df.groupby(filtered_df['posted_date'].dt.date).size()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(daily.index, daily.values, color='#e67e22', linewidth=2, marker='o', markersize=4)
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Jobs')
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.grid(True, alpha=0.2)
        ax.fill_between(daily.index, daily.values, alpha=0.15, color='#e67e22')
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No data for selected filters")

# ============================================================================
# SKILLS SECTION (ROW 5)
# ============================================================================

st.subheader("🛠️ Top Skills in Demand")

col1, col2 = st.columns([2, 1])

with col1:
    if len(filtered_df) > 0:
        all_skills = [s for skills in filtered_df['skills'] for s in skills]
        skill_counts = Counter(all_skills).most_common(10)
        
        if skill_counts:
            skill_names = [s[0] for s in skill_counts]
            skill_vals = [s[1] for s in skill_counts]
            
            fig, ax = plt.subplots(figsize=(12, 5))
            colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(skill_counts)))
            bars = ax.bar(range(len(skill_counts)), skill_vals, color=colors, width=0.5)
            ax.set_xticks(range(len(skill_counts)))
            ax.set_xticklabels(skill_names, rotation=45, ha='right', fontsize=9)
            ax.set_ylabel('Number of Jobs')
            ax.grid(axis='y', alpha=0.2)
            for bar, val in zip(bars, skill_vals):
                pct = val/len(filtered_df)*100
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                        f'{val}\n({pct:.0f}%)', ha='center', va='bottom', 
                        fontsize=8, fontweight='bold')
            st.pyplot(fig)
            plt.close()
        else:
            st.info("No skills data available")
    else:
        st.info("No data for selected filters")

with col2:
    st.subheader("📊 Quick Stats")
    st.markdown(f"""
    - **Total Jobs:** {len(filtered_df)}
    - **Companies:** {filtered_df['company'].nunique()}
    - **Titles:** {filtered_df['title'].nunique()}
    - **Locations:** {filtered_df['location'].nunique()}
    - **Avg Skills/Job:** {filtered_df['skills'].apply(len).mean():.1f}
    """)

# ============================================================================
# DATA TABLE (ROW 6)
# ============================================================================

with st.expander("📋 View Filtered Data"):
    st.dataframe(
        filtered_df[['title', 'company', 'location', 'platform', 'is_remote', 'employment_type', 'posted_date']],
        use_container_width=True,
        height=300
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"job_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666; font-size: 12px;'>
        Job Market Analytics Dashboard | Data updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
        Total records: {len(df)} | Filtered: {len(filtered_df)}
    </div>
    """,
    unsafe_allow_html=True
)