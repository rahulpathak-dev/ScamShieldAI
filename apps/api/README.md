# ScamShieldAI API

FastAPI backend for ScamShieldAI.

## Stack

- FastAPI
- Pydantic Settings
- SQLAlchemy and Alembic scaffolding
- PostgreSQL
- Structured JSON logging
- Centralized error handling

## Local Setup

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `GET /ready`
- `POST /api/v1/analyze/text`

## API Layers

```text
app/domain/              Business entities and domain services
app/application/         Use cases and DTOs
app/infrastructure/      Database and external implementations
app/interfaces/api/      FastAPI routes, middleware, exception handlers
app/core/                Config, logging, app-level errors
```

## Docker

```powershell
docker build -t scamshieldai-api .
docker run --rm -p 8000:8000 --env-file .env.example scamshieldai-api
```
