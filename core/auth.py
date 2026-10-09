"""Autenticação com Supabase Auth."""
"""Autenticação com Supabase Auth — apenas login/logout."""

from __future__ import annotations
from typing import Optional
from core.database import get_supabase


def cadastrar_usuario(email: str, senha: str, nome: str) -> dict:
    client = get_supabase()
    auth_response = client.auth.sign_up({"email": email, "password": senha})

    if auth_response.user:
        try:
            client.table("profiles").insert({
                "id": auth_response.user.id,
                "nome": nome,
                "email": email,
                "ciclo_atual": 1,
            }).execute()
        except Exception as e:
            print(f"[aviso] Perfil pode já existir: {e}")

    return {"user": auth_response.user, "session": auth_response.session}


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
