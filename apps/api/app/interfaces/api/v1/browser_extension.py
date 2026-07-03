from fastapi import APIRouter, Depends, status

from app.application.platform_dto import BrowserPageScanCommand, PlatformAnalysisDTO
from app.application.services.platform_analysis_service import PlatformAnalysisService
from app.interfaces.api.dependencies import get_platform_analysis_service

router = APIRouter(prefix="/browser-extension", tags=["browser-extension"])


@router.post(
    "/scan-page",
    response_model=PlatformAnalysisDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Scan browser page content for scam risk",
)
def scan_browser_page(
    command: BrowserPageScanCommand,
    platform_service: PlatformAnalysisService = Depends(get_platform_analysis_service),
) -> PlatformAnalysisDTO:
    return platform_service.analyze_browser_page(command)