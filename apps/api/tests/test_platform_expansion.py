from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_supported_languages_include_requested_global_languages():
    response = client.get("/api/v1/i18n/languages")

    assert response.status_code == 200
    codes = {item["code"] for item in response.json()}
    assert {"en", "hi", "es", "de", "fr", "zh"}.issubset(codes)


def test_mobile_sms_scan_uses_analysis_pipeline():
    response = client.post(
        "/api/v1/mobile/scan-sms",
        json={"sender": "BANK", "content": "Urgent bank alert. Verify OTP now or account suspended.", "language": "en"},
    )

    payload = response.json()

    assert response.status_code == 201
    assert payload["channel"] == "mobile_sms"
    assert payload["analysis"]["risk_level"] in {"high", "critical"}


def test_voice_scan_transcript_flows_to_analysis():
    response = client.post(
        "/api/v1/voice/scan-audio",
        json={
            "audio_base64": "dGhpcyBpcyBhIHBsYWNlaG9sZGVyIGF1ZGlvIHBheWxvYWQ=",
            "transcript": "Urgent crypto wallet verification required now.",
            "language": "en",
        },
    )

    payload = response.json()

    assert response.status_code == 201
    assert payload["transcript"] == "Urgent crypto wallet verification required now."
    assert payload["analysis"]["source_type"] == "voice_transcript"


def test_enterprise_batch_requires_api_key():
    response = client.post(
        "/api/v1/enterprise/batch-analyze",
        json={
            "tenant_id": "acme-bank",
            "items": [{"external_id": "msg-1", "content": "hello", "source_type": "chat"}],
        },
    )

    assert response.status_code == 401