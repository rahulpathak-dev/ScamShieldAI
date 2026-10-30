from typing import Protocol
from uuid import UUID

from app.domain.entities import ScamAnalysis


class AnalysisRepository(Protocol):
    def save(self, analysis: ScamAnalysis) -> ScamAnalysis:
        raise NotImplementedError

    def get(self, analysis_id: UUID) -> ScamAnalysis | None:
        raise NotImplementedError

    def list_recent(self, *, limit: int = 50) -> list[ScamAnalysis]:
        raise NotImplementedError