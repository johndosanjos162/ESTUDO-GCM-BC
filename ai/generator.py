"""Geração de questões via IA — com blocos de estudo."""

from __future__ import annotations
import hashlib
import json

from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
from ai.prompts import SYSTEM_PROMPT, BLOCOS
from core.database import salvar_questao, questao_ja_existe

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY não configurada.")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _hash(texto: str) -> str:
    return hashlib.sha256(texto.strip().encode("utf-8")).hexdigest()


def listar_blocos() -> dict:
    """Retorna todos os blocos disponíveis."""
    return BLOCOS


def gerar_questoes(
    bloco: str,
    quantidade: int = 5,
    dificuldade: str = "medio",
    salvar: bool = True,
) -> list[dict]:
    """
    Gera questões para um bloco específico com foco EXCLUSIVO na GMBC.
    """
    info = BLOCOS.get(bloco)
    if not info:
        raise ValueError(f"Bloco inválido: {bloco}")

    user_prompt = info["prompt"].format(
        n=quantidade, dificuldade=dificuldade
    )

    # ⚠️ REFORÇO OBRIGATÓRIO DO FOCO
    user_prompt += """

============================================================
REFORÇO OBRIGATÓRIO DE FOCO:
Todas as questões geradas devem ser EXCLUSIVAMENTE sobre o concurso
da Guarda Municipal de Balneário Camboriú (SC).
- NÃO gere questões genéricas de concursos de outras áreas.
- NÃO gere questões sobre temas que não constam no edital da GMBC.
- Contextualize SEMPRE com situações, leis e dados do município.
- Se a questão for de Português/Matemática, use exemplos da corporação.
============================================================
"""

    try:
        response = _get_client().chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.85,
        )
    except Exception as e:
        msg = str(e)
        if "429" in msg or "insufficient_quota" in msg:
            raise RuntimeError(
                "Sem créditos na API. Adicione fundos ou troque o modelo."
            ) from e
        if "404" in msg or "model_not_found" in msg:
            raise RuntimeError(
                f"Modelo '{OPENAI_MODEL}' não encontrado. "
                "Verifique os Secrets."
            ) from e
        raise

    raw = response.choices[0].message.content or "{}"
    dados = json.loads(raw)
    questoes_raw = dados.get("questoes", [])

    resultado = []
    for q in questoes_raw:
        if not all(k in q for k in ("enunciado", "alternativas", "resposta_correta")):
            continue

        payload = {
            "disciplina": bloco,
            "enunciado": q["enunciado"],
            "alternativas": json.dumps(q["alternativas"], ensure_ascii=False),
            "resposta_correta": q["resposta_correta"].upper()[0],
            "explicacao": q.get("explicacao", ""),
            "dificuldade": dificuldade,
            "fonte": "IA",
            "hash_conteudo": _hash(q["enunciado"]),
        }

        if salvar and not questao_ja_existe(payload["hash_conteudo"]):
            salvo = salvar_questao(payload)
            if salvo:
                resultado.append(salvo)
        else:
            payload["id"] = f"temp-{payload['hash_conteudo'][:8]}"
            resultado.append(payload)

    return resultado

def gerar_lote(blocos: list, n_por_bloco: int = 5) -> list:
    """Gera questões para múltiplos blocos."""
    todas = []
    for b in blocos:
        try:
            todas.extend(gerar_questoes(b, n_por_bloco))
        except Exception as e:
            print(f"[erro] Falha ao gerar questões de {b}: {e}")
    return todas
