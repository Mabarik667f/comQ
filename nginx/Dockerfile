FROM node:latest as build-stage
WORKDIR /app
COPY root/comQ/frontend/package*.json ./
RUN npm install
COPY root/comQ/frontend .
RUN npm run build

FROM nginx:1.23.1-alpine as production-stage
RUN rm /etc/nginx/conf.d/default.conf
COPY root/comQ/nginx/nginx.conf /etc/nginx/conf.d/

COPY etc/letsencrypt  /etc/letsencrypt
COPY --from=build-stage /app/dist /app

EXPOSE 80
EXPOSE 443
CMD ["nginx", "-g", "daemon off;"]