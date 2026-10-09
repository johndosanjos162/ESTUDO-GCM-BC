"""Geração de questões via IA — com anti-repetição e foco na GMBC."""

from __future__ import annotations
import hashlib
import json
from typing import Optional

from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
from ai.prompts import SYSTEM_PROMPT, BLOCOS
from core.database import (
    salvar_questao,
    questao_ja_existe,
    buscar_enunciados_existentes,
)

_client: Optional[OpenAI] = None

# Quantas questões antigas enviar no prompt (evita estourar tokens)
MAX_ENUNCIADOS_NO_PROMPT = 150

# Quantas rodadas tentar caso a IA repita questões
MAX_TENTATIVAS = 5


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY não configurada.")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _hash(texto: str) -> str:
    return hashlib.sha256(texto.strip().encode("utf-8")).hexdigest()


def listar_blocos() -> dict:
    """Retorna todos os blocos disponíveis."""
    return BLOCOS


def _montar_prompt(
    bloco: str,
    quantidade: int,
    dificuldade: str,
    enunciados_existentes: list[str],
) -> str:
    """Monta o prompt final incluindo a lista de questões a NÃO repetir."""
    info = BLOCOS.get(bloco)
    if not info:
        raise ValueError(f"Bloco inválido: {bloco}")

    prompt_base = info["prompt"].format(n=quantidade, dificuldade=dificuldade)

    # Reforço obrigatório de foco no concurso
    prompt_base += """

============================================================
REFORÇO OBRIGATÓRIO DE FOCO:
Todas as questões geradas devem ser EXCLUSIVAMENTE sobre o concurso
da Guarda Municipal de Balneário Camboriú (SC).
- NÃO gere questões genéricas de concursos de outras áreas.
- NÃO gere questões sobre temas que não constam no edital da GMBC.
- Contextualize SEMPRE com situações, leis e dados do município.
- Se a questão for de Português/Matemática, use exemplos da corporação.
============================================================
"""

    # Lista de enunciados já existentes (evitar repetição)
    if enunciados_existentes:
        lista = enunciados_existentes[-MAX_ENUNCIADOS_NO_PROMPT:]
        lista_formatada = "\n".join(
            f"{i + 1}. {e[:180]}{'...' if len(e) > 180 else ''}"
            for i, e in enumerate(lista)
        )
        prompt_base += f"""

============================================================
⚠️ PROIBIDO REPETIR — NÃO gere questões iguais ou muito
semelhantes a NENHUMA das {len(lista)} questões abaixo.
Use temas, dados e abordagens DIFERENTES:

{lista_formatada}
============================================================
"""
    return prompt_base


def _chamar_ia(prompt: str) -> list[dict]:
    """Chama a IA e retorna a lista de questões brutas."""
    try:
        response = _get_client().chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.95,   # mais criativo = mais variedade
        )
    except Exception as e:
        msg = str(e)
        if "429" in msg or "insufficient_quota" in msg:
            raise RuntimeError(
                "Sem créditos na API. Adicione fundos ou troque o modelo."
            ) from e
        if "404" in msg or "model_not_found" in msg:
            raise RuntimeError(
                f"Modelo '{OPENAI_MODEL}' não encontrado. "
                "Verifique os Secrets."
            ) from e
        raise

    raw = response.choices[0].message.content or "{}"
    dados = json.loads(raw)
    return dados.get("questoes", [])


def _validar_e_persistir(
    bloco: str,
    dificuldade: str,
    questoes_raw: list[dict],
    hashes_sessao: set,
    salvar: bool = True,
) -> list[dict]:
    """
    Valida cada questão:
      - descarta se o hash já existe no banco
      - descarta se o hash já foi gerado nesta sessão
      - salva as novas no banco (se salvar=True)
    Retorna apenas as válidas.
    """
    validas = []
    for q in questoes_raw:
        if not all(k in q for k in ("enunciado", "alternativas", "resposta_correta")):
            continue

        enunciado = q["enunciado"].strip()
        if not enunciado:
            continue

        h = _hash(enunciado)

        # Já apareceu nesta sessão? Descarta
        if h in hashes_sessao:
            continue

        # Já existe no banco? Descarta
        try:
            if questao_ja_existe(h):
                hashes_sessao.add(h)
                continue
        except Exception:
            pass  # se o banco falhar, deixa passar

        payload = {
            "disciplina": bloco,
            "enunciado": enunciado,
            "alternativas": json.dumps(q["alternativas"], ensure_ascii=False),
            "resposta_correta": q["resposta_correta"].upper()[0],
            "explicacao": q.get("explicacao", ""),
            "dificuldade": dificuldade,
            "fonte": "IA",
            "hash_conteudo": h,
        }

        if not salvar:
            payload["id"] = f"temp-{h[:8]}"
            validas.append(payload)
            hashes_sessao.add(h)
            continue

        try:
            salvo = salvar_questao(payload)
            if salvo:
                validas.append(salvo)
                hashes_sessao.add(h)
            else:
                hashes_sessao.add(h)
        except Exception as e:
            print(f"[aviso] Falha ao salvar questão: {e}")
            hashes_sessao.add(h)

    return validas


def gerar_questoes(
    bloco: str,
    quantidade: int = 5,
    dificuldade: str = "medio",
    salvar: bool = True,
) -> list[dict]:
    """
    Gera questões ÚNICAS para um bloco, com foco EXCLUSIVO na GMBC.

    Estratégia anti-repetição:
      1. Busca enunciados já existentes no banco para NÃO repetir
      2. Envia a lista no prompt (a IA evita repetir)
      3. Valida cada questão pelo hash SHA-256
      4. Se faltarem, tenta novamente (até MAX_TENTATIVAS)
      5. Salva as novas no banco para futuras consultas
    """
    if bloco not in BLOCOS:
        raise ValueError(f"Bloco inválido: {bloco}")

    # 1) Busca enunciados já existentes no banco
    try:
        enunciados_existentes = buscar_enunciados_existentes(bloco, limite=200)
    except Exception:
        enunciados_existentes = []

    resultado: list[dict] = []
    hashes_sessao: set = set()
    tentativa = 0

    # 2) Loop até conseguir a quantidade pedida (ou estourar tentativas)
    while len(resultado) < quantidade and tentativa < MAX_TENTATIVAS:
        tentativa += 1
        faltam = quantidade - len(resultado)

        # Junta existentes do banco + já gerados nesta sessão
        existentes_para_prompt = enunciados_existentes + [
            q["enunciado"] for q in resultado
        ]

        prompt = _montar_prompt(
            bloco, faltam, dificuldade, existentes_para_prompt
        )

        try:
            questoes_raw = _chamar_ia(prompt)
        except Exception as e:
            if tentativa == 1:
                raise  # primeira tentativa falhou → propaga o erro
            print(f"[aviso] Tentativa {tentativa} falhou: {e}")
            continue

        novas = _validar_e_persistir(
            bloco, dificuldade, questoes_raw, hashes_sessao, salvar=salvar
        )
        resultado.extend(novas)

    return resultado[:quantidade]


def gerar_lote(blocos: list, n_por_bloco: int = 5) -> list:
    """Gera questões para múltiplos blocos (útil para testes em lote)."""
    todas = []
    for b in blocos:
        try:
            todas.extend(gerar_questoes(b, n_por_bloco))
        except Exception as e:
            print(f"[erro] Falha ao gerar questões de {b}: {e}")
    return todas
