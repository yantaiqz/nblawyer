import streamlit as st
import pandas as pd

# ======================== 全局配置 ========================
st.set_page_config(
    page_title="Global Legal Institutions | 全球法律机构",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================== 硅谷风格 CSS ========================
st.markdown("""
<style>
    /* 基础重置 */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* 全局样式 */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* 标题样式 */
    h1, h2, h3, h4 {
        color: #1e293b;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    h1 {
        font-size: 2.2rem;
        margin-bottom: 1rem;
    }
    
    h2 {
        font-size: 1.5rem;
        margin: 1.5rem 0 0.8rem 0;
    }
    
    h3 {
        font-size: 1.2rem;
        color: #334155;
        margin-bottom: 0.6rem;
    }
    
    /* 卡片样式 - 核心组件 */
    .institution-card {
        background: white;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        border-left: 3px solid #3b82f6;
    }
    
    .institution-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    /* 链接样式 */
    .institution-link {
        color: #3b82f6;
        text-decoration: none;
        font-weight: 500;
        font-size: 1.1rem;
    }
    
    .institution-link:hover {
        color: #2563eb;
        text-decoration: underline;
    }
    
    /* 描述文本 */
    .institution-desc {
        color: #64748b;
        font-size: 0.95rem;
        margin-top: 4px;
        line-height: 1.4;
    }
    
    /* 筛选器样式 */
    .stSelectbox > div {
        background: white;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }
    
    /* 侧边栏隐藏（如需展开筛选可取消） */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* 响应式调整 */
    @media (max-width: 768px) {
        .institution-card {
            padding: 12px;
        }
        
        h1 {
            font-size: 1.8rem;
        }
        
        h2 {
            font-size: 1.3rem;
        }
    }
    
    /* 分隔线 */
    .divider {
        border: none;
        height: 1px;
        background-color: #e2e8f0;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ======================== 核心数据 ========================
LEGAL_DATA = {
    # 🌏 亚太地区 (Asia Pacific)
    "🌏 Asia Pacific (亚太)": {
        "🇨🇳 China (中国)": {
            "🤖 LegalTech & Data (科技/数据)": [
                {"name": "法大大", "url": "https://www.fadada.com", "desc": "E-Signature Platform"},
                {"name": "iTerms", "url": "https://www.iterms.com", "desc": "AI Contract Revew"},
                {"name": "北大法宝", "url": "https://www.pkulaw.com", "desc": "Leading Legal Database"},
                {"name": "威科先行", "url": "https://law.wkinfo.com.cn", "desc": "Wolters Kluwer China"},
                {"name": "无讼", "url": "https://www.itslaw.com", "desc": "Litigation Data"},
                {"name": "天眼查", "url": "https://www.tianyancha.com", "desc": "Business Data"},
                {"name": "企查查", "url": "https://www.qcc.com", "desc": "Credit Info"},
                {"name": "秘塔科技", "url": "https://www.metaso.cn", "desc": "AI Search"},
                {"name": "幂律智能", "url": "https://www.powerlaw.ai", "desc": "AI Contract Review"},
                {"name": "理脉", "url": "https://www.legalminer.com", "desc": "Legal Big Data"},
                {"name": "法天使", "url": "https://www.fats.cn", "desc": "Contract Templates"},
                {"name": "华宇信息", "url": "https://www.thunisoft.com", "desc": "Court Information Systems"},
                {"name": "国双 (Gridsum)", "url": "http://www.gridsum.com", "desc": "Judicial Big Data"},
            ],
            "🏛️ Red Circle & Top Firms (红圈/顶级律所)": [
                {"name": "金杜 (KWM)", "url": "https://www.kwm.com", "desc": "Red Circle Elite"},
                {"name": "君合 (JunHe)", "url": "https://www.junhe.com", "desc": "Premier Commercial Firm"},
                {"name": "中伦 (Zhong Lun)", "url": "https://www.zhonglun.com", "desc": "Full Service Giant"},
                {"name": "方达 (Fangda)", "url": "https://www.fangdalaw.com", "desc": "M&A and Capital Markets"},
                {"name": "海问 (Haiwen)", "url": "https://www.haiwen-law.com", "desc": "Prestigious Securities"},
                {"name": "汉坤 (Han Kun)", "url": "https://www.hankunlaw.com", "desc": "Leading in PE/VC & Tech"},
                {"name": "竞天公诚 (Jingtian)", "url": "http://www.jingtian.com", "desc": "Capital Markets Specialist"},
                {"name": "通商 (C&F)", "url": "http://www.tongshang.com", "desc": "Capital Markets & Dispute"},
                {"name": "环球 (Global Law)", "url": "http://www.glo.com.cn", "desc": "Oldest PRC Firm"},
                {"name": "天同 (Tiantong)", "url": "https://www.tiantonglaw.com", "desc": "Supreme Court Litigation"},
                {"name": "植德 (Merits & Tree)", "url": "http://www.meritsandtree.com", "desc": "Asset Management"},
            ],
            "🏙️ Major Commercial Firms (大型综合律所)": [
                {"name": "锦天城 (AllBright)", "url": "https://www.allbrightlaw.com", "desc": "Shanghai-based Giant"},
                {"name": "大成 (Dentons CN)", "url": "https://www.dentons.com.cn", "desc": "Largest Global Coverage"},
                {"name": "盈科 (Yingke)", "url": "http://www.yingkelawyer.com", "desc": "Global Network Firm"},
                {"name": "国浩 (Grandall)", "url": "http://www.grandall.com.cn", "desc": "IPO/Securities Focus"},
                {"name": "天元 (Tian Yuan)", "url": "http://www.tylaw.com.cn", "desc": "Comprehensive Practice"},
                {"name": "中银 (Zhong Yin)", "url": "http://www.zhongyinlawyer.com", "desc": "Banking & Finance"},
                {"name": "德恒 (DeHeng)", "url": "http://www.dehenglaw.com", "desc": "Govt & Infrastructure"},
                {"name": "京师 (Jingsh)", "url": "http://www.jingsh.com", "desc": "Large Scale Partnership"},
                {"name": "隆安 (Long An)", "url": "http://www.longanlaw.com", "desc": "IP & Commercial"},
                {"name": "炜衡 (Weiheng)", "url": "http://www.weihenglaw.com", "desc": "Comprehensive Litigation"},
                {"name": "康达 (Kangda)", "url": "http://www.kangdalawyers.com", "desc": "Criminal Defense"},
                {"name": "泰和泰 (Tahota)", "url": "http://www.tahota.com", "desc": "Leading West China Firm"},
                {"name": "建纬 (City Development)", "url": "http://www.jianwei.com", "desc": "Construction & RE"},
                {"name": "广悦 (Guangyue)", "url": "http://www.guangyuelaw.com", "desc": "Guangzhou Leading"},
                {"name": "安杰世泽 (AnJie Broad)", "url": "http://www.anjielaw.com", "desc": "Insurance & Antitrust"},
                {"name": "汇业 (Hui Ye)", "url": "http://www.huiyelaw.com", "desc": "Corporate & Compliance"},
                {"name": "中伦文德 (ZW)", "url": "http://www.zlwd.com", "desc": "Insurance & Dispute"},
                {"name": "融孚 (Rong Fu)", "url": "http://www.rongfulaw.com", "desc": "Finance & Real Estate"},
                {"name": "万商天勤 (WS)", "url": "http://www.wandl-law.com", "desc": "Commercial & Dispute"},
                {"name": "法兰克 (Frank)", "url": "http://www.franklawfirm.com", "desc": "IP & Tech"},
                {"name": "浩天 (Hao Tian)", "url": "http://www.haotianlawyers.com", "desc": "Dispute Resolution"},
            ],
            "🔬 IP & Boutique (知识产权/精品)": [
                {"name": "CCPIT Patent (贸促会)", "url": "https://www.ccpit-patent.com.cn", "desc": "Oldest IP Agency"},
                {"name": "Lung Tin (隆天)", "url": "http://www.lungtin.com", "desc": "IP Litigation"},
                {"name": "Liu, Shen (柳沈)", "url": "http://www.liushen.com", "desc": "Patent Prosecution"},
                {"name": "Wanhuida (万慧达)", "url": "http://www.wanhuida.com", "desc": "Trademark & IP"},
                {"name": "Merits & Tree (植德)", "url": "http://www.meritsandtree.com", "desc": "Asset Management"},
                {"name": "Llinks (通力)", "url": "http://www.llinkslaw.com", "desc": "Financial Law"},
                {"name": "AnJie Broad (安杰世泽)", "url": "http://www.anjielaw.com", "desc": "Antitrust & Insurance"},
            ],
            "💼 Compliance & Consulting (合规/四大)": [
                {"name": "普华永道 (PwC Legal)", "url": "https://www.pwccn.com", "desc": "Legal & Tax Services"},
                {"name": "德勤 (Deloitte Legal)", "url": "https://www2.deloitte.com/cn", "desc": "Legal Consulting"},
                {"name": "安永 (EY Law)", "url": "https://www.ey.com/cn", "desc": "Corporate Law Services"},
                {"name": "毕马威 (KPMG Law)", "url": "https://home.kpmg/cn", "desc": "Legal Compliance"},
                {"name": "甫瀚咨询 (Protiviti)", "url": "https://www.protiviti.com", "desc": "Risk & Compliance"},
                {"name": "贝克顾法律 (Baker & McKenzie CN)", "url": "https://www.bakermckenzie.com", "desc": "Foreign Law Firm"},
            ],
            "⚖️ Official & Judiciary (官方司法/监管)": [
                {"name": "裁判文书网", "url": "https://wenshu.court.gov.cn", "desc": "Supreme Court Judgments"},
                {"name": "法律法规库", "url": "https://flk.npc.gov.cn", "desc": "Official Laws Database"},
                {"name": "执行信息网", "url": "http://zxgk.court.gov.cn", "desc": "Enforcement Information"},
                {"name": "庭审公开网", "url": "http://tingshen.court.gov.cn", "desc": "Court Trial Live"},
                {"name": "知识产权局 (CNIPA)", "url": "https://www.cnipa.gov.cn", "desc": "Patent & Trademark Office"},
                {"name": "市监总局 (SAMR)", "url": "https://www.samr.gov.cn", "desc": "Antitrust & Regulation"},
                {"name": "网信办 (CAC)", "url": "http://www.cac.gov.cn", "desc": "Cybersecurity"},
                {"name": "证监会 (CSRC)", "url": "http://www.csrc.gov.cn", "desc": "Securities Regulator"},
                {"name": "最高检 (SPP)", "url": "https://www.spp.gov.cn", "desc": "Supreme Procuratorate"},
                {"name": "司法部 (MoJ)", "url": "http://www.moj.gov.cn", "desc": "Ministry of Justice"},
                {"name": "中国律协", "url": "http://www.allchina-lawyers.org", "desc": "All China Lawyers Assn"},
                {"name": "贸仲委 (CIETAC)", "url": "http://www.cietac.org", "desc": "Intl Arbitration"},
                {"name": "北仲 (BAC)", "url": "https://www.bjac.org.cn", "desc": "Beijing Arbitration"},
                {"name": "深仲 (SCIA)", "url": "http://www.scia.com.cn", "desc": "Shenzhen Arbitration"},
                {"name": "上仲 (SHiac)", "url": "http://www.shiac.org", "desc": "Shanghai Arbitration"},
            ],
        },
        "🇯🇵 Japan (日本)": {
            "🏛️ Big Four (四大律所)": [
                {"name": "Nishimura & Asahi", "url": "https://www.nishimura.com", "desc": "Largest in Japan"},
                {"name": "Nagashima Ohno (NO&T)", "url": "https://www.noandt.com", "desc": "Corporate Elite"},
                {"name": "Mori Hamada (MHM)", "url": "https://www.mhmjapan.com", "desc": "M&A and Finance"},
                {"name": "Anderson Mori (AMT)", "url": "https://www.amt-law.com", "desc": "International Focus"},
            ],
            "⛩️ Major Firms (主要律所)": [
                {"name": "TMI Associates", "url": "https://www.tmi.gr.jp", "desc": "IP & Corporate Mix"},
                {"name": "City-Yuwa", "url": "https://www.city-yuwa.com", "desc": "Finance Real Estate"},
                {"name": "Atsumi & Sakai", "url": "https://www.aplaw.jp", "desc": "Fintech Innovation"},
                {"name": "Oh-Ebashi", "url": "https://www.ohebashi.com", "desc": "Osaka Leader"},
                {"name": "Ushijima & Partners", "url": "https://www.ushijima-law.gr.jp", "desc": "Litigation"},
            ],
            "🌍 Gaiben (外资所)": [
                {"name": "Baker McKenzie Tokyo", "url": "https://www.bakermckenzie.co.jp", "desc": "Largest International"},
                {"name": "Morrison Foerster", "url": "https://www.mofo.com", "desc": "Tech & IP Leader"},
                {"name": "White & Case Tokyo", "url": "https://www.whitecase.com", "desc": "Projects"},
                {"name": "Skadden Tokyo", "url": "https://www.skadden.com", "desc": "M&A"},
            ],
            "💻 Tech & Official": [
                {"name": "Bengo4.com", "url": "https://www.bengo4.com", "desc": "Lawyer Portal"},
                {"name": "LegalOn Cloud", "url": "https://www.legalon-cloud.com", "desc": "AI Contract"},
                {"name": "CloudSign", "url": "https://www.cloudsign.jp", "desc": "E-Signature"},
                {"name": "MNTSQ", "url": "https://www.mntsq.co.jp", "desc": "Contract Database"},
                {"name": "J-PlatPat", "url": "https://www.j-platpat.inpit.go.jp", "desc": "IP Database"},
                {"name": "e-Gov Japan", "url": "https://www.e-gov.go.jp", "desc": "Laws"},
            ]
        },
        "🇸🇬 Singapore (新加坡)": {
            "🏛️ Big Four Firms": [
                {"name": "Allen & Gledhill", "url": "https://www.allenandgledhill.com", "desc": "Largest SG Firm"},
                {"name": "Rajah & Tann", "url": "https://www.rajahtannasia.com", "desc": "Full Service Asia"},
                {"name": "WongPartnership", "url": "https://www.wongpartnership.com", "desc": "Corporate Elite"},
                {"name": "Drew & Napier", "url": "https://www.drewnapier.com", "desc": "Litigation Powerhouse"},
                {"name": "Dentons Rodyk", "url": "https://www.dentonsrodyk.com", "desc": "Oldest SG Firm"},
                {"name": "Shook Lin & Bok", "url": "https://www.shooklin.com", "desc": "Banking & Finance"},
                {"name": "RPC Premier Law", "url": "https://www.rpc.com.sg", "desc": "Insurance & Dispute"},
                {"name": "TSMP Law", "url": "https://tsmplaw.com", "desc": "Boutique Corporate"},
                {"name": "Duane Morris & Selvam", "url": "https://www.duanemorris.com/singapore", "desc": "US Intl Presence"},
                {"name": "Withers KhattarWong", "url": "https://www.withersworldwide.com", "desc": "Private Client"},
                {"name": "Cavenagh Law", "url": "https://www.cliffordchance.com", "desc": "Clifford Chance JLV"},
                {"name": "Allen & Overy SG", "url": "https://www.allenovery.com", "desc": "Projects & Finance"},
                {"name": "Freshfields SG", "url": "https://www.freshfields.com", "desc": "M&A & Arbitration"},
                {"name": "Linklaters SG", "url": "https://www.linklaters.com", "desc": "Capital Markets"},
                {"name": "Gibson Dunn SG", "url": "https://www.gibsondunn.com", "desc": "Disputes"},
            ],
            "⚖️ Official & Tech": [
                {"name": "Singapore Law Watch", "url": "https://www.singaporelawwatch.sg", "desc": "Legal News & Updates"},
                {"name": "LawNet", "url": "https://www.lawnet.sg", "desc": "Legal Research Portal"},
                {"name": "Supreme Court SG", "url": "https://www.judiciary.gov.sg", "desc": "Judiciary"},
                {"name": "ACRA", "url": "https://www.acra.gov.sg", "desc": "Company Registry"},
                {"name": "IPOS", "url": "https://www.ipos.gov.sg", "desc": "Intellectual Property"},
                {"name": "SIAC", "url": "https://siac.org.sg", "desc": "Intl Arbitration Centre"},
                {"name": "LiteLab", "url": "https://litelab.com", "desc": "Legal Intelligence"},
                {"name": "Lupl", "url": "https://www.lupl.com", "desc": "Matter Management"},
                {"name": "MinLaw", "url": "https://www.mlaw.gov.sg", "desc": "Ministry of Law"},
                {"name": "SICC", "url": "https://www.sicc.gov.sg", "desc": "Intl Commercial Court"},
                {"name": "Law Society SG", "url": "https://www.lawsociety.org.sg", "desc": "Professional Body"},
            ],
            "💼 Consulting": [
                {"name": "Deloitte Legal SG", "url": "https://www2.deloitte.com/sg", "desc": "Consulting"},
                {"name": "PwC Legal SG", "url": "https://www.pwc.com/sg", "desc": "Advisory"},
            ]
        },
        "🇰🇷 South Korea (韩国)": {
            "🏛️ Big 6 Firms": [
                {"name": "Kim & Chang", "url": "https://www.kimchang.com", "desc": "Dominant Leader"},
                {"name": "Lee & Ko", "url": "http://www.leeko.com", "desc": "Premier Firm"},
                {"name": "Bae, Kim & Lee (BKL)", "url": "https://www.bkl.co.kr", "desc": "Litigation"},
                {"name": "Shin & Kim", "url": "https://www.shinkim.com", "desc": "Global Corp"},
                {"name": "Yulchon", "url": "https://www.yulchon.com", "desc": "Tax & Dispute"},
                {"name": "Yoon & Yang", "url": "https://www.yoonyang.com", "desc": "Antitrust"},
            ],
            "⚖️ Official": [
                {"name": "Supreme Court", "url": "https://eng.scourt.go.kr", "desc": "Judiciary"},
                {"name": "Statutes of Korea", "url": "https://elaw.klri.re.kr", "desc": "Laws"},
                {"name": "KIPO", "url": "https://www.kipo.go.kr", "desc": "IP Office"},
            ]
        },
        "🇮🇳 India (印度)": {
            "🏛️ Top Firms": [
                {"name": "Cyril Amarchand Mangaldas", "url": "https://www.cyrilshroff.com", "desc": "Largest Firm"},
                {"name": "Shardul Amarchand Mangaldas", "url": "https://www.amsshardul.com", "desc": "Premium Corp"},
                {"name": "Khaitan & Co", "url": "https://www.khaitanco.com", "desc": "Oldest & Leading"},
                {"name": "AZB & Partners", "url": "https://www.azbpartners.com", "desc": "M&A Specialist"},
                {"name": "Trilegal", "url": "https://www.trilegal.com", "desc": "Modern Full Service"},
                {"name": "IndusLaw", "url": "https://www.induslaw.com", "desc": "Tech & VC"},
                {"name": "Nishith Desai", "url": "https://www.nishithdesai.com", "desc": "Tax & Tech Boutique"},
            ],
            "⚖️ Gov": [
                {"name": "Supreme Court", "url": "https://main.sci.gov.in", "desc": "Highest Court"},
                {"name": "Manupatra", "url": "https://www.manupatra.com", "desc": "Legal Research"},
            ]
        },
    }
}

# ======================== 核心功能 ========================
def main():
    # 页面标题
    st.title("🌐 Global Legal Institutions | 全球法律机构库")
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # 提取所有地区、国家、类别选项
    regions = list(LEGAL_DATA.keys())
    selected_region = st.selectbox("🌍 Select Region | 选择地区", regions)

    # 根据选中的地区获取国家列表
    countries = list(LEGAL_DATA[selected_region].keys())
    selected_country = st.selectbox("🇨🇳 Select Country | 选择国家", countries)

    # 根据选中的国家获取类别列表
    categories = list(LEGAL_DATA[selected_region][selected_country].keys())
    selected_category = st.selectbox("📌 Select Category | 选择类别", categories)

    # 分隔线
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # 显示选中类别的机构列表
    institutions = LEGAL_DATA[selected_region][selected_country][selected_category]
    
    st.subheader(f"{selected_category} ({len(institutions)} institutions)")
    
    # 渲染机构卡片
    for inst in institutions:
        st.markdown(f"""
        <div class="institution-card">
            <a href="{inst['url']}" target="_blank" class="institution-link">{inst['name']}</a>
            <div class="institution-desc">{inst['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# ======================== 运行应用 ========================
if __name__ == "__main__":
    main()
