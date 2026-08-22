pipeline {
    agent any

    environment {
        SONARQUBE = 'sonarqube'
        SCANNER = 'SonarScanner'
        SONAR_PROJECT_KEY = 'hello-python'
        SONAR_API_TOKEN = credentials('sonar-token')
        SONAR_HOST_URL = 'http://34.47.162.151:9000'
        APP_VM_IP = '34.14.158.127'
        APP_VM_USER = 'adityalakhotia21'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out project from GitHub...'
                git branch: 'main', url: 'https://github.com/Aditya22-smart/hello-python.git'
            }
        }

        stage('Install Dependencies & Test') {
            steps {
                sh '''
                    echo "Installing Python dependencies..."
                    python3 -m pip install --upgrade pip
                    pip3 install --user -r requirements.txt

                    echo "Running unit tests with pytest..."
                    python3 -m pytest -q
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE}") {
                    withEnv(["PATH+SONAR=${tool SCANNER}/bin"]) {
                        sh '''
                            echo "Running SonarQube Scanner..."
                            sonar-scanner \
                              -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                              -Dsonar.sources=. \
                              -Dsonar.host.url=$SONAR_HOST_URL \
                              -Dsonar.login=$SONAR_API_TOKEN \
                              -Dsonar.python.version=3.10
                        '''
                    }
                }
            }
        }

        stage('Quality Gate Status') {
            steps {
                script {
                    echo "Verifying SonarQube Quality Gate result..."
                    sleep 5
                    sh """
                        curl -s -u $SONAR_API_TOKEN: \
                          "$SONAR_HOST_URL/api/qualitygates/project_status?projectKey=$SONAR_PROJECT_KEY" \
                          | grep -o '"status":"[^"]*"' || true
                    """
                }
            }
        }

        stage('Deploy to App VM') {
            steps {
                sshagent(credentials: ['gce-ssh']) {
                    sh '''
                        echo "Deploying application to App VM..."
                        ssh -o StrictHostKeyChecking=no ${APP_VM_USER}@${APP_VM_IP} "mkdir -p /home/${APP_VM_USER}/app"
                        scp -o StrictHostKeyChecking=no -r * ${APP_VM_USER}@${APP_VM_IP}:/home/${APP_VM_USER}/app/
                        ssh -o StrictHostKeyChecking=no ${APP_VM_USER}@${APP_VM_IP} "
                            sudo systemctl daemon-reload &&
                            sudo systemctl restart flaskapp &&
                            sudo systemctl enable flaskapp
                        "
                        echo "Deployment complete. Verify at: curl http://${APP_VM_IP}:8080"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "CI/CD Pipeline Succeeded!"
        }
        failure {
            echo "CI/CD Pipeline Failed."
        }
    }
}
