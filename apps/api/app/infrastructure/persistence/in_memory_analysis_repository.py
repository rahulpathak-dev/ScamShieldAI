from uuid import UUID

from app.domain.entities import ScamAnalysis
from app.domain.repositories import AnalysisRepository


class InMemoryAnalysisRepository(AnalysisRepository):
    def __init__(self) -> None:
        self._items: dict[UUID, ScamAnalysis] = {}

    def save(self, analysis: ScamAnalysis) -> ScamAnalysis:
        self._items[analysis.id] = analysis
        return analysis

    def get(self, analysis_id: UUID) -> ScamAnalysis | None:
        return self._items.get(analysis_id)

