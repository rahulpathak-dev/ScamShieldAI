from typing import Annotated

from fastapi import APIRouter, Depends, Header, status

from app.application.platform_dto import EnterpriseBatchAnalyzeCommand, EnterpriseBatchAnalyzeDTO
from app.application.services.platform_analysis_service import PlatformAnalysisService
from app.core.config import Settings, get_settings
from app.core.errors import AuthenticationError, AuthorizationError
from app.interfaces.api.dependencies import get_platform_analysis_service

router = APIRouter(prefix="/enterprise", tags=["enterprise-api"])


def require_enterprise_api_key(
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
    settings: Settings = Depends(get_settings),
) -> str:
    if not x_api_key:
        raise AuthenticationError("Missing enterprise API key.")

    allowed_keys = {key.strip() for key in settings.enterprise_api_keys.split(",") if key.strip()}
    if not allowed_keys or x_api_key not in allowed_keys:
        raise AuthorizationError("Invalid enterprise API key.")
    return x_api_key


@router.post(
    "/batch-analyze",
    response_model=EnterpriseBatchAnalyzeDTO,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Batch analyze messages for enterprise tenants",
)
def batch_analyze(
    command: EnterpriseBatchAnalyzeCommand,
    _: Annotated[str, Depends(require_enterprise_api_key)],
    settings: Settings = Depends(get_settings),
    platform_service: PlatformAnalysisService = Depends(get_platform_analysis_service),
) -> EnterpriseBatchAnalyzeDTO:
    return platform_service.analyze_enterprise_batch(command, max_batch_size=settings.enterprise_max_batch_size)