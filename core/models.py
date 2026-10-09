"""Modelos de dados."""

from typing import TypedDict


class Questao(TypedDict, total=False):
    id: str
    disciplina: str
    enunciado: str
    alternativas: list
    resposta_correta: str
    explicacao: str
    dificuldade: str
    fonte: str
    hash_conteudo: str
    criado_em: str


class Resposta(TypedDict, total=False):
    id: str
    usuario_id: str
    questao_id: str
    disciplina: str
    resposta_usuario: str
    resposta_correta: str
    acertou: bool
    respondido_em: str
