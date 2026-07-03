from typing import Literal

from pydantic import BaseModel, Field

from app.application.dto import ScamAnalysisDTO
from app.domain.entities import SourceType

SupportedLanguageCode = Literal["en", "hi", "es", "de", "fr", "zh"]


class SupportedLanguageDTO(BaseModel):
    code: SupportedLanguageCode
    name: str
    native_name: str
    enabled: bool = True


class LanguageDetectionCommand(BaseModel):
    content: str = Field(min_length=3, max_length=20_000)


class LanguageDetectionDTO(BaseModel):
    detected_language: SupportedLanguageCode
    confidence: float = Field(ge=0, le=1)
    supported_languages: list[SupportedLanguageDTO]


class BrowserPageScanCommand(BaseModel):
    page_url: str = Field(min_length=3, max_length=2048)
    page_title: str | None = Field(default=None, max_length=300)
    visible_text: str = Field(min_length=3, max_length=50_000)
    language: SupportedLanguageCode | None = None


class MobileSmsScanCommand(BaseModel):
    sender: str | None = Field(default=None, max_length=120)
    content: str = Field(min_length=3, max_length=20_000)
    received_at: str | None = Field(default=None, max_length=64)
    language: SupportedLanguageCode | None = None


class MobileScreenshotScanCommand(BaseModel):
    image_base64: str = Field(min_length=20, max_length=8_000_000)
    ocr_text: str | None = Field(default=None, max_length=20_000)
    language: SupportedLanguageCode | None = None


class VoiceScanCommand(BaseModel):
    audio_base64: str = Field(min_length=20, max_length=15_000_000)
    filename: str | None = Field(default=None, max_length=255)
    mime_type: str | None = Field(default=None, max_length=120)
    transcript: str | None = Field(default=None, max_length=20_000)
    language: SupportedLanguageCode | None = None


class VoiceScanDTO(BaseModel):
    transcript: str
    speech_recognition_engine: str
    analysis: ScamAnalysisDTO


class EnterpriseAnalyzeItem(BaseModel):
    external_id: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=3, max_length=20_000)
    source_type: SourceType = SourceType.chat
    language: SupportedLanguageCode | None = None


class EnterpriseBatchAnalyzeCommand(BaseModel):
    tenant_id: str = Field(min_length=2, max_length=120)
    items: list[EnterpriseAnalyzeItem] = Field(min_length=1, max_length=100)


class EnterpriseAnalyzeResult(BaseModel):
    external_id: str
    analysis: ScamAnalysisDTO


class EnterpriseBatchAnalyzeDTO(BaseModel):
    tenant_id: str
    results: list[EnterpriseAnalyzeResult]
    max_batch_size: int


class PlatformAnalysisDTO(BaseModel):
    channel: Literal["browser_extension", "mobile_sms", "mobile_screenshot"]
    normalized_language: SupportedLanguageCode
    analysis: ScamAnalysisDTO