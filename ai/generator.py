"""Geração de questões inéditas via OpenAI."""

from __future__ import annotations
import hashlib
import json

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from ai.prompts import SYSTEM_PROMPT, PROMPTS_DISCIPLINAS
from core.database import salvar_questao, questao_ja_existe

_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY não configurada.")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _hash(texto: str) -> str:
    return hashlib.sha256(texto.strip().encode("utf-8")).hexdigest()


def gerar_questoes(disciplina: str, quantidade: int = 5, dificuldade: str = "medio", salvar: bool = True) -> list:
    template = PROMPTS_DISCIPLINAS.get(disciplina)
    if not template:
        raise ValueError(f"Disciplina inválida: {disciplina}")

    user_prompt = template.format(n=quantidade, dificuldade=dificuldade)

    response = _get_client().chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.85,
    )

    raw = response.choices[0].message.content or "{}"
    dados = json.loads(raw)
    questoes_raw = dados.get("questoes", [])

    resultado = []
    for q in questoes_raw:
        if not all(k in q for k in ("enunciado", "alternativas", "resposta_correta")):
            continue

        payload = {
            "disciplina": disciplina,
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


def gerar_lote(disciplinas: list, n_por_disciplina: int = 5) -> list:
    todas = []
    for d in disciplinas:
        try:
            todas.extend(gerar_questoes(d, n_por_disciplina))
        except Exception as e:
            print(f"[erro] Falha ao gerar questões de {d}: {e}")
    return todas
