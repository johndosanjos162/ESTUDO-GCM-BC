-- =========================================================
-- SCHEMA COMPLETO — Estudos GMBC
-- Versão: 2.0 (atualizada com 8 blocos de estudo)
-- Rodar no SQL Editor do Supabase
-- =========================================================

-- ---------------------------------------------------------
-- 1. EXTENSÃO PARA UUID
-- ---------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ---------------------------------------------------------
-- 2. TABELA: profiles (perfis de usuários)
-- Complementa a tabela auth.users do Supabase
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    ciclo_atual INT DEFAULT 1 CHECK (ciclo_atual IN (1, 2)),
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    atualizado_em TIMESTAMPTZ DEFAULT NOW()
);

-- ---------------------------------------------------------
-- 3. TABELA: questoes (repositório gerado pela IA)
-- Aceita os 8 blocos de estudo
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.questoes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    disciplina TEXT NOT NULL CHECK (
        disciplina IN (
            'Lingua_Portuguesa',
            'Matematica_Logica',
            'Direito_Penal_Processual',
            'Legislacao_Guarda_Municipal',
            'Direito_Constitucional_Administrativo',
            'Conhecimentos_Balneario_Camboriu',
            'Legislacoes_Especiais',
            'Conhecimentos_Gerais_Atualidades'
        )
    ),
    enunciado TEXT NOT NULL,
    alternativas JSONB NOT NULL,
    resposta_correta CHAR(1) NOT NULL CHECK (resposta_correta IN ('A','B','C','D','E')),
    explicacao TEXT,
    dificuldade TEXT CHECK (dificuldade IN ('facil','medio','dificil')),
    fonte TEXT DEFAULT 'IA',
    hash_conteudo TEXT UNIQUE,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- ---------------------------------------------------------
-- 4. TABELA: respostas (histórico do usuário)
-- A coluna "acertou" é calculada automaticamente
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.respostas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    usuario_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    questao_id UUID REFERENCES public.questoes(id) ON DELETE SET NULL,
    disciplina TEXT NOT NULL,
    resposta_usuario CHAR(1) NOT NULL,
    resposta_correta CHAR(1) NOT NULL,
    acertou BOOLEAN GENERATED ALWAYS AS (resposta_usuario = resposta_correta) STORED,
    tempo_segundos INT,
    respondido_em TIMESTAMPTZ DEFAULT NOW()
);

-- ---------------------------------------------------------
-- 5. ÍNDICES (performance)
-- ---------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_respostas_usuario ON public.respostas(usuario_id);
CREATE INDEX IF NOT EXISTS idx_respostas_disciplina ON public.respostas(disciplina);
CREATE INDEX IF NOT EXISTS idx_questoes_disciplina ON public.questoes(disciplina);
CREATE INDEX IF NOT EXISTS idx_questoes_hash ON public.questoes(hash_conteudo);

-- ---------------------------------------------------------
-- 6. ATUALIZAR CONSTRAINT (caso a tabela já exista)
-- Remove a constraint antiga e cria a nova com 8 blocos
-- ---------------------------------------------------------
ALTER TABLE public.questoes
    DROP CONSTRAINT IF EXISTS questoes_disciplina_check;

ALTER TABLE public.questoes
    ADD CONSTRAINT questoes_disciplina_check
    CHECK (
        disciplina IN (
            'Lingua_Portuguesa',
            'Matematica_Logica',
            'Direito_Penal_Processual',
            'Legislacao_Guarda_Municipal',
            'Direito_Constitucional_Administrativo',
            'Conhecimentos_Balneario_Camboriu',
            'Legislacoes_Especiais',
            'Conhecimentos_Gerais_Atualidades'
        )
    );

-- ---------------------------------------------------------
-- 7. ROW LEVEL SECURITY (segurança por usuário)
-- ---------------------------------------------------------
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.respostas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.questoes ENABLE ROW LEVEL SECURITY;

-- ---------------------------------------------------------
-- 8. POLÍTICAS RLS
-- ---------------------------------------------------------

-- Profiles: cada usuário vê/edita só o próprio perfil
DROP POLICY IF EXISTS "Perfil proprio" ON public.profiles;
CREATE POLICY "Perfil proprio" ON public.profiles
    FOR ALL USING (auth.uid() = id);

-- Respostas: cada usuário vê/insere só as próprias respostas
DROP POLICY IF EXISTS "Respostas proprias" ON public.respostas;
CREATE POLICY "Respostas proprias" ON public.respostas
    FOR ALL USING (auth.uid() = usuario_id);

-- Questões: leitura para usuários autenticados
DROP POLICY IF EXISTS "Questoes leitura" ON public.questoes;
CREATE POLICY "Questoes leitura" ON public.questoes
    FOR SELECT TO authenticated USING (true);

-- Questões: inserção para usuários autenticados (IA gera)
DROP POLICY IF EXISTS "Questoes insercao" ON public.questoes;
CREATE POLICY "Questoes insercao" ON public.questoes
    FOR INSERT TO authenticated WITH CHECK (true);

-- ---------------------------------------------------------
-- 9. TRIGGER: atualizar "atualizado_em" automaticamente
-- ---------------------------------------------------------
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_profiles_updated ON public.profiles;
CREATE TRIGGER trg_profiles_updated
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

-- ---------------------------------------------------------
-- 10. FUNÇÃO RPC: estatísticas por disciplina
-- Usada pelo dashboard para calcular acertos
-- ---------------------------------------------------------
CREATE OR REPLACE FUNCTION public.estatisticas_disciplina(
    p_usuario_id UUID
)
RETURNS TABLE (
    disciplina TEXT,
    total BIGINT,
    acertos BIGINT
)
LANGUAGE sql
SECURITY DEFINER
AS $$
    SELECT
        r.disciplina,
        COUNT(*) AS total,
        COUNT(*) FILTER (WHERE r.acertou) AS acertos
    FROM public.respostas r
    WHERE r.usuario_id = p_usuario_id
    GROUP BY r.disciplina
    ORDER BY r.disciplina;
$$;

-- ---------------------------------------------------------
-- 11. TRIGGER: criar profile automaticamente
-- quando um novo usuário se cadastrar via Supabase Auth
-- ---------------------------------------------------------
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, nome, email, ciclo_atual)
    VALUES (
        NEW.id,
        COALESCE(NEW.raw_user_meta_data->>'nome', 'Usuário'),
        NEW.email,
        1
    )
    ON CONFLICT (id) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- =========================================================
-- FIM — Schema v2.0 criado com sucesso
-- =========================================================
