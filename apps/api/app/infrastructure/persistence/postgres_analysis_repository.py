import json
import logging
from datetime import UTC
from uuid import UUID

from sqlalchemy import text

from app.domain.entities import Evidence, PersuasionStrategy, RiskLevel, ScamAnalysis, ScamCategory, SourceType
from app.domain.repositories import AnalysisRepository
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.persistence.in_memory_analysis_repository import InMemoryAnalysisRepository

logger = logging.getLogger(__name__)


class PostgresAnalysisRepository(AnalysisRepository):
    def save(self, analysis: ScamAnalysis) -> ScamAnalysis:
        payload = {
            "id": analysis.id,
            "source_type": analysis.source_type.value,
            "language": analysis.language,
            "content_sha256": analysis.content_sha256,
            "risk_score": analysis.risk_score,
            "risk_level": analysis.risk_level.value,
            "scam_categories": json.dumps([item.value for item in analysis.scam_categories]),
            "persuasion_strategies": json.dumps([item.value for item in analysis.persuasion_strategies]),
            "evidence": json.dumps(
                [
                    {
                        "signal": item.signal,
                        "description": item.description,
                        "weight": item.weight,
                        "matched_terms": item.matched_terms,
                    }
                    for item in analysis.evidence
                ]
            ),
            "recommended_actions": json.dumps(analysis.recommended_actions),
            "created_at": analysis.created_at,
        }

        statement = text(
            """
            INSERT INTO scam_analyses (
                id, source_type, language, content_sha256, risk_score, risk_level,
                scam_categories, persuasion_strategies, evidence, recommended_actions, created_at
            ) VALUES (
                :id, :source_type, :language, :content_sha256, :risk_score, :risk_level,
                CAST(:scam_categories AS jsonb), CAST(:persuasion_strategies AS jsonb),
                CAST(:evidence AS jsonb), CAST(:recommended_actions AS jsonb), :created_at
            )
            ON CONFLICT (id) DO NOTHING
            """
        )
        with SessionLocal() as session:
            session.execute(statement, payload)
            session.commit()
        return analysis

    def get(self, analysis_id: UUID) -> ScamAnalysis | None:
        statement = text("SELECT * FROM scam_analyses WHERE id = :id")
        with SessionLocal() as session:
            row = session.execute(statement, {"id": analysis_id}).mappings().first()

        if row is None:
            return None

        return ScamAnalysis(
            id=row["id"],
            source_type=SourceType(row["source_type"]),
            language=row["language"],
            content_sha256=row["content_sha256"],
            risk_score=float(row["risk_score"]),
            risk_level=RiskLevel(row["risk_level"]),
            scam_categories=[ScamCategory(item) for item in row["scam_categories"]],
            persuasion_strategies=[PersuasionStrategy(item) for item in row["persuasion_strategies"]],
            evidence=[Evidence(**item) for item in row["evidence"]],
            recommended_actions=list(row["recommended_actions"]),
            created_at=row["created_at"].astimezone(UTC),
        )


class ResilientAnalysisRepository(AnalysisRepository):
    def __init__(self, primary: AnalysisRepository | None = None, fallback: InMemoryAnalysisRepository | None = None) -> None:
        self._primary = primary or PostgresAnalysisRepository()
        self._fallback = fallback or InMemoryAnalysisRepository()

    def save(self, analysis: ScamAnalysis) -> ScamAnalysis:
        self._fallback.save(analysis)
        try:
            return self._primary.save(analysis)
        except Exception:
            logger.exception("Could not persist scam analysis to PostgreSQL; returned in-memory result.")
            return analysis

    def get(self, analysis_id: UUID) -> ScamAnalysis | None:
        try:
            analysis = self._primary.get(analysis_id)
            if analysis is not None:
                return analysis
        except Exception:
            logger.exception("Could not read scam analysis from PostgreSQL; using in-memory fallback.")
        return self._fallback.get(analysis_id)