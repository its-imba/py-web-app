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
                sh 'sudo apt-get install -y python3 python3-pip python3-venv'
                sh 'python3 -m venv ${WORKSPACE}/venv'  // Create a virtual environment
                sh '. ${WORKSPACE}/venv/bin/activate'  // Activate the virtual environment
                sh 'cd ${WORKSPACE}'
                sh 'export PATH=/var/lib/jenkins/.local/bin:$PATH'  // Add the directory to PATH
                sh 'pip install -r requirements.txt'  // Install other dependencies from a requirements file
            }
        }

        stage('Verify Dependencies') {
            steps {
                sh 'python3 -m pytest --version' // Check pytest is installed
            }
        }

        stage('Testing') {
            steps {
                sh '''
                python3 -c "import sys; sys.path.append('/var/lib/jenkins/workspace/py-app-dev-v2')"
                python3 -m pytest --verbose --cov=tests/
        '''
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
