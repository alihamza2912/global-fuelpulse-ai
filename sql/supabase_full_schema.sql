-- ==============================================================================
-- GLOBAL FUELPULSE AI — COMPREHENSIVE PRODUCTION SUPABASE SCHEMA & RLS
-- Target: Supabase (PostgreSQL 15+)
-- Features:
--   1. Auth Integration & User Profiles (with preferences)
--   2. Atomic AI Quota Function (3 free questions per 24 hours per user)
--   3. Private Chat Conversations & Message History
--   4. Shared Commodity Data Mart (Fuel Prices, Trade Flows, Indicators)
--   5. Analytical Views & High-Performance Indexes
--   6. Production Row Level Security (RLS) on all tables
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. EXTENSIONS
-- ------------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ------------------------------------------------------------------------------
-- 2. USER PROFILES & SETTINGS (Linked with auth.users)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE,
    full_name TEXT,
    email TEXT,
    avatar_url TEXT,
    role TEXT DEFAULT 'analyst',
    preferences JSONB DEFAULT '{"theme": "dark", "default_fuel": "petrol", "notifications": true}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Public profiles are viewable by authenticated users" ON public.profiles;
CREATE POLICY "Public profiles are viewable by authenticated users"
    ON public.profiles FOR SELECT
    TO authenticated
    USING (true);

DROP POLICY IF EXISTS "Users can insert their own profile" ON public.profiles;
CREATE POLICY "Users can insert their own profile"
    ON public.profiles FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "Users can update own profile" ON public.profiles;
CREATE POLICY "Users can update own profile"
    ON public.profiles FOR UPDATE
    TO authenticated
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

-- Trigger to automatically create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, username, full_name, email, preferences)
    VALUES (
        new.id,
        COALESCE(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1)),
        COALESCE(new.raw_user_meta_data->>'full_name', split_part(new.email, '@', 1)),
        new.email,
        '{"theme": "dark", "default_fuel": "petrol", "notifications": true}'::jsonb
    )
    ON CONFLICT (id) DO UPDATE SET
        email = EXCLUDED.email,
        updated_at = NOW();
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ------------------------------------------------------------------------------
-- 3. AI USAGE & ATOMIC CONCURRENCY-SAFE QUOTA ENFORCEMENT
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.ai_question_usages (
    usage_id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_hash TEXT NOT NULL,
    status TEXT DEFAULT 'completed', -- 'completed', 'failed', 'blocked'
    model_used TEXT DEFAULT 'gemini-2.0-flash',
    tokens_used INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ai_usage_user_window 
    ON public.ai_question_usages (user_id, created_at, status);
CREATE INDEX IF NOT EXISTS idx_ai_usage_hash 
    ON public.ai_question_usages (question_hash);

ALTER TABLE public.ai_question_usages ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can view only their own question usage" ON public.ai_question_usages;
CREATE POLICY "Users can view only their own question usage"
    ON public.ai_question_usages FOR SELECT
    TO authenticated
    USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert their own question usage" ON public.ai_question_usages;
CREATE POLICY "Users can insert their own question usage"
    ON public.ai_question_usages FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

-- Atomic stored procedure enforcing exactly 3 questions per rolling 24-hour window
CREATE OR REPLACE FUNCTION public.check_and_consume_ai_quota(
    p_user_id UUID,
    p_question_text TEXT,
    p_question_hash TEXT,
    p_model TEXT DEFAULT 'gemini-2.0-flash',
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
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ------------------------------------------------------------------------------
-- 4. PRIVATE CHAT CONVERSATIONS & MESSAGE HISTORY
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.chat_conversations (
    conversation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL DEFAULT 'New Energy Consultation',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.chat_conversations ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can manage own conversations" ON public.chat_conversations;
CREATE POLICY "Users can manage own conversations"
    ON public.chat_conversations FOR ALL
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

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

DROP POLICY IF EXISTS "Users can manage own messages" ON public.chat_messages;
CREATE POLICY "Users can manage own messages"
    ON public.chat_messages FOR ALL
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE INDEX IF NOT EXISTS idx_chat_messages_conv_time 
    ON public.chat_messages (conversation_id, created_at ASC);

-- ------------------------------------------------------------------------------
-- 5. SHARED ANALYTICAL COMMODITY DATA MART
-- ------------------------------------------------------------------------------

-- Data sources registry
CREATE TABLE IF NOT EXISTS public.data_sources (
    source_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    organization VARCHAR(150),
    homepage_url VARCHAR(255),
    api_docs_url VARCHAR(255),
    auth_type VARCHAR(50) DEFAULT 'none',
    update_frequency VARCHAR(50) DEFAULT 'daily',
    license_terms TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Dimension: Countries
CREATE TABLE IF NOT EXISTS public.dim_country (
    country_iso3 CHAR(3) PRIMARY KEY,
    country_iso2 CHAR(2) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    continent VARCHAR(50) NOT NULL,
    region VARCHAR(100),
    income_group VARCHAR(50),
    currency_code CHAR(3),
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    is_opec BOOLEAN DEFAULT FALSE,
    is_opec_plus BOOLEAN DEFAULT FALSE,
    is_major_net_importer BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Dimension: Locations
CREATE TABLE IF NOT EXISTS public.dim_location (
    location_id VARCHAR(50) PRIMARY KEY,
    country_iso3 CHAR(3) NOT NULL REFERENCES public.dim_country(country_iso3) ON DELETE CASCADE,
    location_name VARCHAR(100) NOT NULL,
    location_type VARCHAR(50) DEFAULT 'city',
    state_province VARCHAR(100),
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Fact: Retail Fuel Prices
CREATE TABLE IF NOT EXISTS public.fuel_prices (
    price_id BIGSERIAL PRIMARY KEY,
    country_iso3 CHAR(3) NOT NULL REFERENCES public.dim_country(country_iso3),
    location_id VARCHAR(50),
    observation_date DATE NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    price_local NUMERIC(12, 4) NOT NULL,
    currency_local CHAR(3) NOT NULL,
    unit VARCHAR(30) DEFAULT 'litre',
    price_usd_per_litre NUMERIC(10, 4) NOT NULL,
    tax_component_percent NUMERIC(5, 2),
    source_id VARCHAR(50) NOT NULL REFERENCES public.data_sources(source_id),
    source_updated_at TIMESTAMPTZ,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    is_verified BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_fuel_price_obs UNIQUE (country_iso3, location_id, observation_date, fuel_type, source_id)
);

CREATE INDEX IF NOT EXISTS idx_fuel_prices_country_date 
    ON public.fuel_prices (country_iso3, observation_date DESC, fuel_type);

-- Fact: Petroleum Trade Flows
CREATE TABLE IF NOT EXISTS public.fact_petroleum_trade (
    trade_id BIGSERIAL PRIMARY KEY,
    reporting_period VARCHAR(10) NOT NULL,
    reporting_year INT NOT NULL,
    exporter_iso3 CHAR(3) REFERENCES public.dim_country(country_iso3),
    importer_iso3 CHAR(3) REFERENCES public.dim_country(country_iso3),
    product_category VARCHAR(50) NOT NULL,
    hs_code VARCHAR(10),
    trade_direction VARCHAR(10) NOT NULL,
    quantity NUMERIC(16, 4) NOT NULL,
    quantity_unit VARCHAR(30) NOT NULL,
    value_usd NUMERIC(18, 2),
    transport_mode VARCHAR(50) DEFAULT 'tanker_pipeline',
    source_id VARCHAR(50) NOT NULL REFERENCES public.data_sources(source_id),
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_petroleum_trade UNIQUE (reporting_period, exporter_iso3, importer_iso3, product_category, trade_direction, source_id)
);

-- Fact: Energy Indicators
CREATE TABLE IF NOT EXISTS public.fact_energy_indicator (
    indicator_id BIGSERIAL PRIMARY KEY,
    country_iso3 CHAR(3) NOT NULL REFERENCES public.dim_country(country_iso3),
    indicator_code VARCHAR(50) NOT NULL,
    indicator_name VARCHAR(150) NOT NULL,
    observation_year INT NOT NULL,
    value_numeric NUMERIC(18, 4) NOT NULL,
    unit VARCHAR(30) NOT NULL,
    source_id VARCHAR(50) NOT NULL REFERENCES public.data_sources(source_id),
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_energy_indicator UNIQUE (country_iso3, indicator_code, observation_year, source_id)
);

-- Fact: Affordability Metrics
CREATE TABLE IF NOT EXISTS public.fact_affordability (
    affordability_id BIGSERIAL PRIMARY KEY,
    country_iso3 CHAR(3) NOT NULL REFERENCES public.dim_country(country_iso3),
    observation_year INT NOT NULL,
    gdp_per_capita_usd NUMERIC(12, 2) NOT NULL,
    daily_income_usd NUMERIC(10, 2) NOT NULL,
    petrol_price_usd NUMERIC(8, 4) NOT NULL,
    diesel_price_usd NUMERIC(8, 4) NOT NULL,
    petrol_cost_share_daily_pct NUMERIC(6, 2) NOT NULL,
    diesel_cost_share_daily_pct NUMERIC(6, 2) NOT NULL,
    burden_category VARCHAR(30) NOT NULL,
    source_id VARCHAR(50) NOT NULL REFERENCES public.data_sources(source_id),
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_affordability UNIQUE (country_iso3, observation_year, source_id)
);

-- Fact: Exchange Rates
CREATE TABLE IF NOT EXISTS public.fact_exchange_rate (
    rate_id BIGSERIAL PRIMARY KEY,
    currency_code CHAR(3) NOT NULL,
    rate_to_usd NUMERIC(14, 6) NOT NULL,
    observation_date DATE NOT NULL,
    source_id VARCHAR(50) NOT NULL REFERENCES public.data_sources(source_id),
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_exchange_rate UNIQUE (currency_code, observation_date, source_id)
);

-- Predictions & Forecasts
CREATE TABLE IF NOT EXISTS public.forecast_predictions (
    prediction_id BIGSERIAL PRIMARY KEY,
    country_iso3 CHAR(3) NOT NULL REFERENCES public.dim_country(country_iso3),
    fuel_type VARCHAR(50) NOT NULL,
    forecast_date DATE NOT NULL,
    predicted_price_local NUMERIC(12, 4) NOT NULL,
    predicted_price_usd NUMERIC(10, 4) NOT NULL,
    confidence_interval_low NUMERIC(12, 4),
    confidence_interval_high NUMERIC(12, 4),
    model_version VARCHAR(50) DEFAULT 'SARIMAX-v2.1',
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ------------------------------------------------------------------------------
-- 6. ROW LEVEL SECURITY FOR COMMODITY DATA MART
-- Public & Authenticated users can read commodity data; only service-role can mutate.
-- ------------------------------------------------------------------------------
ALTER TABLE public.data_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dim_country ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dim_location ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fuel_prices ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fact_petroleum_trade ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fact_energy_indicator ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fact_affordability ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fact_exchange_rate ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.forecast_predictions ENABLE ROW LEVEL SECURITY;

DO $$ 
DECLARE
    tbl text;
BEGIN
    FOR tbl IN SELECT unnest(ARRAY[
        'data_sources', 'dim_country', 'dim_location', 'fuel_prices',
        'fact_petroleum_trade', 'fact_energy_indicator', 'fact_affordability',
        'fact_exchange_rate', 'forecast_predictions'
    ])
    LOOP
        EXECUTE format('DROP POLICY IF EXISTS "Public read access for %I" ON public.%I;', tbl, tbl);
        EXECUTE format('CREATE POLICY "Public read access for %I" ON public.%I FOR SELECT USING (true);', tbl, tbl);
        
        EXECUTE format('DROP POLICY IF EXISTS "Service role write access for %I" ON public.%I;', tbl, tbl);
        EXECUTE format('CREATE POLICY "Service role write access for %I" ON public.%I FOR ALL TO service_role USING (true) WITH CHECK (true);', tbl, tbl);
    END LOOP;
END $$;

-- ------------------------------------------------------------------------------
-- 7. ANALYTICAL VIEWS
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW public.vw_latest_fuel_prices AS
WITH ranked_prices AS (
    SELECT 
        fp.price_id,
        fp.country_iso3,
        c.country_name,
        c.continent,
        c.region,
        fp.location_id,
        loc.location_name,
        fp.observation_date,
        fp.fuel_type,
        fp.price_local,
        fp.currency_local,
        fp.unit,
        fp.price_usd_per_litre,
        fp.tax_component_percent,
        fp.source_id,
        ds.name AS source_name,
        fp.source_updated_at,
        fp.ingested_at,
        ROW_NUMBER() OVER (
            PARTITION BY fp.country_iso3, fp.fuel_type, COALESCE(fp.location_id, 'NATIONAL') 
            ORDER BY fp.observation_date DESC, fp.ingested_at DESC
        ) as rn
    FROM public.fuel_prices fp
    JOIN public.dim_country c ON fp.country_iso3 = c.country_iso3
    LEFT JOIN public.dim_location loc ON fp.location_id = loc.location_id
    JOIN public.data_sources ds ON fp.source_id = ds.source_id
)
SELECT 
    price_id, country_iso3, country_name, continent, region,
    location_id, location_name, observation_date, fuel_type,
    price_local, currency_local, unit, price_usd_per_litre,
    tax_component_percent, source_id, source_name, source_updated_at, ingested_at
FROM ranked_prices
WHERE rn = 1;
