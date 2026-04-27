import streamlit as st
import pandas as pd
import feedparser
import plotly.graph_objects as go

# 1. Dashboard Configuration
st.set_page_config(page_title="ABW BD Dashboard", layout="wide")

# 2. Sleek, Modern SaaS Styling with Barlow Fonts
st.markdown("""
    <style>
    /* Import Barlow and Inter from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@600;700;800&family=Inter:wght@400;600;800&display=swap');
    
    /* Main Background & Base Text */
    .stApp { background-color: #F8FAFC; font-family: 'Inter', -apple-system, sans-serif; }
    
    /* Block container spacing for more breathing room */
    .block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 1400px; }
    
    /* Metric Cards - Clean White with Soft Shadows */
    div[data-testid="stMetric"] { 
        background-color: #FFFFFF; 
        padding: 24px; 
        border-radius: 12px; 
        border-top: 4px solid #0EA5E9; /* Bright Blue World Accent */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Metric Big Number (Value) */
    div[data-testid="stMetricValue"] > div {
        color: #0F172A !important; /* Deep Slate */
        font-family: 'Barlow', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
    }
    
    /* Metric Title (Label) */
    div[data-testid="stMetricLabel"] p {
        color: #64748B !important; /* Soft Slate */
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Headers (Now in Barlow) */
    h1, h2, h3 { 
        font-family: 'Barlow', sans-serif !important; 
        color: #0F172A !important; 
    }
    h1 { font-weight: 800; letter-spacing: -0.5px; }
    h2, h3 { font-weight: 700; margin-top: 1.5rem; margin-bottom: 1rem; }
    
    /* Expanders (Strategic Assets) */
    div[data-testid="stExpander"] { 
        background-color: #FFFFFF; 
        border: 1px solid #E2E8F0; 
        border-radius: 10px; 
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        margin-bottom: 12px;
    }
    
    /* Dividers */
    hr { border-top: 1px solid #E2E8F0; margin: 2.5rem 0; }
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
        # Escape dollar signs for metrics
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
            textfont=dict(color='#0F172A', size=14, family="Inter"),
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
        # RSS Feed Targeting "A Blue World" specifically
        st.markdown("### 📰 Brand Radar")
        
        rss_url = 'https://news.google.com/rss/search?q=%22A+Blue+World%22'
        
        try:
            feed = feedparser.parse(rss_url)
            if len(feed.entries) > 0:
                for entry in feed.entries[:4]: 
                    st.markdown(f"**[{entry.title}]({entry.link})**")
                    st.caption(f"{entry.source.title} | {entry.published[:16]}")
                    st.write("") 
            else:
                st.info("No new articles indexed in the past 24 hours.")
        except Exception:
            st.warning("RSS Feed temporarily unavailable.")
            
        st.divider()
            
        # Pinned Highlights from the presentation
        st.markdown("### 🏆 Pinned Highlights")
        st.success("**WWD Feature** (April 9): Global category validation")
        st.success("**Cannes Film Festival**: Cultural anchor activated")
        
        st.divider()
        
        st.markdown("### ⚠️ Executive Watch-outs")
        # Escaping the dollar signs here fixes the weird italic 'M' issue
        st.warning("Growth-round materials being finalised; raise kicks off May (\\$13M–\\$16M target)")
        st.warning("All active BD engagements remain under NDA")

except Exception as e:
    st.error("Connection Pending: Please ensure your Google Sheet is set to 'Anyone with the link can view'.")
