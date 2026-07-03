import re
from dataclasses import dataclass
from urllib.parse import urlparse

from app.application.risk_dto import RiskFactorDTO, RiskScoreResponse
from app.application.services.nlp_prediction_service import ScamPredictionService
from app.application.services.persuasion_detection_service import PersuasionDetectionService
from app.core.config import Settings
from app.ml.preprocessing import clean_text

URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
IP_URL_PATTERN = re.compile(r"https?://(?:\d{1,3}\.){3}\d{1,3}", re.IGNORECASE)
SHORTENER_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "cutt.ly",
    "rebrand.ly",
}
SUSPICIOUS_KEYWORDS = {
    "otp": "OTP request detected",
    "password": "Password request detected",
    "cvv": "Card CVV request detected",
    "seed phrase": "Crypto seed phrase request detected",
    "private key": "Private key request detected",
    "gift card": "Gift card payment request detected",
    "wire transfer": "Wire transfer pressure detected",
    "account suspended": "Account suspension threat detected",
    "verify now": "Immediate verification demand detected",
    "kyc": "KYC identity pressure detected",
    "guaranteed return": "Guaranteed return claim detected",
}


@dataclass(frozen=True)
class FactorResult:
    name: str
    score: float
    weight: float
    reasons: list[str]

    @property
    def contribution(self) -> float:
        return self.score * self.weight


class RiskScoringService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._ml = ScamPredictionService(settings)
        self._persuasion = PersuasionDetectionService(settings)

    def score(self, message: str, *, user_report_count: int = 0, threat_matches: list[str] | None = None) -> RiskScoreResponse:
        threat_matches = threat_matches or []
        factors = [
            self._ml_factor(message),
            self._persuasion_factor(message),
            self._keyword_factor(message),
            self._url_factor(message),
            self._threat_database_factor(threat_matches),
            self._user_reports_factor(user_report_count),
        ]
        raw_score = sum(factor.contribution for factor in factors)
        final_score = max(0, min(100, round(raw_score)))
        level = self._level(final_score)
        reasons = self._top_reasons(factors)
        return RiskScoreResponse(
            risk_score=final_score,
            level=level,
            reasons=reasons,
            factors=[
                RiskFactorDTO(
                    name=factor.name,
                    score=round(factor.score, 2),
                    weight=factor.weight,
                    contribution=round(factor.contribution, 2),
                    reasons=factor.reasons,
                )
                for factor in factors
            ],
        )

    def _ml_factor(self, message: str) -> FactorResult:
        prediction = self._ml.predict(message)
        reasons = []
        if prediction.is_scam:
            reasons.append(f"ML model predicted scam with {prediction.scam_probability:.0%} probability")
        elif prediction.risk_score >= 30:
            reasons.append("ML model found suspicious language")
        return FactorResult("ML prediction", prediction.risk_score, 0.40, reasons)

    def _persuasion_factor(self, message: str) -> FactorResult:
        result = self._persuasion.detect(message)
        score = min(100.0, len(result.strategy) * 16.0 + sum(item.score for item in result.evidence) * 10.0)
        reasons = [self._strategy_reason(strategy) for strategy in result.strategy[:5]]
        return FactorResult("Persuasion techniques", score, 0.20, reasons)

    def _keyword_factor(self, message: str) -> FactorResult:
        cleaned = clean_text(message)
        reasons = [reason for keyword, reason in SUSPICIOUS_KEYWORDS.items() if keyword in cleaned]
        score = min(100.0, len(reasons) * 18.0)
        return FactorResult("Suspicious keywords", score, 0.18, reasons)

    def _url_factor(self, message: str) -> FactorResult:
        urls = URL_PATTERN.findall(message)
        reasons: list[str] = []
        if urls:
            reasons.append("URL detected")
        if IP_URL_PATTERN.search(message):
            reasons.append("URL uses raw IP address")
        for url in urls:
            parsed = urlparse(url if url.startswith(("http://", "https://")) else f"https://{url}")
            domain = parsed.netloc.casefold().removeprefix("www.")
            if domain in SHORTENER_DOMAINS:
                reasons.append("Shortened URL detected")
            if parsed.scheme == "http":
                reasons.append("Non-HTTPS URL detected")
        score = min(100.0, 20.0 * len(set(reasons)))
        return FactorResult("URL analysis", score, 0.14, sorted(set(reasons)))

    def _threat_database_factor(self, threat_matches: list[str]) -> FactorResult:
        reasons = [f"Threat database match: {match}" for match in threat_matches[:5] if match]
        score = min(100.0, len(reasons) * 60.0)
        return FactorResult("Threat database", score, 0.15, reasons)

    def _user_reports_factor(self, user_report_count: int) -> FactorResult:
        if user_report_count <= 0:
            return FactorResult("User reports", 0.0, 0.08, [])
        score = min(100.0, 25.0 + user_report_count * 10.0)
        return FactorResult("User reports", score, 0.08, [f"Reported by {user_report_count} user(s)"])

    def _level(self, score: int) -> str:
        if score <= 30:
            return "Safe"
        if score <= 70:
            return "Suspicious"
        return "Dangerous"

    def _top_reasons(self, factors: list[FactorResult]) -> list[str]:
        ranked: list[tuple[float, str]] = []
        for factor in factors:
            for reason in factor.reasons:
                ranked.append((factor.contribution, reason))
        deduped: list[str] = []
        for _, reason in sorted(ranked, key=lambda item: item[0], reverse=True):
            if reason not in deduped:
                deduped.append(reason)
        return deduped[:8]

    def _strategy_reason(self, strategy: str) -> str:
        if strategy == "Authority manipulation":
            return "Fake authority detected"
        return f"{strategy} detected"