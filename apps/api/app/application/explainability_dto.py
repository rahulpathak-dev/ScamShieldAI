from pydantic import BaseModel, Field


class TokenAttributionDTO(BaseModel):
    token: str
    score: float


class ExplanationMethodDTO(BaseModel):
    method: str
    available: bool
    summary: str
    tokens: list[TokenAttributionDTO] = Field(default_factory=list)


class ExplainabilityDTO(BaseModel):
    human_readable: str
    reasons: list[str]
    shap: ExplanationMethodDTO
    lime: ExplanationMethodDTO
    attention: ExplanationMethodDTO