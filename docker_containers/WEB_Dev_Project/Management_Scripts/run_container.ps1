$imageName = "python_server_1"
$imageVersion = "1.0.0"
$containerName = "${imageName}_1"
$projectFolder = "${PSScriptRoot}/../Python_Server_Image"



$dockerArguments = @(
    "run"
    "--detach"
    "--interactive"
    "--rm"
    "--name", $containerName
    "--publish", "8001:8000"
    "--mount", "type=bind,source=${projectFolder}/http_root,target=/http_root"
    "${imageName}:${imageVersion}"

)

Write-Host @dockerArguments -ForegroundColor Yellow

& docker @dockerArguments
