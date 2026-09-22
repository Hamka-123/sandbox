#! /bin/bash 
set -e

curl -X POST "https://dc8c575261676e05-1-8080.spca.r.killercoda.com/job/test/buildWithParameters?RELEASE_TAG=v2.5.1&TARGET_ENV=production&RUN_TESTS=false"


# ADD USER

docker exec -u 0 {CONTAINER_ID} bash -c 'mkdir -p /var/jenkins_home/init.groovy.d && cat << "EOF" > /var/jenkins_home/init.groovy.d/create-admin.groovy
import jenkins.model.*
import hudson.security.*

def instance = Jenkins.get()

def hudsonRealm = new HudsonPrivateSecurityRealm(false)
def user = hudsonRealm.createAccount("admin", "{PASS}")
user.save()
instance.setSecurityRealm(hudsonRealm)

def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(strategy)

instance.save()
println "--> SUCCESS: User admin created successfully."
EOF
chown -R 1000:1000 /var/jenkins_home/init.groovy.d'
docker restart jenkins

# ADD TOKEN

docker exec jenkins bash -c '
curl -s -u admin:{PASS} -X POST "http://localhost:8080/me/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken?newTokenName=remote-trigger-token"
'

# curl -X POST -i -u "admin:{TOKEN}" \
#   "http://localhost:8080/job/lesson3-parameterized-job/buildWithParameters?TARGET_ENV=production&RELEASE_TAG=v3.0.0"

# curl -X POST -i -u "admin:{TOKEN} \
#   "https://dc8c575261676e05-1-8080.spca.r.killercoda.com:8080/job/test/buildWithParameters?TARGET_ENV=production&RELEASE_TAG=v3.0.0"

# https://admin:{TOKEN}@234f2fabd15dda1f-1-8080.spca.r.killercoda.com/job/test/buildWithParameters?TARGET_ENV=production&RELEASE_TAG=v3.0.0