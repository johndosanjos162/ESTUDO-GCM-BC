"""Histórico e estatísticas — com opções de exclusão."""

import streamlit as st
import pandas as pd
from config import BLOCOS
from core.database import (
    buscar_historico_usuario,
    estatisticas_por_disciplina,
    apagar_respostas_por_ids,
    apagar_todo_historico,
    apagar_historico_por_disciplina,
)
from utils.helpers import inicializar_session_state, formatar_data

inicializar_session_state()

user = st.session_state.get("user")
if not user:
    st.switch_page("pages/0_🔐_Login.py")
    st.stop()

st.title("📊 Histórico e Desempenho")

# ============================================================
# MENSAGENS DE SUCESSO (persistem entre reruns)
# ============================================================
if "msg_exclusao" in st.session_state:
    st.success(st.session_state.pop("msg_exclusao"))

# ============================================================
# PAINEL DE EXCLUSÃO (expander no topo)
# ============================================================
with st.expander("🗑️ Gerenciar Histórico — Apagar Respostas", expanded=False):

    st.warning(
        "⚠️ **Atenção**: as exclusões são **permanentes** e não podem ser desfeitas."
    )

    aba_especificas, aba_bloco, aba_tudo = st.tabs([
        "🗂️ Apagar específicas",
        "📚 Apagar por bloco",
        "💣 Apagar TUDO",
    ])

    # ---------- ABA 1: Apagar respostas específicas ----------
    with aba_especificas:
        st.markdown("Selecione as respostas que deseja apagar:")

        historico_completo = buscar_historico_usuario(user.id, limite=500)

        if not historico_completo:
            st.info("Nenhuma resposta no histórico para apagar.")
        else:
            # Monta opções legíveis
            opcoes = {}
            for r in historico_completo:
                bloco_nome = BLOCOS.get(r["disciplina"], r["disciplina"])
                data = formatar_data(r.get("respondido_em", ""))
                icone = "✅" if r.get("acertou") else "❌"
                label = f"{icone} {data} | {bloco_nome} | sua: {r['resposta_usuario']} → correta: {r['resposta_correta']}"
                opcoes[r["id"]] = label

            selecionadas = st.multiselect(
                "Marque as respostas a apagar:",
                options=list(opcoes.keys()),
                format_func=lambda x: opcoes[x],
                key="ms_especificas",
            )

            if selecionadas:
                st.caption(f"**{len(selecionadas)}** resposta(s) selecionada(s).")
                if st.button(
                    f"🗑️ Apagar {len(selecionadas)} resposta(s)",
                    key="btn_apagar_especificas",
                    type="primary",
                    use_container_width=True,
                ):
                    qtd = apagar_respostas_por_ids(selecionadas)
                    st.session_state["msg_exclusao"] = (
                        f"✅ {qtd} resposta(s) apagada(s) com sucesso."
                    )
                    st.rerun()
            else:
                st.caption("Nenhuma resposta selecionada.")

    # ---------- ABA 2: Apagar por bloco ----------
    with aba_bloco:
        st.markdown("Apaga **todo** o histórico de um bloco específico:")

        bloco_escolhido = st.selectbox(
            "Escolha o bloco:",
            options=list(BLOCOS.keys()),
            format_func=lambda x: BLOCOS[x],
            key="sb_bloco_apagar",
        )

        # Conta quantas respostas há nesse bloco
        if historico_completo if 'historico_completo' in dir() else True:
            pass

        historico_bloco = buscar_historico_usuario(
            user.id, disciplina=bloco_escolhido, limite=1000
        )
        total_bloco = len(historico_bloco)

        st.info(
            f"O bloco **{BLOCOS[bloco_escolhido]}** tem "
            f"**{total_bloco}** resposta(s) registrada(s)."
        )

        if total_bloco == 0:
            st.caption("Nada para apagar neste bloco.")
        else:
            confirmar_bloco = st.checkbox(
                f"Confirmo apagar TODAS as {total_bloco} respostas de "
                f"**{BLOCOS[bloco_escolhido]}**",
                key="chk_confirma_bloco",
            )

            if st.button(
                f"🗑️ Apagar histórico de {BLOCOS[bloco_escolhido]}",
                key="btn_apagar_bloco",
                disabled=not confirmar_bloco,
                type="primary",
                use_container_width=True,
            ):
                qtd = apagar_historico_por_disciplina(user.id, bloco_escolhido)
                st.session_state["msg_exclusao"] = (
                    f"✅ Histórico de **{BLOCOS[bloco_escolhido]}** apagado "
                    f"({qtd} resposta(s))."
                )
                st.rerun()

    # ---------- ABA 3: Apagar TUDO ----------
    with aba_tudo:
        st.error(
            "💣 **ZONA DE PERIGO** — Esta ação apaga **TODO** o seu histórico "
            "de respostas. Não pode ser desfeita."
        )

        total_geral = len(buscar_historico_usuario(user.id, limite=5000))

        st.write(f"Total de respostas no histórico: **{total_geral}**")

        if total_geral == 0:
            st.caption("Histórico já está vazio.")
        else:
            confirmar_texto = st.text_input(
                'Digite **APAGAR TUDO** (em maiúsculas) para confirmar:',
                key="txt_confirma_tudo",
            )

            if st.button(
                "💣 Apagar TODO o histórico",
                key="btn_apagar_tudo",
                disabled=(confirmar_texto.strip() != "APAGAR TUDO"),
                type="primary",
                use_container_width=True,
            ):
                qtd = apagar_todo_historico(user.id)
                st.session_state["msg_exclusao"] = (
                    f"✅ TODO o histórico foi apagado ({qtd} resposta(s))."
                )
                st.rerun()

st.divider()

# ============================================================
# ESTATÍSTICAS (parte normal da página)
# ============================================================
stats = estatisticas_por_disciplina(user.id)

if stats:
    st.subheader("Resumo por bloco")
    cols = st.columns(min(len(stats), 4))
    for i, s in enumerate(stats):
        nome = BLOCOS.get(s["disciplina"], s["disciplina"])
        total = int(s.get("total", 0))
        acertos = int(s.get("acertos", 0))
        pct = round((acertos / total) * 100, 1) if total else 0
        with cols[i % len(cols)]:
            st.metric(nome, f"{pct}%", f"{acertos}/{total}")

st.divider()

# ============================================================
# FILTRO E TABELA
# ============================================================
filtro = st.selectbox(
    "Filtrar por bloco",
    options=["Todos"] + list(BLOCOS.keys()),
    format_func=lambda x: "Todos" if x == "Todos" else BLOCOS[x],
    key="sb_filtro_historico",
)

historico = buscar_historico_usuario(
    user.id,
    disciplina=None if filtro == "Todos" else filtro,
    limite=200,
)

if not historico:
    st.info("Sem histórico ainda.")
    st.stop()

df = pd.DataFrame(historico)
df["Bloco"] = df["disciplina"].map(lambda d: BLOCOS.get(d, d))
df["Data"] = df["respondido_em"].map(formatar_data)
df["Acertou"] = df["acertou"].map({True: "✅", False: "❌"})

df_show = df[["Data", "Bloco", "resposta_usuario", "resposta_correta", "Acertou"]]
df_show.columns = ["Data", "Bloco", "Sua resposta", "Correta", "Resultado"]

st.dataframe(df_show, use_container_width=True, hide_index=True)

st.subheader("Acertos por bloco")
acertos_por_bloco = (
    df.groupby("Bloco")["acertou"].mean().mul(100).round(1).sort_values()
)
st.bar_chart(acertos_por_bloco)
