"""Histórico e estatísticas."""

import streamlit as st
import pandas as pd
from config import DISCIPLINAS
from core.database import buscar_historico_usuario, estatisticas_por_disciplina
from utils.helpers import inicializar_session_state, formatar_data

inicializar_session_state()

user = st.session_state.get("user")
if not user:
    st.switch_page("pages/0_🔐_Login.py")
    st.stop()

st.title("📊 Histórico e Desempenho")

stats = estatisticas_por_disciplina(user.id)

if stats:
    st.subheader("Resumo por disciplina")
    cols = st.columns(min(len(stats), 4))
    for i, s in enumerate(stats):
        nome = DISCIPLINAS.get(s["disciplina"], s["disciplina"])
        total = int(s.get("total", 0))
        acertos = int(s.get("acertos", 0))
        pct = round((acertos / total) * 100, 1) if total else 0
        with cols[i % len(cols)]:
            st.metric(nome, f"{pct}%", f"{acertos}/{total}")

st.divider()

filtro = st.selectbox(
    "Filtrar por disciplina",
    options=["Todas"] + list(DISCIPLINAS.keys()),
    format_func=lambda x: "Todas" if x == "Todas" else DISCIPLINAS[x],
)

historico = buscar_historico_usuario(
    user.id,
    disciplina=None if filtro == "Todas" else filtro,
    limite=200,
)

if not historico:
    st.info("Sem histórico ainda.")
    st.stop()

df = pd.DataFrame(historico)
df["Disciplina"] = df["disciplina"].map(lambda d: DISCIPLINAS.get(d, d))
df["Data"] = df["respondido_em"].map(formatar_data)
df["Acertou"] = df["acertou"].map({True: "✅", False: "❌"})

df_show = df[["Data", "Disciplina", "resposta_usuario", "resposta_correta", "Acertou"]]
df_show.columns = ["Data", "Disciplina", "Sua resposta", "Correta", "Resultado"]

st.dataframe(df_show, use_container_width=True, hide_index=True)

st.subheader("Acertos por disciplina")
acertos_por_disc = df.groupby("Disciplina")["acertou"].mean().mul(100).round(1).sort_values()
st.bar_chart(acertos_por_disc)
