#!/bib/bash

imageName="python_server_image"
imageVersion="2.0.0"
dockerfile="/Users/alinababenko/Documents/Israel_course/DevOps/docker_containers/web-site-test/python_server/Dockerfile"
context="/Users/alinababenko/Documents/Israel_course/DevOps/docker_containers/web-site-test/python_server"

buildArguments="
--pull
--rm
-f $dockerfile 
-t $imageName:v.$imageVersion
-t "$imageName:latest"
$context
"

docker build $buildArguments