#!/bin/bash

#docker network create python_net
# Первый сервер
docker run -d --name py-srv1 --network mynet --network-alias py-service py-server

# Второй сервер
docker run -d --name py-srv2 --network mynet --network-alias py-service py-server

docker run -d \
  --name nginx-lb \
  --network mynet \
  -p 80:80 \
  -v $(pwd)/../nginx/nginx.conf:/etc/nginx/nginx.conf:ro \
  nginx:alpine