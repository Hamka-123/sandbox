#!/bib/bash

imageName="python_server_image"
imageversion="latest"
containerName="$imageName""3"
mountSource="/Users/alinababenko/Documents/Israel_course/DevOps/docker_containers/web-site-test/python_server/app/http_root"
mountTarget="/app/http_root"

runArguments="
-d
-i
--rm
--name $containerName
-p 8001:8000
--mount type=bind,source=$mountSource,target=$mountTarget
$imageName:$imageversion
"

docker run $runArguments