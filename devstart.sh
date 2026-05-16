set -e
source ./.env
hadolint services/backend/dev.dockerfile
hadolint services/frontend/dev.dockerfile
# Allow for cleanup after we exit
set +e
sudo podman compose -f compose-dev.yml up --build --abort-on-container-exit
sudo podman compose -f compose-dev.yml down
