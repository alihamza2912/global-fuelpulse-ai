-- ==============================================================================
-- GLOBAL FUELPULSE AI — SUPABASE SECURITY ADVISOR REMEDIATION
-- Target: Supabase PostgreSQL 15+
-- Fixes:
--   1. [ERROR] Security Definer View on public.vw_latest_fuel_prices
--   2. [WARNING] Function Search Path Mutable on public.handle_new_user
--   3. [WARNING] Function Search Path Mutable on public.check_and_consume_ai_quota
--   4. [WARNING] Public Can Execute SECURITY DEFINER on public.handle_new_user()
--   5. [WARNING] Signed-In Users Can Execute SECURITY DEFINER on public.handle_new_user()
--   6. [WARNING] Public Can Execute SECURITY DEFINER on public.check_and_consume_ai_quota
--   7. [WARNING] Signed-In Users Can Execute SECURITY DEFINER on public.check_and_consume_ai_quota
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. FIX ERROR: Security Definer View on public.vw_latest_fuel_prices
-- In PostgreSQL 15+, views should enforce querying user permissions using security_invoker = true
-- ------------------------------------------------------------------------------
ALTER VIEW public.vw_latest_fuel_prices SET (security_invoker = true);

-- ------------------------------------------------------------------------------
-- 2. FIX WARNINGS 1 & 2: Function Search Path Mutable
-- Functions must have a fixed search_path to prevent malicious search-path hijacking
-- ------------------------------------------------------------------------------
ALTER FUNCTION public.handle_new_user() SET search_path = public, auth, pg_temp;

-- ------------------------------------------------------------------------------
-- 3. FIX WARNINGS 3, 4, 5: Restrict Execution of handle_new_user()
-- handle_new_user() is an internal trigger for auth.users; it must never be called directly
-- ------------------------------------------------------------------------------
REVOKE EXECUTE ON FUNCTION public.handle_new_user() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION public.handle_new_user() FROM anon;
REVOKE EXECUTE ON FUNCTION public.handle_new_user() FROM authenticated;

-- ------------------------------------------------------------------------------
-- 4. UPDATE check_and_consume_ai_quota: Fixed search_path & Secure Permissions
-- Sets fixed search_path, revokes from public and anon, grants only to authenticated & service_role
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.check_and_consume_ai_quota(
    p_user_id UUID,
    p_question_text TEXT,
    p_question_hash TEXT,
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
BEGIN
    -- Security guard: If called by an authenticated user, verify they are consuming their own quota
    IF auth.uid() IS NOT NULL AND auth.uid() != p_user_id THEN
        RAISE EXCEPTION 'Access Denied: You can only consume your own AI question quota.';
    END IF;

    v_cutoff := NOW() - (p_window_hours || ' hours')::INTERVAL;

    -- Concurrency safety: lock active usage rows for this user within window
    PERFORM 1 FROM public.ai_question_usages
    WHERE user_id = p_user_id AND created_at >= v_cutoff
    FOR UPDATE;

    -- Count active completed queries in rolling window
    SELECT COUNT(*), MIN(created_at)
    INTO v_used_count, v_earliest
    FROM public.ai_question_usages
    WHERE user_id = p_user_id
      AND created_at >= v_cutoff
      AND status = 'completed';

    -- Check if daily limit reached
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

    -- Record accepted question atomically
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
$$;

-- Secure execution permissions on check_and_consume_ai_quota
REVOKE EXECUTE ON FUNCTION public.check_and_consume_ai_quota(UUID, TEXT, TEXT, TEXT, INT, INT) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION public.check_and_consume_ai_quota(UUID, TEXT, TEXT, TEXT, INT, INT) FROM anon;
GRANT EXECUTE ON FUNCTION public.check_and_consume_ai_quota(UUID, TEXT, TEXT, TEXT, INT, INT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.check_and_consume_ai_quota(UUID, TEXT, TEXT, TEXT, INT, INT) TO service_role;
