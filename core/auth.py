"""Autenticação com Supabase Auth — apenas login/logout."""

from __future__ import annotations
from typing import Optional
from core.database import get_supabase


def login(email: str, senha: str):
    """Realiza login e retorna sessão."""
    client = get_supabase()
    return client.auth.sign_in_with_password({"email": email, "password": senha})


def logout() -> None:
    """Encerra sessão."""
    client = get_supabase()
    client.auth.sign_out()


def usuario_atual() -> Optional[object]:
    """Retorna usuário logado ou None."""
    client = get_supabase()
    try:
        response = client.auth.get_user()
        return response.user if response else None
    except Exception:
        return None
