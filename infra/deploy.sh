#!/usr/bin/env bash
# Production deploy helper. Reads .env, builds images, brings stack up.
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -f infra/.env ]]; then
    echo "infra/.env not found. Copy from infra/.env.example and edit values." >&2
    exit 1
fi

# shellcheck disable=SC1091
set -a; source infra/.env; set +a

echo "==> Pulling base images"
docker compose -f infra/docker-compose.yml pull --ignore-pull-failures

echo "==> Building services"
docker compose -f infra/docker-compose.yml build

echo "==> Starting stack"
docker compose -f infra/docker-compose.yml up -d

echo "==> Waiting for health"
for i in {1..30}; do
    if curl -fsS http://localhost/api/health >/dev/null 2>&1; then
        echo "==> API is up"
        break
    fi
    sleep 2
done

docker compose -f infra/docker-compose.yml ps
