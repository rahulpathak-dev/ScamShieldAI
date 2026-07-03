from pydantic import BaseModel, Field

from app.application.explainability_dto import ExplainabilityDTO


class ScamPredictionRequest(BaseModel):
    text: str = Field(min_length=3, max_length=20_000)


class ModelInfoDTO(BaseModel):
    model_name: str
    model_type: str
    artifact_loaded: bool
    artifact_path: str | None = None
    metrics: dict | None = None


class ScamPredictionResponse(BaseModel):
    label: str
    is_scam: bool
    scam_probability: float
    confidence: float
    risk_score: float
    model: ModelInfoDTO
    explanation: str
    explainability: ExplainabilityDTO | None = None