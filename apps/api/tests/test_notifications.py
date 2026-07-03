from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_high_risk_warning_generates_browser_payload():
    response = client.post(
        "/api/v1/notifications/high-risk-warning",
        json={
            "risk_score": 95,
            "scam_probability": 95,
            "risk_level": "critical",
            "message_excerpt": "Urgent bank alert: verify OTP now.",
            "reasons": ["Urgency detected", "Fake authority detected"],
            "channels": ["browser"],
        },
    )

    payload = response.json()

    assert response.status_code == 202
    assert payload["severity"] == "critical"
    assert payload["body"] == "Warning: This message has 95% scam probability."
    assert payload["deliveries"] == [
        {
            "channel": "browser",
            "status": "sent",
            "detail": "Browser notification payload generated for the client.",
        }
    ]


def test_email_warning_skips_when_email_is_disabled():
    response = client.post(
        "/api/v1/notifications/high-risk-warning",
        json={
            "risk_score": 88,
            "risk_level": "high",
            "message_excerpt": "Claim your crypto airdrop fee now.",
            "recipient_email": "security@example.com",
            "channels": ["email"],
        },
    )

    payload = response.json()

    assert response.status_code == 202
    assert payload["severity"] == "warning"
    assert payload["deliveries"][0]["channel"] == "email"
    assert payload["deliveries"][0]["status"] == "skipped"