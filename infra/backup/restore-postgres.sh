#!/bin/sh
set -eu

if [ "${1:-}" = "" ]; then
  echo "Usage: restore-postgres.sh /backups/postgres/scamshieldai-YYYYMMDDTHHMMSSZ.dump"
  exit 1
fi

export PGPASSWORD="$POSTGRES_PASSWORD"
pg_restore -h postgres -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists "$1"