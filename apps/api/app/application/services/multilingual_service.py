from app.application.platform_dto import LanguageDetectionDTO, SupportedLanguageDTO

SUPPORTED_LANGUAGES: list[SupportedLanguageDTO] = [
    SupportedLanguageDTO(code="en", name="English", native_name="English"),
    SupportedLanguageDTO(code="hi", name="Hindi", native_name="Hindi"),
    SupportedLanguageDTO(code="es", name="Spanish", native_name="Espanol"),
    SupportedLanguageDTO(code="de", name="German", native_name="Deutsch"),
    SupportedLanguageDTO(code="fr", name="French", native_name="Francais"),
    SupportedLanguageDTO(code="zh", name="Chinese", native_name="Chinese"),
]
SUPPORTED_LANGUAGE_CODES = {item.code for item in SUPPORTED_LANGUAGES}


class MultilingualService:
    def supported_languages(self) -> list[SupportedLanguageDTO]:
        return SUPPORTED_LANGUAGES

    def normalize_language(self, language: str | None, content: str = "") -> str:
        if language and language.lower() in SUPPORTED_LANGUAGE_CODES:
            return language.lower()
        return self.detect_language(content).detected_language

    def detect_language(self, content: str) -> LanguageDetectionDTO:
        lowered = content.lower()
        detected = "en"
        confidence = 0.62

        if any("\u0900" <= char <= "\u097f" for char in content) or any(term in lowered for term in ["otp", "bank", "khata", "turant"]):
            detected = "hi" if any("\u0900" <= char <= "\u097f" for char in content) else detected
            confidence = 0.78 if detected == "hi" else confidence
        if any(term in lowered for term in ["urgente", "banco", "premio", "verificar"]):
            detected = "es"
            confidence = 0.76
        if any(term in lowered for term in ["dringend", "konto", "gewinn", "bestatigen"]):
            detected = "de"
            confidence = 0.76
        if any(term in lowered for term in ["urgent", "banque", "cadeau", "verifiez"]):
            detected = "fr"
            confidence = 0.74
        if any("\u4e00" <= char <= "\u9fff" for char in content):
            detected = "zh"
            confidence = 0.86

        return LanguageDetectionDTO(
            detected_language=detected, confidence=confidence, supported_languages=SUPPORTED_LANGUAGES
        )