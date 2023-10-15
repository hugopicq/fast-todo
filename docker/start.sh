#!/bin/sh

set -eu

echo "run db migration"
/app/migrate -path /app/database/migrations -database "$POSTGRES_DSN" -verbose up

exec python -m fast_todo.main --host ${HOST} --port ${PORT}