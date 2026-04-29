import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Dashboard Configuration
st.set_page_config(page_title="ABW BD Dashboard", layout="wide")

# 2. Sleek, High-Contrast SaaS Styling
st.markdown("""
    <style>
    /* Import Barlow and Inter from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@600;700;800&family=Inter:wght@400;500;600;800&display=swap');
    
    /* Main Background & Base Text - Slightly darker bg for high contrast white cards */
    .stApp { background-color: #F1F5F9; font-family: 'Inter', -apple-system, sans-serif; color: #020617; }
    
    /* Block container spacing */
    .block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 1400px; }
    
    /* Metric Cards - High Contrast with Interactive Hover */
    div[data-testid="stMetric"] { 
        background-color: #FFFFFF; 
        padding: 24px; 
        border-radius: 12px; 
        border-top: 5px solid #0EA5E9; /* Bolder Blue Accent */
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); /* Deeper shadow for pop */
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.12);
    }
    
    /* Metric Big Number (Value) */
    div[data-testid="stMetricValue"] > div {
        color: #020617 !important; /* Pitch Slate */
        font-family: 'Barlow', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2.4rem !important;
    }
    
    /* Metric Title (Label) */
    div[data-testid="stMetricLabel"] p {
        color: #475569 !important; /* Mid Slate */
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Headers */
    h1, h2, h3 { 
        font-family: 'Barlow', sans-serif !important; 
        color: #020617 !important; 
    }
    h1 { font-weight: 800; letter-spacing: -0.5px; }
    h2, h3 { font-weight: 700; margin-top: 1.5rem; margin-bottom: 1rem; }
    
    /* Expanders (Strategic Assets) */
    div[data-testid="stExpander"] { 
        background-color: #FFFFFF; 
        border: 1px solid #CBD5E1; /* Darker border for contrast */
        border-radius: 10px; 
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
        margin-bottom: 12px;
    }
    
    /* Dividers */
    hr { border-top: 2px solid #E2E8F0; margin: 2.5rem 0; }
    
    /* Custom Profile Card CSS */
    .profile-card {
        background-color: #FFFFFF;
        padding: 14px 18px;
        border-radius: 8px;
        border-left: 4px solid #0EA5E9;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .profile-card strong {
        color: #0F172A;
        font-family: 'Barlow', sans-serif;
        font-size: 1.1em;
    }
    .profile-link {
        color: #0EA5E9;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.85em;
        display: block;
        margin-top: 4px;
    }
    .profile-link:hover {
        text-decoration: underline;
        color: #0284C7;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Live Spreadsheet Connection
SHEET_ID = "1KpIHmw1vmOzs0t_k3l6TI6L45ZF8GmKtBg5ndUbAzg0"

def get_google_sheet_url(gid):
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"

@st.cache_data(ttl=600)
def load_all_data():
    metrics_df = pd.read_csv(get_google_sheet_url("0"))
    pipeline_df = pd.read_csv(get_google_sheet_url("347629712"))
    assets_df = pd.read_csv(get_google_sheet_url("1844315915"))
    return metrics_df, pipeline_df, assets_df

try:
    df_metrics, df_pipeline, df_assets = load_all_data()

    # 4. Header Section
    st.title("A Blue World")
    st.markdown("**Business Development & Infrastructure | Live Dashboard**")
    st.write("---")

    # 5. Top-Level Metrics
    cols = st.columns(len(df_metrics))
    for i, row in df_metrics.iterrows():
        safe_value = str(row['Value']).replace('$', r'\$')
        cols[i].metric(label=str(row['Category']), value=safe_value, delta=str(row['Delta / Note']))

    st.write("---")

    # 6. Main Content Layout
    col_left, spacer, col_right = st.columns([2, 0.1, 1])

    with col_left:
        # Dynamic Chart: Revenue Velocity
        st.markdown("### 📈 Revenue Velocity & Scale")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=['FY2025 Actual', 'FY2026 Forecast', 'Post-Round Target'], 
            y=[1.3, 3.0, 6.0], 
            mode='lines+markers+text',
            text=['$1.3M', '$3.0M', '$6M+'],
            textposition="top left",
            textfont=dict(color='#0F172A', size=14, family="Inter", weight="bold"),
            line=dict(color='#0EA5E9', width=4),
            marker=dict(size=14, color='#0284C7', line=dict(color='white', width=2))
        ))
        fig.update_layout(
            template="plotly_white", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            height=280,
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0', zeroline=False, tickfont=dict(color='#64748B')),
            xaxis=dict(showgrid=False, tickfont=dict(color='#64748B'))
        )
        st.plotly_chart(fig, use_container_width=True)

        # Pipeline DataFrame
        st.markdown("### 🎯 Sector Pipeline Status")
        st.dataframe(
            df_pipeline, 
            use_container_width=True, 
            hide_index=True,
            height=210
        )
        
        # Strategic Assets Expanders
        st.markdown("### 🛠 Infrastructure & Strategic Assets")
        for _, row in df_assets.iterrows():
            with st.expander(f"**{row['Asset Name']}** | {row['Category']}"):
                st.write(f"**Status:** {row['Status / Details']}")
                st.caption(f"Last Updated: {row['Key Date']}")

    with col_right:
        # Leadership Team Profiles
        st.markdown("### 👥 Leadership Team")
        
        # Custom HTML profile cards
        profiles = [
            ("Christopher Suarez", "Co-Founder", "https://linkedin.com/in/placeholder-christopher"),
            ("Baptiste Auzeau", "Co-Founder", "https://linkedin.com/in/placeholder-baptiste"),
            ("Athina Karamalis", "Co-Founder", "https://linkedin.com/in/placeholder-athina"),
            ("Julia von Boehm", "Co-Founder", "https://linkedin.com/in/placeholder-julia")
        ]
        
        for name, title, link in profiles:
            st.markdown(f"""
                <div class="profile-card">
                    <strong>{name}</strong><br>
                    <span style="color: #64748B; font-size: 0.9em;">{title}</span>
                    <a href="{link}" target="_blank" class="profile-link">🔗 View LinkedIn Profile</a>
                </div>
            """, unsafe_allow_html=True)

        st.divider()
            
        # Pinned Press / PDF Downloads
        st.markdown("### 📰 Featured Press")
        st.caption("Download the latest media coverage")
        
        # Placeholders for actual PDF data. Currently just downloads empty txt files for demonstration.
        # Replace `data="PDF_BYTES_HERE"` with your actual file loading logic later.
        st.download_button(
            label="📄 Download WWD Feature (Apr 9)",
            data="Placeholder content for WWD Article", 
            file_name="WWD_Feature_April9.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        st.download_button(
            label="📄 Download Vogue Italia Coverage",
            data="Placeholder content for Vogue Italia Article", 
            file_name="Vogue_Italia_Coverage.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        st.divider()
        
        st.markdown("### ⚠️ Executive Watch-outs")
        st.warning("Growth-round materials being finalised; raise kicks off May (\\$13M–\\$16M target)")
        st.warning("All active BD engagements remain under NDA")

except Exception as e:
    st.error("Connection Pending: Please ensure your Google Sheet is set to 'Anyone with the link can view'.")
