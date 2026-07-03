from app.application.services.cybersecurity_assistant_service import CybersecurityAssistantService
from app.core.config import Settings


def test_assistant_answers_with_local_fallback_and_risk_analysis():
    service = CybersecurityAssistantService(Settings(jwt_secret_key="unit-test-secret-key-that-is-long-enough"))

    result = service.answer(
        question="Is this message dangerous?",
        message="Urgent bank alert. Verify OTP now or your account will be suspended.",
        provider="local",
    )

    assert "Risk analysis" in result.answer
    assert result.risk_analysis.level in {"Suspicious", "Dangerous"}
    assert result.safety_advice
    assert result.provider.provider == "local"
    assert not result.provider.used_llm