import json
from pathlib import Path
from typing import Any

import joblib

from app.application.nlp_dto import ModelInfoDTO, ScamPredictionResponse
from app.application.services.explainability_service import ExplainabilityService
from app.core.config import Settings
from app.domain.entities import SourceType
from app.domain.services.risk_engine import ScamRiskEngine
from app.ml.config import PROJECT_ROOT
from app.ml.preprocessing import clean_text


class ScamPredictionService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model_path = self._resolve_path(settings.scam_classifier_model_path)
        self._model_card_path = self._resolve_path(settings.scam_classifier_model_card_path)
        self._model = None
        self._model_card: dict[str, Any] | None = None
        self._risk_engine = ScamRiskEngine()
        self._explainability = ExplainabilityService(settings)
        self._load_artifacts()

    def predict(self, text: str) -> ScamPredictionResponse:
        cleaned = clean_text(text)
        if self._model is not None:
            label_id, probability = self._predict_with_model(cleaned)
            label = "scam" if label_id == 1 else "safe"
            risk_score = round(probability * 100, 2)
            explainability = self._explainability.explain(
                message=text,
                label=label,
                risk_score=risk_score,
                model=self._model,
            )
            return ScamPredictionResponse(
                label=label,
                is_scam=label == "scam",
                scam_probability=round(probability, 4),
                confidence=round(max(probability, 1 - probability), 4),
                risk_score=risk_score,
                model=self.model_info(),
                explanation=explainability.human_readable,
                explainability=explainability,
            )

        fallback = self._risk_engine.analyze(content=text, source_type=SourceType.chat, language="en")
        probability = fallback.risk_score / 100
        label = "scam" if fallback.risk_score >= 60 else "safe"
        explainability = self._explainability.explain(
            message=text,
            label=label,
            risk_score=fallback.risk_score,
            model=None,
        )
        return ScamPredictionResponse(
            label=label,
            is_scam=fallback.risk_score >= 60,
            scam_probability=round(probability, 4),
            confidence=round(max(probability, 1 - probability), 4),
            risk_score=fallback.risk_score,
            model=self.model_info(),
            explanation=explainability.human_readable,
            explainability=explainability,
        )

    def model_info(self) -> ModelInfoDTO:
        if self._model_card:
            return ModelInfoDTO(
                model_name=str(self._model_card.get("model_name", "unknown")),
                model_type=str(self._model_card.get("model_type", "unknown")),
                artifact_loaded=self._model is not None,
                artifact_path=str(self._model_path),
                metrics=self._model_card.get("best_metrics") or self._model_card.get("metrics"),
            )
        return ModelInfoDTO(
            model_name="rule_baseline",
            model_type="explainable_keyword_risk_engine",
            artifact_loaded=False,
            artifact_path=str(self._model_path),
            metrics=None,
        )

    def _load_artifacts(self) -> None:
        if self._model_path.exists():
            self._model = joblib.load(self._model_path)
        if self._model_card_path.exists():
            self._model_card = json.loads(self._model_card_path.read_text(encoding="utf-8"))

    def _predict_with_model(self, cleaned_text: str) -> tuple[int, float]:
        prediction = int(self._model.predict([cleaned_text])[0])
        if hasattr(self._model, "predict_proba"):
            probabilities = self._model.predict_proba([cleaned_text])[0]
            scam_probability = float(probabilities[1])
        else:
            scam_probability = 1.0 if prediction == 1 else 0.0
        return prediction, scam_probability

    def _resolve_path(self, value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else PROJECT_ROOT / path