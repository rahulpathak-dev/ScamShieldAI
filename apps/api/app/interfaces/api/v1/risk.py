from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.risk_dto import RiskScoreRequest, RiskScoreResponse
from app.application.services.risk_scoring_service import RiskScoringService
from app.core.config import Settings, get_settings

router = APIRouter(prefix="/risk", tags=["risk"])


def get_risk_scoring_service(settings: Annotated[Settings, Depends(get_settings)]) -> RiskScoringService:
    return RiskScoringService(settings)


@router.post("/score", response_model=RiskScoreResponse, response_model_by_alias=True, summary="Generate intelligent scam risk score")
def score_risk(
    payload: RiskScoreRequest,
    service: Annotated[RiskScoringService, Depends(get_risk_scoring_service)],
) -> RiskScoreResponse:
    return service.score(
        payload.message,
        user_report_count=payload.user_report_count,
        threat_matches=payload.threat_matches,
    )