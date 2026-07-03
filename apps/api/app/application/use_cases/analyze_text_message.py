from app.application.dto import AnalyzeTextCommand, ScamAnalysisDTO
from app.domain.repositories import AnalysisRepository
from app.domain.services.risk_engine import ScamRiskEngine


class AnalyzeTextMessageUseCase:
    def __init__(self, risk_engine: ScamRiskEngine, repository: AnalysisRepository) -> None:
        self._risk_engine = risk_engine
        self._repository = repository

    def execute(self, command: AnalyzeTextCommand) -> ScamAnalysisDTO:
        analysis = self._risk_engine.analyze(
            content=command.content,
            source_type=command.source_type,
            language=command.language,
        )
        saved = self._repository.save(analysis)
        return ScamAnalysisDTO.from_domain(saved)

