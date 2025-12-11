import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st
import datetime
import json
import os

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
# 0. 多语言配置（核心：语言字典 + 切换逻辑）
# -----------------------------------------------------------------------------
# 定义语言字典：key为统一标识，value为{简体中文, 繁体中文, 英文}
LANG_DICT = {
    # 页面基础
    "page_title": {
        "zh-CN": "香港财富投影计算器",
        "zh-TW": "香港財富投影計算器",
        "en": "HK Wealth Projector"
    },
    "sidebar_config": {
        "zh-CN": "⚙️ 模拟配置",
        "zh-TW": "⚙️ 模擬配置",
        "en": "⚙️ Simulation Config"
    },
    "initial_investment": {
        "zh-CN": "初始投资额 (港币)",
        "zh-TW": "初始投資額 (港幣)",
        "en": "Initial Investment (HKD)"
    },
    "time_horizon": {
        "zh-CN": "投资年限 (年)",
        "zh-TW": "投資年限 (年)",
        "en": "Time Horizon (Years)"
    },
    "asset_classes": {
        "zh-CN": "📊 资产类别",
        "zh-TW": "📊 資產類別",
        "en": "📊 Asset Classes"
    },
    
    # 资产1：现金/定期存款
    "cash_deposit": {
        "zh-CN": "🇭🇰 银行储蓄/定期存款",
        "zh-TW": "🇭🇰 銀行儲蓄/定期存款",
        "en": "🇭🇰 Bank Savings / Time Deposit"
    },
    "avg_interest_rate": {
        "zh-CN": "平均年利率 (%)",
        "zh-TW": "平均年利率 (%)",
        "en": "Avg. Interest Rate (%)"
    },
    
    # 资产2：保险产品
    "insurance_savings": {
        "zh-CN": "🛡️ 保险（储蓄计划）",
        "zh-TW": "🛡️ 保險（儲蓄計劃）",
        "en": "🛡️ Insurance (Savings Plans)"
    },
    "insurance_caption": {
        "zh-CN": "模拟典型的香港分红保单。",
        "zh-TW": "模擬典型的香港分紅保單。",
        "en": "Simulating typical HK Par products (分紅保單)."
    },
    "product_a_conservative": {
        "zh-CN": "**产品 A（保守型/保证收益为主）**",
        "zh-TW": "**產品 A（保守型/保證收益為主）**",
        "en": "**Product A (Conservative/Guaranteed focus)**"
    },
    "total_irr_a": {
        "zh-CN": "总内部收益率 % (A)",
        "zh-TW": "總內部收益率 % (A)",
        "en": "Total IRR % (A)"
    },
    "breakeven_year_a": {
        "zh-CN": "回本年限 (A)",
        "zh-TW": "回本年限 (A)",
        "en": "Breakeven Year (A)"
    },
    "product_b_aggressive": {
        "zh-CN": "**产品 B（进取型/长期收益为主）**",
        "zh-TW": "**產品 B（進取型/長期收益為主）**",
        "en": "**Product B (Aggressive/Long-term focus)**"
    },
    "total_irr_b": {
        "zh-CN": "总内部收益率 % (B)",
        "zh-TW": "總內部收益率 % (B)",
        "en": "Total IRR % (B)"
    },
    "breakeven_year_b": {
        "zh-CN": "回本年限 (B)",
        "zh-TW": "回本年限 (B)",
        "en": "Breakeven Year (B)"
    },
    
    # 资产3：房地产
    "hk_real_estate": {
        "zh-CN": "🏠 香港房地产",
        "zh-TW": "🏠 香港房地產",
        "en": "🏠 HK Real Estate"
    },
    "real_estate_caption": {
        "zh-CN": "假设全款购买或净资产增长。",
        "zh-TW": "假設全款購買或淨資產增長。",
        "en": "Assuming cash purchase or net equity growth."
    },
    "capital_appreciation": {
        "zh-CN": "资本增值率 (%)",
        "zh-TW": "資本增值率 (%)",
        "en": "Capital Appreciation (%)"
    },
    "rental_yield_net": {
        "zh-CN": "净租金收益率 (%)",
        "zh-TW": "淨租金收益率 (%)",
        "en": "Rental Yield (Net) (%)"
    },
    
    # 资产4：全球股票
    "global_equities": {
        "zh-CN": "🌎 全球股票（标普500）",
        "zh-TW": "🌎 全球股票（標普500）",
        "en": "🌎 Global Equities (S&P 500)"
    },
    "avg_annual_return": {
        "zh-CN": "平均年回报率 (%)",
        "zh-TW": "平均年回報率 (%)",
        "en": "Avg. Annual Return (%)"
    },
    
    # 主页面
    "title": {
        "zh-CN": "财富投影分析",
        "zh-TW": "財富投影分析",
        "en": "Wealth Projection"
    },
    "comparison_text": {
        "zh-CN": "对比 **{amount} 港币** 在 **{years} 年** 内的投资回报。",
        "zh-TW": "對比 **{amount} 港幣** 在 **{years} 年** 內的投資回報。",
        "en": "Comparing returns on **HKD {amount}** over **{years} years**."
    },
    "snapshot_at_year": {
        "zh-CN": "第 {years} 年快照",
        "zh-TW": "第 {years} 年快照",
        "en": "Snapshot at Year {years}"
    },
    "growth_trajectory": {
        "zh-CN": "增长轨迹",
        "zh-TW": "增長軌跡",
        "en": "Growth Trajectory"
    },
    
    # 资产名称（图表/Metric）
    "cash_deposit_short": {
        "zh-CN": "现金/存款",
        "zh-TW": "現金/存款",
        "en": "Cash/Deposit"
    },
    "insurance_conservative": {
        "zh-CN": "保险（保守型）",
        "zh-TW": "保險（保守型）",
        "en": "Insurance (Cons.)"
    },
    "insurance_aggressive": {
        "zh-CN": "保险（进取型）",
        "zh-TW": "保險（進取型）",
        "en": "Insurance (Aggr.)"
    },
    "real_estate_short": {
        "zh-CN": "房地产",
        "zh-TW": "房地產",
        "en": "Real Estate"
    },
    "global_equities_short": {
        "zh-CN": "全球股票",
        "zh-TW": "全球股票",
        "en": "Global Equities"
    },
    
    # 数据表格
    "view_data_table": {
        "zh-CN": "📂 查看底层数据表格",
        "zh-TW": "📂 查看底層數據表格",
        "en": "📂 View Underlying Data Table"
    },
    "download_csv": {
        "zh-CN": "下载数据为CSV文件",
        "zh-TW": "下載數據為CSV文件",
        "en": "Download Data as CSV"
    },
    "csv_filename": {
        "zh-CN": "香港财富投影数据.csv",
        "zh-TW": "香港財富投影數據.csv",
        "en": "hk_wealth_projection.csv"
    },
    
    # 免责声明
    "disclaimer": {
        "zh-CN": "免责声明：本工具仅用于教育模拟目的。保险收益曲线为简化模型，仅考虑回本周期，不代表具体保单演示。房地产收益假设租金再投资且不包含交易成本。",
        "zh-TW": "免責聲明：本工具僅用於教育模擬目的。保險收益曲線為簡化模型，僅考慮回本周期，不代表具體保單演示。房地產收益假設租金再投資且不包含交易成本。",
        "en": "Disclaimer: This tool is for educational simulation purposes only. Insurance curves are simplified to account for break-even periods and do not represent specific policy illustrations. Real estate assumes reinvested rental yield without transaction costs."
    },
    
    # 图表字段
    "year": {
        "zh-CN": "年份",
        "zh-TW": "年份",
        "en": "Year"
    },
    "asset_class": {
        "zh-CN": "资产类别",
        "zh-TW": "資產類別",
        "en": "Asset Class"
    },
    "value": {
        "zh-CN": "价值 (港币)",
        "zh-TW": "價值 (港幣)",
        "en": "Value (HKD)"
    }
}

# 语言选择控件（侧边栏顶部，默认简体中文）
st.sidebar.markdown("### 🌐 语言 / Language")
selected_lang = st.sidebar.selectbox(
    "选择语言 / Select Language",
    options=["zh-CN", "zh-TW", "en"],
    format_func=lambda x: {"zh-CN": "简体中文", "zh-TW": "繁體中文", "en": "English"}[x],
    index=0  # 默认简体中文
)

# 快捷获取对应语言文本的函数
def t(key):
    return LANG_DICT[key][selected_lang]

# -----------------------------------------------------------------------------
# 1. Page Configuration & Silicon Valley Style CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title=t("page_title"),
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
st.sidebar.markdown(f"### {t('sidebar_config')}")

# Global Settings
initial_investment = st.sidebar.number_input(
    t("initial_investment"), 
    min_value=10000, 
    value=1000000, 
    step=50000,
    format="%d"
)

years = st.sidebar.slider(t("time_horizon"), 0, 100, 50)

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t('asset_classes')}")

# Asset 1: Cash / Time Deposit
with st.sidebar.expander(t("cash_deposit"), expanded=True):
    r_cash = st.sidebar.slider(t("avg_interest_rate"), 0.0, 6.0, 3.5, 0.1) / 100

# Asset 2: Insurance Products (Split into Conservative vs Aggressive)
with st.sidebar.expander(t("insurance_savings"), expanded=False):
    st.caption(t("insurance_caption"))
    # Brand A: Conservative (e.g., Traditional Savings)
    st.markdown(t("product_a_conservative"))
    r_ins_a = st.sidebar.slider(t("total_irr_a"), 1.0, 7.0, 4.2, 0.1) / 100
    breakeven_a = st.sidebar.slider(t("breakeven_year_a"), 1, 15, 6)
    breakeven_a = max(1, breakeven_a)  # 防呆：确保至少为1
    
    st.divider()
    
    # Brand B: Aggressive (e.g., High Equity mix)
    st.markdown(t("product_b_aggressive"))
    r_ins_b = st.sidebar.slider(t("total_irr_b"), 1.0, 10.0, 6.5, 0.1) / 100
    breakeven_b = st.sidebar.slider(t("breakeven_year_b"), 1, 20, 9)
    breakeven_b = max(1, breakeven_b)  # 防呆：确保至少为1

# Asset 3: Real Estate
with st.sidebar.expander(t("hk_real_estate"), expanded=False):
    st.caption(t("real_estate_caption"))
    r_prop_appreciation = st.sidebar.slider(t("capital_appreciation"), -2.0, 10.0, 3.0, 0.1) / 100
    r_prop_yield = st.sidebar.slider(t("rental_yield_net"), 0.0, 6.0, 2.5, 0.1) / 100

# Asset 4: Global Market
with st.sidebar.expander(t("global_equities"), expanded=False):
    r_stocks = st.sidebar.slider(t("avg_annual_return"), 0.0, 15.0, 8.5, 0.1) / 100

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

# 构建 DataFrame（适配多语言列名）
df = pd.DataFrame({
    t("year"): years_arr,
    t("cash_deposit_short"): cash_vals,
    t("real_estate_short"): prop_vals,
    t("insurance_conservative"): ins_a_vals,
    t("insurance_aggressive"): ins_b_vals,
    t("global_equities_short"): stocks_vals
})

# -----------------------------------------------------------------------------
# 4. Main UI Layout
# -----------------------------------------------------------------------------
# Title Section
col_header_1, col_header_2 = st.columns([3, 1])
with col_header_1:
    st.title(t("title"))
    # 格式化金额显示（适配不同语言的千位分隔符）
    amount_formatted = f"{initial_investment:,.0f}" if selected_lang in ["zh-CN", "zh-TW"] else f"${initial_investment:,.0f}"
    st.markdown(t("comparison_text").format(amount=amount_formatted, years=years))
with col_header_2:
    st.write("") 

st.markdown("---")

# Key Metrics Row (Snapshot at End of Horizon)
st.subheader(t("snapshot_at_year").format(years=years))
m1, m2, m3, m4, m5 = st.columns(5)

# Extract final values
final_row = df.iloc[-1]

# 格式化 Metric 显示（统一用百万为单位，适配语言）
def format_metric_value(val):
    if selected_lang in ["zh-CN", "zh-TW"]:
        return f"{val/1000000:.2f} 百万"
    else:
        return f"${val/1000000:.2f}M"

def format_metric_delta(val, initial):
    delta = ((val - initial) / initial) * 100
    return f"{delta:.0f}%"

# 渲染 Metric
m1.metric(
    t("cash_deposit_short"), 
    format_metric_value(final_row[t("cash_deposit_short")]), 
    format_metric_delta(final_row[t("cash_deposit_short")], initial_investment)
)
m2.metric(
    t("insurance_conservative"), 
    format_metric_value(final_row[t("insurance_conservative")]), 
    format_metric_delta(final_row[t("insurance_conservative")], initial_investment)
)
m3.metric(
    t("insurance_aggressive"), 
    format_metric_value(final_row[t("insurance_aggressive")]), 
    format_metric_delta(final_row[t("insurance_aggressive")], initial_investment)
)
m4.metric(
    t("real_estate_short"), 
    format_metric_value(final_row[t("real_estate_short")]), 
    format_metric_delta(final_row[t("real_estate_short")], initial_investment)
)
m5.metric(
    t("global_equities_short"), 
    format_metric_value(final_row[t("global_equities_short")]), 
    format_metric_delta(final_row[t("global_equities_short")], initial_investment)
)

st.markdown(f"### {t('growth_trajectory')}")

# -----------------------------------------------------------------------------
# 5. Visualization (Plotly)
# -----------------------------------------------------------------------------
# Reshape for Plotly（适配多语言）
df_melted = df.melt(
    id_vars=[t("year")], 
    var_name=t("asset_class"), 
    value_name=t("value")
)

# Custom Color Palette (Silicon Valley / Professional)
colors = {
    t("cash_deposit_short"): "#9CA3AF",          # Gray
    t("insurance_conservative"): "#60A5FA",      # Light Blue
    t("insurance_aggressive"): "#2563EB",        # Strong Blue
    t("real_estate_short"): "#059669",           # Emerald Green
    t("global_equities_short"): "#7C3AED"        # Purple
}

fig = px.line(
    df_melted, 
    x=t("year"), 
    y=t("value"), 
    color=t("asset_class"),
    color_discrete_map=colors,
    height=500
)

# 图表样式优化（适配多语言）
fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_family="Inter",
    hovermode="x unified",
    xaxis=dict(
        showgrid=False, 
        linecolor="#E5E7EB",
        title=t("year")
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor="#F3F4F6",
        title=t("value"),
        # 适配语言的货币符号
        tickprefix="" if selected_lang in ["zh-CN", "zh-TW"] else "$"
    ),
    legend=dict(
        orientation="h", 
        y=1.02, 
        yanchor="bottom", 
        x=0, 
        xanchor="left", 
        title=t("asset_class")
    )
)

# Hover 模板优化（适配语言）
hover_template = f"{t('year')}: %{{x}}<br>{t('value')}: "
if selected_lang in ["zh-CN", "zh-TW"]:
    hover_template += "%{y:,.0f} 港币<extra></extra>"
else:
    hover_template += "$%{y:,.0f}<extra></extra>"
fig.update_traces(hovertemplate=hover_template)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# 6. Detailed Data View
# -----------------------------------------------------------------------------
with st.expander(t("view_data_table")):
    # 格式化数据表格（适配语言的货币显示）
    def format_currency(val):
        if selected_lang in ["zh-CN", "zh-TW"]:
            return f"{val:,.0f} 港币"
        else:
            return f"${val:,.0f}"
    
    # 排除年份列，只格式化数值列
    format_dict = {col: format_currency for col in df.columns if col != t("year")}
    st.dataframe(
        df.style.format(format_dict),
        use_container_width=True,
        height=300
    )

    # CSV 下载（适配多语言文件名）
    csv = df.to_csv(index=False, encoding='utf-8-sig')  # 支持中文文件名
    st.download_button(
        t("download_csv"),
        csv,
        t("csv_filename"),
        "text/csv",
        key='download-csv'
    )

# Disclaimer
st.caption(t("disclaimer"))
daily_visits = update_daily_visits()
st.markdown(f"""
<div style="text-align: center; color: #64748b; font-size: 0.7rem; margin: 10px 0;">
    今日访问: {daily_visits}
</div>
""", unsafe_allow_html=True)
