"""Configurações e perfil."""

import streamlit as st
from config import BLOCOS
from core.cycle_manager import obter_ciclo_atual, alternar_ciclo
from core.auth import logout
from core.database import obter_perfil
from utils.helpers import inicializar_session_state

inicializar_session_state()

user = st.session_state.get("user")
if not user:
    st.switch_page("pages/0_🔐_Login.py")
    st.stop()

st.title("⚙️ Configurações")

perfil = obter_perfil(user.id) or {}

st.subheader("👤 Perfil")
st.write(f"**Nome:** {perfil.get('nome', '—')}")
st.write(f"**E-mail:** {perfil.get('email', getattr(user, 'email', '—'))}")
st.write(f"**ID:** `{user.id}`")

st.divider()

st.subheader("🔄 Ciclo de Estudos")
ciclo = obter_ciclo_atual(user.id)
st.write(f"Ciclo ativo: **Semana {'A' if ciclo['numero_ciclo'] == 1 else 'B'}**")
for nome in ciclo["nomes"]:
    st.write(f"- {nome}")
st.caption(f"Próxima alternância automática: {ciclo['proxima_alternancia']}")

if st.button("🔀 Alternar ciclo manualmente", use_container_width=True):
    novo = alternar_ciclo(user.id)
    st.success(f"Ciclo alterado para Semana {'A' if novo == 1 else 'B'}.")
    st.rerun()

st.divider()

st.subheader("📚 Blocos de Estudo")
for chave, nome in BLOCOS.items():
    st.write(f"- **{nome}**")

st.divider()

if st.button("🚪 Encerrar sessão", use_container_width=True):
    logout()
    st.session_state.user = None
    st.rerun()
