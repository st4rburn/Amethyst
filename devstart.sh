set -e
source ./.env
hadolint services/backend/dev.dockerfile
hadolint services/frontend/dev.dockerfile
sudo podman compose -f compose-dev.yml up --build
