"""Página de login — visual de tecnologia avançada."""

import streamlit as st
from core.auth import login as auth_login
from utils.helpers import inicializar_session_state

inicializar_session_state()

# ============================================================
# CSS CUSTOMIZADO — ESTILO CYBER/TECH
# ============================================================
st.markdown("""
<style>
/* ---------- FUNDO GERAL ---------- */
.stApp {
    background: radial-gradient(circle at 20% 20%, #0a1628 0%, #050810 50%, #000000 100%);
    overflow-x: hidden;
}

/* Grade de fundo estilo "matrix" */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* Esconde a sidebar e o botão de abrir */
section[data-testid="stSidebar"] { display: none !important; }
button[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarNav"] { display: none !important; }

/* Remove espaçamentos padrão */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}

/* ---------- CONTAINER PRINCIPAL ---------- */
.login-wrapper {
    position: relative;
    z-index: 1;
    max-width: 480px;
    margin: 3vh auto 0 auto;
    padding: 0 20px;
}

/* ---------- CABEÇALHO COM ESCUDO ---------- */
.shield-container {
    text-align: center;
    margin-bottom: 10px;
}

.shield-icon {
    display: inline-block;
    font-size: 72px;
    filter: drop-shadow(0 0 20px #00e5ff) drop-shadow(0 0 40px #00e5ff);
    animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
    0%, 100% { filter: drop-shadow(0 0 20px #00e5ff) drop-shadow(0 0 40px #00e5ff); transform: scale(1); }
    50% { filter: drop-shadow(0 0 30px #00ffea) drop-shadow(0 0 60px #00ffea); transform: scale(1.05); }
}

/* ---------- TÍTULO COM EFEITO NEON ---------- */
.login-title {
    text-align: center;
    font-family: 'Courier New', monospace;
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 10px 0 5px 0;
    text-shadow:
        0 0 10px #00e5ff,
        0 0 20px #00e5ff,
        0 0 40px #00e5ff,
        0 0 80px #0088ff;
    animation: flicker 3s infinite alternate;
}

@keyframes flicker {
    0%, 100% { opacity: 1; }
    92% { opacity: 1; }
    93% { opacity: 0.7; }
    94% { opacity: 1; }
    96% { opacity: 0.85; }
    97% { opacity: 1; }
}

.login-subtitle {
    text-align: center;
    font-family: 'Courier New', monospace;
    color: #00e5ff;
    font-size: 12px;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 30px;
    opacity: 0.85;
}

/* ---------- LINHA DECORATIVA ---------- */
.tech-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, #00e5ff, #00ffea, #00e5ff, transparent);
    margin: 20px 0;
    box-shadow: 0 0 15px #00e5ff;
    animation: line-scan 4s linear infinite;
}

@keyframes line-scan {
    0% { opacity: 0.5; }
    50% { opacity: 1; }
    100% { opacity: 0.5; }
}

/* ---------- CARD DO FORMULÁRIO ---------- */
.form-card {
    background: rgba(10, 22, 40, 0.7);
    border: 1px solid rgba(0, 229, 255, 0.3);
    border-radius: 16px;
    padding: 30px 25px;
    backdrop-filter: blur(10px);
    box-shadow:
        0 0 30px rgba(0, 229, 255, 0.15),
        inset 0 0 20px rgba(0, 229, 255, 0.05);
    position: relative;
    overflow: hidden;
}

.form-card::before {
    content: "";
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(45deg, #00e5ff, #00ffea, #0088ff, #00e5ff);
    background-size: 400% 400%;
    border-radius: 16px;
    z-index: -1;
    opacity: 0.4;
    animation: border-anim 6s ease infinite;
}

@keyframes border-anim {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* ---------- LABELS ---------- */
.stTextInput label p {
    color: #00e5ff !important;
    font-family: 'Courier New', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}

/* ---------- INPUTS ---------- */
.stTextInput input {
    background: rgba(0, 20, 35, 0.8) !important;
    border: 1px solid rgba(0, 229, 255, 0.4) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-family: 'Courier New', monospace !important;
    font-size: 14px !important;
    padding: 12px 14px !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus {
    border-color: #00ffea !important;
    box-shadow:
        0 0 0 1px #00ffea,
        0 0 15px rgba(0, 255, 234, 0.5),
        inset 0 0 10px rgba(0, 255, 234, 0.1) !important;
    background: rgba(0, 30, 50, 0.9) !important;
}

.stTextInput input::placeholder {
    color: rgba(0, 229, 255, 0.4) !important;
}

/* ---------- BOTÃO PRINCIPAL ---------- */
.stFormSubmitButton button {
    width: 100% !important;
    background: linear-gradient(135deg, #00e5ff 0%, #0088ff 100%) !important;
    color: #000814 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Courier New', monospace !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 14px 20px !important;
    margin-top: 10px !important;
    box-shadow:
        0 0 20px rgba(0, 229, 255, 0.5),
        0 4px 15px rgba(0, 136, 255, 0.3) !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}

.stFormSubmitButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow:
        0 0 30px rgba(0, 229, 255, 0.8),
        0 6px 25px rgba(0, 136, 255, 0.5) !important;
    background: linear-gradient(135deg, #00ffea 0%, #00a8ff 100%) !important;
}

.stFormSubmitButton button:active {
    transform: translateY(0) !important;
}

/* ---------- RODAPÉ ---------- */
.footer-info {
    text-align: center;
    margin-top: 30px;
    padding: 15px;
    font-family: 'Courier New', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    color: rgba(0, 229, 255, 0.5);
    text-transform: uppercase;
}

.footer-info .dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    background: #00ff00;
    border-radius: 50%;
    margin-right: 6px;
    box-shadow: 0 0 8px #00ff00;
    animation: blink 2s infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ---------- ALERTAS ---------- */
.stAlert {
    background: rgba(0, 20, 35, 0.9) !important;
    border-left: 3px solid #00e5ff !important;
    border-radius: 6px !important;
    font-family: 'Courier New', monospace !important;
    font-size: 12px !important;
}

/* ---------- ESCONDE ELEMENTOS VAZIOS ---------- */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# INTERFACE DE LOGIN
# ============================================================
st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

# Escudo (ícone animado)
st.markdown("""
<div class="shield-container">
    <div class="shield-icon">🛡️</div>
</div>
""", unsafe_allow_html=True)

# Título
st.markdown('<div class="login-title">Acesso Restrito</div>', unsafe_allow_html=True)
st.markdown('<div class="login-subtitle">Sistema de Estudos GMBC</div>', unsafe_allow_html=True)
st.markdown('<div class="tech-line"></div>', unsafe_allow_html=True)

# Card do formulário
st.markdown('<div class="form-card">', unsafe_allow_html=True)

with st.form("form_login", clear_on_submit=False):
    email = st.text_input(
        "👤 Identificação",
        key="login_email",
        placeholder="seu-email@exemplo.com",
    )
    senha = st.text_input(
        "🔑 Chave de Acesso",
        type="password",
        key="login_senha",
        placeholder="••••••••",
    )
    enviar = st.form_submit_button("▸ INICIAR SESSÃO", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Processa login
if enviar:
    if not email or not senha:
        st.warning("⚠️ Preencha identificação e chave de acesso.")
    else:
        try:
            with st.spinner("Autenticando..."):
                resultado = auth_login(email, senha)
            if resultado.user:
                st.session_state.user = resultado.user
                st.success("✅ Acesso autorizado. Redirecionando...")
                st.switch_page("pages/1_🏠_Home.py")
            else:
                st.error("❌ Credenciais inválidas.")
        except Exception as e:
            st.error(f"❌ Falha na autenticação: {e}")

# Rodapé
st.markdown("""
<div class="footer-info">
    <span class="dot"></span>SISTEMA ATIVO • CONEXÃO SEGURA • CRIPTOGRAFADA
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
