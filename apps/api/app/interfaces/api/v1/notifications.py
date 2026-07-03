from fastapi import APIRouter, Depends, status

from app.application.notification_dto import HighRiskWarningCommand, HighRiskWarningDTO
from app.application.services.notification_service import NotificationService
from app.interfaces.api.dependencies import get_notification_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post(
    "/high-risk-warning",
    response_model=HighRiskWarningDTO,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create and deliver a high-risk scam warning",
)
def create_high_risk_warning(
    command: HighRiskWarningCommand,
    notification_service: NotificationService = Depends(get_notification_service),
) -> HighRiskWarningDTO:
    return notification_service.create_high_risk_warning(command)