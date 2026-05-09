set -e
sudo podman pull docker-daemon:aurillium/amethyst-backend:latest
sudo podman pull docker-daemon:aurillium/amethyst-frontend:latest
sudo podman compose -f compose-prod.yml up
