pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Testing Setup') {
            steps {
                sh 'python -m venv myenv'  // Create a virtual environment
                sh 'source myenv/bin/activate'  // Activate the virtual environment
                sh 'pip install pytest'  // Install pytest
                sh 'pip install -r requirements.txt'  // Install other dependencies from a requirements file
            }
        }

        stage('Verify Dependencies') {
            steps {
                sh 'pytest --version'
            }
        }

        stage('Testing') {
            steps {
                sh 'pytest --verbose --cov=website/tests/'
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
