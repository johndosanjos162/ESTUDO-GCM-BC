"""Gerenciamento do ciclo semanal alternado A/B."""

from __future__ import annotations
from datetime import datetime, timedelta

from config import CICLO_A, CICLO_B, DISCIPLINAS
from core.database import obter_perfil, atualizar_ciclo


def _proxima_segunda() -> str:
    hoje = datetime.now()
    dias = (7 - hoje.weekday()) % 7 or 7
    return (hoje + timedelta(days=dias)).strftime("%d/%m/%Y")


def obter_ciclo_atual(usuario_id: str) -> dict:
    perfil = obter_perfil(usuario_id)
    if not perfil:
        return {
            "numero_ciclo": 1,
            "disciplinas": CICLO_A,
            "nomes": [DISCIPLINAS[d] for d in CICLO_A],
            "proxima_alternancia": _proxima_segunda(),
        }

    ciclo_base = perfil.get("ciclo_atual", 1)
    semana = datetime.now().isocalendar()[1]
    ciclo_ativo = ciclo_base if semana % 2 == 0 else (2 if ciclo_base == 1 else 1)
    disciplinas = CICLO_A if ciclo_ativo == 1 else CICLO_B

    return {
        "numero_ciclo": ciclo_ativo,
        "disciplinas": disciplinas,
        "nomes": [DISCIPLINAS[d] for d in disciplinas],
        "proxima_alternancia": _proxima_segunda(),
    }


def alternar_ciclo(usuario_id: str) -> int:
    perfil = obter_perfil(usuario_id)
    atual = perfil.get("ciclo_atual", 1) if perfil else 1
    novo = 2 if atual == 1 else 1
    atualizar_ciclo(usuario_id, novo)
    return novo
