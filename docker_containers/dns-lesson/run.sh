#!/bin/bash

docker network create mynet
docker run -dit --name web -p 8080:8888 --network mynet --network-alias network_link test1:latest
docker run -it --name client -p 8081:8888 --network mynet --network-alias network_link test1:latest