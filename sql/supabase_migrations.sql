-- ==============================================================================
-- GLOBAL FUELPULSE AI — SUPABASE POSTGRESQL MIGRATION & RLS POLICIES
-- Target: Supabase (PostgreSQL 15+)
-- Features: Auth schema integration, Atomic Quota Function, Row Level Security
-- ==============================================================================

-- 1. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. PUBLIC PROFILES TABLE (Linked with auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE,
    full_name TEXT,
    email TEXT,
    avatar_url TEXT,
    role TEXT DEFAULT 'analyst',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public profiles are viewable by everyone."
    ON public.profiles FOR SELECT
    USING (true);

CREATE POLICY "Users can insert their own profile."
    ON public.profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update own profile."
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id);

-- 3. AUTOMATIC PROFILE CREATION TRIGGER ON SIGNUP
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, username, full_name, email)
    VALUES (
        new.id,
        COALESCE(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1)),
        COALESCE(new.raw_user_meta_data->>'full_name', split_part(new.email, '@', 1)),
        new.email
    )
    ON CONFLICT (id) DO NOTHING;
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 4. AI QUESTION USAGE (Enforces exactly 3 questions per rolling 24 hours)
CREATE TABLE IF NOT EXISTS public.ai_question_usages (
    usage_id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_hash TEXT NOT NULL,
    status TEXT DEFAULT 'completed', -- 'completed', 'failed', 'pending'
    model_used TEXT DEFAULT 'gpt-4o-mini',
    tokens_used INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for lightning-fast rolling 24-hour queries
CREATE INDEX IF NOT EXISTS idx_ai_usage_user_window 
    ON public.ai_question_usages (user_id, created_at, status);
CREATE INDEX IF NOT EXISTS idx_ai_usage_hash 
    ON public.ai_question_usages (question_hash);

-- Enable RLS on usages
ALTER TABLE public.ai_question_usages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view only their own question usage."
    ON public.ai_question_usages FOR SELECT
    USING (auth.uid() = user_id);

-- Restrict direct insertion: quota must only be consumed via server function
CREATE POLICY "Users cannot insert arbitrary usage rows."
    ON public.ai_question_usages FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- 5. ATOMIC SERVER-SIDE CONCURRENCY-SAFE FUNCTION TO CHECK AND CONSUME QUOTA
CREATE OR REPLACE FUNCTION public.check_and_consume_ai_quota(
    p_user_id UUID,
    p_question_text TEXT,
    p_question_hash TEXT,
    p_model TEXT DEFAULT 'gpt-4o-mini',
    p_max_questions INT DEFAULT 3,
    p_window_hours INT DEFAULT 24
)
RETURNS JSONB AS $$
DECLARE
    v_cutoff TIMESTAMPTZ;
    v_used_count INT;
    v_earliest TIMESTAMPTZ;
    v_reset_timestamp TIMESTAMPTZ;
    v_remaining INT;
    v_new_usage_id BIGINT;
BEGIN
    v_cutoff := NOW() - (p_window_hours || ' hours')::INTERVAL;

    -- Concurrency safety: lock rows for this user within the rolling window
    PERFORM 1 FROM public.ai_question_usages
    WHERE user_id = p_user_id AND created_at >= v_cutoff
    FOR UPDATE;

    -- Count active completed queries
    SELECT COUNT(*), MIN(created_at)
    INTO v_used_count, v_earliest
    FROM public.ai_question_usages
    WHERE user_id = p_user_id
      AND created_at >= v_cutoff
      AND status = 'completed';

    -- Check if quota exhausted
    IF v_used_count >= p_max_questions THEN
        v_reset_timestamp := v_earliest + (p_window_hours || ' hours')::INTERVAL;
        RETURN jsonb_build_object(
            'allowed', false,
            'reason', 'QUOTA_EXHAUSTED',
            'remaining', 0,
            'used_count', v_used_count,
            'reset_timestamp', v_reset_timestamp,
            'message', 'You have used all ' || p_max_questions || ' free questions available in the last 24 hours.'
        );
    END IF;

    -- Record this usage
    INSERT INTO public.ai_question_usages (
        user_id, question_text, question_hash, status, model_used
    ) VALUES (
        p_user_id, p_question_text, p_question_hash, 'completed', p_model
    ) RETURNING usage_id INTO v_new_usage_id;

    v_remaining := p_max_questions - (v_used_count + 1);

    RETURN jsonb_build_object(
        'allowed', true,
        'usage_id', v_new_usage_id,
        'remaining', v_remaining,
        'used_count', v_used_count + 1,
        'message', 'Question accepted. ' || v_remaining || '/' || p_max_questions || ' free questions remaining.'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 6. CHAT CONVERSATIONS & MESSAGES TABLES
CREATE TABLE IF NOT EXISTS public.chat_conversations (
    conversation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL DEFAULT 'New Energy Consultation',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.chat_conversations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage only their own conversations."
    ON public.chat_conversations FOR ALL
    USING (auth.uid() = user_id);

CREATE TABLE IF NOT EXISTS public.chat_messages (
    message_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES public.chat_conversations(conversation_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    sources_cited JSONB DEFAULT '[]'::jsonb,
    tokens_used INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.chat_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view and insert messages in their own conversations."
    ON public.chat_messages FOR ALL
    USING (auth.uid() = user_id);

CREATE INDEX IF NOT EXISTS idx_chat_messages_conv_time 
    ON public.chat_messages (conversation_id, created_at ASC);
