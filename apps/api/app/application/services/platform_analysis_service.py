from app.application.dto import AnalyzeTextCommand, ScamAnalysisDTO
from app.application.platform_dto import (
    BrowserPageScanCommand,
    EnterpriseBatchAnalyzeCommand,
    EnterpriseBatchAnalyzeDTO,
    EnterpriseAnalyzeResult,
    MobileScreenshotScanCommand,
    MobileSmsScanCommand,
    PlatformAnalysisDTO,
    VoiceScanCommand,
    VoiceScanDTO,
)
from app.application.services.multilingual_service import MultilingualService
from app.application.use_cases.analyze_text_message import AnalyzeTextMessageUseCase
from app.domain.entities import SourceType


class PlatformAnalysisService:
    def __init__(self, analyze_use_case: AnalyzeTextMessageUseCase, multilingual_service: MultilingualService) -> None:
        self._analyze_use_case = analyze_use_case
        self._multilingual_service = multilingual_service

    def analyze_browser_page(self, command: BrowserPageScanCommand) -> PlatformAnalysisDTO:
        language = self._multilingual_service.normalize_language(command.language, command.visible_text)
        content = f"URL: {command.page_url}\nTitle: {command.page_title or ''}\nText: {command.visible_text}"
        analysis = self._analyze(content=content, source_type=SourceType.social, language=language)
        return PlatformAnalysisDTO(channel="browser_extension", normalized_language=language, analysis=analysis)

    def analyze_mobile_sms(self, command: MobileSmsScanCommand) -> PlatformAnalysisDTO:
        language = self._multilingual_service.normalize_language(command.language, command.content)
        content = f"Sender: {command.sender or 'unknown'}\nMessage: {command.content}"
        analysis = self._analyze(content=content, source_type=SourceType.sms, language=language)
        return PlatformAnalysisDTO(channel="mobile_sms", normalized_language=language, analysis=analysis)

    def analyze_mobile_screenshot(self, command: MobileScreenshotScanCommand) -> PlatformAnalysisDTO:
        extracted_text = command.ocr_text or "Screenshot OCR text is pending extraction. Manual review required."
        language = self._multilingual_service.normalize_language(command.language, extracted_text)
        analysis = self._analyze(content=extracted_text, source_type=SourceType.screenshot_ocr, language=language)
        return PlatformAnalysisDTO(channel="mobile_screenshot", normalized_language=language, analysis=analysis)

    def analyze_voice(self, command: VoiceScanCommand) -> VoiceScanDTO:
        transcript = command.transcript or self._placeholder_transcribe(command)
        language = self._multilingual_service.normalize_language(command.language, transcript)
        analysis = self._analyze(content=transcript, source_type=SourceType.voice_transcript, language=language)
        return VoiceScanDTO(
            transcript=transcript,
            speech_recognition_engine="external_stt_placeholder",
            analysis=analysis,
        )

    def analyze_enterprise_batch(self, command: EnterpriseBatchAnalyzeCommand, max_batch_size: int) -> EnterpriseBatchAnalyzeDTO:
        results: list[EnterpriseAnalyzeResult] = []
        for item in command.items[:max_batch_size]:
            language = self._multilingual_service.normalize_language(item.language, item.content)
            analysis = self._analyze(content=item.content, source_type=item.source_type, language=language)
            results.append(EnterpriseAnalyzeResult(external_id=item.external_id, analysis=analysis))
        return EnterpriseBatchAnalyzeDTO(tenant_id=command.tenant_id, results=results, max_batch_size=max_batch_size)

    def _analyze(self, content: str, source_type: SourceType, language: str) -> ScamAnalysisDTO:
        return self._analyze_use_case.execute(
            AnalyzeTextCommand(content=content, source_type=source_type, language=language)
        )

    def _placeholder_transcribe(self, command: VoiceScanCommand) -> str:
        filename = command.filename or "uploaded audio"
        return f"Speech recognition transcript pending for {filename}. Treat this audio as unverified until STT completes."