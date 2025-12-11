import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. Page Configuration & Silicon Valley Style CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HK Wealth Projector",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for that "Clean SaaS" look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #FAFAFA;
        color: #1F2937;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Inputs Styling */
    div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
        background-color: #3B82F6; 
        border-color: #3B82F6;
    }
    
    /* Headings */
    h1, h2, h3 {
        font-weight: 600;
        letter-spacing: -0.025em;
    }
    
    h1 { color: #111827; }
    h2 { color: #374151; font-size: 1.5rem; margin-top: 1rem; }
    h3 { color: #4B5563; font-size: 1.1rem; }

    /* Metric Cards (Simulated) */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* Chart Container */
    .stPlotlyChart {
        background-color: #FFFFFF;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Sidebar: Investment Parameters
# -----------------------------------------------------------------------------
st.sidebar.markdown("### ⚙️ Simulation Config")

# Global Settings
initial_investment = st.sidebar.number_input(
    "Initial Investment (HKD)", 
    min_value=10000, 
    value=1000000, 
    step=50000,
    format="%d"
)

years = st.sidebar.slider("Time Horizon (Years)", 0, 100, 50)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Asset Classes")

# Asset 1: Cash / Time Deposit
with st.sidebar.expander("🇭🇰 Bank Savings / Time Deposit", expanded=True):
    r_cash = st.sidebar.slider("Avg. Interest Rate (%)", 0.0, 6.0, 3.5, 0.1) / 100

# Asset 2: Insurance Products (Split into Conservative vs Aggressive)
with st.sidebar.expander("🛡️ Insurance (Savings Plans)", expanded=False):
    st.caption("Simulating typical HK Par products (分紅保單).")
    # Brand A: Conservative (e.g., Traditional Savings)
    st.markdown("**Product A (Conservative/Guaranteed focus)**")
    r_ins_a = st.sidebar.slider("Total IRR % (A)", 1.0, 7.0, 4.2, 0.1) / 100
    breakeven_a = st.sidebar.slider("Breakeven Year (A)", 1, 15, 6)
    breakeven_a = max(1, breakeven_a)  # 防呆：确保至少为1
    
    st.divider()
    
    # Brand B: Aggressive (e.g., High Equity mix)
    st.markdown("**Product B (Aggressive/Long-term focus)**")
    r_ins_b = st.sidebar.slider("Total IRR % (B)", 1.0, 10.0, 6.5, 0.1) / 100
    breakeven_b = st.sidebar.slider("Breakeven Year (B)", 1, 20, 9)
    breakeven_b = max(1, breakeven_b)  # 防呆：确保至少为1

# Asset 3: Real Estate
with st.sidebar.expander("🏠 HK Real Estate", expanded=False):
    st.caption("Assuming cash purchase or net equity growth.")
    r_prop_appreciation = st.sidebar.slider("Capital Appreciation (%)", -2.0, 10.0, 3.0, 0.1) / 100
    r_prop_yield = st.sidebar.slider("Rental Yield (Net) (%)", 0.0, 6.0, 2.5, 0.1) / 100

# Asset 4: Global Market
with st.sidebar.expander("🌎 Global Equities (S&P 500)", expanded=False):
    r_stocks = st.sidebar.slider("Avg. Annual Return (%)", 0.0, 15.0, 8.5, 0.1) / 100

# -----------------------------------------------------------------------------
# 3. Calculation Engine (优化为向量化计算)
# -----------------------------------------------------------------------------
years_arr = np.arange(0, years + 1)

# 房产总回报：修正复利逻辑
r_prop_total = (1 + r_prop_appreciation) * (1 + r_prop_yield) - 1

# 向量化计算各资产价值
cash_vals = initial_investment * ((1 + r_cash) ** years_arr)
prop_vals = initial_investment * ((1 + r_prop_total) ** years_arr)

# 保险 A 向量化计算
ins_a_vals = np.where(
    years_arr == 0,
    initial_investment,
    np.where(
        years_arr < breakeven_a,
        initial_investment * (0.8 + 0.2 * (years_arr / breakeven_a)),
        initial_investment * ((1 + r_ins_a) ** years_arr)
    )
)

# 保险 B 向量化计算
ins_b_vals = np.where(
    years_arr == 0,
    initial_investment,
    np.where(
        years_arr < breakeven_b,
        initial_investment * (0.7 + 0.3 * (years_arr / breakeven_b)),
        initial_investment * ((1 + r_ins_b) ** years_arr)
    )
)

# 股票向量化计算
stocks_vals = initial_investment * ((1 + r_stocks) ** years_arr)

# 构建 DataFrame
df = pd.DataFrame({
    "Year": years_arr,
    "Cash/Deposit": cash_vals,
    "HK Real Estate": prop_vals,
    "Insurance (Conservative)": ins_a_vals,
    "Insurance (Aggressive)": ins_b_vals,
    "Global Equities": stocks_vals
})

# -----------------------------------------------------------------------------
# 4. Main UI Layout
# -----------------------------------------------------------------------------
# Title Section
col_header_1, col_header_2 = st.columns([3, 1])
with col_header_1:
    st.title("Wealth Projection")
    st.markdown(f"Comparing returns on **HKD ${initial_investment:,.0f}** over **{years} years**.")
with col_header_2:
    st.write("") 

st.markdown("---")

# Key Metrics Row (Snapshot at End of Horizon)
st.subheader(f"Snapshot at Year {years}")
m1, m2, m3, m4, m5 = st.columns(5)

# Extract final values
final_row = df.iloc[-1]

# 格式化 Metric 显示
m1.metric(
    "Cash/Deposit", 
    f"${final_row['Cash/Deposit']/1000000:.2f}M", 
    f"{(final_row['Cash/Deposit']/initial_investment - 1)*100:.0f}%"
)
m2.metric(
    "Insurance (Cons.)", 
    f"${final_row['Insurance (Conservative)']/1000000:.2f}M", 
    f"{(final_row['Insurance (Conservative)']/initial_investment - 1)*100:.0f}%"
)
m3.metric(
    "Insurance (Aggr.)", 
    f"${final_row['Insurance (Aggressive)']/1000000:.2f}M", 
    f"{(final_row['Insurance (Aggressive)']/initial_investment - 1)*100:.0f}%"
)
m4.metric(
    "Real Estate", 
    f"${final_row['HK Real Estate']/1000000:.2f}M", 
    f"{(final_row['HK Real Estate']/initial_investment - 1)*100:.0f}%"
)
m5.metric(
    "Global Equities", 
    f"${final_row['Global Equities']/1000000:.2f}M", 
    f"{(final_row['Global Equities']/initial_investment - 1)*100:.0f}%"
)

st.markdown("### Growth Trajectory")

# -----------------------------------------------------------------------------
# 5. Visualization (Plotly)
# -----------------------------------------------------------------------------
# Reshape for Plotly
df_melted = df.melt(id_vars=["Year"], var_name="Asset Class", value_name="Value")

# Custom Color Palette (Silicon Valley / Professional)
colors = {
    "Cash/Deposit": "#9CA3AF",          # Gray
    "Insurance (Conservative)": "#60A5FA", # Light Blue
    "Insurance (Aggressive)": "#2563EB",   # Strong Blue
    "HK Real Estate": "#059669",        # Emerald Green
    "Global Equities": "#7C3AED"        # Purple
}

fig = px.line(
    df_melted, 
    x="Year", 
    y="Value", 
    color="Asset Class",
    color_discrete_map=colors,
    height=500
)

# Clean up the chart
fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_family="Inter",
    hovermode="x unified",
    xaxis=dict(showgrid=False, linecolor="#E5E7EB"),
    yaxis=dict(showgrid=True, gridcolor="#F3F4F6", tickprefix="$", title=None),
    legend=dict(orientation="h", y=1.02, yanchor="bottom", x=0, xanchor="left", title=None)
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# 6. Detailed Data View
# -----------------------------------------------------------------------------
with st.expander("📂 View Underlying Data Table"):
    st.dataframe(
        df.style.format("${:,.0f}"),
        use_container_width=True,
        height=300
    )

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Data as CSV",
        csv,
        "hk_wealth_projection.csv",
        "text/csv",
        key='download-csv'
    )

# Disclaimer
st.caption("Disclaimer: This tool is for educational simulation purposes only. Insurance curves are simplified to account for break-even periods and do not represent specific policy illustrations. Real estate assumes reinvested rental yield without transaction costs.")
