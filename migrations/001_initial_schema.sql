CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    ciclo_atual INT DEFAULT 1 CHECK (ciclo_atual IN (1, 2)),
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    atualizado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.questoes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    disciplina TEXT NOT NULL CHECK (
        disciplina IN (
            'Lingua_Portuguesa',
            'Matematica',
            'Legislacao_Guarda_Municipal',
            'Conhecimentos_Balneario_Camboriu'
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

CREATE INDEX IF NOT EXISTS idx_respostas_usuario ON public.respostas(usuario_id);
CREATE INDEX IF NOT EXISTS idx_respostas_disciplina ON public.respostas(disciplina);
CREATE INDEX IF NOT EXISTS idx_questoes_disciplina ON public.questoes(disciplina);
CREATE INDEX IF NOT EXISTS idx_questoes_hash ON public.questoes(hash_conteudo);

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.respostas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.questoes ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Perfil proprio" ON public.profiles;
CREATE POLICY "Perfil proprio" ON public.profiles FOR ALL USING (auth.uid() = id);

DROP POLICY IF EXISTS "Respostas proprias" ON public.respostas;
CREATE POLICY "Respostas proprias" ON public.respostas FOR ALL USING (auth.uid() = usuario_id);

DROP POLICY IF EXISTS "Questoes leitura" ON public.questoes;
CREATE POLICY "Questoes leitura" ON public.questoes FOR SELECT TO authenticated USING (true);

DROP POLICY IF EXISTS "Questoes insercao" ON public.questoes;
CREATE POLICY "Questoes insercao" ON public.questoes FOR INSERT TO authenticated WITH CHECK (true);

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

CREATE OR REPLACE FUNCTION public.estatisticas_disciplina(p_usuario_id UUID)
RETURNS TABLE (disciplina TEXT, total BIGINT, acertos BIGINT)
LANGUAGE sql
SECURITY DEFINER
AS $$
    SELECT r.disciplina, COUNT(*) AS total,
           COUNT(*) FILTER (WHERE r.acertou) AS acertos
    FROM public.respostas r
    WHERE r.usuario_id = p_usuario_id
    GROUP BY r.disciplina
    ORDER BY r.disciplina;
$$;
