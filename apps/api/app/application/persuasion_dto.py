from pydantic import BaseModel, Field


class PersuasionDetectionRequest(BaseModel):
    message: str = Field(min_length=3, max_length=20_000)


class PersuasionEvidenceDTO(BaseModel):
    strategy: str
    score: float
    matched_terms: list[str]
    explanation: str
    source: str


class PersuasionModelInfoDTO(BaseModel):
    model_name: str
    model_type: str
    artifact_loaded: bool
    artifact_path: str | None = None


class PersuasionDetectionResponse(BaseModel):
    strategy: list[str]
    evidence: list[PersuasionEvidenceDTO]
    model: PersuasionModelInfoDTO