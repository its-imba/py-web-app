pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageName = "py-web-app"
                    def imageTag = "latest"

                    docker.build("${imageName}:${imageTag}", '.')
                }
            }
        }

                stage('Test') {
            steps {
                sh 'pip install -r requirements.txt' // Install dependencies
                sh 'pytest -v' // Run pytest
            }
        }

        stage('Remove Existing Docker Containers') {
            steps {
                script {
                    sh 'docker ps -a | grep py-web-app | awk \'{print $1}\' | xargs -r docker rm -f'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    def containerName = "py-web-app"

                    docker.image('py-web-app:latest').run("-p 5000:5000 --name ${containerName}")
                }
            }
        }
    }
}
