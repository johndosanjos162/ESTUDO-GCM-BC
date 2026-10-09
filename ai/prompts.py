"""Templates de prompt por disciplina."""

SYSTEM_PROMPT = """Você é um gerador especializado de questões de concurso público
para a Guarda Municipal de Balneário Camboriú, SC.

Regras:
1. Gere questões INÉDITAS de múltipla escolha (A a E).
2. Cada questão deve ter enunciado claro, 5 alternativas e apenas 1 correta.
3. Inclua uma explicação curta e objetiva.
4. Responda EXCLUSIVAMENTE em JSON válido, sem markdown, no formato:
{
  "questoes": [
    {
      "enunciado": "...",
      "alternativas": ["texto A", "texto B", "texto C", "texto D", "texto E"],
      "resposta_correta": "A",
      "explicacao": "..."
    }
  ]
}"""


PROMPTS_DISCIPLINAS = {
    "Lingua_Portuguesa": """
Gere {n} questões de Língua Portuguesa para concurso público municipal.
Aborde: interpretação de texto, ortografia, pontuação, concordância verbal e nominal,
regência, crase, semântica e figuras de linguagem.
Nível de dificuldade: {dificuldade}.
""",
    "Matematica": """
Gere {n} questões de Matemática para concurso público municipal.
Aborde: aritmética, álgebra, porcentagem, razão e proporção,
regra de três, geometria plana e espacial, interpretação de gráficos e tabelas.
Nível de dificuldade: {dificuldade}.
""",
    "Legislacao_Guarda_Municipal": """
Gere {n} questões sobre legislação da Guarda Municipal de Balneário Camboriú (SC).
Baseie-se na Lei Municipal 3.029/2009 e na Lei Complementar 51/2019.
Temas: atribuições, competências, regime disciplinar, carreira, porte de arma,
uso diferenciado da força, direitos e deveres do servidor.
Nível de dificuldade: {dificuldade}.
""",
    "Conhecimentos_Balneario_Camboriu": """
Gere {n} questões sobre o município de Balneário Camboriú (SC).
Temas: história, emancipação (1964), geografia, população (Censo 2022),
economia, turismo, cultura, pontos turísticos, leis municipais relevantes.
Nível de dificuldade: {dificuldade}.
""",
}
