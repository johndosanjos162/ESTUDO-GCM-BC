"""Dashboard principal."""

import streamlit as st
from config import BLOCOS
from core.cycle_manager import obter_ciclo_atual
from core.database import estatisticas_por_disciplina, buscar_historico_usuario
from utils.helpers import inicializar_session_state, calcular_percentual

inicializar_session_state()

user = st.session_state.get("user")
if not user:
    st.switch_page("pages/0_🔐_Login.py")
    st.stop()

st.title("🏠 Dashboard de Estudos")
st.caption(f"Bem-vindo(a), {getattr(user, 'email', 'estudante')}!")

ciclo = obter_ciclo_atual(user.id)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📅 Ciclo ativo: Semana {'A' if ciclo['numero_ciclo'] == 1 else 'B'}")
    for chave in ciclo["disciplinas"]:
        nome = BLOCOS.get(chave, chave)
        st.markdown(f"- **{nome}**")

with col2:
    st.metric("Próxima alternância", ciclo["proxima_alternancia"])

st.divider()

st.subheader("📊 Desempenho por bloco")
stats = estatisticas_por_disciplina(user.id)

if stats:
    for s in stats:
        nome = BLOCOS.get(s["disciplina"], s["disciplina"])
        total = int(s.get("total", 0))
        acertos = int(s.get("acertos", 0))
        pct = calcular_percentual(acertos, total)
        st.progress(pct / 100, text=f"{nome} — {acertos}/{total} ({pct}%)")
else:
    st.info("Nenhuma resposta registrada ainda. Vamos começar?")

st.divider()

col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.button("📝 Iniciar Estudo", use_container_width=True):
        st.switch_page("pages/2_📝_Estudar.py")
with col_b:
    if st.button("📚 Repositório", use_container_width=True):
        st.switch_page("pages/4_📚_Repositorio.py")
with col_c:
    if st.button("📊 Histórico", use_container_width=True):
        st.switch_page("pages/3_📊_Historico.py")

st.divider()
st.subheader("🕒 Últimas respostas")
historico = buscar_historico_usuario(user.id, limite=5)
if historico:
    for r in historico:
        nome = BLOCOS.get(r["disciplina"], r["disciplina"])
        icone = "✅" if r.get("acertou") else "❌"
        st.write(f"{icone} **{nome}** — sua resposta: {r['resposta_usuario']} | correta: {r['resposta_correta']}")
else:
    st.caption("Sem respostas recentes.")

from core.database import contar_questoes_por_disciplina
from config import BLOCOS

st.subheader("📚 Banco de questões por bloco")
for chave, nome in BLOCOS.items():
    try:
        total = contar_questoes_por_disciplina(chave)
        st.write(f"- **{nome}**: {total} questões no banco")
    except Exception:
        st.write(f"- **{nome}**: indisponível")
