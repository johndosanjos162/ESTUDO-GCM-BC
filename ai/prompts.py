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
@@ -93,9 +89,12 @@
- Crimes contra a Administração Pública (peculato, concussão, corrupção)
- Prisão em flagrante: tipos e procedimentos
- Busca pessoal e domiciliar
- Lei Maria da Penha (Lei 11.340/2006)
- Lei Maria da Penha (Lei 11.340/2006): conceito básico, tipos de violência,
  medidas protetivas e crimes relacionados à violência doméstica
- Lei de Abuso de Autoridade (Lei 13.869/2019)
- Estatuto do Desarmamento (Lei 10.826/2003)
- Patrulha Maria da Penha no Município de Balneário Camboriú (Lei 4.245/2019)
- Aplicativo Alerta Mulher

Foque na atuação prática da Guarda Municipal: o que o guarda pode e não pode fazer.
Nível de dificuldade: {dificuldade}.
@@ -111,22 +110,23 @@

Base legal OBRIGATÓRIA:
- Lei Municipal 3.029/2009 (Estatuto da Guarda Municipal de Balneário Camboriú)
- Lei Complementar 51/2019
- Lei Complementar 36/2019
- Lei Complementar 51/2019 (Estrutura organizacional da Guarda Municipal)
- Lei Federal 13.022/2014 (Estatuto Geral das Guardas Municipais)
- Constituição Federal, art. 144, § 8º

Tópicos obrigatórios:
- Atribuições e competências da Guarda Municipal de Balneário Camboriú
- Estrutura organizacional (Comando, Subcomando, Corregedoria, Ouvidoria)
- Ingresso na carreira (concurso público, requisitos)
- Ingresso na carreira (concurso público, requisitos: ensino médio, CNH AB,
  idade 18 a 35 anos, altura mínima)
- Jornada de trabalho (40 horas semanais em escala)
- Porte de arma e uso diferenciado da força
- Regime disciplinar e infrações
- Direitos, deveres e vantagens do Guarda Municipal
- Adicional de periculosidade (30%)
- Progressão funcional e carreira
- Integração com outras forças de segurança
- Hierarquia e disciplina aplicadas à Guarda Municipal

Nível de dificuldade: {dificuldade}.
"""
@@ -150,6 +150,7 @@
- Segurança Pública (art. 144 da CF/88)
- Competências dos Municípios em segurança pública
- Improbidade administrativa (Lei 8.429/1992)
- Noções de Administração Pública

Contextualize com a atuação da Guarda Municipal.
Nível de dificuldade: {dificuldade}.
@@ -175,6 +176,7 @@
- Distância de Florianópolis (~80 km)
- Lei Orgânica do Município
- Legislação municipal relevante para segurança pública
- Plano Estratégico de Segurança Pública de Balneário Camboriú

Nível de dificuldade: {dificuldade}.
"""
@@ -194,12 +196,14 @@
 - Direitos fundamentais, medidas de proteção
- Código de Trânsito Brasileiro (Lei 9.503/1997)
 - Competências municipais, fiscalização, infrações
  - Legislação de Trânsito (CTB)
- Estatuto do Desarmamento (Lei 10.826/2003)
 - Porte e posse de arma, registros
- Lei Maria da Penha (Lei 11.340/2006)
 - Tipos de violência, medidas protetivas
- Lei de Abuso de Autoridade (Lei 13.869/2019)
- Estatuto Geral das Guardas Municipais (Lei 13.022/2014)
- Lei Municipal 4.245/2019: Patrulha Maria da Penha

Foque na aplicação prática pela Guarda Municipal.
Nível de dificuldade: {dificuldade}.
@@ -224,6 +228,7 @@
- Cidadania e participação social
- Geografia e história de Santa Catarina
- Atualidades de Balneário Camboriú e região
- Tópicos relevantes e atuais de diversas áreas: política, economia, sociedade

Contextualize quando possível com a realidade de Balneário Camboriú.
Nível de dificuldade: {dificuldade}.
