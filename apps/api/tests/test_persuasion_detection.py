from app.application.services.persuasion_detection_service import PersuasionDetectionService
from app.core.config import Settings


def test_persuasion_detector_finds_urgency_fear_and_impersonation():
    service = PersuasionDetectionService(Settings(jwt_secret_key="unit-test-secret-key-that-is-long-enough"))

    result = service.detect("This is your bank security department. Urgent: verify OTP now or your account will be suspended.")

    assert "Urgency" in result.strategy
    assert "Fear" in result.strategy
    assert "Authority manipulation" in result.strategy
    assert "Impersonation" in result.strategy


def test_persuasion_detector_returns_empty_strategy_for_plain_message():
    service = PersuasionDetectionService(Settings(jwt_secret_key="unit-test-secret-key-that-is-long-enough"))

    result = service.detect("The project meeting starts at 10 tomorrow morning.")

    assert result.strategy == []