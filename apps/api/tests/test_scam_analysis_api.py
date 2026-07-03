from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_text_detects_high_risk_banking_phishing():
    response = client.post(
        "/api/v1/analyze/text",
        json={
            "content": "Urgent bank alert: your account is suspended. Verify OTP now at https://bit.ly/secure-bank",
            "source_type": "sms",
            "language": "en",
        },
    )

    payload = response.json()

    assert response.status_code == 201
    assert payload["risk_level"] in {"high", "critical"}
    assert "phishing" in payload["scam_categories"]
    assert "banking_fraud" in payload["scam_categories"]
    assert "urgency" in payload["persuasion_strategies"]
    assert any(item["signal"] == "credential_request" for item in payload["evidence"])


def test_analyze_text_low_risk_message_stays_low():
    response = client.post(
        "/api/v1/analyze/text",
        json={
            "content": "Hi, the meeting agenda is attached for tomorrow.",
            "source_type": "email",
            "language": "en",
        },
    )

    payload = response.json()

    assert response.status_code == 201
    assert payload["risk_level"] == "low"
    assert payload["risk_score"] == 0

