"""Repositório de questões geradas."""

import streamlit as st
from config import BLOCOS
from core.database import buscar_questoes_por_disciplina, listar_questoes
from utils.helpers import inicializar_session_state, parse_alternativas

inicializar_session_state()

user = st.session_state.get("user")
if not user:
    st.switch_page("pages/0_🔐_Login.py")
    st.stop()

st.title("📚 Repositório de Questões")

filtro = st.selectbox(
    "Bloco",
    options=["Todos"] + list(BLOCOS.keys()),
    format_func=lambda x: "Todos" if x == "Todos" else BLOCOS[x],
)

if filtro == "Todos":
    questoes = listar_questoes(limite=100)
else:
    questoes = buscar_questoes_por_disciplina(filtro, limite=100)

st.caption(f"**{len(questoes)}** questões encontradas.")

if not questoes:
    st.info("Nenhuma questão no repositório para este filtro.")
    st.stop()

for i, q in enumerate(questoes, start=1):
    alternativas = parse_alternativas(q["alternativas"])
    titulo = f"[{BLOCOS.get(q['disciplina'], q['disciplina'])}] {q['enunciado'][:80]}..."
    with st.expander(titulo):
        st.write(q["enunciado"])
        for j, alt in enumerate(alternativas):
            letra = chr(65 + j)
            marca = " ✅" if letra == q["resposta_correta"] else ""
            st.write(f"**{letra})** {alt}{marca}")

        if q.get("explicacao"):
            st.info(f"💡 {q['explicacao']}")

        st.caption(
            f"Dificuldade: {q.get('dificuldade', '-')} | "
            f"Fonte: {q.get('fonte', '-')} | "
            f"Criada em: {q.get('criado_em', '-')}"
        )
