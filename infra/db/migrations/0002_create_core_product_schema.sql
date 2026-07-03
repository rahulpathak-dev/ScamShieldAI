CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;

DO $$
BEGIN
    CREATE TYPE user_role AS ENUM ('user', 'analyst', 'admin');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    CREATE TYPE scan_prediction AS ENUM ('legitimate', 'suspicious', 'scam', 'unknown');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    CREATE TYPE scam_report_status AS ENUM ('submitted', 'triaged', 'confirmed', 'rejected', 'resolved');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    CREATE TYPE threat_indicator_type AS ENUM (
        'malicious_url',
        'phone_number',
        'keyword',
        'domain',
        'email_address',
        'crypto_wallet'
    );
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    CREATE TYPE alert_type AS ENUM ('high_risk_scan', 'threat_match', 'report_update', 'system', 'model_drift');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    CREATE TYPE alert_status AS ENUM ('pending', 'sent', 'read', 'dismissed', 'failed');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(120) NOT NULL,
    email CITEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role user_role NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_login_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_users_name_not_blank CHECK (length(btrim(name)) > 0),
    CONSTRAINT chk_users_email_not_blank CHECK (length(btrim(email::TEXT)) > 0),
    CONSTRAINT chk_users_password_hash_not_blank CHECK (length(btrim(password_hash)) > 0)
);

CREATE TABLE IF NOT EXISTS scan_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    message_sha256 CHAR(64) GENERATED ALWAYS AS (encode(digest(message, 'sha256'), 'hex')) STORED,
    source_type VARCHAR(32) NOT NULL DEFAULT 'unknown',
    language VARCHAR(16) NOT NULL DEFAULT 'en',
    prediction scan_prediction NOT NULL DEFAULT 'unknown',
    risk_score NUMERIC(5, 2) NOT NULL,
    model_summary JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_scan_history_message_not_blank CHECK (length(btrim(message)) > 0),
    CONSTRAINT chk_scan_history_risk_score CHECK (risk_score >= 0 AND risk_score <= 100)
);

CREATE TABLE IF NOT EXISTS scam_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    scan_history_id UUID NULL REFERENCES scan_history(id) ON DELETE SET NULL,
    category VARCHAR(80) NOT NULL,
    description TEXT NOT NULL,
    evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
    status scam_report_status NOT NULL DEFAULT 'submitted',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_scam_reports_category_not_blank CHECK (length(btrim(category)) > 0),
    CONSTRAINT chk_scam_reports_description_not_blank CHECK (length(btrim(description)) > 0)
);

CREATE TABLE IF NOT EXISTS threat_database (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    indicator_type threat_indicator_type NOT NULL,
    indicator_value TEXT NOT NULL,
    normalized_value TEXT NOT NULL,
    severity SMALLINT NOT NULL DEFAULT 5,
    confidence NUMERIC(5, 2) NOT NULL DEFAULT 50.00,
    source VARCHAR(120) NULL,
    description TEXT NULL,
    evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_threat_database_indicator UNIQUE (indicator_type, normalized_value),
    CONSTRAINT chk_threat_database_indicator_value_not_blank CHECK (length(btrim(indicator_value)) > 0),
    CONSTRAINT chk_threat_database_normalized_value_not_blank CHECK (length(btrim(normalized_value)) > 0),
    CONSTRAINT chk_threat_database_severity CHECK (severity BETWEEN 1 AND 10),
    CONSTRAINT chk_threat_database_confidence CHECK (confidence >= 0 AND confidence <= 100),
    CONSTRAINT chk_threat_database_seen_order CHECK (last_seen_at >= first_seen_at)
);

CREATE TABLE IF NOT EXISTS scan_threat_matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_history_id UUID NOT NULL REFERENCES scan_history(id) ON DELETE CASCADE,
    threat_id UUID NOT NULL REFERENCES threat_database(id) ON DELETE RESTRICT,
    matched_value TEXT NOT NULL,
    match_context TEXT NULL,
    confidence NUMERIC(5, 2) NOT NULL DEFAULT 100.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_scan_threat_matches_match UNIQUE (scan_history_id, threat_id, matched_value),
    CONSTRAINT chk_scan_threat_matches_confidence CHECK (confidence >= 0 AND confidence <= 100),
    CONSTRAINT chk_scan_threat_matches_value_not_blank CHECK (length(btrim(matched_value)) > 0)
);

CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    alert_type alert_type NOT NULL,
    status alert_status NOT NULL DEFAULT 'pending',
    title VARCHAR(160) NOT NULL,
    message TEXT NOT NULL,
    related_scan_id UUID NULL REFERENCES scan_history(id) ON DELETE SET NULL,
    related_threat_id UUID NULL REFERENCES threat_database(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sent_at TIMESTAMPTZ NULL,
    read_at TIMESTAMPTZ NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_alerts_title_not_blank CHECK (length(btrim(title)) > 0),
    CONSTRAINT chk_alerts_message_not_blank CHECK (length(btrim(message)) > 0)
);

CREATE TABLE IF NOT EXISTS model_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_history_id UUID NULL REFERENCES scan_history(id) ON DELETE CASCADE,
    model_name VARCHAR(120) NOT NULL,
    model_version VARCHAR(64) NOT NULL DEFAULT 'unknown',
    accuracy NUMERIC(5, 4) NULL,
    prediction scan_prediction NOT NULL DEFAULT 'unknown',
    confidence NUMERIC(5, 2) NULL,
    raw_output JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_model_results_model_name_not_blank CHECK (length(btrim(model_name)) > 0),
    CONSTRAINT chk_model_results_accuracy CHECK (accuracy IS NULL OR (accuracy >= 0 AND accuracy <= 1)),
    CONSTRAINT chk_model_results_confidence CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 100))
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_user_id UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(120) NOT NULL,
    entity_type VARCHAR(80) NULL,
    entity_id UUID NULL,
    ip_address INET NULL,
    user_agent TEXT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_audit_logs_action_not_blank CHECK (length(btrim(action)) > 0)
);

DO $$
BEGIN
    IF to_regclass('public.scam_analyses') IS NOT NULL
       AND NOT EXISTS (
           SELECT 1
           FROM pg_constraint
           WHERE conname = 'fk_scam_analyses_user_id'
       ) THEN
        ALTER TABLE scam_analyses
            ADD CONSTRAINT fk_scam_analyses_user_id
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL;
    END IF;
END $$;

DROP TRIGGER IF EXISTS trg_users_updated_at ON users;
CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_scam_reports_updated_at ON scam_reports;
CREATE TRIGGER trg_scam_reports_updated_at
BEFORE UPDATE ON scam_reports
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_threat_database_updated_at ON threat_database;
CREATE TRIGGER trg_threat_database_updated_at
BEFORE UPDATE ON threat_database
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_alerts_updated_at ON alerts;
CREATE TRIGGER trg_alerts_updated_at
BEFORE UPDATE ON alerts
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_active_created_at ON users(is_active, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_scan_history_user_created_at ON scan_history(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_scan_history_prediction_created_at ON scan_history(prediction, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_scan_history_risk_score ON scan_history(risk_score DESC);
CREATE INDEX IF NOT EXISTS idx_scan_history_message_sha256 ON scan_history(message_sha256);
CREATE INDEX IF NOT EXISTS idx_scan_history_source_language ON scan_history(source_type, language);

CREATE INDEX IF NOT EXISTS idx_scam_reports_user_created_at ON scam_reports(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_scam_reports_scan_history_id ON scam_reports(scan_history_id);
CREATE INDEX IF NOT EXISTS idx_scam_reports_category_status ON scam_reports(category, status);
CREATE INDEX IF NOT EXISTS idx_scam_reports_evidence_gin ON scam_reports USING GIN (evidence);

CREATE INDEX IF NOT EXISTS idx_threat_database_type_active ON threat_database(indicator_type, is_active);
CREATE INDEX IF NOT EXISTS idx_threat_database_severity_confidence ON threat_database(severity DESC, confidence DESC);
CREATE INDEX IF NOT EXISTS idx_threat_database_last_seen ON threat_database(last_seen_at DESC);
CREATE INDEX IF NOT EXISTS idx_threat_database_active_not_expired
    ON threat_database(indicator_type, normalized_value)
    WHERE is_active = TRUE AND expires_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_threat_database_evidence_gin ON threat_database USING GIN (evidence);

CREATE INDEX IF NOT EXISTS idx_scan_threat_matches_scan ON scan_threat_matches(scan_history_id);
CREATE INDEX IF NOT EXISTS idx_scan_threat_matches_threat ON scan_threat_matches(threat_id);

CREATE INDEX IF NOT EXISTS idx_alerts_user_status_created_at ON alerts(user_id, status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_type_created_at ON alerts(alert_type, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_related_scan ON alerts(related_scan_id);
CREATE INDEX IF NOT EXISTS idx_alerts_related_threat ON alerts(related_threat_id);
CREATE INDEX IF NOT EXISTS idx_alerts_unread ON alerts(user_id, created_at DESC)
    WHERE status IN ('pending', 'sent');

CREATE INDEX IF NOT EXISTS idx_model_results_scan_created_at ON model_results(scan_history_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_model_results_model_version ON model_results(model_name, model_version, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_model_results_prediction ON model_results(prediction, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_model_results_raw_output_gin ON model_results USING GIN (raw_output);

CREATE INDEX IF NOT EXISTS idx_audit_logs_actor_created_at ON audit_logs(actor_user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action_created_at ON audit_logs(action, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at_brin ON audit_logs USING BRIN (created_at);
CREATE INDEX IF NOT EXISTS idx_audit_logs_metadata_gin ON audit_logs USING GIN (metadata);