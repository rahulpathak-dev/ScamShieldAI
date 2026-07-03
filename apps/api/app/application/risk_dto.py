from pydantic import BaseModel, ConfigDict, Field


class RiskScoreRequest(BaseModel):
    message: str = Field(min_length=3, max_length=20_000)
    user_report_count: int = Field(default=0, ge=0, le=10_000)
    threat_matches: list[str] = Field(default_factory=list, max_length=100)


class RiskFactorDTO(BaseModel):
    name: str
    score: float
    weight: float
    contribution: float
    reasons: list[str]


class RiskScoreResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    risk_score: int = Field(alias="Risk Score", ge=0, le=100)
    level: str = Field(alias="Level")
    reasons: list[str] = Field(alias="Reasons")
    factors: list[RiskFactorDTO]