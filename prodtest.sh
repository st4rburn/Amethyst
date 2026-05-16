set -e
sudo podman pull docker-daemon:aurillium/amethyst-backend:latest
sudo podman pull docker-daemon:aurillium/amethyst-frontend:latest
set +e
sudo podman compose -f compose-prod.yml up
sudo podman compose -f compose-dev.yml down
