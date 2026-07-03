from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ScamShieldAI API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    environment: str = "local"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000"
    database_url: str = "postgresql+psycopg://scamshield:change_me_dev_password@localhost:5432/scamshieldai"
    request_id_header: str = "X-Request-ID"
    jwt_secret_key: str = "change-this-local-development-secret-at-least-32-chars"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    auth_cookie_name: str = "scamshield_access_token"
    scam_classifier_model_path: str = "ml/models/classical/best_model.joblib"
    scam_classifier_model_card_path: str = "ml/models/classical/model_card.json"
    persuasion_classifier_model_path: str = "ml/models/transformers/persuasion"
    assistant_provider: str = "local"
    assistant_model: str = "gpt-4.1-mini"
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    llama_base_url: str | None = None
    llama_api_key: str | None = None
    assistant_knowledge_dir: str = "knowledge"
    assistant_vector_dir: str = "ml/vectorstores/scamshield"
    assistant_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    notification_high_risk_threshold: float = 71.0
    notification_critical_threshold: float = 90.0
    email_notifications_enabled: bool = False
    notification_from_email: str | None = None
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = True
    enterprise_api_keys: str = ""
    enterprise_max_batch_size: int = 100
    speech_recognition_provider: str = "external"
    speech_recognition_model: str = "whisper-large-v3"
    rate_limit_requests_per_minute: int = 240

    model_config = SettingsConfigDict(env_prefix="SCAMSHIELD_", env_file=".env", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    def validate_security_settings(self) -> None:
        default_secret = "change-this-local-development-secret-at-least-32-chars"
        if self.is_production and self.jwt_secret_key == default_secret:
            raise RuntimeError("SCAMSHIELD_JWT_SECRET_KEY must be changed in production.")
        if len(self.jwt_secret_key) < 32:
            raise RuntimeError("SCAMSHIELD_JWT_SECRET_KEY must be at least 32 characters.")


@lru_cache
def get_settings() -> Settings:
    return Settings()