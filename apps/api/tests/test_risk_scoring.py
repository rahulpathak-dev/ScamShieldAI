from app.application.services.risk_scoring_service import RiskScoringService
from app.core.config import Settings


def test_risk_scoring_returns_dangerous_for_high_risk_scam_message():
    service = RiskScoringService(Settings(jwt_secret_key="unit-test-secret-key-that-is-long-enough"))

    result = service.score(
        "Urgent bank security alert. Verify OTP now at http://bit.ly/secure or your account will be suspended.",
        user_report_count=3,
        threat_matches=["bit.ly/secure"],
    )

    assert result.risk_score >= 71
    assert result.level == "Dangerous"
    assert "Urgency detected" in result.reasons
    assert any("Threat database match" in reason for reason in result.reasons)


def test_risk_scoring_returns_safe_for_plain_message():
    service = RiskScoringService(Settings(jwt_secret_key="unit-test-secret-key-that-is-long-enough"))

    result = service.score("The project meeting starts tomorrow at 10.")

    assert result.risk_score <= 30
    assert result.level == "Safe"