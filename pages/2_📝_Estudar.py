"""Sessão de estudo com geração de questões por IA."""

import streamlit as st
from config import DISCIPLINAS
from core.cycle_manager import obter_ciclo_atual
from core.database import salvar_resposta
from ai.generator import gerar_questoes
from ai.evaluator import avaliar_resposta
from utils.helpers import inicializar_session_state, parse_alternativas

inicializar_session_state()

user = st.session_state.get("user")
if not user:
    st.switch_page("pages/0_🔐_Login.py")
    st.stop()

st.title("📝 Sessão de Estudo")

ciclo = obter_ciclo_atual(user.id)

with st.sidebar:
    st.subheader("⚙️ Configuração")
    modo_livre = st.toggle("Modo livre (todas as disciplinas)", value=False)
    opcoes = list(DISCIPLINAS.keys()) if modo_livre else ciclo["disciplinas"]

    disciplina = st.selectbox("Disciplina", options=opcoes, format_func=lambda x: DISCIPLINAS[x])
    dificuldade = st.select_slider(
        "Dificuldade",
        options=["facil", "medio", "dificil"],
        value="medio",
        format_func=lambda x: {"facil": "Fácil", "medio": "Médio", "dificil": "Difícil"}[x],
    )
    quantidade = st.slider("Quantidade", 1, 10, 5)

if st.button("🔄 Gerar novas questões", use_container_width=True):
    with st.spinner("Consultando a IA e gerando questões inéditas..."):
        try:
            questoes = gerar_questoes(disciplina, quantidade, dificuldade)
            st.session_state.questoes_sessao = questoes
            st.session_state.indice_atual = 0
            st.session_state.respostas_sessao = []
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao gerar questões: {e}")

questoes = st.session_state.get("questoes_sessao", [])
idx = st.session_state.get("indice_atual", 0)

if not questoes:
    st.info("Clique em **Gerar novas questões** para começar.")
    st.stop()

if idx >= len(questoes):
    st.success("🎉 Sessão concluída!")
    respostas = st.session_state.get("respostas_sessao", [])
    acertos = sum(1 for r in respostas if r["acertou"])
    st.metric("Acertos", f"{acertos}/{len(respostas)}")
    if st.button("🔁 Nova sessão"):
        st.session_state.questoes_sessao = []
        st.session_state.indice_atual = 0
        st.session_state.respostas_sessao = []
        st.rerun()
    st.stop()

q = questoes[idx]
alternativas = parse_alternativas(q["alternativas"])

st.markdown(f"### Questão {idx + 1} de {len(questoes)}")
st.caption(f"Disciplina: **{DISCIPLINAS.get(q['disciplina'], q['disciplina'])}** | Dificuldade: {q.get('dificuldade', 'medio')}")
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
    confirmar = st.button("✅ Confirmar resposta", use_container_width=True)
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
