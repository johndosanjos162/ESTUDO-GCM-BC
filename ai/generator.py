"""Geração de questões via IA — com detecção automática de Groq/OpenAI."""

from __future__ import annotations
import hashlib
import json
from typing import Optional

from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
from ai.prompts import SYSTEM_PROMPT, BLOCOS
from core.database import (
    salvar_questao,
    questao_ja_existe,
    buscar_enunciados_existentes,
)

_client: Optional[OpenAI] = None

MAX_ENUNCIADOS_NO_PROMPT = 150
MAX_TENTATIVAS = 3


def _get_client() -> OpenAI:
    """Cria cliente detectando automaticamente Groq ou OpenAI pela chave."""
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY não configurada.")

        if OPENAI_API_KEY.startswith("gsk_"):
            # Chave do Groq → endpoint do Groq
            _client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url="https://api.groq.com/openai/v1",
            )
        else:
            # Chave da OpenAI (sk-...)
            _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _hash(texto: str) -> str:
    return hashlib.sha256(texto.strip().encode("utf-8")).hexdigest()


def listar_blocos() -> dict:
    return BLOCOS


def _montar_prompt(bloco, quantidade, dificuldade, enunciados_existentes):
    info = BLOCOS.get(bloco)
    if not info:
        raise ValueError(f"Bloco inválido: {bloco}")

    prompt_base = info["prompt"].format(n=quantidade, dificuldade=dificuldade)

    prompt_base += """

============================================================
REFORÇO OBRIGATÓRIO DE FOCO:
Todas as questões devem ser EXCLUSIVAMENTE sobre o concurso
da Guarda Municipal de Balneário Camboriú (SC).
- NÃO gere questões genéricas de outras áreas.
- Contextualize com situações, leis e dados do município.
============================================================
"""

    if enunciados_existentes:
        lista = enunciados_existentes[-MAX_ENUNCIADOS_NO_PROMPT:]
        lista_formatada = "\n".join(
            f"{i+1}. {e[:180]}{'...' if len(e) > 180 else ''}"
            for i, e in enumerate(lista)
        )
        prompt_base += f"""

============================================================
⚠️ PROIBIDO REPETIR — NÃO gere questões iguais ou muito
semelhantes a NENHUMA das {len(lista)} questões abaixo:

{lista_formatada}
============================================================
"""
    return prompt_base


def _chamar_ia(prompt: str) -> list:
    try:
        response = _get_client().chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.95,
        )
    except Exception as e:
        msg = str(e)
        if "429" in msg or "insufficient_quota" in msg:
            raise RuntimeError(
                "Limite/cota da API atingido. Aguarde ou troque o modelo."
            ) from e
        if "401" in msg or "invalid_api_key" in msg:
            raise RuntimeError(
                "Chave de API inválida. Verifique OPENAI_API_KEY nos Secrets."
            ) from e
        if "404" in msg or "model_not_found" in msg:
            raise RuntimeError(
                f"Modelo '{OPENAI_MODEL}' não encontrado. "
                "Tente 'openai/gpt-oss-120b' (Groq) ou 'gpt-4o-mini' (OpenAI)."
            ) from e
        raise

    raw = response.choices[0].message.content or "{}"
    dados = json.loads(raw)
    return dados.get("questoes", [])


def _validar_e_persistir(bloco, dificuldade, questoes_raw, hashes_sessao):
    validas = []
    for q in questoes_raw:
        if not all(k in q for k in ("enunciado", "alternativas", "resposta_correta")):
            continue

        enunciado = q["enunciado"].strip()
        if not enunciado:
            continue

        h = _hash(enunciado)

        if h in hashes_sessao:
            continue

        try:
            if questao_ja_existe(h):
                hashes_sessao.add(h)
                continue
        except Exception:
            pass

        payload = {
            "disciplina": bloco,
            "enunciado": enunciado,
            "alternativas": json.dumps(q["alternativas"], ensure_ascii=False),
            "resposta_correta": q["resposta_correta"].upper()[0],
            "explicacao": q.get("explicacao", ""),
            "dificuldade": dificuldade,
            "fonte": "IA",
            "hash_conteudo": h,
        }

        try:
            salvo = salvar_questao(payload)
            if salvo:
                validas.append(salvo)
                hashes_sessao.add(h)
            else:
                hashes_sessao.add(h)
        except Exception as e:
            print(f"[aviso] Falha ao salvar: {e}")
            hashes_sessao.add(h)

    return validas


def gerar_questoes(bloco, quantidade=5, dificuldade="medio", salvar=True):
    """Gera questões únicas via IA, com foco na GMBC."""
    if bloco not in BLOCOS:
        raise ValueError(f"Bloco inválido: {bloco}")

    try:
        enunciados_existentes = buscar_enunciados_existentes(bloco, limite=200)
    except Exception:
        enunciados_existentes = []

    resultado = []
    hashes_sessao = set()
    tentativa = 0

    while len(resultado) < quantidade and tentativa < MAX_TENTATIVAS:
        tentativa += 1
        faltam = quantidade - len(resultado)

        existentes_prompt = enunciados_existentes + [q["enunciado"] for q in resultado]
        prompt = _montar_prompt(bloco, faltam, dificuldade, existentes_prompt)

        try:
            questoes_raw = _chamar_ia(prompt)
        except Exception as e:
            if tentativa == 1:
                raise
            print(f"[aviso] Tentativa {tentativa} falhou: {e}")
            continue

        novas = _validar_e_persistir(bloco, dificuldade, questoes_raw, hashes_sessao)
        resultado.extend(novas)

    return resultado[:quantidade]


def gerar_lote(blocos: list, n_por_bloco: int = 5) -> list:
    todas = []
    for b in blocos:
        try:
            todas.extend(gerar_questoes(b, n_por_bloco))
        except Exception as e:
            print(f"[erro] Falha em {b}: {e}")
    return todas
