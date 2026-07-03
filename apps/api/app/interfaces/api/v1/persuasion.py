from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.persuasion_dto import PersuasionDetectionRequest, PersuasionDetectionResponse
from app.application.services.persuasion_detection_service import PersuasionDetectionService
from app.core.config import Settings, get_settings

router = APIRouter(prefix="/persuasion", tags=["persuasion"])


def get_persuasion_service(settings: Annotated[Settings, Depends(get_settings)]) -> PersuasionDetectionService:
    return PersuasionDetectionService(settings)


@router.post("/detect", response_model=PersuasionDetectionResponse, summary="Detect psychological persuasion strategies")
def detect_persuasion(
    payload: PersuasionDetectionRequest,
    service: Annotated[PersuasionDetectionService, Depends(get_persuasion_service)],
) -> PersuasionDetectionResponse:
    return service.detect(payload.message)