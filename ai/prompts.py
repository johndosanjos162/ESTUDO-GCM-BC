"""Prompts especializados por bloco de estudo — foco Guarda Municipal BC."""

SYSTEM_PROMPT = """Você é um gerador especializado de questões para o concurso
da GUARDA MUNICIPAL DE BALNEÁRIO CAMBORIÚ (SC).

REGRAS OBRIGATÓRIAS:
1. Gere questões INÉDITAS de múltipla escolha (A a E).
2. Cada questão deve ter 5 alternativas e apenas 1 correta.
3. Foque EXCLUSIVAMENTE em conteúdos exigidos no edital da Guarda Municipal de Balneário Camboriú.
4. Use linguagem clara e objetiva, nível de concurso público municipal.
5. Inclua uma explicação curta e fundamentada (cite a lei ou artigo quando aplicável).
6. Responda EXCLUSIVAMENTE em JSON válido, sem markdown, no formato:
{
  "questoes": [
    {
      "enunciado": "...",
      "alternativas": ["A", "B", "C", "D", "E"],
      "resposta_correta": "A",
      "explicacao": "..."
    }
  ]
}"""


# ============================================================
# BLOCOS DE ESTUDO — prompts específicos
# ============================================================

BLOCOS = {
    "Lingua_Portuguesa": {
        "nome": "🇧🇷 Língua Portuguesa",
        "descricao": "Interpretação de texto, gramática, ortografia e redação oficial",
        "prompt": """
Gere {n} questões de LÍNGUA PORTUGUESA para o concurso da Guarda Municipal
de Balneário Camboriú (SC).

Tópicos obrigatórios:
- Compreensão e interpretação de texto (textos sobre segurança pública, cidadania, município)
- Ortografia oficial
- Pontuação e acentuação gráfica
- Concordância verbal e nominal
- Regência verbal e nominal
- Crase
- Classes de palavras e análise sintática
- Semântica (sinônimos, antônimos, homônimos, parônimos)
- Redação oficial (ofícios, requerimentos, comunicações internas)

Nível de dificuldade: {dificuldade}.
Contextualize algumas questões com situações do dia a dia da Guarda Municipal.
"""
    },

    "Matematica_Logica": {
        "nome": "🔢 Matemática e Raciocínio Lógico",
        "descricao": "Aritmética, porcentagem, lógica proposicional e análise combinatória",
        "prompt": """
Gere {n} questões de MATEMÁTICA E RACIOCÍNIO LÓGICO para o concurso da
Guarda Municipal de Balneário Camboriú (SC).

Tópicos obrigatórios:
- Operações com números inteiros, fracionários e decimais
- Porcentagem, razão e proporção
- Regra de três simples e composta
- MMC e MDC
- Equações de 1º e 2º grau
- Geometria básica (área, perímetro, volume)
- Interpretação de gráficos e tabelas
- Lógica proposicional (conectivos, tabelas-verdade, equivalências)
- Análise combinatória (princípio fundamental da contagem)
- Probabilidade básica

Contextualize com situações de efetivo policial, escalas de serviço, orçamento
de segurança pública municipal.

Nível de dificuldade: {dificuldade}.
"""
    },

    "Direito_Penal_Processual": {
        "nome": "⚖️ Direito Penal e Processual Penal",
        "descricao": "Crimes, flagrante, busca pessoal, leis especiais",
        "prompt": """
Gere {n} questões de NOÇÕES DE DIREITO PENAL E PROCESSUAL PENAL para o
concurso da Guarda Municipal de Balneário Camboriú (SC).

Tópicos obrigatórios:
- Aplicação da lei penal: princípios da legalidade e anterioridade
- Lei penal no tempo e no espaço
- Conceito de crime, fato típico, ilicitude e culpabilidade
- Crimes contra a pessoa (homicídio, lesão corporal, ameaça)
- Crimes contra a honra (calúnia, difamação, injúria)
- Crimes contra o patrimônio (furto, roubo, extorsão, estelionato)
- Crimes contra a Administração Pública (peculato, concussão, corrupção)
- Prisão em flagrante: tipos e procedimentos
- Busca pessoal e domiciliar
- Lei Maria da Penha (Lei 11.340/2006)
- Lei de Abuso de Autoridade (Lei 13.869/2019)
- Estatuto do Desarmamento (Lei 10.826/2003)

Foque na atuação prática da Guarda Municipal: o que o guarda pode e não pode fazer.
Nível de dificuldade: {dificuldade}.
"""
    },

    "Legislacao_Guarda_Municipal": {
        "nome": "📜 Legislação da Guarda Municipal",
        "descricao": "Lei 3.029/2009, LC 51/2019, Estatuto e atribuições",
        "prompt": """
Gere {n} questões sobre a LEGISLAÇÃO ESPECÍFICA DA GUARDA MUNICIPAL DE
BALNEÁRIO CAMBORIÚ (SC) para o concurso da corporação.

Base legal OBRIGATÓRIA:
- Lei Municipal 3.029/2009 (Estatuto da Guarda Municipal de Balneário Camboriú)
- Lei Complementar 51/2019
- Lei Complementar 36/2019
- Lei Federal 13.022/2014 (Estatuto Geral das Guardas Municipais)
- Constituição Federal, art. 144, § 8º

Tópicos obrigatórios:
- Atribuições e competências da Guarda Municipal de Balneário Camboriú
- Estrutura organizacional (Comando, Subcomando, Corregedoria, Ouvidoria)
- Ingresso na carreira (concurso público, requisitos)
- Jornada de trabalho (40 horas semanais em escala)
- Porte de arma e uso diferenciado da força
- Regime disciplinar e infrações
- Direitos, deveres e vantagens do Guarda Municipal
- Adicional de periculosidade (30%)
- Progressão funcional e carreira
- Integração com outras forças de segurança

Nível de dificuldade: {dificuldade}.
"""
    },

    "Direito_Constitucional_Administrativo": {
        "nome": "🏛️ Direito Constitucional e Administrativo",
        "descricao": "CF/88, princípios, atos administrativos, segurança pública",
        "prompt": """
Gere {n} questões de NOÇÕES DE DIREITO CONSTITUCIONAL E ADMINISTRATIVO
para o concurso da Guarda Municipal de Balneário Camboriú (SC).

Tópicos obrigatórios:
- Princípios fundamentais da República (art. 1º a 4º da CF/88)
- Direitos e garantias individuais e coletivos (art. 5º)
- Organização do Estado e dos Municípios
- Administração Pública: princípios (LIMPE)
- Poderes administrativos (hierárquico, disciplinar, regulamentar, de polícia)
- Atos administrativos: conceito, requisitos, atributos, extinção
- Responsabilidade civil do Estado
- Segurança Pública (art. 144 da CF/88)
- Competências dos Municípios em segurança pública
- Improbidade administrativa (Lei 8.429/1992)

Contextualize com a atuação da Guarda Municipal.
Nível de dificuldade: {dificuldade}.
"""
    },

    "Conhecimentos_Balneario_Camboriu": {
        "nome": "🌴 Conhecimentos de Balneário Camboriú",
        "descricao": "História, geografia, economia, turismo e legislação municipal",
        "prompt": """
Gere {n} questões sobre o MUNICÍPIO DE BALNEÁRIO CAMBORIÚ (SC) para o
concurso da Guarda Municipal.

Tópicos obrigatórios:
- História: fundação (1849), emancipação (20/07/1964), desmembramento de Camboriú
- Geografia: localização (litoral norte de SC), área (~46 km²), municípios limítrofes (Camboriú, Itajaí, Itapema)
- População: aproximadamente 139 mil habitantes (Censo 2022)
- Economia: turismo, construção civil, serviços, indústria
- Pontos turísticos: Cristo Luz, Parque Unipraias, Praia Central, Avenida Atlântica, Barra Sul
- Cultura e eventos: características do município
- Rio Camboriú
- Apelido "Dubai Brasileira" (verticalização e arranha-céus)
- Distância de Florianópolis (~80 km)
- Lei Orgânica do Município
- Legislação municipal relevante para segurança pública

Nível de dificuldade: {dificuldade}.
"""
    },

    "Legislacoes_Especiais": {
        "nome": "📋 Legislações Especiais",
        "descricao": "ECA, Estatuto do Idoso, CTB, Desarmamento, Maria da Penha",
        "prompt": """
Gere {n} questões sobre LEGISLAÇÕES ESPECIAIS para o concurso da Guarda
Municipal de Balneário Camboriú (SC).

Tópicos obrigatórios:
- Estatuto da Criança e do Adolescente (Lei 8.069/1990)
  - Medidas de proteção, ato infracional, conselho tutelar
- Estatuto da Pessoa Idosa (Lei 10.741/2003)
  - Direitos fundamentais, medidas de proteção
- Código de Trânsito Brasileiro (Lei 9.503/1997)
  - Competências municipais, fiscalização, infrações
- Estatuto do Desarmamento (Lei 10.826/2003)
  - Porte e posse de arma, registros
- Lei Maria da Penha (Lei 11.340/2006)
  - Tipos de violência, medidas protetivas
- Lei de Abuso de Autoridade (Lei 13.869/2019)
- Estatuto Geral das Guardas Municipais (Lei 13.022/2014)

Foque na aplicação prática pela Guarda Municipal.
Nível de dificuldade: {dificuldade}.
"""
    },

    "Conhecimentos_Gerais_Atualidades": {
        "nome": "🧠 Conhecimentos Gerais e Atualidades",
        "descricao": "Atualidades, segurança pública, cidadania e direitos humanos",
        "prompt": """
Gere {n} questões de CONHECIMENTOS GERAIS E ATUALIDADES para o concurso da
Guarda Municipal de Balneário Camboriú (SC).

Tópicos obrigatórios:
- Segurança pública no Brasil (políticas, SUSP, SENASP)
- Direitos humanos e cidadania
- Sistema Único de Segurança Pública (SUSP)
- Atualidades relacionadas a segurança pública (últimos 2 anos)
- Meio ambiente e sustentabilidade
- Noções de informática básica
- Ética no serviço público
- Cidadania e participação social
- Geografia e história de Santa Catarina
- Atualidades de Balneário Camboriú e região

Contextualize quando possível com a realidade de Balneário Camboriú.
Nível de dificuldade: {dificuldade}.
"""
    },
}
