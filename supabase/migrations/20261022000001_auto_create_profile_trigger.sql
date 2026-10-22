-- ==============================================================================
-- GLOBAL FUELPULSE AI — MIGRATION 20261022000001
-- IDEMPOTENT AUTOMATIC PROFILE PROVISIONING & RECONCILIATION TRIGGER
-- ==============================================================================

-- 1. Ensure public.profiles table exists with required fields and constraints
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE,
    full_name TEXT,
    email TEXT,
    avatar_url TEXT,
    role TEXT DEFAULT 'analyst',
    preferences JSONB DEFAULT '{"theme": "dark", "default_fuel": "petrol", "notifications": true}'::jsonb,
    preferred_language TEXT DEFAULT 'en',
    preferred_theme TEXT DEFAULT 'dark',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- 2. Row Level Security Policies
DROP POLICY IF EXISTS "Profiles are readable by authenticated users" ON public.profiles;
CREATE POLICY "Profiles are readable by authenticated users"
    ON public.profiles FOR SELECT
    TO authenticated
    USING (true);

DROP POLICY IF EXISTS "Users can insert their own profile" ON public.profiles;
CREATE POLICY "Users can insert their own profile"
    ON public.profiles FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "Users can update own profile preferences" ON public.profiles;
CREATE POLICY "Users can update own profile preferences"
    ON public.profiles FOR UPDATE
    TO authenticated
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

-- 3. Secure, Idempotent Function to Create / Reconcile Profile on New Auth User
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER 
LANGUAGE plpgsql 
SECURITY DEFINER
SET search_path = public, auth, pg_temp
AS $$
DECLARE
    derived_username TEXT;
    derived_name TEXT;
    derived_lang TEXT;
    derived_theme TEXT;
BEGIN
    derived_username := COALESCE(
        new.raw_user_meta_data->>'username',
        split_part(COALESCE(new.email, 'analyst@fuelpulse.ai'), '@', 1)
    );
    derived_name := COALESCE(
        new.raw_user_meta_data->>'full_name',
        initcap(derived_username)
    );
    derived_lang := COALESCE(
        new.raw_user_meta_data->>'preferred_language',
        'en'
    );
    derived_theme := COALESCE(
        new.raw_user_meta_data->>'preferred_theme',
        'dark'
    );

    INSERT INTO public.profiles (
        id,
        username,
        full_name,
        email,
        preferred_language,
        preferred_theme,
        preferences,
        updated_at
    )
    VALUES (
        new.id,
        derived_username,
        derived_name,
        new.email,
        derived_lang,
        derived_theme,
        jsonb_build_object(
            'theme', derived_theme,
            'default_fuel', 'petrol',
            'notifications', true
        ),
        NOW()
    )
    ON CONFLICT (id) DO UPDATE SET
        email = COALESCE(EXCLUDED.email, public.profiles.email),
        full_name = COALESCE(EXCLUDED.full_name, public.profiles.full_name),
        preferred_language = COALESCE(EXCLUDED.preferred_language, public.profiles.preferred_language),
        preferred_theme = COALESCE(EXCLUDED.preferred_theme, public.profiles.preferred_theme),
        updated_at = NOW();

    RETURN new;
END;
$$;

-- Revoke dangerous direct execution permissions
REVOKE EXECUTE ON FUNCTION public.handle_new_user() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION public.handle_new_user() FROM anon;
REVOKE EXECUTE ON FUNCTION public.handle_new_user() FROM authenticated;

-- 4. Trigger on auth.users (guaranteed execution upon new user registration)
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 5. Safe Reconciliation Routine for Any Legacy Accounts Missing Profiles
DO $$
DECLARE
    u RECORD;
BEGIN
    FOR u IN 
        SELECT id, email, raw_user_meta_data 
        FROM auth.users 
        WHERE id NOT IN (SELECT id FROM public.profiles)
    LOOP
        INSERT INTO public.profiles (
            id,
            username,
            full_name,
            email,
            preferred_language,
            preferred_theme,
            preferences,
            created_at,
            updated_at
        )
        VALUES (
            u.id,
            COALESCE(u.raw_user_meta_data->>'username', split_part(COALESCE(u.email, 'analyst@fuelpulse.ai'), '@', 1)),
            COALESCE(u.raw_user_meta_data->>'full_name', 'Analyst'),
            u.email,
            'en',
            'dark',
            '{"theme": "dark", "default_fuel": "petrol", "notifications": true}'::jsonb,
            NOW(),
            NOW()
        )
        ON CONFLICT (id) DO NOTHING;
    END LOOP;
END;
$$;
