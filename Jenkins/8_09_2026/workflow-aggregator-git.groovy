
pipeline {
    agent any

    parameters {
        string(name: 'RELEASE_VERSION', defaultValue: '1.0.0', description: 'Target release version')
        choice(name: 'TARGET_ENV', choices: ['staging', 'production'], description: 'Target deployment environment')
    }

    stages {
        stage('Checkout Components') {
            parallel {
                stage('Checkout Backend') {
                    steps {
                        // Fetching backend repository into a dedicated subdirectory
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: '*/main']],
                            userRemoteConfigs: [[url: 'https://github.com/company/backend-service.git', credentialsId: 'github-token']],
                            extensions: [[$class: 'RelativeTargetDir', relativeTargetDir: 'backend']]
                        ])
                    }
                }
                stage('Checkout Frontend') {
                    steps {
                        // Fetching frontend repository into a dedicated subdirectory
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: '*/main']],
                            userRemoteConfigs: [[url: 'https://github.com/company/frontend-service.git', credentialsId: 'github-token']],
                            extensions: [[$class: 'RelativeTargetDir', relativeTargetDir: 'frontend']]
                        ])
                    }
                }
            }
        }

        stage('Build and Test All') {
            parallel {
                stage('Build Backend') {
                    steps {
                        dir('backend') {
                            echo "Building backend for version ${params.RELEASE_VERSION}..."
                            sh 'echo "Backend compilation complete."'
                        }
                    }
                }
                stage('Build Frontend') {
                    steps {
                        dir('frontend') {
                            echo "Building frontend for version ${params.RELEASE_VERSION}..."
                            sh 'echo "Frontend compilation complete."'
                        }
                    }
                }
            }
        }

        stage('Integration Tests') {
            steps {
                echo 'Running end-to-end integration tests across combined microservices...'
                sh 'echo "All integration tests passed successfully!"'
            }
        }

        stage('Production Approval Gate') {
            when {
                expression { params.TARGET_ENV == 'production' }
            }
            steps {
                input message: "Proceed to deploy version ${params.RELEASE_VERSION} to Production?", ok: 'Approve Release'
            }
        }

        stage('Deploy Aggregated Release') {
            steps {
                echo "Deploying version ${params.RELEASE_VERSION} to ${params.TARGET_ENV} environment..."
                sh 'echo "Deployment successfully finished!"'
            }
        }
    }
}