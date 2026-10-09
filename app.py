"""Ponto de entrada do Streamlit."""

import streamlit as st

from config import APP_TITLE, APP_ICON, APP_LAYOUT, validar_configuracoes
from utils.styles import carregar_css
from utils.helpers import inicializar_session_state

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
    initial_sidebar_state="expanded",
)

carregar_css()
inicializar_session_state()

faltando = validar_configuracoes()
if faltando:
    st.error(
        "⚠️ Variáveis de ambiente ausentes: " + ", ".join(faltando)
        + "\n\nConfigure os Secrets no Streamlit Cloud ou o .env local."
    )
    st.stop()

with st.sidebar:
    st.title(f"{APP_ICON} Estudos GMBC")
    st.caption("Guarda Municipal de Balneário Camboriú")

    user = st.session_state.get("user")
    if user:
        st.success(f"👤 {getattr(user, 'email', 'usuário')}")
        if st.button("🚪 Sair", use_container_width=True):
            from core.auth import logout
            logout()
            st.session_state.user = None
            st.rerun()
    else:
        st.info("Faça login para começar.")

    st.divider()
    st.caption("Navegue pelo menu acima ☝️")

if not st.session_state.get("user"):
    st.switch_page("pages/0_🔐_Login.py")
else:
    st.switch_page("pages/1_🏠_Home.py")
