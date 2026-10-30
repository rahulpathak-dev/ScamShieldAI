from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.application.dto import AnalyzeTextCommand, ScamAnalysisDTO
from app.application.use_cases.analyze_text_message import AnalyzeTextMessageUseCase
from app.domain.repositories import AnalysisRepository
from app.interfaces.api.dependencies import get_analysis_repository, get_analyze_text_use_case

router = APIRouter(prefix="/analyze", tags=["analysis"])


@router.post(
    "/text",
    response_model=ScamAnalysisDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze text for scam risk",
)
def analyze_text(
    command: AnalyzeTextCommand,
    use_case: AnalyzeTextMessageUseCase = Depends(get_analyze_text_use_case),
) -> ScamAnalysisDTO:
    return use_case.execute(command)


@router.get(
    "/history",
    response_model=list[ScamAnalysisDTO],
    summary="List recent scam analysis history",
)
def list_analysis_history(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    repository: AnalysisRepository = Depends(get_analysis_repository),
) -> list[ScamAnalysisDTO]:
    return [ScamAnalysisDTO.from_domain(item) for item in repository.list_recent(limit=limit)]