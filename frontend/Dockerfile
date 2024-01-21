FROM node:19.6-slim

WORKDIR /app

ENV LANG=C.UTF-8 \
    TZ=Asia/Tokyo
    
COPY package*.json ./
RUN npm install
