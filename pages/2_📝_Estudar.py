"""Sessão de estudo — visual tecnológico."""

import streamlit as st
from config import BLOCOS
from core.cycle_manager import obter_ciclo_atual
from core.database import salvar_resposta
from ai.generator import gerar_questoes, listar_blocos
from ai.evaluator import avaliar_resposta
from utils.helpers import inicializar_session_state, parse_alternativas

inicializar_session_state()

user = st.session_state.get("user")
if not user:
    st.switch_page("pages/0_🔐_Login.py")
    st.stop()

# ============================================================
# CABEÇALHO VISUAL
# ============================================================
st.markdown("""
<div style="margin-bottom: 25px;">
    <div class="tech-badge">MODO ESTUDO</div>
    <h1 style="margin: 8px 0 0 0; border: none; padding: 0;">📝 Sessão de Estudo</h1>
    <p style="color: #8fb8cc; font-size: 13px; letter-spacing: 1px;">
        Questões geradas por IA • Foco na Guarda Municipal BC
    </p>
</div>
""", unsafe_allow_html=True)

ciclo = obter_ciclo_atual(user.id)
blocos_disponiveis = listar_blocos()

# ============================================================
# SIDEBAR — CONFIGURAÇÃO (FUNÇÕES ORIGINAIS INTACTAS)
# ============================================================
with st.sidebar:
    st.subheader("📚 Blocos de Estudo")

    modo_livre = st.toggle("Ver todos os blocos", value=False)
    opcoes = list(blocos_disponiveis.keys()) if modo_livre else ciclo["disciplinas"]

    bloco_escolhido = st.selectbox(
        "Selecione o bloco:",
        options=opcoes,
        format_func=lambda x: blocos_disponiveis[x]["nome"],
        key="bloco_selector",
    )

    st.caption(blocos_disponiveis[bloco_escolhido]["descricao"])

    st.divider()

    dificuldade = st.select_slider(
        "Dificuldade",
        options=["facil", "medio", "dificil"],
        value="medio",
        format_func=lambda x: {"facil": "Fácil", "medio": "Médio", "dificil": "Difícil"}[x],
    )

    quantidade = st.slider("Quantidade de questões", 1, 15, 5)

# ============================================================
# BOTÃO GERAR (FUNÇÃO ORIGINAL INTACTA)
# ============================================================
if st.button("🔄 Gerar novas questões", use_container_width=True, type="primary"):
    with st.spinner(f"Gerando {quantidade} questões com IA..."):
        try:
            questoes = gerar_questoes(bloco_escolhido, quantidade, dificuldade)
            st.session_state.questoes_sessao = questoes
            st.session_state.indice_atual = 0
            st.session_state.respostas_sessao = []
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao gerar questões: {e}")

questoes = st.session_state.get("questoes_sessao", [])
idx = st.session_state.get("indice_atual", 0)

# ============================================================
# TELA INICIAL
# ============================================================
if not questoes:
    st.info("👈 Selecione um bloco e clique em **Gerar novas questões**.")
    st.stop()

# ============================================================
# SESSÃO CONCLUÍDA (LÓGICA ORIGINAL INTACTA)
# ============================================================
if idx >= len(questoes):
    st.success("🎉 Sessão concluída!")
    respostas = st.session_state.get("respostas_sessao", [])
    acertos = sum(1 for r in respostas if r["acertou"])
    total = len(respostas)
    pct = round((acertos / total) * 100, 1) if total else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Acertos", f"{acertos}/{total}")
    col2.metric("Aproveitamento", f"{pct}%")
    col3.metric("Bloco", blocos_disponiveis[bloco_escolhido]["nome"].split(" ", 1)[1])

    if st.button("🔁 Nova sessão"):
        st.session_state.questoes_sessao = []
        st.session_state.indice_atual = 0
        st.session_state.respostas_sessao = []
        st.rerun()
    st.stop()

# ============================================================
# QUESTÃO ATUAL (LÓGICA ORIGINAL INTACTA)
# ============================================================
q = questoes[idx]
alternativas = parse_alternativas(q["alternativas"])

nome_bloco = blocos_disponiveis.get(q["disciplina"], {}).get("nome", q["disciplina"])
st.markdown(f"### Questão {idx + 1} de {len(questoes)}")
st.caption(f"**{nome_bloco}** | Dificuldade: {q.get('dificuldade', 'medio')}")
st.write(q["enunciado"])

letras = [chr(65 + i) for i in range(len(alternativas))]
chave = f"resposta_{q.get('id', idx)}_{idx}"

resposta = st.radio(
    "Escolha a alternativa:",
    options=letras,
    format_func=lambda l: f"{l}) {alternativas[ord(l) - 65]}",
    key=chave,
)

col1, col2 = st.columns([1, 1])
with col1:
    confirmar = st.button("✅ Confirmar resposta", use_container_width=True, type="primary")
with col2:
    pular = st.button("⏭️ Pular questão", use_container_width=True)

if pular:
    st.session_state.indice_atual += 1
    st.rerun()

if confirmar:
    resultado = avaliar_resposta(q, resposta)
    try:
        salvar_resposta({
            "usuario_id": user.id,
            "questao_id": q.get("id") if q.get("id", "").count("-") == 4 else None,
            "disciplina": q["disciplina"],
            "resposta_usuario": resultado["resposta_usuario"],
            "resposta_correta": resultado["resposta_correta"],
        })
    except Exception as e:
        st.warning(f"Resposta não salva no banco: {e}")

    st.session_state.respostas_sessao.append(resultado)

    if resultado["acertou"]:
        st.success(resultado["feedback"])
    else:
        st.error(resultado["feedback"])

    if resultado["explicacao"]:
        st.info(f"💡 **Explicação:** {resultado['explicacao']}")

    if st.button("➡️ Próxima questão", key=f"prox_{idx}", use_container_width=True):
        st.session_state.indice_atual += 1
        st.rerun()

st.divider()
st.progress(idx / len(questoes), text=f"Progresso: {idx}/{len(questoes)}")
