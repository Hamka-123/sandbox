$imageName = "python_server_1"
$imageVersion = "1.0.0"
$projectFolder = "${PSScriptRoot}/../Python_Server_Image"
$dockerFile = "${projectFolder}/Dockerfile"

# Write-Host $projectFolder

$dockerArguments = @(
    "build"
    "--rm"
    "-f", $dockerFile
    "-t", "${imageName}:${imageVersion}"
    $projectFolder

)

Write-Host @dockerArguments -ForegroundColor Yellow

& docker @dockerArguments
