"""Sessão de estudo — visual tecnológico + barra de tema."""

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
# CABEÇALHO
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
# SIDEBAR — CONFIGURAÇÃO
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
# BARRA DE TEMA ESPECÍFICO (NOVO)
# ============================================================
st.markdown(f"""
<div class="tech-card" style="margin-bottom: 20px;">
    <div class="tech-badge">🔍 TEMA ESPECÍFICO (OPCIONAL)</div>
    <div style="font-family: 'Segoe UI', sans-serif; color: #8fb8cc; font-size: 13px; margin-top: 8px;">
        Digite um tema para gerar questões SOMENTE sobre ele.
        <br>Exemplos: <b style="color: #00e5ff;">"Regra de Três"</b>, 
        <b style="color: #00e5ff;">"Crase"</b>, 
        <b style="color: #00e5ff;">"Prisão em flagrante"</b>, 
        <b style="color: #00e5ff;">"História de Balneário Camboriú"</b>
    </div>
</div>
""", unsafe_allow_html=True)

col_tema1, col_tema2 = st.columns([4, 1])

with col_tema1:
    tema_especifico = st.text_input(
        "Tema específico",
        key="tema_input",
        placeholder=f"Ex: Regra de Três, Concordância Verbal, Lei Maria da Penha...",
        label_visibility="collapsed",
    )

with col_tema2:
    limpar_tema = st.button("🧹 Limpar", use_container_width=True)

if limpar_tema:
    st.session_state.tema_input = ""
    st.rerun()

# Mostra o tema ativo
if tema_especifico and tema_especifico.strip():
    st.markdown(f"""
    <div style="background: rgba(0, 229, 255, 0.1); border-left: 3px solid #00e5ff; border-radius: 6px; padding: 10px 15px; margin-bottom: 15px;">
        <span style="font-family: 'Courier New', monospace; color: #00e5ff; font-size: 12px; letter-spacing: 1px;">
            🎯 TEMA ATIVO: 
        </span>
        <span style="color: #ffffff; font-weight: 600;">
            {tema_especifico}
        </span>
        <span style="color: #8fb8cc; font-size: 12px;">
            &nbsp;— questões de <b>{blocos_disponiveis[bloco_escolhido]['nome']}</b> filtradas neste tema
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

# ============================================================
# BOTÃO GERAR
# ============================================================
texto_botao = f"⚡ GERAR {quantidade} QUESTÕES"
if tema_especifico and tema_especifico.strip():
    texto_botao += f" SOBRE '{tema_especifico[:30]}'"

if st.button(texto_botao, use_container_width=True, type="primary"):
    with st.spinner(f"Gerando questões..."):
        try:
            questoes = gerar_questoes(
                bloco_escolhido,
                quantidade,
                dificuldade,
                tema=tema_especifico if tema_especifico else "",
            )
            st.session_state.questoes_sessao = questoes
            st.session_state.indice_atual = 0
            st.session_state.respostas_sessao = []
            st.session_state.tema_sessao = tema_especifico
            st.rerun()
        except Exception as e:
            st.error(f"❌ Erro ao gerar questões: {e}")

questoes = st.session_state.get("questoes_sessao", [])
idx = st.session_state.get("indice_atual", 0)
tema_sessao = st.session_state.get("tema_sessao", "")

# ============================================================
# TELA INICIAL
# ============================================================
if not questoes:
    st.info("👈 Selecione um bloco, opcionalmente digite um tema, e clique em **Gerar questões**.")
    st.stop()

# ============================================================
# SESSÃO CONCLUÍDA
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

    if tema_sessao:
        st.caption(f"🎯 Tema desta sessão: **{tema_sessao}**")

    if st.button("🔁 Nova sessão"):
        st.session_state.questoes_sessao = []
        st.session_state.indice_atual = 0
        st.session_state.respostas_sessao = []
        st.session_state.tema_sessao = ""
        st.rerun()
    st.stop()

# ============================================================
# QUESTÃO ATUAL
# ============================================================
q = questoes[idx]
alternativas = parse_alternativas(q["alternativas"])

nome_bloco = blocos_disponiveis.get(q["disciplina"], {}).get("nome", q["disciplina"])
st.markdown(f"### Questão {idx + 1} de {len(questoes)}")

# Mostra tema se houver
if tema_sessao:
    st.caption(f"**{nome_bloco}** | 🎯 Tema: **{tema_sessao}** | Dificuldade: {q.get('dificuldade', 'medio')}")
else:
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
