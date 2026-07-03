# API Documentation

FastAPI serves interactive API documentation at `/docs` and OpenAPI JSON at `/openapi.json`.

## Core Endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/analyze/text`
- `POST /api/v1/ml/predict`
- `POST /api/v1/persuasion/detect`
- `POST /api/v1/risk/score`
- `POST /api/v1/notifications/high-risk-warning`
- `POST /api/v1/assistant/ask`

## Platform Endpoints

- `GET /api/v1/i18n/languages`
- `POST /api/v1/i18n/detect-language`
- `POST /api/v1/browser-extension/scan-page`
- `POST /api/v1/mobile/scan-sms`
- `POST /api/v1/mobile/scan-screenshot`
- `POST /api/v1/voice/scan-audio`
- `POST /api/v1/enterprise/batch-analyze`

## Example Text Scan

```bash
curl -X POST http://localhost:8000/api/v1/analyze/text \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Urgent bank alert: verify OTP now or account will be suspended.",
    "source_type": "sms",
    "language": "en"
  }'
```

## Example Enterprise Batch

```bash
curl -X POST http://localhost:8000/api/v1/enterprise/batch-analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-enterprise-key" \
  -d '{
    "tenant_id": "acme-bank",
    "items": [
      {"external_id": "msg-1", "content": "Urgent wallet verification required now.", "source_type": "chat", "language": "en"}
    ]
  }'
```

## Authentication

User-facing routes use JWT authentication through secure cookies or bearer tokens. Enterprise routes use `X-API-Key` and should be moved to tenant-scoped keys stored in PostgreSQL or a secret manager for full production use.