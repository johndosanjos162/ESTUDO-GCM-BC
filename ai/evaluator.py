"""Avaliação de respostas e feedback."""

from __future__ import annotations
import json


def _parse_alternativas(valor) -> list:
    if isinstance(valor, str):
        try:
            return json.loads(valor)
        except Exception:
            return []
    return valor or []


def avaliar_resposta(questao: dict, resposta_usuario: str) -> dict:
    correta = (questao.get("resposta_correta") or "").upper()
    resposta_usuario = (resposta_usuario or "").upper()
    acertou = resposta_usuario == correta
    alternativas = _parse_alternativas(questao.get("alternativas", []))

    idx_correta = ord(correta) - 65 if correta else -1
    texto_correta = alternativas[idx_correta] if 0 <= idx_correta < len(alternativas) else ""

    return {
        "acertou": acertou,
        "resposta_usuario": resposta_usuario,
        "resposta_correta": correta,
        "texto_correta": texto_correta,
        "explicacao": questao.get("explicacao", ""),
        "feedback": (
            "✅ Parabéns! Resposta correta."
            if acertou
            else f"❌ Incorreto. A resposta certa é {correta}) {texto_correta}"
        ),
    }
