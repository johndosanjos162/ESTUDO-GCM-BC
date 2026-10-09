"""Página de login — acesso restrito, sem cadastro público."""

import streamlit as st
from core.auth import login as auth_login
from utils.helpers import inicializar_session_state

inicializar_session_state()

st.title("🔐 Acesso Restrito")
st.caption("Entre com suas credenciais para acessar o sistema.")

with st.form("form_login", clear_on_submit=False):
    email = st.text_input("E-mail", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_senha")
    enviar = st.form_submit_button("Entrar", use_container_width=True)

if enviar:
    if not email or not senha:
        st.warning("Preencha e-mail e senha.")
    else:
        try:
            resultado = auth_login(email, senha)
            if resultado.user:
                st.session_state.user = resultado.user
                st.success("Login realizado com sucesso!")
                st.switch_page("pages/1_🏠_Home.py")
            else:
                st.error("Credenciais inválidas.")
        except Exception as e:
            st.error(f"Erro ao entrar: {e}")

st.divider()
st.caption("🔒 Sistema de uso restrito. Não há cadastro público.")
