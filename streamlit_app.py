import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import json
import os
from scipy.stats import norm

# -----------------------------------------------------------------------------
# 1. 页面基础配置 (必须放在第一行)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HK Wealth Projector",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------- 访问计数器核心代码 --------------------------
COUNTER_FILE = "visit_stats.json"

def update_daily_visits():
    try:
        today_str = datetime.date.today().isoformat()
        if "has_counted" in st.session_state:
            return json.load(open(COUNTER_FILE)).get("count", 0) if os.path.exists(COUNTER_FILE) else 0

        data = {"date": today_str, "count": 0}
        if os.path.exists(COUNTER_FILE):
            try:
                file_data = json.load(open(COUNTER_FILE))
                if file_data["date"] == today_str:
                    data = file_data
            except:
                pass
        
        data["count"] += 1
        json.dump(data, open(COUNTER_FILE, "w"))
        st.session_state["has_counted"] = True
        return data["count"]
    except:
        return 0

# -----------------------------------------------------------------------------
# 2. 紧凑化 CSS 样式 (Silicon Valley Style)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #FAFAFA;
        color: #1F2937;
    }
    
    /* --- 核心紧凑化设置 --- */
    /* 移除 Streamlit 默认的巨大顶部空白 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 98% !important; /* 利用更多横向空间 */
    }
    
    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {display: none;}

    /* 侧边栏紧凑化 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
    }
    
    /* 标题紧凑化 */
    h1 { 
        font-weight: 700; 
        color: #111827; 
        font-size: 1.5rem !important; /* 缩小大标题 */
        margin-bottom: 0.5rem !important;
    }
    h2 { color: #374151; font-size: 1.2rem !important; margin-top: 0.5rem !important; }
    h3 { color: #4B5563; font-size: 1rem !important; margin-bottom: 5px !important; }

    /* Metric 卡片紧凑化 */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        padding: 10px !important; /* 减少内边距 */
        border-radius: 8px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        min-height: 80px;
    }
    div[data-testid="metric-container"] label {
        font-size: 0.8rem !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 1.1rem !important;
    }
    
    /* 图表容器优化 */
    .stPlotlyChart {
        background-color: #FFFFFF;
        border-radius: 12px;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.05);
        padding: 5px;
    }

    /* 右上角按钮样式 */
    .neal-btn {
        font-family: 'Inter', sans-serif;
        background: #fff;
        border: 1px solid #e5e7eb;
        color: #111;
        font-weight: 600;
        font-size: 13px;
        padding: 6px 12px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        white-space: nowrap;
        text-decoration: none !important;
        width: 100%;
        height: 32px;
    }
    .neal-btn:hover { background: #f9fafb; border-color: #111; }
    .neal-btn-link { text-decoration: none; width: 100%; display: block; }
</style>
""", unsafe_allow_html=True)

# -------------------------- 右上角功能区 --------------------------
col_empty, col_more = st.columns([0.85, 0.15]) # 调整比例
with col_more:
    st.markdown(
        f"""
        <a href="https://haowan.streamlit.app/" target="_blank" class="neal-btn-link">
            <button class="neal-btn">✨ 更多好玩应用</button>
        </a>
        """, 
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# 3. 多语言配置
# -----------------------------------------------------------------------------
LANG_DICT = {
    "page_title": {"zh-CN": "香港投资回报计算器", "zh-TW": "香港財富投影計算器", "en": "HK Wealth Projector"},
    "sidebar_config": {"zh-CN": "⚙️ 模拟配置", "zh-TW": "⚙️ 模擬配置", "en": "⚙️ Simulation Config"},
    "initial_investment": {"zh-CN": "初始投资额 (港币)", "zh-TW": "初始投資額 (港幣)", "en": "Initial Investment (HKD)"},
    "time_horizon": {"zh-CN": "投资年限 (年)", "zh-TW": "投資年限 (年)", "en": "Time Horizon (Years)"},
    "asset_classes": {"zh-CN": "📊 资产类别", "zh-TW": "📊 資產類別", "en": "📊 Asset Classes"},
    "cash_deposit": {"zh-CN": "🇭🇰 银行储蓄/定期存款", "zh-TW": "🇭🇰 銀行儲蓄/定期存款", "en": "🇭🇰 Bank Savings / Time Deposit"},
    "avg_interest_rate": {"zh-CN": "平均年利率 (%)", "zh-TW": "平均年利率 (%)", "en": "Avg. Interest Rate (%)"},
    "insurance_savings": {"zh-CN": "🛡️ 保险（储蓄计划）", "zh-TW": "🛡️ 保險（儲蓄計劃）", "en": "🛡️ Insurance (Savings Plans)"},
    "insurance_caption": {"zh-CN": "模拟典型的香港分红保单。", "zh-TW": "模擬典型的香港分紅保單。", "en": "Simulating typical HK Par products (分紅保單)."},
    "product_a_conservative": {"zh-CN": "**产品 A（保守型/保证收益为主）**", "zh-TW": "**產品 A（保守型/保證收益為主）**", "en": "**Product A (Conservative/Guaranteed focus)**"},
    "total_irr_a": {"zh-CN": "总内部收益率 % (A)", "zh-TW": "總內部收益率 % (A)", "en": "Total IRR % (A)"},
    "breakeven_year_a": {"zh-CN": "回本年限 (A)", "zh-TW": "回本年限 (A)", "en": "Breakeven Year (A)"},
    "product_b_aggressive": {"zh-CN": "**产品 B（进取型/长期收益为主）**", "zh-TW": "**產品 B（進取型/長期收益為主）**", "en": "**Product B (Aggressive/Long-term focus)**"},
    "total_irr_b": {"zh-CN": "总内部收益率 % (B)", "zh-TW": "總內部收益率 % (B)", "en": "Total IRR % (B)"},
    "breakeven_year_b": {"zh-CN": "回本年限 (B)", "zh-TW": "回本年限 (B)", "en": "Breakeven Year (B)"},
    "hk_real_estate": {"zh-CN": "🏠 香港房地产", "zh-TW": "🏠 香港房地產", "en": "🏠 HK Real Estate"},
    "real_estate_caption": {"zh-CN": "假设全款购买或净资产增长。", "zh-TW": "假設全款購買或淨資產增長。", "en": "Assuming cash purchase or net equity growth."},
    "capital_appreciation": {"zh-CN": "资本增值率 (%)", "zh-TW": "資本增值率 (%)", "en": "Capital Appreciation (%)"},
    "rental_yield_net": {"zh-CN": "净租金收益率 (%)", "zh-TW": "淨租金收益率 (%)", "en": "Rental Yield (Net) (%)"},
    "global_equities": {"zh-CN": "🌎 全球股票（标普500）", "zh-TW": "🌎 全球股票（標普500）", "en": "🌎 Global Equities (S&P 500)"},
    "avg_annual_return": {"zh-CN": "平均年回报率 (%)", "zh-TW": "平均年回報率 (%)", "en": "Avg. Annual Return (%)"},
    "volatility": {"zh-CN": "年度波动率 (%)", "zh-TW": "年度波動率 (%)", "en": "Annual Volatility (%)"},
    "volatility_caption": {"zh-CN": "标普500长期波动率约15-20%", "zh-TW": "標普500長期波動率約15-20%", "en": "S&P 500 long-term volatility ~15-20%"},
    "title": {"zh-CN": "百万港元回报", "zh-TW": "財富投影分析", "en": "Wealth Projection"},
    "comparison_text": {"zh-CN": "对比 **{amount} 港币** 在 **{years} 年** 内的投资回报。", "zh-TW": "對比 **{amount} 港幣** 在 **{years} 年** 內的投資回報。", "en": "Comparing returns on **HKD {amount}** over **{years} years**."},
    "snapshot_at_year": {"zh-CN": "第 {years} 年快照", "zh-TW": "第 {years} 年快照", "en": "Snapshot at Year {years}"},
    "growth_trajectory": {"zh-CN": "增长轨迹", "zh-TW": "增長軌跡", "en": "Growth Trajectory"},
    "cash_deposit_short": {"zh-CN": "现金/存款", "zh-TW": "現金/存款", "en": "Cash/Deposit"},
    "insurance_conservative": {"zh-CN": "保险（保守型）", "zh-TW": "保險（保守型）", "en": "Insurance (Cons.)"},
    "insurance_aggressive": {"zh-CN": "保险（进取型）", "zh-TW": "保險（進取型）", "en": "Insurance (Aggr.)"},
    "real_estate_short": {"zh-CN": "房地产", "zh-TW": "房地產", "en": "Real Estate"},
    "global_equities_short": {"zh-CN": "全球股票", "zh-TW": "全球股票", "en": "Global Equities"},
    "view_data_table": {"zh-CN": "📂 查看底层数据表格", "zh-TW": "📂 查看底層數據表格", "en": "📂 View Underlying Data Table"},
    "download_csv": {"zh-CN": "下载数据为CSV文件", "zh-TW": "下載數據為CSV文件", "en": "Download Data as CSV"},
    "csv_filename": {"zh-CN": "香港财富投影数据.csv", "zh-TW": "香港財富投影數據.csv", "en": "hk_wealth_projection.csv"},
    "disclaimer": {"zh-CN": "免责声明：本工具仅用于教育模拟目的。保险收益曲线为简化模型，仅考虑回本周期，不代表具体保单演示。房地产收益假设租金再投资且不包含交易成本。股票波动基于历史数据模拟，不构成投资建议。", "zh-TW": "免責聲明：本工具僅用於教育模擬目的。保險收益曲線為簡化模型，僅考慮回本周期，不代表具體保單演示。房地產收益假設租金再投資且不包含交易成本。股票波動基於歷史數據模擬，不構成投資建議。", "en": "Disclaimer: This tool is for educational simulation purposes only. Insurance curves are simplified to account for break-even periods and do not represent specific policy illustrations. Real estate assumes reinvested rental yield without transaction costs. Stock volatility is simulated based on historical data and does not constitute investment advice."},
    "year": {"zh-CN": "年份", "zh-TW": "年份", "en": "Year"},
    "asset_class": {"zh-CN": "资产类别", "zh-TW": "資產類別", "en": "Asset Class"},
    "value": {"zh-CN": "价值 (港币)", "zh-TW": "價值 (港幣)", "en": "Value (HKD)"}
}

st.sidebar.markdown("### 🌐 语言 / Language")
selected_lang = st.sidebar.selectbox(
    "Select",
    options=["zh-CN", "zh-TW", "en"],
    format_func=lambda x: {"zh-CN": "简体中文", "zh-TW": "繁體中文", "en": "English"}[x],
    index=0,
    label_visibility="collapsed"
)

def t(key):
    return LANG_DICT[key][selected_lang]

# -----------------------------------------------------------------------------
# 4. 侧边栏配置
# -----------------------------------------------------------------------------
st.sidebar.markdown(f"**{t('sidebar_config')}**")

initial_investment = st.sidebar.number_input(
    t("initial_investment"), 
    min_value=10000, 
    value=1000000, 
    step=50000,
    format="%d"
)

years = st.sidebar.slider(t("time_horizon"), 0, 100, 50)

st.sidebar.divider()
st.sidebar.markdown(f"**{t('asset_classes')}**")

# 使用更紧凑的 expander 布局
with st.sidebar.expander(t("cash_deposit"), expanded=True):
    r_cash = st.sidebar.slider(t("avg_interest_rate"), 0.0, 6.0, 3.5, 0.1) / 100

with st.sidebar.expander(t("insurance_savings"), expanded=False):
    st.caption(t("insurance_caption"))
    st.markdown(t("product_a_conservative"))
    r_ins_a = st.sidebar.slider(t("total_irr_a"), 1.0, 7.0, 4.2, 0.1) / 100
    breakeven_a = st.sidebar.slider(t("breakeven_year_a"), 1, 15, 6)
    
    st.divider()
    st.markdown(t("product_b_aggressive"))
    r_ins_b = st.sidebar.slider(t("total_irr_b"), 1.0, 10.0, 6.5, 0.1) / 100
    breakeven_b = st.sidebar.slider(t("breakeven_year_b"), 1, 20, 9)

with st.sidebar.expander(t("hk_real_estate"), expanded=False):
    st.caption(t("real_estate_caption"))
    r_prop_appreciation = st.sidebar.slider(t("capital_appreciation"), -2.0, 10.0, 3.0, 0.1) / 100
    r_prop_yield = st.sidebar.slider(t("rental_yield_net"), 0.0, 6.0, 2.5, 0.1) / 100

with st.sidebar.expander(t("global_equities"), expanded=False):
    r_stocks = st.sidebar.slider(t("avg_annual_return"), 0.0, 15.0, 8.5, 0.1) / 100
    volatility = st.sidebar.slider(t("volatility"), 0.0, 40.0, 14.0, 0.5) / 100

# -----------------------------------------------------------------------------
# 5. 计算逻辑
# -----------------------------------------------------------------------------
years_arr = np.arange(0, years + 1)
r_prop_total = (1 + r_prop_appreciation) * (1 + r_prop_yield) - 1

cash_vals = initial_investment * ((1 + r_cash) ** years_arr)
prop_vals = initial_investment * ((1 + r_prop_total) ** years_arr)

breakeven_a = max(1, breakeven_a)
ins_a_vals = np.where(
    years_arr == 0, initial_investment,
    np.where(years_arr < breakeven_a, initial_investment * (0.8 + 0.2 * (years_arr / breakeven_a)), initial_investment * ((1 + r_ins_a) ** years_arr))
)

breakeven_b = max(1, breakeven_b)
ins_b_vals = np.where(
    years_arr == 0, initial_investment,
    np.where(years_arr < breakeven_b, initial_investment * (0.7 + 0.3 * (years_arr / breakeven_b)), initial_investment * ((1 + r_ins_b) ** years_arr))
)

def simulate_stock_returns(initial, mu, sigma, years, seed=42):
    if years == 0: return np.array([initial])
    np.random.seed(seed)
    dt = 1 
    drift = mu - 0.5 * sigma**2
    random_shocks = np.random.normal(0, 1, years)
    annual_returns = np.exp(drift * dt + sigma * np.sqrt(dt) * random_shocks)
    values = np.zeros(years + 1)
    values[0] = initial
    for t in range(1, years + 1):
        values[t] = values[t-1] * annual_returns[t-1]
    return values

stocks_vals = simulate_stock_returns(initial_investment, r_stocks, volatility, years)

df = pd.DataFrame({
    t("year"): years_arr,
    t("cash_deposit_short"): cash_vals,
    t("real_estate_short"): prop_vals,
    t("insurance_conservative"): ins_a_vals,
    t("insurance_aggressive"): ins_b_vals,
    t("global_equities_short"): stocks_vals
})

# -----------------------------------------------------------------------------
# 6. 主界面布局
# -----------------------------------------------------------------------------
# 标题区更紧凑
amount_formatted = f"{initial_investment:,.0f}" if selected_lang in ["zh-CN", "zh-TW"] else f"${initial_investment:,.0f}"
st.markdown(f"### {t('title')} <span style='font-size:0.9rem;color:#6B7280;font-weight:normal'> | {t('comparison_text').format(amount=amount_formatted, years=years)}</span>", unsafe_allow_html=True)

# 指标区
final_row = df.iloc[-1]
m1, m2, m3, m4, m5 = st.columns(5)

def format_metric_value(val):
    if selected_lang in ["zh-CN", "zh-TW"]: return f"{val/1000000:.2f} M"
    else: return f"${val/1000000:.2f}M"

def format_metric_delta(val, initial):
    return f"{((val - initial) / initial) * 100:.0f}%"

m1.metric(t("cash_deposit_short"), format_metric_value(final_row[t("cash_deposit_short")]), format_metric_delta(final_row[t("cash_deposit_short")], initial_investment))
m2.metric(t("insurance_conservative"), format_metric_value(final_row[t("insurance_conservative")]), format_metric_delta(final_row[t("insurance_conservative")], initial_investment))
m3.metric(t("insurance_aggressive"), format_metric_value(final_row[t("insurance_aggressive")]), format_metric_delta(final_row[t("insurance_aggressive")], initial_investment))
m4.metric(t("real_estate_short"), format_metric_value(final_row[t("real_estate_short")]), format_metric_delta(final_row[t("real_estate_short")], initial_investment))
m5.metric(t("global_equities_short"), format_metric_value(final_row[t("global_equities_short")]), format_metric_delta(final_row[t("global_equities_short")], initial_investment))

# -----------------------------------------------------------------------------
# 7. 可视化 (Plotly)
# -----------------------------------------------------------------------------
df_melted = df.melt(id_vars=[t("year")], var_name=t("asset_class"), value_name=t("value"))

colors = {
    t("cash_deposit_short"): "#9CA3AF", 
    t("insurance_conservative"): "#60A5FA", 
    t("insurance_aggressive"): "#2563EB", 
    t("real_estate_short"): "#059669", 
    t("global_equities_short"): "#7C3AED" 
}

# 高度设为 380px，更紧凑
fig = px.line(
    df_melted, x=t("year"), y=t("value"), color=t("asset_class"),
    color_discrete_map=colors, height=380 
)

fig.update_layout(
    plot_bgcolor="white", paper_bgcolor="white", font_family="Inter",
    hovermode="x unified",
    margin=dict(l=10, r=10, t=30, b=10), # 移除图表周围空白
    xaxis=dict(showgrid=False, linecolor="#E5E7EB", title=None),
    yaxis=dict(showgrid=True, gridcolor="#F3F4F6", title=None, tickprefix="" if selected_lang in ["zh-CN", "zh-TW"] else "$"),
    legend=dict(orientation="h", y=1.1, x=0, title=None, font=dict(size=12)) # 图例放上面
)

hover_template = f"{t('year')}: %{{x}}<br>{t('value')}: " + ("%{y:,.0f}<extra></extra>" if selected_lang not in ["zh-CN", "zh-TW"] else "%{y:,.0f} <extra></extra>")
fig.update_traces(hovertemplate=hover_template)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# 8. 数据表 & 底部
# -----------------------------------------------------------------------------
with st.expander(t("view_data_table"), expanded=False):
    format_dict = {col: (lambda x: f"{x:,.0f}") for col in df.columns if col != t("year")}
    st.dataframe(df.style.format(format_dict), use_container_width=True, height=250)
    
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(t("download_csv"), csv, t("csv_filename"), "text/csv", key='download-csv')

st.markdown(f"<div style='font-size:0.75rem;color:#9CA3AF;margin-top:10px;'>{t('disclaimer')} | Visits: {update_daily_visits()}</div>", unsafe_allow_html=True)
