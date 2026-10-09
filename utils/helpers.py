"""Funções auxiliares."""

from __future__ import annotations
import json
from datetime import datetime


def parse_alternativas(valor) -> list:
    if isinstance(valor, str):
        try:
            return json.loads(valor)
        except Exception:
            return []
    return valor or []


def formatar_data(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return iso_str


def calcular_percentual(acertos: int, total: int) -> float:
    return round((acertos / total) * 100, 1) if total else 0.0


def inicializar_session_state() -> None:
    import streamlit as st
    defaults = {
        "user": None,
        "questoes_sessao": [],
        "indice_atual": 0,
        "respostas_sessao": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
