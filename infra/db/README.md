# Database Foundation

ScamShieldAI uses PostgreSQL as the source-of-truth database.

## Local Docker

The root `docker-compose.yml` starts PostgreSQL and mounts SQL migrations from:

```text
infra/db/migrations
```

Files in that directory are run by the official PostgreSQL image only when the database volume is first created.

## Migrations

Current bootstrap migrations:

1. `0001_create_scam_analyses.sql` - first analysis module storage.
2. `0002_create_core_product_schema.sql` - canonical product database schema for users, scans, reports, threat intelligence, alerts, model results, and audit logs.

## Full Design

See:

```text
docs/database-system.md
```

## Migration Strategy

The SQL files in `infra/db/migrations` bootstrap local development. The API also includes Alembic scaffolding so production migrations can be versioned and promoted through CI/CD once SQLAlchemy models are introduced.

## Data Principles

- Store plaintext passwords never; store password hashes only.
- Store raw scam content only when product policy requires it.
- Prefer hashes and metadata for deduplication.
- Use JSONB for explainability payloads while model outputs are still evolving.
- Add relational tables when a concept becomes stable enough to query directly.