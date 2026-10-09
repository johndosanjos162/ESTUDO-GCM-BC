"""Página de login e cadastro."""

import streamlit as st
from core.auth import cadastrar_usuario, login as auth_login
from utils.helpers import inicializar_session_state

inicializar_session_state()

st.title("🔐 Acesso ao Sistema")
st.caption("Entre ou crie sua conta para começar a estudar.")

aba_login, aba_cadastro = st.tabs(["Entrar", "Cadastrar"])

with aba_login:
    with st.form("form_login", clear_on_submit=False):
        email = st.text_input("E-mail", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")
        enviar = st.form_submit_button("Entrar", use_container_width=True)

    if enviar:
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

with aba_cadastro:
    with st.form("form_cadastro", clear_on_submit=False):
        nome = st.text_input("Nome completo", key="cad_nome")
        email_c = st.text_input("E-mail", key="cad_email")
        senha_c = st.text_input("Senha (mín. 6 caracteres)", type="password", key="cad_senha")
        confirmar = st.text_input("Confirme a senha", type="password", key="cad_conf")
        criar = st.form_submit_button("Criar conta", use_container_width=True)

    if criar:
        if not nome or not email_c or not senha_c:
            st.warning("Preencha todos os campos.")
        elif senha_c != confirmar:
            st.warning("As senhas não coincidem.")
        elif len(senha_c) < 6:
            st.warning("A senha deve ter ao menos 6 caracteres.")
        else:
            try:
                cadastrar_usuario(email_c, senha_c, nome)
                st.success("Conta criada! Verifique seu e-mail se a confirmação estiver ativa.")
            except Exception as e:
                st.error(f"Erro ao cadastrar: {e}")
