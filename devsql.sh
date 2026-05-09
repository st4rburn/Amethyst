#!/bin/sh

source ./.env
sudo podman exec -it $(basename $(pwd))-database-1 psql -U "${DB_USER}" -d "${DB_NAME}"
