# ------------------- EXCLUSÃO DE HISTÓRICO -------------------

def apagar_resposta(resposta_id: str) -> bool:
    """Apaga uma resposta específica pelo ID."""
    client = get_supabase()
    response = (
        client.table("respostas")
        .delete()
        .eq("id", resposta_id)
        .execute()
    )
    return bool(response.data)


def apagar_respostas_por_ids(ids: list) -> int:
    """Apaga várias respostas de uma vez."""
    if not ids:
        return 0
    client = get_supabase()
    response = (
        client.table("respostas")
        .delete()
        .in_("id", ids)
        .execute()
    )
    return len(response.data) if response.data else 0


def apagar_todo_historico(usuario_id: str) -> int:
    """Apaga TODO o histórico do usuário."""
    client = get_supabase()
    response = (
        client.table("respostas")
        .delete()
        .eq("usuario_id", usuario_id)
        .execute()
    )
    return len(response.data) if response.data else 0


def apagar_historico_por_disciplina(usuario_id: str, disciplina: str) -> int:
    """Apaga todo o histórico de um bloco específico."""
    client = get_supabase()
    response = (
        client.table("respostas")
        .delete()
        .eq("usuario_id", usuario_id)
        .eq("disciplina", disciplina)
        .execute()
    )
    return len(response.data) if response.data else 0
