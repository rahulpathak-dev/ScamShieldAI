import re
from pathlib import Path

from app.application.persuasion_dto import PersuasionDetectionResponse, PersuasionEvidenceDTO, PersuasionModelInfoDTO
from app.core.config import Settings
from app.ml.config import PROJECT_ROOT
from app.ml.preprocessing import clean_text

try:
    from transformers import pipeline
except Exception:  # pragma: no cover - optional ML runtime dependency
    pipeline = None


class PersuasionDetectionService:
    _strategy_terms: dict[str, tuple[str, ...]] = {
        "Urgency": ("urgent", "immediately", "right now", "act now", "within 24 hours", "final notice", "expires today", "do not delay"),
        "Fear": ("blocked", "suspended", "legal action", "arrest", "penalty", "account locked", "unauthorized transaction", "you will lose"),
        "Authority manipulation": ("bank", "police", "government", "tax department", "security team", "support team", "official", "compliance"),
        "Greed": ("guaranteed return", "double your money", "profit", "bonus", "prize", "lottery", "reward", "free money", "high returns"),
        "Scarcity": ("limited time", "last chance", "only today", "few spots", "exclusive offer", "limited seats", "offer ends"),
        "Emotional pressure": ("please help", "i need you", "trust me", "family emergency", "love", "alone", "do this for me", "disappointed"),
        "Fake trust": ("verified", "trusted", "secure", "official partner", "guaranteed safe", "no risk", "approved", "certified"),
        "Social engineering": ("do not tell", "keep this secret", "confidential", "send otp", "share password", "gift card", "wire transfer", "move to whatsapp"),
        "Impersonation": ("i am from", "this is your bank", "customer care", "security department", "ceo", "hr department", "delivery agent", "account officer"),
    }

    _strategy_explanations: dict[str, str] = {
        "Urgency": "The message pressures the recipient to act quickly.",
        "Fear": "The message uses threats, penalties, or account-loss language.",
        "Authority manipulation": "The message invokes institutions or official authority to gain compliance.",
        "Greed": "The message promises rewards, profit, prizes, or unusually attractive returns.",
        "Scarcity": "The message frames the offer as limited or disappearing soon.",
        "Emotional pressure": "The message applies affection, guilt, dependency, or distress.",
        "Fake trust": "The message claims safety, verification, or trustworthiness without proof.",
        "Social engineering": "The message attempts to manipulate behavior or extract sensitive actions.",
        "Impersonation": "The message appears to imitate a person, company, institution, or role.",
    }

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model_path = self._resolve_path(settings.persuasion_classifier_model_path)
        self._classifier = None
        self._load_transformer()

    def detect(self, message: str) -> PersuasionDetectionResponse:
        cleaned = clean_text(message)
        evidence = self._keyword_evidence(cleaned)
        evidence.extend(self._transformer_evidence(message))
        evidence = self._dedupe_evidence(evidence)
        strategies = [item.strategy for item in sorted(evidence, key=lambda item: item.score, reverse=True)]
        return PersuasionDetectionResponse(strategy=strategies, evidence=evidence, model=self.model_info())

    def model_info(self) -> PersuasionModelInfoDTO:
        return PersuasionModelInfoDTO(
            model_name="persuasion_transformer" if self._classifier else "keyword_persuasion_baseline",
            model_type="transformer_multilabel_classifier" if self._classifier else "keyword_analysis",
            artifact_loaded=self._classifier is not None,
            artifact_path=str(self._model_path),
        )

    def _keyword_evidence(self, cleaned: str) -> list[PersuasionEvidenceDTO]:
        evidence: list[PersuasionEvidenceDTO] = []
        for strategy, terms in self._strategy_terms.items():
            matched = [term for term in terms if self._term_matches(cleaned, term)]
            if not matched:
                continue
            score = min(1.0, round(0.35 + 0.18 * len(matched), 4))
            evidence.append(
                PersuasionEvidenceDTO(
                    strategy=strategy,
                    score=score,
                    matched_terms=matched,
                    explanation=self._strategy_explanations[strategy],
                    source="keyword_analysis",
                )
            )
        return evidence

    def _transformer_evidence(self, message: str) -> list[PersuasionEvidenceDTO]:
        if self._classifier is None:
            return []
        predictions = self._classifier(message, candidate_labels=list(self._strategy_terms.keys()), multi_label=True)
        evidence: list[PersuasionEvidenceDTO] = []
        for label, score in zip(predictions.get("labels", []), predictions.get("scores", [])):
            if float(score) < 0.5:
                continue
            evidence.append(
                PersuasionEvidenceDTO(
                    strategy=str(label),
                    score=round(float(score), 4),
                    matched_terms=[],
                    explanation=self._strategy_explanations.get(str(label), "Transformer classifier detected this persuasion strategy."),
                    source="transformer_classification",
                )
            )
        return evidence

    def _dedupe_evidence(self, evidence: list[PersuasionEvidenceDTO]) -> list[PersuasionEvidenceDTO]:
        by_strategy: dict[str, PersuasionEvidenceDTO] = {}
        for item in evidence:
            existing = by_strategy.get(item.strategy)
            if existing is None or item.score > existing.score:
                by_strategy[item.strategy] = item
        return list(by_strategy.values())

    def _load_transformer(self) -> None:
        if pipeline is None or not self._model_path.exists():
            return
        self._classifier = pipeline("zero-shot-classification", model=str(self._model_path))

    def _term_matches(self, cleaned: str, term: str) -> bool:
        return re.search(rf"(?<!\w){re.escape(term)}(?!\w)", cleaned) is not None

    def _resolve_path(self, value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else PROJECT_ROOT / path