from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4


class SourceType(StrEnum):
    sms = "sms"
    email = "email"
    social = "social"
    investment_ad = "investment_ad"
    banking = "banking"
    chat = "chat"
    screenshot_ocr = "screenshot_ocr"
    voice_transcript = "voice_transcript"


class ScamCategory(StrEnum):
    phishing = "phishing"
    banking_fraud = "banking_fraud"
    investment_scam = "investment_scam"
    crypto_scam = "crypto_scam"
    romance_scam = "romance_scam"
    job_scam = "job_scam"
    lottery_scam = "lottery_scam"
    identity_theft = "identity_theft"
    social_engineering = "social_engineering"


class PersuasionStrategy(StrEnum):
    urgency = "urgency"
    authority_impersonation = "authority_impersonation"
    scarcity = "scarcity"
    reward_promise = "reward_promise"
    fear_or_threat = "fear_or_threat"
    secrecy = "secrecy"
    trust_building = "trust_building"
    reciprocity = "reciprocity"


class RiskLevel(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


@dataclass(frozen=True)
class Evidence:
    signal: str
    description: str
    weight: float
    matched_terms: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ScamAnalysis:
    id: UUID
    source_type: SourceType
    language: str
    content_sha256: str
    risk_score: float
    risk_level: RiskLevel
    scam_categories: list[ScamCategory]
    persuasion_strategies: list[PersuasionStrategy]
    evidence: list[Evidence]
    recommended_actions: list[str]
    created_at: datetime

    @classmethod
    def create(
        cls,
        *,
        source_type: SourceType,
        language: str,
        content_sha256: str,
        risk_score: float,
        risk_level: RiskLevel,
        scam_categories: list[ScamCategory],
        persuasion_strategies: list[PersuasionStrategy],
        evidence: list[Evidence],
        recommended_actions: list[str],
    ) -> "ScamAnalysis":
        return cls(
            id=uuid4(),
            source_type=source_type,
            language=language,
            content_sha256=content_sha256,
            risk_score=risk_score,
            risk_level=risk_level,
            scam_categories=scam_categories,
            persuasion_strategies=persuasion_strategies,
            evidence=evidence,
            recommended_actions=recommended_actions,
            created_at=datetime.now(UTC),
        )

