"""Prompts especializados por bloco — foco EXCLUSIVO no concurso da GMBC."""

SYSTEM_PROMPT = """Você é um gerador especializado de questões para o concurso
da GUARDA MUNICIPAL DE BALNEÁRIO CAMBORIÚ (SC).

CONTEXTO DO CONCURSO (use sempre que aplicável):
- Vagas: 90 novas vagas (quadro passando de 200 para 290)
- Remuneração inicial: R$ 7.000,00 (podendo chegar a R$ 15.000,00 com progressão)
- Escolaridade: Ensino Médio completo
- CNH: Categoria AB obrigatória
- Idade: 18 a 35 anos incompletos até o fim das inscrições
- Altura mínima: 1,65m
- Curso de Formação: mínimo 800 horas-aula (Matriz SENASP)
- Efetivo atual: 165 guardas em atuação

REGRAS OBRIGATÓRIAS:
1. Gere questões INÉDITAS de múltipla escolha (A a E).
2. Cada questão deve ter 5 alternativas e apenas 1 correta.
3. Foque EXCLUSIVAMENTE em conteúdos exigidos no edital da GMBC.
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


BLOCOS = {
    "Lingua_Portuguesa": {
        "nome": "🇧🇷 Língua Portuguesa",
        "descricao": "Interpretação, gramática e redação oficial com textos de segurança pública",
        "prompt": """
Gere {n} questões de LÍNGUA PORTUGUESA para o concurso da Guarda Municipal
de Balneário Camboriú (SC).

CONTEXTO OBRIGATÓRIO:
- Os textos de interpretação devem abordar: segurança pública municipal,
  cidadania, o município de Balneário Camboriú, atribuições da Guarda Municipal,
  direitos humanos ou legislação municipal.
- As questões de gramática devem contextualizar situações do dia a dia
  da corporação (ex: redação de ofícios, comunicações internas, relatórios).

TÓPICOS:
- Compreensão e interpretação de texto
- Ortografia oficial
- Pontuação e acentuação gráfica
- Concordância verbal e nominal
- Regência verbal e nominal
- Crase
- Classes de palavras e análise sintática
- Semântica (sinônimos, antônimos, homônimos, parônimos)
- Redação oficial (ofícios, requerimentos, comunicações internas)

Nível de dificuldade: {dificuldade}.
"""
    },

    "Matematica_Logica": {
        "nome": "🔢 Matemática e Raciocínio Lógico",
        "descricao": "Aritmética e lógica aplicadas a segurança pública municipal",
        "prompt": """
Gere {n} questões de MATEMÁTICA E RACIOCÍNIO LÓGICO para o concurso da
Guarda Municipal de Balneário Camboriú (SC).

CONTEXTO OBRIGATÓRIO:
- Contextualize TODAS as questões com situações reais da corporação:
  * Cálculo de efetivo em escala de serviço (ex: 165 guardas, escalas 12x36)
  * Distribuição de viaturas por região do município
  * Orçamento da Secretaria de Segurança
  * Estatísticas de ocorrências atendidas
  * Dimensionamento de rondas ostensivas
  * Cálculo de adicional de periculosidade (30%)

TÓPICOS:
- Operações com números inteiros, fracionários e decimais
- Porcentagem, razão e proporção
- Regra de três simples e composta
- MMC e MDC
- Equações de 1º e 2º grau
- Geometria básica (área, perímetro, volume)
- Interpretação de gráficos e tabelas
- Lógica proposicional
- Análise combinatória
- Probabilidade básica

Nível de dificuldade: {dificuldade}.
"""
    },

    "Direito_Penal_Processual": {
        "nome": "⚖️ Direito Penal e Processual Penal",
        "descricao": "Foco na atuação real da GMBC: flagrante, uso da força e leis especiais",
        "prompt": """
Gere {n} questões de DIREITO PENAL E PROCESSUAL PENAL para o concurso da
Guarda Municipal de Balneário Camboriú (SC).

CONTEXTO OBRIGATÓRIO:
- Foque na atuação PRÁTICA da Guarda Municipal: o que o guarda PODE e
  NÃO PODE fazer no exercício da função.
- Contextualize com situações reais de Balneário Camboriú:
  * Abordagem em Praia Central, Avenida Atlântica, Cristo Luz
  * Ocorrências envolvendo turistas
  * Atuação integrada com Polícia Militar e Civil
  * Patrulha Maria da Penha (Lei Municipal 4.245/2019)

TÓPICOS:
- Aplicação da lei penal (legalidade, anterioridade)
- Crime, fato típico, ilicitude e culpabilidade
- Crimes contra a pessoa, honra e patrimônio
- Crimes contra a Administração Pública
- Prisão em flagrante: tipos e procedimentos
- Busca pessoal e domiciliar
- Lei Maria da Penha (Lei 11.340/2006)
- Lei de Abuso de Autoridade (Lei 13.869/2019)
- Estatuto do Desarmamento (Lei 10.826/2003)
- Patrulha Maria da Penha e Aplicativo Alerta Mulher

Nível de dificuldade: {dificuldade}.
"""
    },

    "Legislacao_Guarda_Municipal": {
        "nome": "📜 Legislação da Guarda Municipal",
        "descricao": "Lei 3.029/2009, LC 51/2019 e Estatuto da GMBC",
        "prompt": """
Gere {n} questões sobre a LEGISLAÇÃO ESPECÍFICA DA GUARDA MUNICIPAL DE
BALNEÁRIO CAMBORIÚ (SC).

BASE LEGAL OBRIGATÓRIA:
- Lei Municipal 3.029/2009 (Estatuto da Guarda Municipal de BC)
- Lei Complementar 51/2019 (alterações na estrutura)
- Lei Federal 13.022/2014 (Estatuto Geral das Guardas Municipais)
- Constituição Federal, art. 144, § 8º

DADOS CONCRETOS DO CONCURSO (use nas questões):
- Requisitos: Ensino Médio, CNH AB, 18 a 35 anos, altura mínima 1,65m
- Jornada: até 40 horas semanais em escala
- Estrutura: Comando, Subcomando, Corregedoria, Ouvidoria
- Carreira: Guarda 3ª Classe → 2ª Classe → 1ª Classe → Inspetor
- Adicional de periculosidade: 30%
- Supervisão: Guarda de 3ª, 2ª ou 1ª classe (gratificação de 40%)
- Corregedor: cargo de livre nomeação e exoneração
- Ouvidor: controle externo, servidor efetivo

TÓPICOS:
- Atribuições e competências da GMBC
- Estrutura organizacional
- Ingresso na carreira (concurso, requisitos)
- Jornada de trabalho (40h em escala)
- Porte de arma e uso diferenciado da força
- Regime disciplinar e infrações
- Direitos, deveres e vantagens
- Progressão funcional
- Integração com outras forças de segurança

Nível de dificuldade: {dificuldade}.
"""
    },

    "Direito_Constitucional_Administrativo": {
        "nome": "🏛️ Direito Constitucional e Administrativo",
        "descricao": "CF/88 e princípios aplicados à segurança pública municipal",
        "prompt": """
Gere {n} questões de DIREITO CONSTITUCIONAL E ADMINISTRATIVO para o
concurso da Guarda Municipal de Balneário Camboriú (SC).

CONTEXTO OBRIGATÓRIO:
- Contextualize com a atuação da Guarda Municipal de Balneário Camboriú
- Foque no art. 144, § 8º da CF/88 (segurança pública municipal)
- Aborde a competência do Município para criar Guarda Municipal
- Relacione com a Lei Orgânica do Município de Balneário Camboriú

TÓPICOS:
- Princípios fundamentais da República (art. 1º a 4º)
- Direitos e garantias individuais (art. 5º)
- Organização do Estado e dos Municípios
- Administração Pública: princípios (LIMPE)
- Poderes administrativos (hierárquico, disciplinar, regulamentar, de polícia)
- Atos administrativos
- Responsabilidade civil do Estado
- Segurança Pública (art. 144 da CF/88)
- Competências dos Municípios em segurança pública
- Improbidade administrativa (Lei 8.429/1992)

Nível de dificuldade: {dificuldade}.
"""
    },

    "Conhecimentos_Balneario_Camboriu": {
        "nome": "🌴 Conhecimentos de Balneário Camboriú",
        "descricao": "História, geografia, economia e legislação municipal",
        "prompt": """
Gere {n} questões sobre o MUNICÍPIO DE BALNEÁRIO CAMBORIÚ (SC) para o
concurso da Guarda Municipal.

DADOS OBRIGATÓRIOS PARA CONTEXTUALIZAÇÃO:
- Emancipação: 20/07/1964 (desmembrado de Camboriú)
- Área: ~46,8 km² (segunda menor de SC em extensão)
- População: ~139.155 habitantes (Censo 2022)
- Densidade demográfica: ~2.337 hab/km² (uma das maiores de SC)
- Economia: turismo (99,21% no setor terciário), construção civil
- Pontos turísticos: Cristo Luz, Parque Unipraias, Praia Central,
  Avenida Atlântica, Barra Sul, Praia de Laranjeiras, Praia do Estaleiro
- Rio Camboriú
- Apelido: "Dubai Brasileira" (verticalização e arranha-céus)
- Distância de Florianópolis: ~80 km
- Municípios limítrofes: Camboriú, Itajaí, Itapema
- BR-101: importante eixo de desenvolvimento

TÓPICOS:
- História e emancipação
- Geografia e localização
- População e demografia
- Economia e turismo
- Pontos turísticos
- Cultura e eventos
- Lei Orgânica do Município
- Legislação municipal relevante para segurança pública
- Plano Estratégico de Segurança Pública de BC

Nível de dificuldade: {dificuldade}.
"""
    },

    "Legislacoes_Especiais": {
        "nome": "📋 Legislações Especiais",
        "descricao": "ECA, Estatuto do Idoso, CTB, Desarmamento e Maria da Penha",
        "prompt": """
Gere {n} questões sobre LEGISLAÇÕES ESPECIAIS para o concurso da Guarda
Municipal de Balneário Camboriú (SC).

CONTEXTO OBRIGATÓRIO:
- Foque na aplicação PRÁTICA pela Guarda Municipal
- Contextualize com situações de Balneário Camboriú:
  * Fiscalização de trânsito na Avenida Atlântica e Praia Central
  * Proteção de crianças e adolescentes no turismo
  * Atendimento a idosos em situação de vulnerabilidade
  * Patrulha Maria da Penha (Lei Municipal 4.245/2019)
  * Porte de arma pela Guarda Municipal

TÓPICOS:
- Estatuto da Criança e do Adolescente (Lei 8.069/1990)
- Estatuto da Pessoa Idosa (Lei 10.741/2003)
- Código de Trânsito Brasileiro (Lei 9.503/1997)
- Estatuto do Desarmamento (Lei 10.826/2003)
- Lei Maria da Penha (Lei 11.340/2006)
- Lei de Abuso de Autoridade (Lei 13.869/2019)
- Estatuto Geral das Guardas Municipais (Lei 13.022/2014)
- Lei Municipal 4.245/2019 (Patrulha Maria da Penha)

Nível de dificuldade: {dificuldade}.
"""
    },

    "Conhecimentos_Gerais_Atualidades": {
        "nome": "🧠 Conhecimentos Gerais e Atualidades",
        "descricao": "Segurança pública, cidadania e realidade de Balneário Camboriú",
        "prompt": """
Gere {n} questões de CONHECIMENTOS GERAIS E ATUALIDADES para o concurso da
Guarda Municipal de Balneário Camboriú (SC).

CONTEXTO OBRIGATÓRIO:
- Priorize atualidades de Balneário Camboriú e Santa Catarina
- Aborde o Sistema Único de Segurança Pública (SUSP)
- Contextualize com a realidade de segurança pública municipal
- Inclua temas como turismo, verticalização e desafios urbanos de BC
- Foque em direitos humanos e cidadania aplicados à segurança pública

TÓPICOS:
- Segurança pública no Brasil (políticas, SUSP, SENASP)
- Direitos humanos e cidadania
- Sistema Único de Segurança Pública (SUSP)
- Atualidades de segurança pública (últimos 2 anos)
- Meio ambiente e sustentabilidade
- Noções de informática básica
- Ética no serviço público
- Geografia e história de Santa Catarina
- Atualidades de Balneário Camboriú e região

Nível de dificuldade: {dificuldade}.
"""
    },
}
