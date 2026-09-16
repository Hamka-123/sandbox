// Comments in code should only be in English.

pipeline {
agent any

    stages {
        stage('Compile') {
            steps {
                echo 'Compiling source code...'
                sh 'echo "Simulating code compilation complete."'
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests...'
                sh 'echo "All 15 tests passed!"'
            }
        }

        stage('Deploy to Pre-Prod Environments') {
            parallel {
                stage('Deploy to Staging') {
                    steps {
                        echo 'Deploying application to Staging...'
                        sh 'echo "App successfully deployed to Staging!"'
                    }
                }
                stage('Deploy to QA Environment') {
                    steps {
                        echo 'Deploying application to QA...'
                        sh 'echo "App successfully deployed to QA!"'
                    }
                }
            }
        }

        stage('Production Gate') {
            steps {
                input message: 'Proceed to Production release?', ok: 'Approve'
            }
        }

        stage('Deploy to Production') {
            steps {
                echo 'Deploying application to Production...'
                sh 'echo "App successfully deployed to Production!"'
            }
        }
    }

}
