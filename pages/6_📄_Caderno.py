"""Caderno de Questões em PDF — com tema específico por bloco."""

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
st.caption(
    "Escolha quantas questões quer de cada bloco. "
    "Opcionalmente, defina um TEMA ESPECÍFICO por bloco."
)

# ============================================================
# SESSÃO
# ============================================================
if "qtd_por_bloco" not in st.session_state:
    st.session_state.qtd_por_bloco = {k: 0 for k in BLOCOS.keys()}
if "incluir_bloco" not in st.session_state:
    st.session_state.incluir_bloco = {k: False for k in BLOCOS.keys()}
if "tema_por_bloco" not in st.session_state:
    st.session_state.tema_por_bloco = {k: "" for k in BLOCOS.keys()}

# ============================================================
# SIDEBAR
# ============================================================
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
            st.session_state.tema_por_bloco[k] = ""
        st.rerun()

# ============================================================
# SELEÇÃO POR BLOCO
# ============================================================
st.subheader("🎯 Escolha a quantidade por bloco")
st.caption("Marque os blocos, defina quantas questões e (opcional) um tema específico.")

st.markdown("---")

for chave, nome in BLOCOS.items():
    # Linha principal
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

    # Campo de tema (só aparece se o bloco foi marcado)
    if inc:
        tema_atual = st.text_input(
            f"🎯 Tema específico (opcional) para {nome}",
            value=st.session_state.tema_por_bloco[chave],
            key=f"tema_{chave}",
            placeholder="Ex: Regra de Três, Crase, Prisão em flagrante...",
        )
        st.session_state.tema_por_bloco[chave] = tema_atual

        if tema_atual.strip():
            st.caption(f"✅ As questões de **{nome}** serão SOMENTE sobre **{tema_atual}**")

st.markdown("---")

# ============================================================
# RESUMO
# ============================================================
selecionados = {
    k: st.session_state.qtd_por_bloco[k]
    for k in BLOCOS
    if st.session_state.incluir_bloco[k] and st.session_state.qtd_por_bloco[k] > 0
}
total = sum(selecionados.values())

st.subheader("📋 Resumo do caderno")

if not selecionados:
    st.warning("⚠️ Selecione ao menos um bloco com quantidade maior que zero.")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Blocos", len(selecionados))
    c2.metric("Questões", total)
    c3.metric("Estimativa", f"~{max(1, len(selecionados))} min")

    with st.expander("📖 Ver distribuição", expanded=True):
        for k, q in selecionados.items():
            tema = st.session_state.tema_por_bloco.get(k, "").strip()
            if tema:
                st.write(f"- **{BLOCOS[k]}**: {q} questão(ões) — 🎯 Tema: **{tema}**")
            else:
                st.write(f"- **{BLOCOS[k]}**: {q} questão(ões)")

st.divider()

# ============================================================
# BOTÃO GERAR PDF
# ============================================================
if st.button(
    "🎯 Gerar Caderno PDF",
    use_container_width=True,
    type="primary",
    disabled=not selecionados,
):
    prog = st.progress(0, text="Iniciando geração...")
    questoes_por_bloco = {}
    erros = []
    avisos = []

    total_blocos = len(selecionados)

    for i, (chave, qtd) in enumerate(selecionados.items()):
        nome_bloco = BLOCOS[chave]
        tema = st.session_state.tema_por_bloco.get(chave, "").strip()

        texto = f"Gerando {qtd} questões de {nome_bloco}"
        if tema:
            texto += f" sobre '{tema}'"
        prog.progress(i / total_blocos, text=texto + "...")

        try:
            qs = gerar_questoes(chave, qtd, dificuldade, tema=tema)

            # Nome do bloco no PDF inclui o tema quando existir
            nome_final = f"{nome_bloco} — {tema}" if tema else nome_bloco

            if qs:
                questoes_por_bloco[nome_final] = qs
                if len(qs) < qtd:
                    faltam = qtd - len(qs)
                    avisos.append(
                        f"**{nome_bloco}**"
                        + (f" ({tema})" if tema else "")
                        + f": pedidas {qtd}, geradas {len(qs)} "
                        f"({faltam} não vieram — tente novamente)"
                    )
            else:
                erros.append(
                    f"**{nome_bloco}**"
                    + (f" ({tema})" if tema else "")
                    + ": a IA não conseguiu gerar questões."
                )
        except Exception as e:
            erros.append(f"**{nome_bloco}**: {e}")

    prog.progress(1.0, text="Montando o PDF...")

    if avisos:
        st.warning("⚠️ Alguns blocos geraram menos questões que o solicitado:")
        for a in avisos:
            st.markdown(f"- {a}")

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
                st.success(
                    f"✅ Caderno gerado com **{total_real}** de "
                    f"**{total}** questões solicitadas."
                )
            else:
                st.success(f"✅ Caderno gerado com **{total_real}** questões!")
        except Exception as e:
            st.error(f"Erro ao montar PDF: {e}")
            prog.empty()

# ============================================================
# DOWNLOAD
# ============================================================
if "pdf_caderno_bytes" in st.session_state:
    st.divider()
    st.subheader("📥 Download")

    kb = len(st.session_state["pdf_caderno_bytes"]) / 1024
    st.caption(f"Tamanho do arquivo: **{kb:.0f} KB**")

    col_dl1, col_dl2 = st.columns([3, 1])

    with col_dl1:
        st.download_button(
            label="⬇️ Baixar Caderno PDF",
            data=st.session_state["pdf_caderno_bytes"],
            file_name=st.session_state.get("pdf_caderno_nome", "caderno_gmbc.pdf"),
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )

    with col_dl2:
        if st.button("🗑️ Limpar", use_container_width=True):
            st.session_state.pop("pdf_caderno_bytes", None)
            st.session_state.pop("pdf_caderno_nome", None)
            st.rerun()
