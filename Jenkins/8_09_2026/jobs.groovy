
pipeline {
agent any

    stages {
        stage('Environment Check') {
            steps {
                echo 'Checking workspace and system info...'
                sh 'uname -a'
                sh 'java -version'
                sh 'docker --version'
            }
        }

        stage('Echo Message') {
            steps {
                echo 'Hello from Jenkins Pipeline!'
                sh 'echo "Current user: $(whoami)"'
                sh 'echo "Current directory: $(pwd)"'
            }
        }

        stage('Test Step') {
            steps {
                script {
                    def greeting = "Pipeline is working correctly"
                    echo "${greeting}"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished.'
        }
    }

}
