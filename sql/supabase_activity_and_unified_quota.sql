-- ==============================================================================
-- GLOBAL FUELPULSE AI — SUPABASE ACTIVITY TRACKING & UNIFIED QUOTA SYSTEM
-- Target: Supabase PostgreSQL 15+
-- Features:
--   1. Profile enhancement (last_login_at)
--   2. Audit login history table (user_login_history) with RLS
--   3. AI question usage enhancements (request_id, quota_unit_consumed, response_metadata)
--   4. Concurrency-safe atomic quota enforcement & idempotent retry protection
--   5. Server-side quota summary RPC (get_user_quota_summary)
--   6. Login activity tracking RPC (record_user_login)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. PROFILES ENHANCEMENT
-- ------------------------------------------------------------------------------
ALTER TABLE IF EXISTS public.profiles 
    ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMPTZ;

-- ------------------------------------------------------------------------------
-- 2. USER LOGIN HISTORY (AUDIT TRAIL)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.user_login_history (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    login_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_type TEXT NOT NULL DEFAULT 'login', -- 'login', 'logout', 'failed_attempt'
    result TEXT NOT NULL DEFAULT 'success',   -- 'success', 'failed'
    session_id TEXT,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_login_history_user_time 
    ON public.user_login_history (user_id, login_timestamp DESC);

ALTER TABLE public.user_login_history ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view only their own login history" ON public.user_login_history;
CREATE POLICY "Users can view only their own login history"
    ON public.user_login_history FOR SELECT
    TO authenticated
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Service role can insert login history" ON public.user_login_history;
CREATE POLICY "Service role can insert login history"
    ON public.user_login_history FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS "Authenticated users can insert own login events" ON public.user_login_history;
CREATE POLICY "Authenticated users can insert own login events"
    ON public.user_login_history FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

-- ------------------------------------------------------------------------------
-- 3. AI QUESTION USAGES ENHANCEMENTS
-- ------------------------------------------------------------------------------
ALTER TABLE IF EXISTS public.ai_question_usages
    ADD COLUMN IF NOT EXISTS request_id TEXT,
    ADD COLUMN IF NOT EXISTS quota_unit_consumed BOOLEAN DEFAULT true,
    ADD COLUMN IF NOT EXISTS response_metadata JSONB DEFAULT '{}'::jsonb;

CREATE INDEX IF NOT EXISTS idx_ai_usage_request_id 
    ON public.ai_question_usages (request_id)
    WHERE request_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_ai_usage_user_status_quota
    ON public.ai_question_usages (user_id, created_at DESC)
    WHERE quota_unit_consumed = true AND status = 'completed';

-- ------------------------------------------------------------------------------
-- 4. RPC: RECORD USER LOGIN & UPDATE LAST LOGIN
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.record_user_login(
    p_user_id UUID,
    p_event_type TEXT DEFAULT 'login',
    p_result TEXT DEFAULT 'success',
    p_session_id TEXT DEFAULT NULL,
    p_ip_address TEXT DEFAULT NULL,
    p_user_agent TEXT DEFAULT NULL
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, auth, pg_temp
AS $$
DECLARE
    v_history_id BIGINT;
BEGIN
    -- Verify caller permission
    IF auth.uid() IS NOT NULL AND auth.uid() != p_user_id THEN
        RAISE EXCEPTION 'Access Denied: You cannot record login events for other users.';
    END IF;

    -- Record login entry
    INSERT INTO public.user_login_history (
        user_id, event_type, result, session_id, ip_address, user_agent, login_timestamp
    ) VALUES (
        p_user_id, p_event_type, p_result, p_session_id, p_ip_address, p_user_agent, NOW()
    ) RETURNING id INTO v_history_id;

    -- If successful login, update profile last_login_at
    IF p_result = 'success' AND p_event_type = 'login' THEN
        UPDATE public.profiles
        SET last_login_at = NOW(),
            updated_at = NOW()
        WHERE id = p_user_id;
    END IF;

    RETURN jsonb_build_object(
        'success', true,
        'history_id', v_history_id,
        'recorded_at', NOW()
    );
END;
$$;

REVOKE EXECUTE ON FUNCTION public.record_user_login(UUID, TEXT, TEXT, TEXT, TEXT, TEXT) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION public.record_user_login(UUID, TEXT, TEXT, TEXT, TEXT, TEXT) FROM anon;
GRANT EXECUTE ON FUNCTION public.record_user_login(UUID, TEXT, TEXT, TEXT, TEXT, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.record_user_login(UUID, TEXT, TEXT, TEXT, TEXT, TEXT) TO service_role;

-- ------------------------------------------------------------------------------
-- 5. RPC: GET USER QUOTA SUMMARY (SINGLE AUTHORITATIVE SERVER CALCULATION)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_user_quota_summary(
    p_user_id UUID,
    p_max_questions INT DEFAULT 3,
    p_window_hours INT DEFAULT 24
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
DECLARE
    v_cutoff TIMESTAMPTZ;
    v_used_count INT;
    v_total_historical INT;
    v_earliest TIMESTAMPTZ;
    v_reset_timestamp TIMESTAMPTZ;
    v_remaining INT;
    v_last_login TIMESTAMPTZ;
BEGIN
    v_cutoff := NOW() - (p_window_hours || ' hours')::INTERVAL;

    -- Count active completed queries within rolling window that consumed quota
    SELECT COUNT(*), MIN(created_at)
    INTO v_used_count, v_earliest
    FROM public.ai_question_usages
    WHERE user_id = p_user_id
      AND created_at >= v_cutoff
      AND status = 'completed'
      AND quota_unit_consumed = true;

    -- Lifetime historical queries count
    SELECT COUNT(*)
    INTO v_total_historical
    FROM public.ai_question_usages
    WHERE user_id = p_user_id;

    -- Fetch user last login
    SELECT last_login_at
    INTO v_last_login
    FROM public.profiles
    WHERE id = p_user_id;

    v_remaining := GREATEST(0, p_max_questions - v_used_count);

    IF v_earliest IS NOT NULL THEN
        v_reset_timestamp := v_earliest + (p_window_hours || ' hours')::INTERVAL;
    ELSE
        v_reset_timestamp := NULL;
    END IF;

    RETURN jsonb_build_object(
        'user_id', p_user_id,
        'used', v_used_count,
        'limit', p_max_questions,
        'remaining', v_remaining,
        'window_hours', p_window_hours,
        'window_started_at', v_earliest,
        'resets_at', v_reset_timestamp,
        'quota_exhausted', (v_used_count >= p_max_questions),
        'total_historical', v_total_historical,
        'last_login_at', v_last_login
    );
END;
$$;

REVOKE EXECUTE ON FUNCTION public.get_user_quota_summary(UUID, INT, INT) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION public.get_user_quota_summary(UUID, INT, INT) FROM anon;
GRANT EXECUTE ON FUNCTION public.get_user_quota_summary(UUID, INT, INT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_user_quota_summary(UUID, INT, INT) TO service_role;

-- ------------------------------------------------------------------------------
-- 6. RPC: ATOMIC CHECK AND CONSUME AI QUOTA (WITH IDEMPOTENCY & LOCKING)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.check_and_consume_ai_quota(
    p_user_id UUID,
    p_question_text TEXT,
    p_question_hash TEXT,
    p_request_id TEXT DEFAULT NULL,
    p_model TEXT DEFAULT 'gemini-2.0-flash',
    p_max_questions INT DEFAULT 3,
    p_window_hours INT DEFAULT 24
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
DECLARE
    v_cutoff TIMESTAMPTZ;
    v_used_count INT;
    v_earliest TIMESTAMPTZ;
    v_reset_timestamp TIMESTAMPTZ;
    v_remaining INT;
    v_new_usage_id BIGINT;
    v_existing_id BIGINT;
BEGIN
    -- Security guard: If called by an authenticated user, verify they are consuming their own quota
    IF auth.uid() IS NOT NULL AND auth.uid() != p_user_id THEN
        RAISE EXCEPTION 'Access Denied: You can only consume your own AI question quota.';
    END IF;

    -- Idempotency check: If this exact request_id was already processed, return existing record
    IF p_request_id IS NOT NULL THEN
        SELECT usage_id INTO v_existing_id
        FROM public.ai_question_usages
        WHERE user_id = p_user_id AND request_id = p_request_id
        LIMIT 1;

        IF v_existing_id IS NOT NULL THEN
            -- Already recorded; return success without double-decrementing quota
            SELECT COUNT(*) INTO v_used_count
            FROM public.ai_question_usages
            WHERE user_id = p_user_id
              AND created_at >= NOW() - (p_window_hours || ' hours')::INTERVAL
              AND status = 'completed'
              AND quota_unit_consumed = true;

            RETURN jsonb_build_object(
                'allowed', true,
                'usage_id', v_existing_id,
                'remaining', GREATEST(0, p_max_questions - v_used_count),
                'used_count', v_used_count,
                'is_idempotent_duplicate', true,
                'message', 'Request already recorded.'
            );
        END IF;
    END IF;

    v_cutoff := NOW() - (p_window_hours || ' hours')::INTERVAL;

    -- Concurrency safety: lock existing active rows for this user in window
    PERFORM 1 FROM public.ai_question_usages
    WHERE user_id = p_user_id AND created_at >= v_cutoff
    FOR UPDATE;

    -- Count completed queries that consumed quota
    SELECT COUNT(*), MIN(created_at)
    INTO v_used_count, v_earliest
    FROM public.ai_question_usages
    WHERE user_id = p_user_id
      AND created_at >= v_cutoff
      AND status = 'completed'
      AND quota_unit_consumed = true;

    -- Check if daily limit reached
    IF v_used_count >= p_max_questions THEN
        v_reset_timestamp := v_earliest + (p_window_hours || ' hours')::INTERVAL;
        -- Record rejected attempt for audit (does NOT consume quota)
        INSERT INTO public.ai_question_usages (
            user_id, question_text, question_hash, status, model_used, request_id, quota_unit_consumed
        ) VALUES (
            p_user_id, p_question_text, p_question_hash, 'rejected', p_model, p_request_id, false
        );

        RETURN jsonb_build_object(
            'allowed', false,
            'reason', 'QUOTA_EXHAUSTED',
            'remaining', 0,
            'used_count', v_used_count,
            'reset_timestamp', v_reset_timestamp,
            'message', 'Daily quota exhausted (' || v_used_count || '/' || p_max_questions || ' used). 0 remaining.'
        );
    END IF;

    -- Record accepted question atomically
    INSERT INTO public.ai_question_usages (
        user_id, question_text, question_hash, status, model_used, request_id, quota_unit_consumed
    ) VALUES (
        p_user_id, p_question_text, p_question_hash, 'completed', p_model, p_request_id, true
    ) RETURNING usage_id INTO v_new_usage_id;

    v_remaining := p_max_questions - (v_used_count + 1);

    RETURN jsonb_build_object(
        'allowed', true,
        'usage_id', v_new_usage_id,
        'remaining', v_remaining,
        'used_count', v_used_count + 1,
        'is_idempotent_duplicate', false,
        'message', 'Question accepted. ' || (v_used_count + 1) || '/' || p_max_questions || ' used. ' || v_remaining || ' remaining.'
    );
END;
$$;

REVOKE EXECUTE ON FUNCTION public.check_and_consume_ai_quota(UUID, TEXT, TEXT, TEXT, TEXT, INT, INT) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION public.check_and_consume_ai_quota(UUID, TEXT, TEXT, TEXT, TEXT, INT, INT) FROM anon;
GRANT EXECUTE ON FUNCTION public.check_and_consume_ai_quota(UUID, TEXT, TEXT, TEXT, TEXT, INT, INT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.check_and_consume_ai_quota(UUID, TEXT, TEXT, TEXT, TEXT, INT, INT) TO service_role;
