"""Caderno de Questões em PDF — geração via IA."""

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
st.caption("Escolha quantas questões quer de cada bloco. IA gera questões inéditas com foco na GMBC.")

if "qtd_por_bloco" not in st.session_state:
    st.session_state.qtd_por_bloco = {k: 0 for k in BLOCOS.keys()}
if "incluir_bloco" not in st.session_state:
    st.session_state.incluir_bloco = {k: False for k in BLOCOS.keys()}

with st.sidebar:
    st.subheader("⚙️ Configurações")

    dificuldade = st.selectbox(
        "Dificuldade",
        options=["facil", "medio", "dificil"],
        index=1,
        format_func=lambda x: {"facil": "Fácil", "medio": "Médio", "dificil": "Difícil"}[x],
    )

    st.divider()
    incluir_gabarito = st.checkbox("Incluir gabarito no final", value=True)
    incluir_explicacao = st.checkbox("Incluir explicações no gabarito", value=False)
    st.divider()

    titulo_caderno = st.text_input(
        "Título do caderno",
        value="Caderno de Questões — Guarda Municipal BC",
    )

    st.divider()

    if st.button("🔢 Marcar 5 em todos", use_container_width=True):
        for k in BLOCOS:
            st.session_state.incluir_bloco[k] = True
            st.session_state.qtd_por_bloco[k] = 5
        st.rerun()

    if st.button("🔢 Marcar 10 em todos", use_container_width=True):
        for k in BLOCOS:
            st.session_state.incluir_bloco[k] = True
            st.session_state.qtd_por_bloco[k] = 10
        st.rerun()

    if st.button("🧹 Limpar seleção", use_container_width=True):
        for k in BLOCOS:
            st.session_state.incluir_bloco[k] = False
            st.session_state.qtd_por_bloco[k] = 0
        st.rerun()

st.subheader("🎯 Escolha a quantidade por bloco")

h1, h2, h3 = st.columns([3, 1, 1])
with h1:
    st.markdown("**Bloco**")
with h2:
    st.markdown("**Incluir?**")
with h3:
    st.markdown("**Nº questões**")

st.markdown("---")

for chave, nome in BLOCOS.items():
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        st.markdown(f"**{nome}**")
    with c2:
        inc = st.checkbox(
            "Incluir",
            value=st.session_state.incluir_bloco[chave],
            key=f"chk_{chave}",
            label_visibility="collapsed",
        )
        st.session_state.incluir_bloco[chave] = inc
    with c3:
        q = st.number_input(
            "Qtd",
            min_value=0, max_value=50,
            value=st.session_state.qtd_por_bloco[chave],
            step=1,
            key=f"num_{chave}",
            label_visibility="collapsed",
            disabled=not inc,
        )
        st.session_state.qtd_por_bloco[chave] = q

st.markdown("---")

selecionados = {
    k: st.session_state.qtd_por_bloco[k]
    for k in BLOCOS
    if st.session_state.incluir_bloco[k] and st.session_state.qtd_por_bloco[k] > 0
}
total = sum(selecionados.values())

st.subheader("📋 Resumo")

if not selecionados:
    st.warning("⚠️ Selecione ao menos um bloco com quantidade maior que zero.")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Blocos", len(selecionados))
    c2.metric("Questões", total)
    c3.metric("Estimativa", f"~{max(1, len(selecionados))} min")
    with st.expander("📖 Distribuição", expanded=True):
        for k, q in selecionados.items():
            st.write(f"- **{BLOCOS[k]}**: {q} questão(ões)")

st.divider()

if st.button("🎯 Gerar Caderno PDF", use_container_width=True, type="primary", disabled=not selecionados):
    prog = st.progress(0, text="Iniciando geração...")
    questoes_por_bloco = {}
    erros = []
    avisos = []

    total_blocos = len(selecionados)

    for i, (chave, qtd) in enumerate(selecionados.items()):
        nome_bloco = BLOCOS[chave]
        prog.progress(i / total_blocos, text=f"Gerando {qtd} questões de {nome_bloco}...")
        try:
            qs = gerar_questoes(chave, qtd, dificuldade)
            if qs:
                questoes_por_bloco[nome_bloco] = qs
                if len(qs) < qtd:
                    faltam = qtd - len(qs)
                    avisos.append(
                        f"**{nome_bloco}**: você pediu **{qtd}** questões, mas a IA gerou **{len(qs)}** inéditas. "
                        f"**{faltam}** não puderam ser criadas porque o banco de questões inéditas está se esgotando."
                    )
            else:
                erros.append(
                    f"**{nome_bloco}**: nenhuma questão inédita foi gerada."
                )
        except Exception as e:
            erros.append(f"**{nome_bloco}**: {e}")

    prog.progress(1.0, text="Montando o PDF...")

    if avisos:
        st.warning("⚠️ Alguns blocos geraram menos questões que o solicitado:")
        for a in avisos:
            st.markdown(f"- {a}")
        st.info(
            "💡 **O que fazer?**\n\n"
            "- Reduza a quantidade pedida para o bloco afetado;\n"
            "- Tente novamente mais tarde (a IA pode encontrar novos ângulos);\n"
            "- Limpe o banco em **📊 Histórico → Apagar** e recomece."
        )

    if erros:
        st.error("❌ Não foi possível gerar questões em alguns blocos:")
        for e in erros:
            st.markdown(f"- {e}")

    if not questoes_por_bloco:
        st.error("Nenhuma questão foi gerada. Ajuste os blocos e tente novamente.")
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
                f"caderno_gmbc_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            )
            prog.empty()

            total_real = sum(len(q) for q in questoes_por_bloco.values())
            if total_real < total:
                st.success(f"✅ Caderno gerado com **{total_real}** de **{total}** questões solicitadas.")
            else:
                st.success(f"✅ Caderno gerado com **{total_real}** questões!")
        except Exception as e:
            st.error(f"Erro ao montar PDF: {e}")
            prog.empty()

if "pdf_caderno_bytes" in st.session_state:
    st.divider()
    st.subheader("📥 Download")
    kb = len(st.session_state["pdf_caderno_bytes"]) / 1024
    st.caption(f"Tamanho: **{kb:.0f} KB**")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.download_button(
            label="⬇️ Baixar Caderno PDF",
            data=st.session_state["pdf_caderno_bytes"],
            file_name=st.session_state.get("pdf_caderno_nome", "caderno.pdf"),
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )
    with col2:
        if st.button("🗑️ Limpar", use_container_width=True):
            st.session_state.pop("pdf_caderno_bytes", None)
            st.session_state.pop("pdf_caderno_nome", None)
            st.rerun()
