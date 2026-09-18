"""
Job Portal Analytics — Complete Dashboard with Report
Generates console report + clean dashboard

Usage: python job_analytics.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
import re
from collections import Counter

warnings.filterwarnings('ignore')

# -------- CONFIG --------
INPUT_CSV = "job_data_clean.csv"
OUTPUT_PREFIX = "job_report"
# -------------------------

# Clean styling
plt.style.use('default')
plt.rcParams['font.size'] = 9
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#f8f9fa'
plt.rcParams['grid.alpha'] = 0.2

def load_data():
    """Load data"""
    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"✅ Loaded {len(df)} jobs")
        return df
    except:
        print(f"❌ File '{INPUT_CSV}' not found")
        return None

def generate_full_report(df):
    """Generate complete console report"""
    
    print("\n" + "="*70)
    print("📈 INDIAN TECH JOB MARKET REPORT - 2026")
    print("="*70)
    print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Jobs Analyzed: {len(df):,}")
    print("="*70)
    
    # ----- 1. OVERVIEW -----
    print("\n📊 OVERVIEW STATISTICS")
    print("-"*50)
    print(f"  • Unique Companies: {df['company'].nunique():,}")
    print(f"  • Unique Job Titles: {df['title'].nunique():,}")
    print(f"  • Unique Locations: {df['location'].nunique():,}")
    if 'platform' in df.columns:
        print(f"  • Unique Platforms: {df['platform'].nunique():,}")
    
    # ----- 2. JOB TITLES -----
    print("\n💼 TOP 10 JOB TITLES")
    print("-"*50)
    title_counts = df['title'].value_counts().head(10)
    for i, (title, count) in enumerate(title_counts.items(), 1):
        pct = count/len(df)*100
        print(f"  {i:2d}. {title[:40]:<40} {count:>3} ({pct:>4.1f}%)")
    
    # ----- 3. COMPANIES -----
    print("\n🏢 TOP 10 HIRING COMPANIES")
    print("-"*50)
    company_counts = df['company'].value_counts().head(10)
    for i, (company, count) in enumerate(company_counts.items(), 1):
        print(f"  {i:2d}. {company[:35]:<35} {count:>3}")
    
    # ----- 4. LOCATIONS -----
    print("\n📍 TOP 10 HIRING LOCATIONS")
    print("-"*50)
    location_counts = df['location'].value_counts().head(10)
    for i, (loc, count) in enumerate(location_counts.items(), 1):
        pct = count/len(df)*100
        print(f"  {i:2d}. {loc[:30]:<30} {count:>3} ({pct:>4.1f}%)")
    
    # ----- 5. PLATFORMS -----
    if 'platform' in df.columns:
        print("\n🌐 JOBS BY PLATFORM")
        print("-"*50)
        platform_counts = df['platform'].value_counts()
        for platform, count in platform_counts.items():
            pct = count/len(df)*100
            print(f"  • {platform:<15} {count:>3} ({pct:>4.1f}%)")
    
    # ----- 6. REMOTE WORK -----
    if 'is_remote' in df.columns:
        print("\n🏠 REMOTE WORK STATUS")
        print("-"*50)
        remote_counts = df['is_remote'].value_counts()
        for status, count in remote_counts.items():
            pct = count/len(df)*100
            print(f"  • {status:<10} {count:>3} ({pct:>4.1f}%)")
        
        # Remote by platform
        print("\n  Remote Jobs by Platform:")
        remote_by_platform = df[df['is_remote']=='Yes'].groupby('platform').size()
        total_by_platform = df.groupby('platform').size()
        for platform in remote_by_platform.index:
            pct = (remote_by_platform[platform] / total_by_platform[platform] * 100)
            print(f"    • {platform:<15}: {remote_by_platform[platform]:>3} jobs ({pct:>4.1f}% remote)")
    
    # ----- 7. EMPLOYMENT TYPE -----
    if 'employment_type' in df.columns:
        print("\n📋 EMPLOYMENT TYPES")
        print("-"*50)
        emp_counts = df['employment_type'].value_counts().head(5)
        for emp_type, count in emp_counts.items():
            pct = count/len(df)*100
            print(f"  • {emp_type:<20} {count:>3} ({pct:>4.1f}%)")
    
    # ----- 8. SEARCH QUERY -----
    if 'search_term' in df.columns:
        print("\n🔍 JOBS BY SEARCH QUERY")
        print("-"*50)
        search_counts = df['search_term'].value_counts().head(10)
        for term, count in search_counts.items():
            pct = count/len(df)*100
            print(f"  • {term:<25} {count:>3} ({pct:>4.1f}%)")
    
    return {
        'title_counts': title_counts,
        'company_counts': company_counts,
        'location_counts': location_counts
    }

def extract_skills(text):
    """Extract skills from text"""
    if pd.isna(text):
        return []
    
    text = str(text).lower()
    skills = []
    
    skill_list = [
        'python', 'java', 'sql', 'js', 'react', 'angular', 'vue', 'node',
        'aws', 'azure', 'gcp', 'docker', 'k8s', 'terraform', 'jenkins',
        'spark', 'kafka', 'airflow', 'snowflake', 'tableau', 'pbi',
        'ml', 'dl', 'nlp', 'llm', 'genai', 'tensorflow', 'pytorch'
    ]
    
    for skill in skill_list:
        if skill in text:
            skills.append(skill)
    
    return list(set(skills))

def skill_analysis(df):
    """Analyze skills and print report"""
    
    print("\n" + "="*70)
    print("🛠️ SKILLS ANALYSIS")
    print("="*70)
    
    # Extract skills
    print("Extracting skills from job descriptions...")
    df['skills'] = df['description'].apply(extract_skills)
    df['skill_count'] = df['skills'].apply(len)
    
    # Overall skill frequency
    all_skills = [skill for skills in df['skills'] for skill in skills]
    skill_counts = Counter(all_skills)
    
    print(f"\n📊 Skill Statistics:")
    print(f"  • Unique skills identified: {len(skill_counts)}")
    print(f"  • Average skills per job: {df['skill_count'].mean():.1f}")
    print(f"  • Jobs with 0 skills: {(df['skill_count']==0).sum()}")
    
    print("\n🔥 TOP 20 MOST IN-DEMAND SKILLS:")
    print("-"*50)
    for i, (skill, count) in enumerate(skill_counts.most_common(20), 1):
        pct = count/len(df)*100
        print(f"  {i:2d}. {skill:<20} {count:>3} jobs ({pct:>4.1f}%)")
    
    return skill_counts

def create_dashboard(df):
    """Create clean dashboard with bar chart for employment type"""
    
    print("\n📊 Generating Dashboard...")
    
    # Create figure
    fig = plt.figure(figsize=(20, 15))
    
    # Grid with good spacing
    gs = fig.add_gridspec(
        3, 3,
        hspace=0.5,
        wspace=0.4,
        top=0.93,
        bottom=0.08,
        left=0.08,
        right=0.92
    )
    
    # ----- 1. Platform (Pie) -----
    ax1 = fig.add_subplot(gs[0, 0])
    if 'platform' in df.columns:
        counts = df['platform'].value_counts()
        labels = [p.replace('Company Site', 'Company') for p in counts.index]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        wedges, texts, autotexts = ax1.pie(
            counts.values,
            labels=labels,
            autopct=lambda pct: f'{pct:.0f}%',
            colors=colors[:len(counts)],
            textprops={'fontsize': 10},
            labeldistance=1.15,
            pctdistance=0.7,
            startangle=90,
            explode=[0.02] * len(counts),
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
        )
        
        for text in texts:
            text.set_fontsize(10)
            text.set_weight('bold')
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_color('white')
            autotext.set_weight('bold')
        
        ax1.set_title('Jobs by Platform', fontsize=13, fontweight='bold', pad=20)
    
    # ----- 2. Top Jobs (Bar) -----
    ax2 = fig.add_subplot(gs[0, 1])
    top_jobs = df['title'].value_counts().head(6)
    short_titles = [t.replace('Software', 'SW').replace('Engineer', 'Eng') 
                   for t in top_jobs.index]
    colors2 = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_jobs)))
    bars = ax2.bar(range(len(top_jobs)), top_jobs.values, color=colors2, width=0.5)
    ax2.set_title('Top Job Roles', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Jobs', fontsize=10)
    ax2.set_xticks(range(len(top_jobs)))
    ax2.set_xticklabels(short_titles, rotation=25, ha='right', fontsize=8)
    ax2.grid(axis='y', alpha=0.2)
    for bar, val in zip(bars, top_jobs.values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                str(val), ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax2.set_ylim(0, max(top_jobs.values) * 1.12)
    
    # ----- 3. Remote Status -----
    ax3 = fig.add_subplot(gs[0, 2])
    if 'is_remote' in df.columns:
        counts = df['is_remote'].value_counts()
        colors3 = ['#27ae60', '#e74c3c']
        bars = ax3.bar(counts.index, counts.values, color=colors3, width=0.3)
        ax3.set_title('Remote Work', fontsize=13, fontweight='bold')
        ax3.set_ylabel('Jobs', fontsize=10)
        for bar, val in zip(bars, counts.values):
            pct = val/len(df)*100
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val}\n({pct:.0f}%)', ha='center', va='bottom', 
                    fontsize=8, fontweight='bold')
        ax3.set_ylim(0, max(counts.values) * 1.15)
        ax3.grid(axis='y', alpha=0.2)
    
    # ----- 4. Top Companies -----
    ax4 = fig.add_subplot(gs[1, 0])
    top_companies = df['company'].value_counts().head(6)
    short_comp = [c.replace('Technologies', 'Tech').replace('Private', 'Pvt')
                 for c in top_companies.index]
    colors4 = plt.cm.coolwarm(np.linspace(0.2, 0.8, len(top_companies)))
    bars = ax4.barh(range(len(top_companies)), top_companies.values, 
                    color=colors4, height=0.5)
    ax4.set_title('Top Companies', fontsize=13, fontweight='bold')
    ax4.set_xlabel('Jobs', fontsize=10)
    ax4.set_yticks(range(len(top_companies)))
    ax4.set_yticklabels(short_comp, fontsize=8)
    ax4.invert_yaxis()
    for bar, val in zip(bars, top_companies.values):
        ax4.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                str(val), va='center', fontsize=8, fontweight='bold')
    ax4.grid(axis='x', alpha=0.2)
    
    # ----- 5. Top Locations -----
    ax5 = fig.add_subplot(gs[1, 1])
    top_locs = df['location'].value_counts().head(6)
    short_locs = [l.replace('Not specified', 'Other') for l in top_locs.index]
    colors5 = plt.cm.magma(np.linspace(0.3, 0.9, len(top_locs)))
    bars = ax5.bar(range(len(top_locs)), top_locs.values, color=colors5, width=0.5)
    ax5.set_title('Top Cities', fontsize=13, fontweight='bold')
    ax5.set_ylabel('Jobs', fontsize=10)
    ax5.set_xticks(range(len(top_locs)))
    ax5.set_xticklabels(short_locs, rotation=25, ha='right', fontsize=8)
    ax5.grid(axis='y', alpha=0.2)
    for bar, val in zip(bars, top_locs.values):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                str(val), ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax5.set_ylim(0, max(top_locs.values) * 1.12)
    
    # ----- 6. Employment Type (BAR CHART - NO OVERLAP!) -----
    ax6 = fig.add_subplot(gs[1, 2])
    if 'employment_type' in df.columns:
        counts = df['employment_type'].value_counts().head(5)
        labels = [e.replace('Full-time', 'Full Time') for e in counts.index]
        labels = [l.replace('Part-time', 'Part Time') for l in labels]
        
        colors6 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        bars = ax6.bar(range(len(counts)), counts.values, 
                      color=colors6[:len(counts)], width=0.5)
        ax6.set_title('Employment Type', fontsize=13, fontweight='bold')
        ax6.set_ylabel('Jobs', fontsize=10)
        ax6.set_xticks(range(len(counts)))
        ax6.set_xticklabels(labels, rotation=0, fontsize=9, ha='center')
        ax6.grid(axis='y', alpha=0.2)
        
        for bar, val in zip(bars, counts.values):
            pct = val/len(df)*100
            ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val}\n({pct:.0f}%)', ha='center', va='bottom', 
                    fontsize=8, fontweight='bold')
        ax6.set_ylim(0, max(counts.values) * 1.15)
    
    # ----- 7. Remote by Platform -----
    ax7 = fig.add_subplot(gs[2, 0])
    if 'platform' in df.columns and 'is_remote' in df.columns:
        remote_by_platform = df[df['is_remote']=='Yes'].groupby('platform').size()
        total_by_platform = df.groupby('platform').size()
        remote_pct = (remote_by_platform / total_by_platform * 100).sort_values(ascending=False)
        labels = [p.replace('Company Site', 'Company') for p in remote_pct.index]
        colors7 = plt.cm.Blues(np.linspace(0.3, 0.9, len(remote_pct)))[::-1]
        bars = ax7.bar(range(len(remote_pct)), remote_pct.values, color=colors7, width=0.5)
        ax7.set_title('Remote % by Platform', fontsize=13, fontweight='bold')
        ax7.set_ylabel('% Remote', fontsize=10)
        ax7.set_xticks(range(len(remote_pct)))
        ax7.set_xticklabels(labels, rotation=25, ha='right', fontsize=8)
        ax7.grid(axis='y', alpha=0.2)
        for bar, val in zip(bars, remote_pct.values):
            ax7.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{val:.0f}%', ha='center', va='bottom', fontsize=8, fontweight='bold')
        ax7.set_ylim(0, max(remote_pct.values) * 1.12)
    
    # ----- 8. Jobs Over Time -----
    ax8 = fig.add_subplot(gs[2, 1])
    if 'posted_date' in df.columns:
        df['posted_date'] = pd.to_datetime(df['posted_date'])
        daily = df.groupby(df['posted_date'].dt.date).size()
        ax8.plot(daily.index, daily.values, color='#e67e22', 
                linewidth=2, marker='o', markersize=4)
        ax8.set_title('Jobs Over Time', fontsize=13, fontweight='bold')
        ax8.set_xlabel('Date', fontsize=10)
        ax8.set_ylabel('Jobs', fontsize=10)
        ax8.tick_params(axis='x', rotation=25, labelsize=8)
        ax8.grid(True, alpha=0.2)
        ax8.fill_between(daily.index, daily.values, alpha=0.15, color='#e67e22')
    
    # ----- 9. Top Skills -----
    ax9 = fig.add_subplot(gs[2, 2])
    all_skills = []
    for desc in df['description']:
        all_skills.extend(extract_skills(desc))
    top_skills = Counter(all_skills).most_common(6)
    
    if top_skills:
        skill_names = [s[0] for s in top_skills]
        skill_vals = [s[1] for s in top_skills]
        short_skills = [s.replace('tensorflow', 'tf').replace('pytorch', 'pt')
                       for s in skill_names]
        colors9 = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(top_skills)))
        bars = ax9.bar(range(len(top_skills)), skill_vals, color=colors9, width=0.5)
        ax9.set_title('Top Skills', fontsize=13, fontweight='bold')
        ax9.set_ylabel('Jobs', fontsize=10)
        ax9.set_xticks(range(len(top_skills)))
        ax9.set_xticklabels(short_skills, rotation=25, ha='right', fontsize=8)
        ax9.grid(axis='y', alpha=0.2)
        for bar, val in zip(bars, skill_vals):
            ax9.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    str(val), ha='center', va='bottom', fontsize=8, fontweight='bold')
        ax9.set_ylim(0, max(skill_vals) * 1.12)
    
    # Title
    fig.suptitle('Tech Job Market Dashboard', fontsize=18, fontweight='bold', y=0.98)
    
    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_PREFIX}_{timestamp}.png"
    plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='white')
    print(f"✅ Dashboard saved: {filename}")
    
    plt.show()
    return filename

def export_data(df, skill_counts):
    """Export data to CSV files"""
    
    print("\n" + "="*70)
    print("📁 EXPORTING DATA")
    print("="*70)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    files = []
    
    # 1. Job titles
    title_df = df['title'].value_counts().reset_index()
    title_df.columns = ['job_title', 'count']
    title_file = f"{OUTPUT_PREFIX}_titles_{timestamp}.csv"
    title_df.to_csv(title_file, index=False)
    files.append(title_file)
    
    # 2. Companies
    company_df = df['company'].value_counts().head(50).reset_index()
    company_df.columns = ['company', 'count']
    company_file = f"{OUTPUT_PREFIX}_companies_{timestamp}.csv"
    company_df.to_csv(company_file, index=False)
    files.append(company_file)
    
    # 3. Locations
    location_df = df['location'].value_counts().reset_index()
    location_df.columns = ['location', 'count']
    location_file = f"{OUTPUT_PREFIX}_locations_{timestamp}.csv"
    location_df.to_csv(location_file, index=False)
    files.append(location_file)
    
    # 4. Skills
    skill_df = pd.DataFrame(skill_counts.most_common(50), columns=['skill', 'count'])
    skill_df['percentage'] = (skill_df['count'] / len(df) * 100).round(1)
    skill_file = f"{OUTPUT_PREFIX}_skills_{timestamp}.csv"
    skill_df.to_csv(skill_file, index=False)
    files.append(skill_file)
    
    # 5. Platforms
    if 'platform' in df.columns:
        platform_df = df['platform'].value_counts().reset_index()
        platform_df.columns = ['platform', 'count']
        platform_file = f"{OUTPUT_PREFIX}_platforms_{timestamp}.csv"
        platform_df.to_csv(platform_file, index=False)
        files.append(platform_file)
    
    print(f"✅ Exported {len(files)} files:")
    for f in files:
        print(f"   • {f}")

def main():
    """Main execution"""
    
    print("="*60)
    print("📊 JOB MARKET ANALYTICS")
    print("="*60)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # ----- 1. GENERATE FULL REPORT -----
    stats = generate_full_report(df)
    
    # ----- 2. SKILLS ANALYSIS -----
    skill_counts = skill_analysis(df)
    
    # ----- 3. CREATE DASHBOARD -----
    dashboard_file = create_dashboard(df)
    
    # ----- 4. EXPORT DATA -----
    export_data(df, skill_counts)
    
    # ----- 5. SUMMARY -----
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE!")
    print("="*70)
    print(f"\n📁 Output Files Generated:")
    print(f"   • Dashboard: {dashboard_file}")
    print(f"   • CSV Reports: job_report_*.csv")
    print("\n📊 Summary:")
    print(f"   • Total Jobs: {len(df)}")
    print(f"   • Companies: {df['company'].nunique()}")
    print(f"   • Job Titles: {df['title'].nunique()}")
    print(f"   • Locations: {df['location'].nunique()}")
    if 'is_remote' in df.columns:
        remote_pct = (df['is_remote']=='Yes').sum()/len(df)*100
        print(f"   • Remote Jobs: {remote_pct:.1f}%")
    print("="*70)

if __name__ == "__main__":
    main()