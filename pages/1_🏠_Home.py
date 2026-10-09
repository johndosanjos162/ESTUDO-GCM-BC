"""Dashboard principal — visual tecnológico."""

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

# ============================================================
# CABEÇALHO VISUAL
# ============================================================
st.markdown(f"""
<div style="margin-bottom: 25px;">
    <div class="tech-badge">PAINEL DO ESTUDANTE</div>
    <h1 style="margin: 8px 0 0 0; border: none; padding: 0; font-size: 32px !important;">
        Bem-vindo(a), {getattr(user, 'email', 'estudante').split('@')[0]}!
    </h1>
    <p style="color: #8fb8cc; font-size: 13px; letter-spacing: 1px; margin-top: 5px;">
        🎯 Prepare-se para a Guarda Municipal de Balneário Camboriú
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CICLO ATIVO
# ============================================================
ciclo = obter_ciclo_atual(user.id)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📅 Ciclo ativo: Semana {'A' if ciclo['numero_ciclo'] == 1 else 'B'}")
    for nome in ciclo["nomes"]:
        st.markdown(f"- **{nome}**")

with col2:
    st.metric("Próxima alternância", ciclo["proxima_alternancia"])

st.divider()

# ============================================================
# DESEMPENHO POR BLOCO
# ============================================================
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

# ============================================================
# AÇÕES RÁPIDAS
# ============================================================
col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.button("📝 Iniciar Estudo", use_container_width=True, type="primary"):
        st.switch_page("pages/2_📝_Estudar.py")
with col_b:
    if st.button("📚 Repositório", use_container_width=True):
        st.switch_page("pages/4_📚_Repositorio.py")
with col_c:
    if st.button("📊 Histórico", use_container_width=True):
        st.switch_page("pages/3_📊_Historico.py")

st.divider()

# ============================================================
# ÚLTIMAS RESPOSTAS
# ============================================================
st.subheader("🕒 Últimas respostas")
historico = buscar_historico_usuario(user.id, limite=5)
if historico:
    for r in historico:
        nome = BLOCOS.get(r["disciplina"], r["disciplina"])
        icone = "✅" if r.get("acertou") else "❌"
        st.write(f"{icone} **{nome}** — sua resposta: {r['resposta_usuario']} | correta: {r['resposta_correta']}")
else:
    st.caption("Sem respostas recentes.")
