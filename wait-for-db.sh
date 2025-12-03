#!/bin/sh
set -e

# Usage: wait-for-db.sh <host> -- <cmd...>
# Waits for Postgres at <host> to become available, then execs the provided command.

host="$1"
shift || true

DB_USER=${DB_USER:-myuser}
DB_NAME=${DB_NAME:-new_db}

echo "Waiting for postgres at ${host} (user=${DB_USER} db=${DB_NAME})..."
until pg_isready -h "${host}" -U "${DB_USER}" -d "${DB_NAME}" >/dev/null 2>&1; do
  printf '.'
  sleep 1
done

echo "\nPostgres is available — starting command."

exec "$@"
#!/bin/sh
set -e

# Usage: wait-for-db.sh <host> -- <cmd...>
# Waits for Postgres at <host> to become available, then execs the provided command.

host="$1"
shift || true

DB_USER=${DB_USER:-myuser}
DB_NAME=${DB_NAME:-new_db}

echo "Waiting for postgres at ${host} (user=${DB_USER} db=${DB_NAME})..."
until pg_isready -h "${host}" -U "${DB_USER}" -d "${DB_NAME}" >/dev/null 2>&1; do
  printf '.'
  sleep 1
done

echo "\nPostgres is available — starting command."

exec "$@"
