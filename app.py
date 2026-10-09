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

# ============================================================
# VALIDAÇÃO DE CONFIGURAÇÃO
# ============================================================
faltando = validar_configuracoes()
if faltando:
    st.error(
        "⚠️ Variáveis de ambiente ausentes: " + ", ".join(faltando)
        + "\n\nConfigure os Secrets no Streamlit Cloud."
    )
    st.stop()

# ============================================================
# VERIFICA SE ESTÁ LOGADO
# ============================================================
logado = bool(st.session_state.get("user"))

# ============================================================
# ESCONDE A SIDEBAR QUANDO NÃO ESTIVER LOGADO
# ============================================================
if not logado:
    st.markdown(
        """
        <style>
        /* Esconde a barra lateral inteira */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        /* Remove o botão de abrir/fechar a sidebar */
        button[data-testid="collapsedControl"] {
            display: none !important;
        }
        /* Esconde a navegação multipágina automática */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Redireciona para Login
    st.switch_page("pages/0_🔐_Login.py")
    st.stop()

# ============================================================
# SIDEBAR (só aparece quando logado)
# ============================================================
with st.sidebar:
    st.title(f"{APP_ICON} Estudos GMBC")
    st.caption("Guarda Municipal de Balneário Camboriú")

    user = st.session_state.get("user")
    st.success(f"👤 {getattr(user, 'email', 'usuário')}")

    if st.button("🚪 Sair", use_container_width=True):
        from core.auth import logout
        logout()
        st.session_state.user = None
        st.rerun()

    st.divider()
    st.caption("Navegue pelo menu acima ☝️")

# ============================================================
# REDIRECIONA PARA HOME (já logado)
# ============================================================
st.switch_page("pages/1_🏠_Home.py")
