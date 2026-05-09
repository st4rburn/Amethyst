FROM nginx:1.29-alpine-slim

WORKDIR /var/www/html

# Basic setup
COPY dist frontend
# Should be used via mount
RUN mkdir devlog_assets

COPY docker_nginx.conf /etc/nginx/templates/default.conf.template
