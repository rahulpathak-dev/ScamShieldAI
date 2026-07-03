from fastapi import APIRouter, Depends

from app.application.platform_dto import LanguageDetectionCommand, LanguageDetectionDTO, SupportedLanguageDTO
from app.application.services.multilingual_service import MultilingualService
from app.interfaces.api.dependencies import get_multilingual_service

router = APIRouter(prefix="/i18n", tags=["multi-language"])


@router.get("/languages", response_model=list[SupportedLanguageDTO], summary="List supported languages")
def list_supported_languages(
    multilingual_service: MultilingualService = Depends(get_multilingual_service),
) -> list[SupportedLanguageDTO]:
    return multilingual_service.supported_languages()


@router.post("/detect-language", response_model=LanguageDetectionDTO, summary="Detect supported scam analysis language")
def detect_language(
    command: LanguageDetectionCommand,
    multilingual_service: MultilingualService = Depends(get_multilingual_service),
) -> LanguageDetectionDTO:
    return multilingual_service.detect_language(command.content)