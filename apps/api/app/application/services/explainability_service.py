from __future__ import annotations

import re
from collections import Counter
from typing import Sequence

from app.application.explainability_dto import ExplainabilityDTO, ExplanationMethodDTO, TokenAttributionDTO
from app.application.persuasion_dto import PersuasionDetectionResponse
from app.application.risk_dto import RiskScoreResponse
from app.application.services.persuasion_detection_service import PersuasionDetectionService
from app.core.config import Settings
from app.ml.preprocessing import clean_text, tokenize

try:
    import shap
except Exception:  # pragma: no cover - optional ML dependency
    shap = None

try:
    from lime.lime_text import LimeTextExplainer
except Exception:  # pragma: no cover - optional ML dependency
    LimeTextExplainer = None

URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
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


class ExplainabilityService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._persuasion = PersuasionDetectionService(settings)

    def explain(
        self,
        *,
        message: str,
        label: str,
        risk_score: float,
        model=None,
        risk_result: RiskScoreResponse | None = None,
        persuasion_result: PersuasionDetectionResponse | None = None,
    ) -> ExplainabilityDTO:
        persuasion = persuasion_result or self._persuasion.detect(message)
        reasons = self._reasons(message, label, risk_score, persuasion, risk_result)
        return ExplainabilityDTO(
            human_readable=self._human_readable(label, reasons),
            reasons=reasons,
            shap=self._shap_explanation(message, model),
            lime=self._lime_explanation(message, model),
            attention=self._attention_explanation(model),
        )

    def _reasons(
        self,
        message: str,
        label: str,
        risk_score: float,
        persuasion: PersuasionDetectionResponse,
        risk_result: RiskScoreResponse | None,
    ) -> list[str]:
        reasons: list[str] = []
        cleaned = clean_text(message)

        for strategy in persuasion.strategy:
            if strategy == "Urgency":
                reasons.append("It creates urgency.")
            elif strategy == "Fear":
                reasons.append("It uses fear or threat language.")
            elif strategy == "Authority manipulation":
                reasons.append("It uses fake authority or institutional pressure.")
            elif strategy == "Impersonation":
                reasons.append("It appears to impersonate a trusted organization or role.")
            elif strategy == "Greed":
                reasons.append("It promises unrealistic rewards or profit.")
            elif strategy == "Scarcity":
                reasons.append("It uses scarcity or limited-time pressure.")
            elif strategy == "Emotional pressure":
                reasons.append("It applies emotional pressure.")
            elif strategy == "Fake trust":
                reasons.append("It makes unsupported trust or safety claims.")
            elif strategy == "Social engineering":
                reasons.append("It attempts to manipulate the recipient into unsafe action.")

        for keyword, reason in SUSPICIOUS_KEYWORDS.items():
            if keyword in cleaned:
                if keyword in {"otp", "password", "cvv", "seed phrase", "private key"}:
                    reasons.append("It requests sensitive information.")
                else:
                    reasons.append(reason)

        if URL_PATTERN.search(message):
            reasons.append("It includes a link that should be verified before clicking.")

        if risk_result:
            reasons.extend(risk_result.reasons)

        if label == "scam" and risk_score >= 70:
            reasons.append("The combined AI risk score is in the dangerous range.")
        elif label == "scam":
            reasons.append("The AI classifier found scam-like language.")

        return self._dedupe(reasons)[:8]

    def _human_readable(self, label: str, reasons: Sequence[str]) -> str:
        if not reasons:
            return "The message does not show strong scam indicators based on the available signals."
        heading = "The message is suspicious because:" if label == "scam" else "The message has some risk signals because:"
        return "\n".join([heading, *[f"{index}. {reason}" for index, reason in enumerate(reasons, start=1)]])

    def _shap_explanation(self, message: str, model) -> ExplanationMethodDTO:
        if shap is None:
            return ExplanationMethodDTO(method="SHAP", available=False, summary="SHAP is not installed in the current runtime.")
        if model is None or not hasattr(model, "predict_proba"):
            return ExplanationMethodDTO(method="SHAP", available=False, summary="SHAP requires a loaded probability-capable model artifact.")
        try:
            masker = shap.maskers.Text(r"\W+")
            explainer = shap.Explainer(lambda texts: model.predict_proba(list(texts))[:, 1], masker)
            values = explainer([message])
            tokens = [
                TokenAttributionDTO(token=str(token), score=round(float(score), 4))
                for token, score in zip(values.data[0], values.values[0])
                if str(token).strip()
            ]
            tokens = sorted(tokens, key=lambda item: abs(item.score), reverse=True)[:10]
            return ExplanationMethodDTO(method="SHAP", available=True, summary="SHAP token attribution generated for scam probability.", tokens=tokens)
        except Exception as exc:  # pragma: no cover - defensive runtime guard
            return ExplanationMethodDTO(method="SHAP", available=False, summary=f"SHAP explanation failed: {exc.__class__.__name__}", tokens=self._heuristic_token_scores(message))

    def _lime_explanation(self, message: str, model) -> ExplanationMethodDTO:
        if LimeTextExplainer is None:
            return ExplanationMethodDTO(method="LIME", available=False, summary="LIME is not installed in the current runtime.")
        if model is None or not hasattr(model, "predict_proba"):
            return ExplanationMethodDTO(method="LIME", available=False, summary="LIME requires a loaded probability-capable model artifact.")
        try:
            explainer = LimeTextExplainer(class_names=["safe", "scam"])
            explanation = explainer.explain_instance(message, model.predict_proba, num_features=8, labels=[1])
            tokens = [TokenAttributionDTO(token=token, score=round(float(score), 4)) for token, score in explanation.as_list(label=1)]
            return ExplanationMethodDTO(method="LIME", available=True, summary="LIME local explanation generated for scam class.", tokens=tokens)
        except Exception as exc:  # pragma: no cover - defensive runtime guard
            return ExplanationMethodDTO(method="LIME", available=False, summary=f"LIME explanation failed: {exc.__class__.__name__}")

    def _attention_explanation(self, model) -> ExplanationMethodDTO:
        if model is None or not hasattr(model, "config"):
            return ExplanationMethodDTO(method="Attention", available=False, summary="Attention visualization requires a loaded transformer model artifact.")
        return ExplanationMethodDTO(
            method="Attention",
            available=False,
            summary="Transformer artifact detected, but tokenizer and attention tensors are not exposed by the current prediction service yet.",
        )

    def _heuristic_token_scores(self, message: str) -> list[TokenAttributionDTO]:
        suspicious_terms = set(SUSPICIOUS_KEYWORDS) | {"urgent", "suspended", "verify", "bank", "otp", "password", "prize", "guaranteed"}
        counts = Counter(tokenize(message))
        scored = []
        for token, count in counts.items():
            base = 0.2 if token in suspicious_terms else 0.03
            if token.endswith("_token"):
                base = 0.15
            scored.append(TokenAttributionDTO(token=token, score=round(base * count, 4)))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:10]

    def _dedupe(self, values: Sequence[str]) -> list[str]:
        deduped: list[str] = []
        for value in values:
            normalized = re.sub(r"\s+", " ", value).strip()
            if normalized and normalized not in deduped:
                deduped.append(normalized)
        return deduped