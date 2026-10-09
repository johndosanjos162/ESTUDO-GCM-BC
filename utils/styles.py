"""CSS customizado do Streamlit — tema tecnológico avançado."""

import streamlit as st


def carregar_css() -> None:
    """Carrega o CSS global do app."""
    st.markdown("""
<style>
/* ============================================================
   FUNDO GERAL
   ============================================================ */
.stApp {
    background: radial-gradient(circle at 20% 20%, #0a1628 0%, #050810 60%, #000000 100%);
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(0, 255, 255, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 255, 0.02) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
    position: relative;
    z-index: 1;
}

/* ============================================================
   SIDEBAR
   ============================================================ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071018 0%, #0a1628 100%) !important;
    border-right: 1px solid rgba(0, 229, 255, 0.2) !important;
    box-shadow: 4px 0 30px rgba(0, 229, 255, 0.1) !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 20px;
}

section[data-testid="stSidebar"] h1 {
    color: #00e5ff !important;
    font-family: 'Courier New', monospace !important;
    font-size: 18px !important;
    letter-spacing: 2px !important;
    text-shadow: 0 0 10px #00e5ff !important;
}

section[data-testid="stSidebar"] .stButton button {
    background: rgba(0, 229, 255, 0.08) !important;
    color: #00e5ff !important;
    border: 1px solid rgba(0, 229, 255, 0.3) !important;
    font-family: 'Courier New', monospace !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(0, 229, 255, 0.2) !important;
    border-color: #00ffea !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.4) !important;
    transform: translateX(3px) !important;
}

/* Navegação multipágina */
[data-testid="stSidebarNav"] a {
    font-family: 'Courier New', monospace !important;
    font-size: 13px !important;
    color: #8fb8cc !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(0, 229, 255, 0.1) !important;
    color: #00e5ff !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(90deg, rgba(0, 229, 255, 0.2), transparent) !important;
    color: #00ffea !important;
    border-left: 3px solid #00ffea !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.3) !important;
}

/* ============================================================
   TIPOGRAFIA
   ============================================================ */
h1, h2, h3 {
    font-family: 'Courier New', monospace !important;
    color: #ffffff !important;
    letter-spacing: 1px !important;
}

h1 {
    font-size: 28px !important;
    text-shadow: 0 0 20px rgba(0, 229, 255, 0.5) !important;
    border-bottom: 1px solid rgba(0, 229, 255, 0.3);
    padding-bottom: 15px !important;
    margin-bottom: 25px !important;
}

h2 {
    font-size: 20px !important;
    color: #00e5ff !important;
    text-shadow: 0 0 10px rgba(0, 229, 255, 0.4) !important;
}

h3 {
    font-size: 16px !important;
    color: #00ffea !important;
}

p, li, label, span {
    color: #b8d4e0 !important;
}

/* ============================================================
   BOTÕES
   ============================================================ */
.stButton button {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.15), rgba(0, 136, 255, 0.1)) !important;
    color: #00e5ff !important;
    border: 1px solid rgba(0, 229, 255, 0.4) !important;
    border-radius: 8px !important;
    font-family: 'Courier New', monospace !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 1.5px !important;
    padding: 12px 20px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0, 229, 255, 0.1) !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.3), rgba(0, 136, 255, 0.2)) !important;
    border-color: #00ffea !important;
    color: #ffffff !important;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.5) !important;
    transform: translateY(-2px) !important;
}

.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #00e5ff 0%, #0088ff 100%) !important;
    color: #000814 !important;
    border: none !important;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.5) !important;
}

.stButton button[kind="primary"]:hover {
    background: linear-gradient(135deg, #00ffea 0%, #00a8ff 100%) !important;
    box-shadow: 0 0 30px rgba(0, 229, 255, 0.8) !important;
}

/* ============================================================
   MÉTRICAS
   ============================================================ */
div[data-testid="stMetric"] {
    background: rgba(10, 22, 40, 0.7) !important;
    border: 1px solid rgba(0, 229, 255, 0.25) !important;
    border-radius: 12px !important;
    padding: 18px !important;
    backdrop-filter: blur(8px) !important;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.08) !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stMetric"]:hover {
    border-color: #00e5ff !important;
    box-shadow: 0 0 25px rgba(0, 229, 255, 0.25) !important;
    transform: translateY(-3px) !important;
}

div[data-testid="stMetric"] label {
    color: #00e5ff !important;
    font-family: 'Courier New', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'Courier New', monospace !important;
    font-size: 24px !important;
    text-shadow: 0 0 15px rgba(0, 229, 255, 0.5) !important;
}

/* ============================================================
   INPUTS
   ============================================================ */
.stTextInput input,
.stSelectbox div[data-baseweb="select"],
.stNumberInput input,
.stTextArea textarea {
    background: rgba(0, 20, 35, 0.7) !important;
    border: 1px solid rgba(0, 229, 255, 0.3) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-family: 'Courier New', monospace !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border-color: #00ffea !important;
    box-shadow: 0 0 15px rgba(0, 255, 234, 0.4) !important;
}

.stSelectbox label p,
.stNumberInput label p,
.stSlider label p,
.stTextInput label p,
.stMultiSelect label p {
    color: #00e5ff !important;
    font-family: 'Courier New', monospace !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* ============================================================
   PROGRESS
   ============================================================ */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00e5ff, #00ffea) !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.6) !important;
}

.stProgress > div > div {
    background: rgba(0, 229, 255, 0.1) !important;
    border-radius: 6px !important;
}

/* ============================================================
   ALERTAS
   ============================================================ */
.stAlert {
    background: rgba(0, 20, 35, 0.85) !important;
    border-radius: 8px !important;
    border-left: 3px solid #00e5ff !important;
    backdrop-filter: blur(8px) !important;
}

/* ============================================================
   EXPANDER
   ============================================================ */
.streamlit-expanderHeader,
details summary {
    background: rgba(10, 22, 40, 0.7) !important;
    border: 1px solid rgba(0, 229, 255, 0.2) !important;
    border-radius: 8px !important;
    font-family: 'Courier New', monospace !important;
    color: #00e5ff !important;
    transition: all 0.3s ease !important;
}

.streamlit-expanderHeader:hover,
details summary:hover {
    border-color: #00e5ff !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.3) !important;
}

/* ============================================================
   RADIO
   ============================================================ */
.stRadio > div {
    background: rgba(10, 22, 40, 0.5) !important;
    border: 1px solid rgba(0, 229, 255, 0.15) !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

.stRadio label {
    font-size: 14px !important;
    color: #d8e8f0 !important;
    padding: 8px 10px !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
}

.stRadio label:hover {
    background: rgba(0, 229, 255, 0.08) !important;
    color: #00e5ff !important;
}

/* ============================================================
   DIVIDER
   ============================================================ */
hr {
    border-color: rgba(0, 229, 255, 0.2) !important;
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.15) !important;
}

/* ============================================================
   TABS
   ============================================================ */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(10, 22, 40, 0.6) !important;
    border: 1px solid rgba(0, 229, 255, 0.2) !important;
    border-radius: 8px !important;
    padding: 10px 18px !important;
    font-family: 'Courier New', monospace !important;
    font-size: 12px !important;
    color: #8fb8cc !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.25), rgba(0, 136, 255, 0.15)) !important;
    color: #00ffea !important;
    border-color: #00e5ff !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.3) !important;
}

/* ============================================================
   DOWNLOAD BUTTON
   ============================================================ */
.stDownloadButton button {
    background: linear-gradient(135deg, #00ff88 0%, #00cc66 100%) !important;
    color: #001a0d !important;
    border: none !important;
    font-family: 'Courier New', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.4) !important;
}

.stDownloadButton button:hover {
    box-shadow: 0 0 30px rgba(0, 255, 136, 0.7) !important;
    transform: translateY(-2px) !important;
}

/* ============================================================
   ESCONDE ELEMENTOS PADRÃO
   ============================================================ */
#MainMenu, footer, header { visibility: hidden; }

/* ============================================================
   CLASSES AUXILIARES (uso via HTML)
   ============================================================ */
.tech-card {
    background: rgba(10, 22, 40, 0.7);
    border: 1px solid rgba(0, 229, 255, 0.25);
    border-radius: 14px;
    padding: 20px;
    margin: 10px 0;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 25px rgba(0, 229, 255, 0.08);
    transition: all 0.3s ease;
}

.tech-card:hover {
    border-color: #00e5ff;
    box-shadow: 0 0 30px rgba(0, 229, 255, 0.25);
    transform: translateY(-3px);
}

.tech-badge {
    display: inline-block;
    padding: 4px 12px;
    background: rgba(0, 229, 255, 0.15);
    border: 1px solid rgba(0, 229, 255, 0.4);
    border-radius: 20px;
    font-family: 'Courier New', monospace;
    font-size: 10px;
    color: #00e5ff;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.tech-title {
    font-family: 'Courier New', monospace;
    font-size: 18px;
    color: #ffffff;
    letter-spacing: 1px;
    margin: 10px 0;
    text-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
}

.tech-sub {
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    color: #8fb8cc;
    margin: 5px 0;
}

.tech-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #00e5ff, transparent);
    margin: 15px 0;
    box-shadow: 0 0 10px #00e5ff;
}
</style>
""", unsafe_allow_html=True)
