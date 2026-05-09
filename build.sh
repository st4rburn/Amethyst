#!/bin/sh

# Build Vue as static files
cd services/frontend
npm i
npm run build
cp ../../nginx.prod.conf docker_nginx.conf
sudo docker build -t aurillium/amethyst-frontend . -f ./prod.dockerfile
rm docker_nginx.conf

cd ../backend
sudo docker build -t aurillium/amethyst-backend . -f ./prod.dockerfile
