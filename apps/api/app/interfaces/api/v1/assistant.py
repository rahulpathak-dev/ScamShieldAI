from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.assistant_dto import AssistantChatRequest, AssistantChatResponse
from app.application.services.cybersecurity_assistant_service import CybersecurityAssistantService
from app.core.config import Settings, get_settings

router = APIRouter(prefix="/assistant", tags=["assistant"])


def get_assistant_service(settings: Annotated[Settings, Depends(get_settings)]) -> CybersecurityAssistantService:
    return CybersecurityAssistantService(settings)


@router.post("/chat", response_model=AssistantChatResponse, summary="Ask ScamShieldAI cybersecurity assistant")
def chat(
    payload: AssistantChatRequest,
    service: Annotated[CybersecurityAssistantService, Depends(get_assistant_service)],
) -> AssistantChatResponse:
    return service.answer(question=payload.question, message=payload.message, provider=payload.provider)