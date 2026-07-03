from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

NotificationChannel = Literal["browser", "email"]
NotificationSeverity = Literal["info", "warning", "critical"]
NotificationDeliveryStatus = Literal["sent", "skipped", "failed"]


class HighRiskWarningCommand(BaseModel):
    analysis_id: UUID | None = None
    risk_score: float = Field(ge=0, le=100)
    scam_probability: float | None = Field(default=None, ge=0, le=100)
    risk_level: str = Field(min_length=2, max_length=32)
    message_excerpt: str = Field(min_length=3, max_length=500)
    reasons: list[str] = Field(default_factory=list, max_length=10)
    recipient_email: EmailStr | None = None
    channels: list[NotificationChannel] = Field(default_factory=lambda: ["browser"])


class NotificationDeliveryDTO(BaseModel):
    channel: NotificationChannel
    status: NotificationDeliveryStatus
    detail: str


class HighRiskWarningDTO(BaseModel):
    severity: NotificationSeverity
    title: str
    body: str
    risk_score: float
    scam_probability: float
    recommended_actions: list[str]
    deliveries: list[NotificationDeliveryDTO]