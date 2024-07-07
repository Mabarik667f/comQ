FROM node:latest as build-stage
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

FROM nginx:1.23.1-alpine as production-stage
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY --from=build-stage /app/dist /app

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
