from fastapi import APIRouter, Depends, status

from app.application.dto import AnalyzeTextCommand, ScamAnalysisDTO
from app.application.use_cases.analyze_text_message import AnalyzeTextMessageUseCase
from app.interfaces.api.dependencies import get_analyze_text_use_case

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
