"""Gerador de Caderno de Questões em PDF."""

from datetime import datetime

import streamlit as st

from config import BLOCOS
from ai.generator import gerar_questoes
from utils.pdf_generator import gerar_caderno_pdf
from utils.helpers import inicializar_session_state

inicializar_session_state()

user = st.session_state.get("user")
if not user:
    st.switch_page("pages/0_🔐_Login.py")
    st.stop()

st.title("📄 Caderno de Questões em PDF")
st.caption("Gere um caderno completo com questões de todos os blocos, pronto para imprimir ou estudar offline.")

# ============================================================
# CONFIGURAÇÃO (SIDEBAR)
# ============================================================
with st.sidebar:
    st.subheader("⚙️ Configuração do Caderno")

    blocos_escolhidos = st.multiselect(
        "Blocos a incluir:",
        options=list(BLOCOS.keys()),
        default=list(BLOCOS.keys()),
        format_func=lambda x: BLOCOS[x],
        key="caderno_blocos",
    )

    por_bloco = st.number_input(
        "Questões por bloco",
        min_value=1, max_value=30, value=10, step=1,
        key="caderno_por_bloco",
    )

    dificuldade = st.selectbox(
        "Dificuldade",
        options=["facil", "medio", "dificil"],
        index=1,
        format_func=lambda x: {
            "facil": "Fácil", "medio": "Médio", "dificil": "Difícil"
        }[x],
        key="caderno_dificuldade",
    )

    st.divider()

    incluir_gabarito = st.checkbox(
        "Incluir gabarito no final",
        value=True,
        key="caderno_gabarito",
    )

    incluir_explicacao = st.checkbox(
        "Incluir explicações no gabarito",
        value=False,
        key="caderno_explicacao",
    )

    titulo_caderno = st.text_input(
        "Título do caderno",
        value="Caderno de Questões — Guarda Municipal BC",
        key="caderno_titulo",
    )

# ============================================================
# RESUMO ANTES DE GERAR
# ============================================================
if not blocos_escolhidos:
    st.warning("⚠️ Selecione ao menos um bloco na barra lateral.")
    st.stop()

total_questoes = len(blocos_escolhidos) * por_bloco

col1, col2, col3 = st.columns(3)
col1.metric("Blocos selecionados", len(blocos_escolhidos))
col2.metric("Questões por bloco", por_bloco)
col3.metric("Total de questões", total_questoes)

with st.expander("📋 Blocos selecionados", expanded=False):
    for b in blocos_escolhidos:
        st.write(f"- {BLOCOS[b]}")

st.info(
    f"⏱️ A geração pode levar de **1 a 3 minutos** "
    f"({len(blocos_escolhidos)} chamadas à IA). Não feche a página."
)

st.divider()

# ============================================================
# BOTÃO GERAR
# ============================================================
if st.button("🎯 Gerar Caderno PDF", use_container_width=True, type="primary"):
    if not blocos_escolhidos:
        st.error("Selecione ao menos um bloco.")
    else:
        prog = st.progress(0, text="Iniciando geração...")
        questoes_por_bloco = {}
        erros = []

        for i, bloco_key in enumerate(blocos_escolhidos):
            nome_bloco = BLOCOS[bloco_key]
            prog.progress(
                i / len(blocos_escolhidos),
                text=f"Gerando {por_bloco} questões de {nome_bloco}...",
            )
            try:
                qs = gerar_questoes(bloco_key, por_bloco, dificuldade)
                if qs:
                    questoes_por_bloco[nome_bloco] = qs
                else:
                    erros.append(f"{nome_bloco}: nenhuma questão retornada")
            except Exception as e:
                erros.append(f"{nome_bloco}: {e}")

        prog.progress(1.0, text="Montando o PDF...")

        if erros:
            for e in erros:
                st.error(f"⚠️ {e}")

        if not questoes_por_bloco:
            st.error("Nenhuma questão foi gerada. Tente novamente.")
            prog.empty()
        else:
            try:
                pdf_bytes = gerar_caderno_pdf(
                    questoes_por_bloco,
                    incluir_gabarito=incluir_gabarito,
                    incluir_explicacao=incluir_explicacao,
                    titulo=titulo_caderno,
                )
                st.session_state["pdf_caderno_bytes"] = pdf_bytes
                st.session_state["pdf_caderno_nome"] = (
                    f"caderno_gmbc_"
                    f"{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                )
                prog.empty()
                st.success(
                    f"✅ Caderno gerado com sucesso! "
                    f"({sum(len(q) for q in questoes_por_bloco.values())} questões)"
                )
            except Exception as e:
                st.error(f"Erro ao montar o PDF: {e}")
                prog.empty()

# ============================================================
# BOTÃO DE DOWNLOAD (persiste até navegar fora)
# ============================================================
if "pdf_caderno_bytes" in st.session_state:
    st.divider()
    st.subheader("📥 Download")

    tamanho_kb = len(st.session_state["pdf_caderno_bytes"]) / 1024
    st.caption(f"Tamanho do arquivo: **{tamanho_kb:.0f} KB**")

    st.download_button(
        label="⬇️ Baixar Caderno PDF",
        data=st.session_state["pdf_caderno_bytes"],
        file_name=st.session_state.get(
            "pdf_caderno_nome", "caderno_gmbc.pdf"
        ),
        mime="application/pdf",
        use_container_width=True,
        type="primary",
    )

    if st.button("🗑️ Limpar PDF gerado", use_container_width=False):
        st.session_state.pop("pdf_caderno_bytes", None)
        st.session_state.pop("pdf_caderno_nome", None)
        st.rerun()
