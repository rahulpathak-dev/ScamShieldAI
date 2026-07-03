# ADR 0001: Scalable Foundation Architecture

## Status

Accepted

## Context

ScamShieldAI will eventually include authentication, dashboards, NLP models, LLM explanations, threat intelligence, alerting, and multilingual support. Building all of that at once would create tight coupling and make the product difficult to test or secure.

## Decisions

1. Use a monorepo with `apps/web`, `apps/api`, `infra`, and `docs`.

   Reason: the product has multiple deployable services, but they share contracts and should evolve together during early development.

2. Use Next.js for the frontend.

   Reason: it supports TypeScript, server/client rendering boundaries, routing, production builds, and dashboard-style product development.

3. Use a direct operational workspace as the first UI screen.

   Reason: ScamShieldAI is a cybersecurity product. The primary user need is analysis, not a landing page.

4. Use Tailwind CSS with shadcn-compatible components.

   Reason: Tailwind keeps styling local and predictable, while shadcn conventions provide accessible reusable primitives without locking the app into a heavy component framework.

5. Use FastAPI for the backend.

   Reason: FastAPI provides strong request validation, OpenAPI documentation, Python ML ecosystem compatibility, and clean async-ready API ergonomics.

6. Use clean architecture in the API.

   Reason: scam detection rules, future models, persistence, and HTTP transport must remain independently testable and replaceable.

7. Version REST routes under `/api/v1`.

   Reason: API clients need stable contracts as the product grows and model behavior changes.

8. Use PostgreSQL as the source-of-truth database.

   Reason: ScamShieldAI needs reliable relational data for users, analyses, audit trails, alerts, and admin workflows.

9. Use JSONB for early explainability payloads.

   Reason: model evidence schemas will evolve. JSONB gives flexibility now while preserving the option to normalize later.

10. Add Alembic scaffolding but keep bootstrap SQL under `infra/db/migrations`.

    Reason: Docker bootstrap SQL is simple for local setup. Alembic is the right long-term tool for controlled production migrations.

11. Use environment-based configuration.

    Reason: images should be deployable across local, staging, and production without code changes.

12. Use centralized API error handling.

    Reason: clients need predictable failures, and production systems should not leak internal exceptions.

13. Use structured JSON logging.

    Reason: logs must be searchable in cloud observability systems and useful during security incident response.

14. Add request ID middleware.

    Reason: every user-visible failure should be traceable through backend logs and downstream services.

15. Split `/health` and `/ready`.

    Reason: health tells an orchestrator the process is alive; readiness verifies dependencies such as the database.

16. Do not build AI models in this foundation pass.

    Reason: model work should start after contracts, storage, observability, and deployment boundaries are stable.

## Consequences

- The project can run locally with Docker Compose.
- Frontend, backend, and database can evolve independently.
- Future AI services can be added without rewriting API routes.
- Production hardening work has clear extension points: auth, migrations, secrets, CI/CD, monitoring, and model services.
