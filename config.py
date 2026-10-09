"""Configurações centrais do aplicativo."""

import os
from dotenv import load_dotenv

load_dotenv()


def _get(key: str, default: str = "") -> str:
    """Lê de st.secrets (Cloud) ou de variáveis de ambiente (local)."""
    try:
        import streamlit as st
        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)


SUPABASE_URL: str = _get("SUPABASE_URL")
SUPABASE_ANON_KEY: str = _get("SUPABASE_ANON_KEY")
OPENAI_API_KEY: str = _get("OPENAI_API_KEY")
OPENAI_MODEL: str = _get("OPENAI_MODEL", "gpt-4o-mini")

APP_TITLE = "Estudos GM Balneário Camboriú"
APP_ICON = "📚"
APP_LAYOUT = "wide"

DISCIPLINAS = {
    "Lingua_Portuguesa": "Língua Portuguesa",
    "Matematica": "Matemática",
    "Legislacao_Guarda_Municipal": "Legislação da Guarda Municipal",
    "Conhecimentos_Balneario_Camboriu": "Conhecimentos de Balneário Camboriú",
}

CICLO_A = ["Lingua_Portuguesa", "Legislacao_Guarda_Municipal"]
CICLO_B = ["Matematica", "Conhecimentos_Balneario_Camboriu"]


def validar_configuracoes() -> list:
    erros = []
    if not SUPABASE_URL:
        erros.append("SUPABASE_URL")
    if not SUPABASE_ANON_KEY:
        erros.append("SUPABASE_ANON_KEY")
    if not OPENAI_API_KEY:
        erros.append("OPENAI_API_KEY")
    return erros
