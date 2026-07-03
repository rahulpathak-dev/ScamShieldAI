from pydantic import BaseModel, Field

from app.application.risk_dto import RiskScoreResponse


class AssistantChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4_000)
    message: str = Field(min_length=3, max_length=20_000)
    provider: str | None = Field(default=None, pattern="^(openai|gemini|llama|local)$")


class AssistantSourceDTO(BaseModel):
    source: str
    score: float
    excerpt: str


class AssistantProviderDTO(BaseModel):
    provider: str
    model: str
    used_llm: bool


class AssistantChatResponse(BaseModel):
    answer: str
    scam_explanation: str
    risk_analysis: RiskScoreResponse
    safety_advice: list[str]
    sources: list[AssistantSourceDTO]
    provider: AssistantProviderDTO