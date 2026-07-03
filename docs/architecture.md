# ScamShieldAI System Architecture

## Goal

ScamShieldAI is a global AI cybersecurity product for financial scam detection, risk scoring, explainability, and prevention. The foundation is designed to support future NLP, ML, LLM, vector search, and threat intelligence modules without coupling those concerns to the first API or UI screens.

## High-Level Architecture

```text
User / Analyst
   |
   v
Next.js Web App
   |
   v
FastAPI REST API
   |
   +--> PostgreSQL
   +--> Redis (future cache and queues)
   +--> Vector Database (future semantic retrieval)
   +--> ML / LLM Services (future model execution)
   +--> Threat Intelligence Feeds (future enrichment)
```

## Runtime Services

- `web`: Next.js frontend served on port `3000`.
- `api`: FastAPI backend served on port `8000`.
- `postgres`: PostgreSQL source-of-truth database served on port `5432`.

Docker Compose is used for local orchestration because it mirrors production service boundaries while keeping development setup simple.

## Backend Architecture

The API follows clean architecture:

```text
app/core/                Cross-cutting concerns: config, logging, errors
app/domain/              Business entities, domain services, repository protocols
app/application/         Use cases and transport-neutral DTOs
app/infrastructure/      Database sessions and external implementation adapters
app/interfaces/api/      FastAPI routes, middleware, exception handlers
```

Dependency direction flows inward. The domain layer does not import FastAPI, SQLAlchemy, model SDKs, or cloud APIs.

## Frontend Architecture

The frontend uses the Next.js App Router:

```text
src/app/                 Routes, layouts, global styles
src/components/ui/       shadcn-compatible reusable primitives
src/components/          Product-specific components
src/lib/                 Runtime config, API client, utility functions
src/types/               API DTO types used by the UI
```

The first screen is an operational analysis workspace rather than a marketing page. This matches the product purpose: users should immediately perform scam analysis.

## API Architecture

API routes are versioned under `/api/v1`.

Reasons:

- Mobile apps, browser clients, and partner integrations need stable contracts.
- Future model changes should not force immediate client rewrites.
- Admin, user, and public APIs can evolve independently.

Current endpoints:

- `GET /health`
- `GET /ready`
- `POST /api/v1/analyze/text`

## Configuration

Configuration is loaded from environment variables with the `SCAMSHIELD_` prefix for the API and `NEXT_PUBLIC_` for browser-visible frontend values.

Reasons:

- The same image can run in local, staging, and production.
- Secrets stay out of source code.
- Docker, CI/CD, and cloud platforms can inject environment-specific settings.

## Error Handling

The API returns one consistent error envelope:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed.",
    "details": {},
    "request_id": "..."
  }
}
```

Reasons:

- Frontend code can handle failures consistently.
- Support teams can trace errors with request IDs.
- Production responses avoid leaking stack traces.

## Logging

The API emits structured JSON logs with request metadata.

Reasons:

- JSON logs work well with cloud log aggregators.
- Request IDs connect frontend errors to backend logs.
- Structured fields make security incident review easier.

## Database Architecture

PostgreSQL is the source-of-truth database.

Reasons:

- Strong consistency for users, submissions, alerts, and audit data.
- JSONB can store evolving explainability payloads during early AI development.
- Relational constraints can be introduced as concepts stabilize.

Local bootstrap SQL lives under `infra/db/migrations`. Alembic scaffolding exists in `apps/api/alembic` for production-grade migrations once ORM models are added.

## AI Boundary

AI models are not part of this foundation pass.

Future AI components should enter through application/domain services, such as:

- classifier service
- persuasion strategy detector
- explanation generator
- threat intelligence enricher
- vector retrieval service

This prevents ML provider choices from leaking into HTTP routes or database code.

## Security Baseline

- CORS is environment-configured.
- Next.js removes the powered-by header and adds basic browser security headers.
- API responses include request IDs.
- Raw submitted content is hashed in the current analysis object.
- Centralized errors prevent accidental stack trace leaks in production.
- Docker Compose isolates services for local development.
