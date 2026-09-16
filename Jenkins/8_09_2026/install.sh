#! /bin/bash

set -e

echo "Cleaning up existing containers and volumes if any..."
docker rm -f my-jenkins || true
docker volume rm jenkins_home || true

echo "Starting Jenkins container..."
docker run -d \
  --name my-jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/lib/jenkins_home \
  -e JAVA_OPTS="-Djenkins.install.runSetupWizard=false -Dhudson.security.csrf.GlobalCrumbIssuerConfiguration.DISABLE_CSRF_PROTECTION=true" \
  jenkins/jenkins:lts-jdk17

echo "Waiting for Jenkins to generate the initial admin password..."
until docker exec my-jenkins [ -f /var/lib/jenkins/secrets/initialAdminPassword ]; do
  sleep 2
done

echo "=========================================="
echo "Jenkins is running via Docker successfully!"
echo "Access port: 8080"
echo "Initial Admin Password:"
docker exec my-jenkins cat /var/lib/jenkins/secrets/initialAdminPassword
echo "=========================================="