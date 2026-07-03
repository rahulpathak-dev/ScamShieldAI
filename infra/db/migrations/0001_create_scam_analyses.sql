CREATE TABLE IF NOT EXISTS scam_analyses (
    id UUID PRIMARY KEY,
    user_id UUID NULL,
    source_type VARCHAR(32) NOT NULL,
    language VARCHAR(16) NOT NULL DEFAULT 'en',
    content_sha256 CHAR(64) NOT NULL,
    risk_score NUMERIC(5, 2) NOT NULL,
    risk_level VARCHAR(16) NOT NULL,
    scam_categories JSONB NOT NULL DEFAULT '[]'::jsonb,
    persuasion_strategies JSONB NOT NULL DEFAULT '[]'::jsonb,
    evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
    recommended_actions JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_scam_analyses_created_at
    ON scam_analyses (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_scam_analyses_risk_level
    ON scam_analyses (risk_level);

CREATE INDEX IF NOT EXISTS idx_scam_analyses_content_sha256
    ON scam_analyses (content_sha256);

