#!/bin/sh
set -eu

BACKUP_DIR="/backups/postgres"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"
mkdir -p "$BACKUP_DIR"

export PGPASSWORD="$POSTGRES_PASSWORD"
pg_dump -h postgres -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f "$BACKUP_DIR/scamshieldai-$TIMESTAMP.dump"
find "$BACKUP_DIR" -type f -name 'scamshieldai-*.dump' -mtime "+$RETENTION_DAYS" -delete

echo "PostgreSQL backup complete: $BACKUP_DIR/scamshieldai-$TIMESTAMP.dump"