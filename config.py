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


def _get_first(keys: list, default: str = "") -> str:
    """Tenta várias chaves e retorna a primeira encontrada."""
    for k in keys:
        val = _get(k, "")
        if val:
            return val
    return default


# ---------- IA (aceita GROQ_API_KEY ou OPENAI_API_KEY) ----------
OPENAI_API_KEY: str = _get_first(["OPENAI_API_KEY", "GROQ_API_KEY"])
OPENAI_MODEL: str = _get_first(
    ["OPENAI_MODEL", "GROQ_MODEL"],
    default="openai/gpt-oss-120b",
)

# ---------- Supabase ----------
SUPABASE_URL: str = _get("SUPABASE_URL")
SUPABASE_ANON_KEY: str = _get("SUPABASE_ANON_KEY")

# ---------- Aplicação ----------
APP_TITLE = "Estudos GM Balneário Camboriú"
APP_ICON = "📚"
APP_LAYOUT = "wide"

# ---------- Blocos de Estudo ----------
BLOCOS = {
    "Lingua_Portuguesa": "🇧🇷 Língua Portuguesa",
    "Matematica_Logica": "🔢 Matemática e Raciocínio Lógico",
    "Direito_Penal_Processual": "⚖️ Direito Penal e Processual Penal",
    "Legislacao_Guarda_Municipal": "📜 Legislação da Guarda Municipal",
    "Direito_Constitucional_Administrativo": "🏛️ Direito Constitucional e Administrativo",
    "Conhecimentos_Balneario_Camboriu": "🌴 Conhecimentos de Balneário Camboriú",
    "Legislacoes_Especiais": "📋 Legislações Especiais",
    "Conhecimentos_Gerais_Atualidades": "🧠 Conhecimentos Gerais e Atualidades",
}

# Alias para compatibilidade
DISCIPLINAS = BLOCOS

# ---------- Ciclos semanais ----------
CICLO_A = [
    "Lingua_Portuguesa",
    "Legislacao_Guarda_Municipal",
    "Direito_Penal_Processual",
]

CICLO_B = [
    "Matematica_Logica",
    "Conhecimentos_Balneario_Camboriu",
    "Direito_Constitucional_Administrativo",
]


def validar_configuracoes() -> list:
    erros = []
    if not SUPABASE_URL:
        erros.append("SUPABASE_URL")
    if not SUPABASE_ANON_KEY:
        erros.append("SUPABASE_ANON_KEY")
    if not OPENAI_API_KEY:
        erros.append("OPENAI_API_KEY (ou GROQ_API_KEY)")
    return erros
