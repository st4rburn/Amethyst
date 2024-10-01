FROM node:lts-slim

WORKDIR /app

# Provided with one of the worst Dockerfiles in history,
# probably not needed but not going to risk it
#ENV PATH /app/node_modules/.bin:$PATH

# Copy package info
COPY package.json .
COPY package-lock.json .

# Basic setup
COPY index.html .
COPY env.d.ts .
COPY tsconfig* .
COPY vite*.config.ts .

# Public folder + source
COPY public/ ./public
COPY src/ ./src

# Install packages
RUN npm install

# Last two arguments pass --host to Vite, as app must
# be accessible outside of localhost for Docker
CMD ["npm", "run", "dev", "--", "--host"]
