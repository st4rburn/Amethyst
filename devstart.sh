set -e
hadolint services/backend/dev.dockerfile
hadolint services/frontend/dev.dockerfile
docker compose -f compose-dev.yml up --build
