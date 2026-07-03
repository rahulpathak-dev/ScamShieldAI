# Operations Runbook

## Health Checks

- API: `GET /health`
- API docs: `GET /docs`
- Web: `GET /`
- PostgreSQL: `pg_isready`
- Redis: `redis-cli ping`

## Backup

Manual backup from the production Compose stack:

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml exec postgres-backup sh /usr/local/bin/postgres-backup.sh
```

## Restore

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml exec postgres-backup \
  sh /usr/local/bin/restore-postgres.sh /backups/postgres/scamshieldai-YYYYMMDDTHHMMSSZ.dump
```

## Incident Response

1. Confirm whether the issue affects API, web, database, or model services.
2. Check Nginx and API logs.
3. Check database health and storage.
4. Disable affected enterprise API keys if abuse is detected.
5. Rotate secrets if exposure is suspected.
6. Restore from backup only after identifying the correct recovery point.

## Monitoring Alerts

- API down for more than 2 minutes: critical
- Any Prometheus target down for more than 5 minutes: warning
- Add cloud alerts for CPU, memory, storage, 5xx rates, and queue depth.