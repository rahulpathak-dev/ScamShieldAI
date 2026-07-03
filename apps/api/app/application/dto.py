from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.domain.entities import Evidence, ScamAnalysis, SourceType


class AnalyzeTextCommand(BaseModel):
    content: str = Field(min_length=3, max_length=20_000)
    source_type: SourceType
    language: str = Field(default="en", min_length=2, max_length=16)

    @field_validator("content")
    @classmethod
    def normalize_content(cls, value: str) -> str:
        normalized = " ".join(value.replace("\x00", " ").split())
        if len(normalized) < 3:
            raise ValueError("Content must contain at least 3 visible characters.")
        return normalized

    @field_validator("language")
    @classmethod
    def normalize_language(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized.replace("-", "").isalnum():
            raise ValueError("Language must be a valid language code.")
        return normalized


class EvidenceDTO(BaseModel):
    signal: str
    description: str
    weight: float
    matched_terms: list[str]

    @classmethod
    def from_domain(cls, evidence: Evidence) -> "EvidenceDTO":
        return cls(
            signal=evidence.signal,
            description=evidence.description,
            weight=evidence.weight,
            matched_terms=evidence.matched_terms,
        )


class ScamAnalysisDTO(BaseModel):
    analysis_id: UUID
    source_type: str
    language: str
    risk_score: float
    risk_level: str
    scam_categories: list[str]
    persuasion_strategies: list[str]
    evidence: list[EvidenceDTO]
    recommended_actions: list[str]
    created_at: datetime

    @classmethod
    def from_domain(cls, analysis: ScamAnalysis) -> "ScamAnalysisDTO":
        return cls(
            analysis_id=analysis.id,
            source_type=analysis.source_type.value,
            language=analysis.language,
            risk_score=analysis.risk_score,
            risk_level=analysis.risk_level.value,
            scam_categories=[item.value for item in analysis.scam_categories],
            persuasion_strategies=[item.value for item in analysis.persuasion_strategies],
            evidence=[EvidenceDTO.from_domain(item) for item in analysis.evidence],
            recommended_actions=analysis.recommended_actions,
            created_at=analysis.created_at,
        )

