from fastapi import APIRouter, Depends, status

from app.application.platform_dto import VoiceScanCommand, VoiceScanDTO
from app.application.services.platform_analysis_service import PlatformAnalysisService
from app.interfaces.api.dependencies import get_platform_analysis_service

router = APIRouter(prefix="/voice", tags=["voice-scam-detection"])


@router.post(
    "/scan-audio",
    response_model=VoiceScanDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Transcribe audio and analyze voice scam risk",
)
def scan_audio(
    command: VoiceScanCommand,
    platform_service: PlatformAnalysisService = Depends(get_platform_analysis_service),
) -> VoiceScanDTO:
    return platform_service.analyze_voice(command)