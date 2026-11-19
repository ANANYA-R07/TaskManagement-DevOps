pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t task-management-api:latest .'
            }
        }

        stage('Verify Docker Image') {
            steps {
                bat 'docker images task-management-api'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed and Docker image built!'
        }
        failure {
            echo 'FAILURE: Check the Jenkins console output.'
        }
    }
}