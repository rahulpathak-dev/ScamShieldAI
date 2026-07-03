from app.application.services.explainability_service import ExplainabilityService
from app.core.config import Settings


def test_explainability_generates_human_readable_reasons():
    service = ExplainabilityService(Settings(jwt_secret_key="unit-test-secret-key-that-is-long-enough"))

    result = service.explain(
        message="Urgent bank alert. Verify OTP now or your account will be suspended.",
        label="scam",
        risk_score=92,
    )

    assert "The message is suspicious because:" in result.human_readable
    assert "It creates urgency." in result.reasons
    assert "It requests sensitive information." in result.reasons
    assert "It appears to impersonate a trusted organization or role." in result.reasons or "It uses fake authority or institutional pressure." in result.reasons
    assert result.shap.method == "SHAP"
    assert result.lime.method == "LIME"
    assert result.attention.method == "Attention"


def test_explainability_handles_plain_safe_message():
    service = ExplainabilityService(Settings(jwt_secret_key="unit-test-secret-key-that-is-long-enough"))

    result = service.explain(
        message="The meeting is confirmed for tomorrow morning.",
        label="safe",
        risk_score=3,
    )

    assert result.human_readable == "The message does not show strong scam indicators based on the available signals."
    assert result.reasons == []