# Module 001: Scam Analysis API v1

## Architecture

This module implements the first production-shaped backend slice for ScamShieldAI.

Flow:

```text
FastAPI route
  -> AnalyzeTextMessageUseCase
  -> ScamRiskEngine
  -> AnalysisRepository
```

Layer responsibilities:

- `interfaces/api`: HTTP request and response handling.
- `application`: orchestration, DTOs, and use cases.
- `domain`: scam categories, persuasion strategy signals, evidence, and risk scoring.
- `infrastructure`: persistence implementations.

The current risk engine is deterministic and explainable. It is intentionally isolated so future PyTorch, Transformers, LangChain, threat intelligence, and vector search components can become additional domain/application services without changing API contracts.

## Folder Structure

```text
apps/api/
  app/
    application/
    core/
    domain/
    infrastructure/
    interfaces/
  tests/
infra/db/migrations/
```

## Database Changes

This module introduces the `scam_analyses` table for submitted analysis results.

Migration:

- `infra/db/migrations/0001_create_scam_analyses.sql`

The API currently uses an in-memory repository so the module can run locally before PostgreSQL is configured. The repository boundary is already in place for a PostgreSQL implementation.

## API

### `POST /api/v1/analyze/text`

Request:

```json
{
  "content": "Urgent: your bank account is locked. Verify OTP now to avoid suspension.",
  "source_type": "sms",
  "language": "en"
}
```

Response includes:

- `analysis_id`
- `risk_score`
- `risk_level`
- `scam_categories`
- `persuasion_strategies`
- `evidence`
- `recommended_actions`

## Testing Steps

From `apps/api`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

Then call:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/analyze/text `
  -ContentType "application/json" `
  -Body '{"content":"Urgent bank alert. Verify OTP now or account will be suspended.","source_type":"sms","language":"en"}'
```

## Documentation

OpenAPI is available at:

- `http://127.0.0.1:8000/docs`

