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