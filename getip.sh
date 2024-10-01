#!/bin/sh
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(sudo docker ps | grep proxy | cut -f 1 -d ' ')
