"""Configurações centrais do aplicativo."""

import os
from dotenv import load_dotenv

load_dotenv()


def _get(key: str, default: str = "") -> str:
    """Lê de st.secrets (Streamlit Cloud) ou de variáveis de ambiente (local)."""
    try:
        import streamlit as st
        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)


# ---------- IA ----------
# Aceita tanto GROQ_API_KEY quanto OPENAI_API_KEY (o primeiro que existir)
_API_KEY: str = (
    _get("GROQ_API_KEY")
    or _get("OPENAI_API_KEY")
    or _get("API_KEY")
)

# Alias exposto para o resto do código
OPENAI_API_KEY: str = _API_KEY
GROQ_API_KEY: str = _API_KEY

# Modelo — aceita qualquer um dos nomes nas Secrets
OPENAI_MODEL: str = (
    _get("GROQ_MODEL")
    or _get("OPENAI_MODEL")
    or "openai/gpt-oss-120b"
)

# URL base — Groq por padrão, mas pode ser sobrescrita
API_BASE_URL: str = _get("API_BASE_URL", "https://api.groq.com/openai/v1")


# ---------- Supabase ----------
SUPABASE_URL: str = _get("SUPABASE_URL")
SUPABASE_ANON_KEY: str = _get("SUPABASE_ANON_KEY")

# ---------- Aplicação ----------
APP_TITLE = "Estudos GM Balneário Camboriú"
APP_ICON = "📚"
APP_LAYOUT = "wide"

# ---------- Blocos de Estudo (8 blocos) ----------
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
    """Retorna lista de variáveis faltantes."""
    erros = []
    if not SUPABASE_URL:
        erros.append("SUPABASE_URL")
    if not SUPABASE_ANON_KEY:
        erros.append("SUPABASE_ANON_KEY")
    if not _API_KEY:
        erros.append("GROQ_API_KEY (ou OPENAI_API_KEY)")
    return erros
