"""Geração de questões via IA — sem trava de anti-repetição."""

from __future__ import annotations
import hashlib
import json
import re
from typing import Optional

from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
from ai.prompts import SYSTEM_PROMPT, BLOCOS
from core.database import salvar_questao

_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    """Cria cliente detectando automaticamente Groq ou OpenAI pela chave."""
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY (ou GROQ_API_KEY) não configurada.")

        if OPENAI_API_KEY.startswith("gsk_"):
            _client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url="https://api.groq.com/openai/v1",
            )
        else:
            _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _hash(texto: str) -> str:
    return hashlib.sha256(texto.strip().encode("utf-8")).hexdigest()


def listar_blocos() -> dict:
    return BLOCOS


def _montar_prompt(bloco, quantidade, dificuldade):
    info = BLOCOS.get(bloco)
    if not info:
        raise ValueError(f"Bloco inválido: {bloco}")

    prompt = info["prompt"].format(n=quantidade, dificuldade=dificuldade)

    prompt += """

============================================================
FOCO OBRIGATÓRIO:
Todas as questões devem ser EXCLUSIVAMENTE sobre o concurso
da Guarda Municipal de Balneário Camboriú (SC).
- Contextualize com situações, leis e dados do município.
- Responda no formato JSON:
  {"questoes": [{"enunciado": "...", "alternativas": ["A","B","C","D","E"], "resposta_correta": "A", "explicacao": "..."}]}
============================================================
"""
    return prompt


def _extrair_questoes(dados) -> list:
    """Extrai lista de questões de qualquer formato retornado pela IA."""
    if isinstance(dados, list):
        return dados

    if isinstance(dados, dict):
        for key in ("questoes", "questions", "questões", "items", "data", "result"):
            if key in dados and isinstance(dados[key], list):
                return dados[key]

        for v in dados.values():
            if isinstance(v, list) and v:
                return v

        if "enunciado" in dados:
            return [dados]

    return []


def _parse_json_seguro(raw: str):
    """Tenta parsear JSON com várias estratégias."""
    if not raw:
        return None

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    match = re.search(r"```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    for abre, fecha in [("{", "}"), ("[", "]")]:
        inicio = raw.find(abre)
        fim = raw.rfind(fecha)
        if inicio >= 0 and fim > inicio:
            try:
                return json.loads(raw[inicio:fim + 1])
            except json.JSONDecodeError:
                pass

    return None


def _chamar_ia(prompt: str) -> list:
    """Chama a IA e retorna lista de questões brutas."""
    try:
        response = _get_client().chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.85,
        )
    except Exception as e:
        msg = str(e)
        if "429" in msg or "insufficient_quota" in msg or "rate_limit" in msg.lower():
            raise RuntimeError(
                "Limite da API atingido. Aguarde 1 minuto e tente novamente."
            ) from e
        if "401" in msg or "invalid_api_key" in msg:
            raise RuntimeError(
                "Chave de API inválida. Verifique nos Secrets."
            ) from e
        if "404" in msg or "model_not_found" in msg:
            raise RuntimeError(
                f"Modelo '{OPENAI_MODEL}' não encontrado. "
                "Tente 'openai/gpt-oss-120b' (Groq) ou 'gpt-4o-mini' (OpenAI)."
            ) from e
        raise

    raw = response.choices[0].message.content or "{}"
    dados = _parse_json_seguro(raw)

    if dados is None:
        return []

    return _extrair_questoes(dados)


def _processar_questoes(bloco, dificuldade, questoes_raw):
    """Valida e salva as questões no banco. Não bloqueia por duplicatas."""
    validas = []
    for q in questoes_raw:
        if not isinstance(q, dict):
            continue

        if not all(k in q for k in ("enunciado", "alternativas", "resposta_correta")):
            continue

        enunciado = str(q.get("enunciado", "")).strip()
        if not enunciado:
            continue

        alts = q.get("alternativas", [])
        if not isinstance(alts, list) or len(alts) < 2:
            continue

        resp = str(q.get("resposta_correta", "")).strip().upper()
        if not resp or resp[0] not in "ABCDE":
            continue

        payload = {
            "disciplina": bloco,
            "enunciado": enunciado,
            "alternativas": json.dumps(alts, ensure_ascii=False),
            "resposta_correta": resp[0],
            "explicacao": str(q.get("explicacao", "")),
            "dificuldade": dificuldade,
            "fonte": "IA",
            "hash_conteudo": _hash(enunciado),
        }

        # Tenta salvar no banco, mas NÃO bloqueia se der erro
        try:
            salvo = salvar_questao(payload)
            if salvo:
                validas.append(salvo)
            else:
                # Se não salvou, usa o payload local mesmo assim
                payload["id"] = f"temp-{payload['hash_conteudo'][:8]}"
                validas.append(payload)
        except Exception as e:
            # Mesmo se o banco falhar, retorna a questão para o usuário
            print(f"[aviso] Falha ao salvar: {e}")
            payload["id"] = f"temp-{payload['hash_conteudo'][:8]}"
            validas.append(payload)

    return validas


def gerar_questoes(bloco, quantidade=5, dificuldade="medio", salvar=True):
    """Gera questões via IA. Sem trava de ineditismo."""
    if bloco not in BLOCOS:
        raise ValueError(f"Bloco inválido: {bloco}")

    prompt = _montar_prompt(bloco, quantidade, dificuldade)

    questoes_raw = _chamar_ia(prompt)

    if not questoes_raw:
        return []

    return _processar_questoes(bloco, dificuldade, questoes_raw)


def gerar_lote(blocos: list, n_por_bloco: int = 5) -> list:
    todas = []
    for b in blocos:
        try:
            todas.extend(gerar_questoes(b, n_por_bloco))
        except Exception as e:
            print(f"[erro] Falha em {b}: {e}")
    return todas
