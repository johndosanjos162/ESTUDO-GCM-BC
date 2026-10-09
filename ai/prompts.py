"""Prompts especializados por bloco — cada matéria gera SOMENTE sua matéria."""

SYSTEM_PROMPT = """Você é um gerador de questões de concurso público.
Gere questões de múltipla escolha (A a E), com apenas 1 alternativa correta.

REGRAS CRÍTICAS:
1. Cada questão deve ser EXCLUSIVAMENTE sobre a matéria do bloco solicitado.
2. NUNCA misture matérias. Se o bloco é Língua Portuguesa, NÃO gere questões
   sobre Direito, Constituição, Leis ou Administração Pública.
3. Se o bloco é Matemática, NÃO gere questões sobre leis ou gramática.
4. Só mencione a Guarda Municipal de Balneário Camboriú como CONTEXTO/EXEMPLO,
   nunca como conteúdo temático da questão.
5. Responda EXCLUSIVAMENTE em JSON válido, sem markdown:
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


BLOCOS = {
    "Lingua_Portuguesa": {
        "nome": "🇧🇷 Língua Portuguesa",
        "descricao": "Gramática, ortografia, interpretação e redação oficial",
        "prompt": """
Gere {n} questões de LÍNGUA PORTUGUESA.

⚠️ ATENÇÃO: As questões devem ser sobre GRAMÁTICA, ORTOGRAFIA,
INTERPRETAÇÃO DE TEXTO ou REDAÇÃO OFICIAL. NÃO gere questões sobre
Constituição, Leis, Direito Administrativo, Penal ou qualquer outra matéria.

TÓPICOS PERMITIDOS (escolha apenas estes):
- Ortografia oficial (grafia correta de palavras)
- Acentuação gráfica
- Pontuação (vírgula, ponto e vírgula, dois-pontos)
- Concordância verbal e nominal
- Regência verbal e nominal
- Crase
- Classes de palavras (substantivo, verbo, adjetivo, advérbio, etc.)
- Análise sintática (sujeito, predicado, objeto, adjunto)
- Figuras de linguagem (metáfora, metonímia, pleonasmo, etc.)
- Semântica (sinônimos, antônimos, homônimos, parônimos)
- Compreensão e interpretação de texto (perguntas sobre o que o texto diz)
- Redação oficial (ofícios, memorandos, comunicações)

EXEMPLOS de questões CORRETAS:
1. "Assinale a alternativa em que todas as palavras estão escritas corretamente:"
2. "Qual é o sujeito da oração 'Os guardas chegaram cedo'?"
3. "Em qual alternativa o uso da crase está correto?"
4. "A palavra 'rapidamente' pertence a qual classe gramatical?"

EXEMPLOS de questões PROIBIDAS:
❌ "Qual é o princípio constitucional..."
❌ "Segundo a Lei 3.029/2009..."
❌ "A Guarda Municipal tem como atribuição..."
❌ "Conforme o art. 144 da CF..."

Se usar texto de apoio, ele pode mencionar a Guarda Municipal, mas as
PERGUNTAS devem ser sobre PORTUGUÊS (gramática, interpretação, etc.).

Nível de dificuldade: {dificuldade}.
"""
    },

    "Matematica_Logica": {
        "nome": "🔢 Matemática e Raciocínio Lógico",
        "descricao": "Aritmética, porcentagem, geometria e lógica",
        "prompt": """
Gere {n} questões de MATEMÁTICA E RACIOCÍNIO LÓGICO.

⚠️ ATENÇÃO: NÃO gere questões sobre leis, direito, português ou
qualquer outra matéria. Apenas CÁLCULOS e RACIOCÍNIO LÓGICO.

TÓPICOS PERMITIDOS:
- Operações básicas (soma, subtração, multiplicação, divisão)
- Porcentagem
- Razão e proporção
- Regra de três simples e composta
- MMC e MDC
- Equações de 1º e 2º grau
- Geometria (área, perímetro, volume)
- Interpretação de gráficos e tabelas
- Lógica proposicional (conectivos: E, OU, NÃO, SE...ENTÃO)
- Análise combinatória (princípio da contagem)
- Probabilidade básica

Se contextualizar, use situações como: cálculo de efetivo em escala,
orçamento, horas extras, adicional de periculosidade (30%), distribuição
de viaturas — mas a QUESTÃO deve ser sobre MATEMÁTICA, não sobre a lei.

EXEMPLO CORRETO:
"Um guarda recebe R$ 7.000,00 e tem adicional de 30%. Qual é o valor total?"
(Aqui a matemática é o foco, o contexto é apenas ilustrativo)

EXEMPLO PROIBIDO:
❌ "Segundo a lei municipal, qual é o adicional de periculosidade?"
(Isso é Legislação, não Matemática)

Nível de dificuldade: {dificuldade}.
"""
    },

    "Direito_Penal_Processual": {
        "nome": "⚖️ Direito Penal e Processual Penal",
        "descricao": "Crimes, flagrante, Maria da Penha e leis penais",
        "prompt": """
Gere {n} questões de DIREITO PENAL E PROCESSUAL PENAL.

TÓPICOS PERMITIDOS (apenas estes):
- Aplicação da lei penal (legalidade, anterioridade)
- Conceito de crime, fato típico, ilicitude, culpabilidade
- Crimes contra a pessoa (homicídio, lesão corporal, ameaça)
- Crimes contra a honra (calúnia, difamação, injúria)
- Crimes contra o patrimônio (furto, roubo, extorsão, estelionato)
- Crimes contra a Administração Pública (peculato, concussão, corrupção)
- Prisão em flagrante (art. 301 a 310 do CPP)
- Busca pessoal e domiciliar
- Lei Maria da Penha (Lei 11.340/2006)
- Lei de Abuso de Autoridade (Lei 13.869/2019)
- Estatuto do Desarmamento (Lei 10.826/2003)

⚠️ NÃO gere questões sobre: Constituição em geral, Administração Pública
(princípios, atos), Português, Matemática ou Conhecimentos Gerais.
Foque em CRIMES, PENAS e PROCEDIMENTOS PENAIS.

Nível de dificuldade: {dificuldade}.
"""
    },

    "Legislacao_Guarda_Municipal": {
        "nome": "📜 Legislação da Guarda Municipal",
        "descricao": "Lei 3.029/2009, LC 51/2019 e Estatuto da GMBC",
        "prompt": """
Gere {n} questões sobre a LEGISLAÇÃO ESPECÍFICA DA GUARDA MUNICIPAL DE
BALNEÁRIO CAMBORIÚ (SC).

BASE LEGAL:
- Lei Municipal 3.029/2009 (Estatuto da Guarda Municipal de BC)
- Lei Complementar 51/2019 (estrutura organizacional)
- Lei Federal 13.022/2014 (Estatuto Geral das Guardas Municipais)

TÓPICOS PERMITIDOS:
- Atribuições e competências da Guarda Municipal de BC
- Estrutura organizacional (Comando, Subcomando, Corregedoria, Ouvidoria)
- Ingresso na carreira e requisitos
- Jornada de trabalho (40 horas semanais em escala)
- Porte de arma
- Regime disciplinar e infrações
- Direitos, deveres e vantagens
- Adicional de periculosidade (30%)
- Progressão funcional
- Carreira (Guarda 3ª Classe, 2ª Classe, 1ª Classe, Inspetor)
- Integração com outras forças de segurança

⚠️ Foque APENAS na legislação da Guarda Municipal. NÃO gere questões
genéricas de Direito Constitucional ou Administrativo.

Nível de dificuldade: {dificuldade}.
"""
    },

    "Direito_Constitucional_Administrativo": {
        "nome": "🏛️ Direito Constitucional e Administrativo",
        "descricao": "CF/88, princípios e segurança pública",
        "prompt": """
Gere {n} questões de DIREITO CONSTITUCIONAL E ADMINISTRATIVO.

TÓPICOS PERMITIDOS:
- Princípios fundamentais (art. 1º a 4º da CF/88)
- Direitos e garantias individuais (art. 5º da CF/88)
- Organização do Estado e dos Municípios
- Administração Pública: LIMPE (Legalidade, Impessoalidade, Moralidade,
  Publicidade, Eficiência)
- Poderes administrativos
- Atos administrativos
- Responsabilidade civil do Estado
- Segurança Pública (art. 144 da CF/88)
- Improbidade administrativa (Lei 8.429/1992)

⚠️ NÃO gere questões sobre: crimes específicos, penas, ECA, CTB,
Legislação da Guarda Municipal, Português ou Matemática.

Nível de dificuldade: {dificuldade}.
"""
    },

    "Conhecimentos_Balneario_Camboriu": {
        "nome": "🌴 Conhecimentos de Balneário Camboriú",
        "descricao": "História, geografia, economia e turismo de BC",
        "prompt": """
Gere {n} questões sobre o MUNICÍPIO DE BALNEÁRIO CAMBORIÚ (SC).

DADOS CONCRETOS:
- Emancipação: 20/07/1964 (desmembrado de Camboriú)
- Área: ~46,8 km² (segunda menor de SC)
- População: ~139.155 habitantes (Censo 2022)
- Economia: turismo, construção civil
- Pontos turísticos: Cristo Luz, Parque Unipraias, Praia Central,
  Avenida Atlântica, Barra Sul, Praia de Laranjeiras, Praia do Estaleiro
- Rio Camboriú
- Apelido: "Dubai Brasileira"
- Distância de Florianópolis: ~80 km
- Municípios limítrofes: Camboriú, Itajaí, Itapema
- BR-101: eixo de desenvolvimento

TÓPICOS PERMITIDOS:
- História e emancipação de BC
- Geografia (localização, área, rio, praias)
- População e demografia
- Economia e turismo
- Pontos turísticos e cultura
- Lei Orgânica do Município
- Legislação municipal relevante

⚠️ NÃO gere questões sobre: direito penal, português, matemática
ou outras matérias.

Nível de dificuldade: {dificuldade}.
"""
    },

    "Legislacoes_Especiais": {
        "nome": "📋 Legislações Especiais",
        "descricao": "ECA, Estatuto do Idoso, CTB, Desarmamento",
        "prompt": """
Gere {n} questões sobre LEGISLAÇÕES ESPECIAIS.

TÓPICOS PERMITIDOS:
- Estatuto da Criança e do Adolescente (Lei 8.069/1990)
- Estatuto da Pessoa Idosa (Lei 10.741/2003)
- Código de Trânsito Brasileiro (Lei 9.503/1997)
- Estatuto do Desarmamento (Lei 10.826/2003)
- Lei Maria da Penha (Lei 11.340/2006)
- Lei de Abuso de Autoridade (Lei 13.869/2019)
- Estatuto Geral das Guardas Municipais (Lei 13.022/2014)

⚠️ NÃO gere questões genéricas de Direito Penal, Constitucional ou
Português. Foque nas LEIS ESPECIAIS acima.

Nível de dificuldade: {dificuldade}.
"""
    },

    "Conhecimentos_Gerais_Atualidades": {
        "nome": "🧠 Conhecimentos Gerais e Atualidades",
        "descricao": "Segurança pública, cidadania e temas gerais",
        "prompt": """
Gere {n} questões de CONHECIMENTOS GERAIS sobre temas ATEMPORAIS
(que não mudam com o tempo).

⚠️ IMPORTANTE: NÃO gere questões sobre notícias recentes, eventos do ano
atual ou fatos que exigem conhecimento de data específica. Foque em
conceitos que permanecem válidos independentemente do ano.

TÓPICOS PERMITIDOS (escolha apenas estes):
- Conceito de cidadania e direitos do cidadão
- Direitos humanos fundamentais (conceito geral)
- Noções básicas de segurança pública (o que é, para que serve)
- Sistema Único de Segurança Pública (SUSP) — conceito e finalidade
- SENASP — o que é e o que faz
- Noções básicas de informática (hardware, software, internet, e-mail)
- Ética no serviço público (conceito)
- Meio ambiente e sustentabilidade (conceito geral)
- Geografia geral do Brasil (regiões, estados, capitais)
- História geral do Brasil (períodos: colônia, império, república)
- Geografia e história de Santa Catarina (colonização, cidades principais)

EXEMPLOS CORRETOS:
1. "O que é cidadania?"
2. "Qual é a função principal do Sistema Único de Segurança Pública (SUSP)?"
3. "Quantas regiões tem o Brasil?"
4. "Em que período histórico o Brasil foi colônia de Portugal?"
5. "O que significa o princípio da ética no serviço público?"

EXEMPLOS PROIBIDOS:
❌ "Qual foi a notícia mais importante de 2026?"
❌ "Quem é o atual prefeito de..."
❌ "Qual evento ocorreu no mês passado?"
❌ Qualquer questão que dependa de saber o ano atual.

Nível de dificuldade: {dificuldade}.
"""
    },
}
