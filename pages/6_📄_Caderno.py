"""Gerador de Caderno de Questões em PDF — quantidade personalizada por bloco."""

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
    "O PDF sai com alternativas de A a E e gabarito no final. "
    "Questões repetidas são automaticamente bloqueadas."
)

# ============================================================
# SESSÃO: quantidades por bloco
# ============================================================
if "qtd_por_bloco" not in st.session_state:
    st.session_state.qtd_por_bloco = {k: 0 for k in BLOCOS.keys()}

if "incluir_bloco" not in st.session_state:
    st.session_state.incluir_bloco = {k: False for k in BLOCOS.keys()}


# ============================================================
# CONFIGURAÇÕES GERAIS (sidebar)
# ============================================================
with st.sidebar:
    st.subheader("⚙️ Configurações do Caderno")

    dificuldade = st.selectbox(
        "Dificuldade das questões",
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
        "Incluir explicações junto ao gabarito",
        value=False,
        key="caderno_explicacao",
    )

    st.divider()

    titulo_caderno = st.text_input(
        "Título do caderno",
        value="Caderno de Questões — Guarda Municipal BC",
        key="caderno_titulo",
    )

    st.divider()

    # Botões utilitários
    if st.button("🔢 Marcar 5 em todos", use_container_width=True):
        for k in BLOCOS.keys():
            st.session_state.incluir_bloco[k] = True
            st.session_state.qtd_por_bloco[k] = 5
        st.rerun()

    if st.button("🔢 Marcar 10 em todos", use_container_width=True):
        for k in BLOCOS.keys():
            st.session_state.incluir_bloco[k] = True
            st.session_state.qtd_por_bloco[k] = 10
        st.rerun()

    if st.button("🧹 Limpar seleção", use_container_width=True):
        for k in BLOCOS.keys():
            st.session_state.incluir_bloco[k] = False
            st.session_state.qtd_por_bloco[k] = 0
        st.rerun()


# ============================================================
# TABELA DE SELEÇÃO POR BLOCO
# ============================================================
st.subheader("🎯 Escolha a quantidade por bloco")
st.caption("Marque os blocos que deseja incluir e defina quantas questões de cada um.")

cab1, cab2, cab3 = st.columns([3, 1, 1])
with cab1:
    st.markdown("**Bloco**")
with cab2:
    st.markdown("**Incluir?**")
with cab3:
    st.markdown("**Nº questões**")

st.markdown("---")

for chave, nome in BLOCOS.items():
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.markdown(f"**{nome}**")

    with col2:
        incluir = st.checkbox(
            "Incluir",
            value=st.session_state.incluir_bloco[chave],
            key=f"chk_{chave}",
            label_visibility="collapsed",
        )
        st.session_state.incluir_bloco[chave] = incluir

    with col3:
        qtd = st.number_input(
            "Quantidade",
            min_value=0,
            max_value=30,
            value=st.session_state.qtd_por_bloco[chave],
            step=1,
            key=f"num_{chave}",
            label_visibility="collapsed",
            disabled=not incluir,
        )
        st.session_state.qtd_por_bloco[chave] = qtd

st.markdown("---")


# ============================================================
# RESUMO DO QUE SERÁ GERADO
# ============================================================
blocos_selecionados = {
    k: st.session_state.qtd_por_bloco[k]
    for k in BLOCOS.keys()
    if st.session_state.incluir_bloco[k] and st.session_state.qtd_por_bloco[k] > 0
}

total_questoes = sum(blocos_selecionados.values())

st.subheader("📋 Resumo do caderno")

if not blocos_selecionados:
    st.warning(
        "⚠️ Selecione ao menos um bloco com quantidade maior que zero "
        "para gerar o caderno."
    )
else:
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Blocos", len(blocos_selecionados))
    col_b.metric("Questões", total_questoes)
    col_c.metric("Estimativa", f"~{max(1, len(blocos_selecionados))} min")

    with st.expander("📖 Ver distribuição", expanded=True):
        for chave, qtd in blocos_selecionados.items():
            st.write(f"- **{BLOCOS[chave]}**: {qtd} questão(ões)")

st.divider()


# ============================================================
# BOTÃO GERAR PDF
# ============================================================
if st.button(
    "🎯 Gerar Caderno PDF",
    use_container_width=True,
    type="primary",
    disabled=not blocos_selecionados,
):
    prog = st.progress(0, text="Iniciando geração...")
    questoes_por_bloco = {}
    erros = []
    avisos = []

    total_blocos = len(blocos_selecionados)

    for i, (chave, qtd) in enumerate(blocos_selecionados.items()):
        nome_bloco = BLOCOS[chave]
        prog.progress(
            i / total_blocos,
            text=f"Gerando {qtd} questão(ões) de {nome_bloco}..."
        )
        try:
            qs = gerar_questoes(chave, qtd, dificuldade)

            if qs:
                questoes_por_bloco[nome_bloco] = qs

                # ⚠️ Aviso: gerou menos que o pedido (questões inéditas esgotadas)
                if len(qs) < qtd:
                    faltam = qtd - len(qs)
                    avisos.append(
                        f"**{nome_bloco}**: você pediu **{qtd}** questões, "
                        f"mas a IA só conseguiu gerar **{len(qs)}** inéditas. "
                        f"**{faltam}** não puderam ser criadas porque o banco "
                        f"de questões inéditas desse bloco está se esgotando."
                    )
            else:
                erros.append(
                    f"**{nome_bloco}**: nenhuma questão inédita foi gerada. "
                    f"Todas as questões possíveis desse bloco já estão no banco."
                )
        except Exception as e:
            erros.append(f"**{nome_bloco}**: {e}")

    prog.progress(1.0, text="Montando o PDF...")

    # -----------------------------------------------------------
    # AVISOS DE ESCASSEZ (amigável — não é erro)
    # -----------------------------------------------------------
    if avisos:
        st.warning("⚠️ Alguns blocos geraram menos questões que o solicitado:")
        for a in avisos:
            st.markdown(f"- {a}")
        st.info(
            "💡 **O que fazer?**\n\n"
            "- Reduza a quantidade pedida para o bloco afetado;\n"
            "- Tente novamente mais tarde (a IA pode encontrar novos ângulos);\n"
            "- Aumente a temperatura em `ai/generator.py` (de 0.95 para 1.0);\n"
            "- Limpe o banco de questões em **📊 Histórico → Apagar** e recomece."
        )

    # -----------------------------------------------------------
    # ERROS (nada foi gerado no bloco)
    # -----------------------------------------------------------
    if erros:
        st.error("❌ Não foi possível gerar questões em alguns blocos:")
        for e in erros:
            st.markdown(f"- {e}")

    # -----------------------------------------------------------
    # MONTA O PDF (se houver pelo menos 1 questão)
    # -----------------------------------------------------------
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
            if total_real < total_questoes:
                st.success(
                    f"✅ Caderno gerado com **{total_real}** de "
                    f"**{total_questoes}** questões solicitadas."
                )
            else:
                st.success(f"✅ Caderno gerado com **{total_real}** questões!")
        except Exception as e:
            st.error(f"Erro ao montar o PDF: {e}")
            prog.empty()


# ============================================================
# DOWNLOAD DO PDF
# ============================================================
if "pdf_caderno_bytes" in st.session_state:
    st.divider()
    st.subheader("📥 Download")

    tamanho_kb = len(st.session_state["pdf_caderno_bytes"]) / 1024
    st.caption(f"Tamanho do arquivo: **{tamanho_kb:.0f} KB**")

    col_dl1, col_dl2 = st.columns([3, 1])

    with col_dl1:
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

    with col_dl2:
        if st.button("🗑️ Limpar", use_container_width=True):
            st.session_state.pop("pdf_caderno_bytes", None)
            st.session_state.pop("pdf_caderno_nome", None)
            st.rerun()
