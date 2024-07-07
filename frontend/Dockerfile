FROM node:lts-alpine

WORKDIR /usr/src/app
COPY . ./frontend
WORKDIR /usr/src/app/frontend

COPY package*.json ./
RUN npm install
RUN npm run build