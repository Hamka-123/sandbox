#!/bin/bash

docker volume create vol_test_1
docker volume ls
docker volume inspect vol_test_1   

# монтирование volume в любой контейнер и просмотр
docker run --rm -it -v vol_test_1:/data alpine sh
ls /data

# попасть внутрь виртуальной машины docker
docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i sh
cd /var/lib/docker/volumes/vol_test_1/_data

# bind в папку на хосте
docker run -d -v /Users/твой_юзер/project_folder:/data alpine
docker run -d -v $(pwd)/project_folder:/data alpine