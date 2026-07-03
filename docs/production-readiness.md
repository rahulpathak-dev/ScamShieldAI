# Production Readiness

## Production Architecture

ScamShieldAI runs as independently deployable containers:

- Next.js web application
- FastAPI backend
- PostgreSQL database
- Redis cache and future queue backend
- Nginx reverse proxy
- Prometheus monitoring
- Scheduled PostgreSQL backup container

## Container Strategy

- `docker-compose.yml` is the local developer stack.
- `docker-compose.prod.yml` is the production-style stack.
- API and web images are built in CI and published to GHCR.
- Runtime secrets are injected through environment variables or cloud secret managers.

## Security Controls

- Production mode rejects the default JWT secret.
- CORS must be restricted to trusted web origins.
- API keys, database URLs, SMTP credentials, and LLM keys must not be committed.
- Nginx adds baseline security headers and API rate limiting.
- Enterprise APIs require `X-API-Key`.
- Logs should avoid raw secrets, passwords, OTPs, and full scam message payloads.

## Monitoring

Prometheus configuration lives in `infra/monitoring`.

Monitored signals:

- API health availability
- Prometheus target availability
- Container health checks
- Reverse proxy access and error logs

Recommended cloud additions:

- API latency percentiles
- HTTP 4xx and 5xx rates
- Database CPU, memory, storage, and connection count
- Queue depth when async workers are added
- Model drift and prediction distribution dashboards

## Backups

`postgres-backup` in `docker-compose.prod.yml` runs a daily `pg_dump` into `./backups/postgres` and deletes backups older than `BACKUP_RETENTION_DAYS`.

Production backup recommendations:

- Store backups in encrypted object storage.
- Use RDS automated backups and point-in-time recovery.
- Test restores at least monthly.
- Keep restore credentials separate from application credentials.

## Release Checklist

1. CI is green.
2. API and web images are published.
3. Production secrets are rotated and loaded from a secret manager.
4. Database migrations are reviewed.
5. Backups are enabled.
6. Monitoring alerts route to the on-call channel.
7. Smoke tests pass after deployment.