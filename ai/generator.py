"""Geração de questões via IA — robusto contra recusa e formato inválido."""

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
FORMATO OBRIGATÓRIO DE RESPOSTA:
Responda APENAS com JSON válido, sem texto antes ou depois, sem markdown.
Se não conseguir gerar, retorne {"questoes": []}.
Formato exato:
{
  "questoes": [
    {
      "enunciado": "texto da pergunta",
      "alternativas": ["texto A", "texto B", "texto C", "texto D", "texto E"],
      "resposta_correta": "A",
      "explicacao": "explicação curta"
    }
  ]
}
============================================================
"""
    return prompt


def _extrair_questoes(dados) -> list:
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
    if not raw:
        return None

    # Detecta recusa da IA
    recusas = [
        "i'm sorry", "i cannot", "i can't", "não posso", "não consigo",
        "desculpe", "sorry", "unable to", "cannot fulfill",
    ]
    raw_lower = raw.lower()
    if any(r in raw_lower for r in recusas) and "{" not in raw:
        print(f"[aviso] IA recusou gerar: {raw[:150]}")
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
    try:
        response = _get_client().chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
    except Exception as e:
        msg = str(e)
        # Erro 400 do Groq quando a IA se recusa a gerar
        if "400" in msg or "json_validate_failed" in msg or "Failed to generate JSON" in msg:
            print(f"[aviso] IA recusou/formato inválido: {msg[:200]}")
            return []
        if "429" in msg or "insufficient_quota" in msg or "rate_limit" in msg.lower():
            raise RuntimeError(
                "Limite da API atingido. Aguarde 1 minuto e tente novamente."
            ) from e
        if "401" in msg or "invalid_api_key" in msg:
            raise RuntimeError("Chave de API inválida. Verifique os Secrets.") from e
        if "404" in msg or "model_not_found" in msg:
            raise RuntimeError(
                f"Modelo '{OPENAI_MODEL}' não encontrado."
            ) from e
        raise

    raw = response.choices[0].message.content or "{}"
    dados = _parse_json_seguro(raw)
    if dados is None:
        return []
    return _extrair_questoes(dados)


def _normalizar_alternativas(alts) -> list:
    """Garante que alternativas seja uma lista de strings não vazias."""
    if not isinstance(alts, list):
        return []
    resultado = []
    for a in alts:
        if a is None:
            continue
        texto = str(a).strip()
        # Remove prefixos tipo "A) ", "A. ", "a) "
        texto = re.sub(r"^[A-Ea-e][\)\.\-\:]\s*", "", texto)
        if texto:
            resultado.append(texto)
    return resultado


def _processar_questoes(bloco, dificuldade, questoes_raw):
    validas = []
    for q in questoes_raw:
        if not isinstance(q, dict):
            continue

        # Aceita chaves alternativas
        enunciado = q.get("enunciado") or q.get("pergunta") or q.get("question")
        alternativas = q.get("alternativas") or q.get("options") or q.get("opcoes")
        resposta = q.get("resposta_correta") or q.get("correct") or q.get("gabarito")

        if not enunciado or not alternativas or not resposta:
            continue

        enunciado = str(enunciado).strip()
        if len(enunciado) < 10:
            continue

        alts = _normalizar_alternativas(alternativas)
        if len(alts) < 4:
            continue

        resp = str(resposta).strip().upper()
        letra = resp[0] if resp else ""
        if letra not in "ABCDE":
            continue

        # Índice da resposta — se inválido, descarta
        idx = ord(letra) - 65
        if idx >= len(alts):
            continue

        payload = {
            "disciplina": bloco,
            "enunciado": enunciado,
            "alternativas": json.dumps(alts, ensure_ascii=False),
            "resposta_correta": letra,
            "explicacao": str(q.get("explicacao", "") or q.get("explanation", "")),
            "dificuldade": dificuldade,
            "fonte": "IA",
            "hash_conteudo": _hash(enunciado),
        }

        try:
            salvo = salvar_questao(payload)
            if salvo:
                validas.append(salvo)
            else:
                payload["id"] = f"temp-{payload['hash_conteudo'][:8]}"
                validas.append(payload)
        except Exception as e:
            print(f"[aviso] Falha ao salvar: {e}")
            payload["id"] = f"temp-{payload['hash_conteudo'][:8]}"
            validas.append(payload)

    return validas


def gerar_questoes(bloco, quantidade=5, dificuldade="medio", salvar=True):
    """Gera questões via IA. Tenta 3 vezes se a IA recusar ou retornar vazio."""
    if bloco not in BLOCOS:
        raise ValueError(f"Bloco inválido: {bloco}")

    resultado = []
    tentativas = 3

    for tentativa in range(tentativas):
        faltam = quantidade - len(resultado)
        if faltam <= 0:
            break

        prompt = _montar_prompt(bloco, faltam, dificuldade)

        try:
            questoes_raw = _chamar_ia(prompt)
        except Exception as e:
            # Se for erro fatal (401, 404), propaga
            if any(x in str(e) for x in ["Chave de API", "não encontrado"]):
                raise
            print(f"[aviso] Tentativa {tentativa + 1}: {e}")
            continue

        if not questoes_raw:
            print(f"[aviso] Tentativa {tentativa + 1}: vazio/recusa")
            continue

        validas = _processar_questoes(bloco, dificuldade, questoes_raw)
        resultado.extend(validas)

    return resultado[:quantidade]


def gerar_lote(blocos: list, n_por_bloco: int = 5) -> list:
    todas = []
    for b in blocos:
        try:
            todas.extend(gerar_questoes(b, n_por_bloco))
        except Exception as e:
            print(f"[erro] Falha em {b}: {e}")
    return todas
