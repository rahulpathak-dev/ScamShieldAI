from fastapi import APIRouter, Depends, status

from app.application.platform_dto import MobileScreenshotScanCommand, MobileSmsScanCommand, PlatformAnalysisDTO
from app.application.services.platform_analysis_service import PlatformAnalysisService
from app.interfaces.api.dependencies import get_platform_analysis_service

router = APIRouter(prefix="/mobile", tags=["mobile"])


@router.post("/scan-sms", response_model=PlatformAnalysisDTO, status_code=status.HTTP_201_CREATED, summary="Scan SMS content")
def scan_sms(
    command: MobileSmsScanCommand,
    platform_service: PlatformAnalysisService = Depends(get_platform_analysis_service),
) -> PlatformAnalysisDTO:
    return platform_service.analyze_mobile_sms(command)


@router.post(
    "/scan-screenshot",
    response_model=PlatformAnalysisDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze screenshot OCR text for scam risk",
)
def scan_screenshot(
    command: MobileScreenshotScanCommand,
    platform_service: PlatformAnalysisService = Depends(get_platform_analysis_service),
) -> PlatformAnalysisDTO:
    return platform_service.analyze_mobile_screenshot(command)