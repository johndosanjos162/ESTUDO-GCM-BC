"""Conexão e operações com o Supabase."""

from __future__ import annotations
from typing import Optional
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_ANON_KEY

_client: Optional[Client] = None


def get_supabase() -> Client:
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            raise RuntimeError("Credenciais do Supabase ausentes.")
        _client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    return _client


# ---------------- QUESTÕES ----------------

def buscar_questoes_por_disciplina(disciplina, dificuldade=None, limite=20):
    client = get_supabase()
    query = client.table("questoes").select("*").eq("disciplina", disciplina)
    if dificuldade:
        query = query.eq("dificuldade", dificuldade)
    response = query.limit(limite).execute()
    return response.data or []


def salvar_questao(dados):
    client = get_supabase()
    response = client.table("questoes").insert(dados).execute()
    return response.data[0] if response.data else {}


def questao_ja_existe(hash_conteudo):
    client = get_supabase()
    response = client.table("questoes").select("id").eq("hash_conteudo", hash_conteudo).limit(1).execute()
    return bool(response.data)


def listar_questoes(limite=100):
    client = get_supabase()
    response = client.table("questoes").select("*").order("criado_em", desc=True).limit(limite).execute()
    return response.data or []


def buscar_enunciados_existentes(disciplina, limite=200):
    client = get_supabase()
    response = (
        client.table("questoes")
        .select("enunciado")
        .eq("disciplina", disciplina)
        .order("criado_em", desc=True)
        .limit(limite)
        .execute()
    )
    return [row["enunciado"] for row in (response.data or [])]


def contar_questoes_por_disciplina(disciplina):
    client = get_supabase()
    response = client.table("questoes").select("id", count="exact").eq("disciplina", disciplina).execute()
    return response.count or 0


# ---------------- RESPOSTAS ----------------

def salvar_resposta(dados):
    client = get_supabase()
    response = client.table("respostas").insert(dados).execute()
    return response.data[0] if response.data else {}


def buscar_historico_usuario(usuario_id, disciplina=None, limite=100):
    client = get_supabase()
    query = client.table("respostas").select("*").eq("usuario_id", usuario_id).order("respondido_em", desc=True)
    if disciplina:
        query = query.eq("disciplina", disciplina)
    response = query.limit(limite).execute()
    return response.data or []


def estatisticas_por_disciplina(usuario_id):
    client = get_supabase()
    try:
        response = client.rpc("estatisticas_disciplina", {"p_usuario_id": usuario_id}).execute()
        return response.data or []
    except Exception:
        historico = buscar_historico_usuario(usuario_id, limite=1000)
        agregado = {}
        for r in historico:
            disc = r["disciplina"]
            agregado.setdefault(disc, {"disciplina": disc, "total": 0, "acertos": 0})
            agregado[disc]["total"] += 1
            if r.get("acertou"):
                agregado[disc]["acertos"] += 1
        return list(agregado.values())


# ---------------- EXCLUSÃO DE HISTÓRICO ----------------

def apagar_resposta(resposta_id):
    client = get_supabase()
    response = client.table("respostas").delete().eq("id", resposta_id).execute()
    return bool(response.data)


def apagar_respostas_por_ids(ids):
    if not ids:
        return 0
    client = get_supabase()
    response = client.table("respostas").delete().in_("id", ids).execute()
    return len(response.data) if response.data else 0


def apagar_todo_historico(usuario_id):
    client = get_supabase()
    response = client.table("respostas").delete().eq("usuario_id", usuario_id).execute()
    return len(response.data) if response.data else 0


def apagar_historico_por_disciplina(usuario_id, disciplina):
    client = get_supabase()
    response = client.table("respostas").delete().eq("usuario_id", usuario_id).eq("disciplina", disciplina).execute()
    return len(response.data) if response.data else 0


# ---------------- PERFIL ----------------

def obter_perfil(usuario_id):
    client = get_supabase()
    response = client.table("profiles").select("*").eq("id", usuario_id).limit(1).execute()
    return response.data[0] if response.data else None


def atualizar_ciclo(usuario_id, novo_ciclo):
    client = get_supabase()
    client.table("profiles").update({"ciclo_atual": novo_ciclo}).eq("id", usuario_id).execute()
