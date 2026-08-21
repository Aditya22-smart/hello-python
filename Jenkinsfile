pipeline {
    agent any
    environment {
        SONARQUBE = 'sonarqube'
        SCANNER = 'SonarScanner'
        SONAR_PROJECT_KEY = 'hello-python'
        SONAR_API_TOKEN = credentials('sonar-token')  // Jenkins secret credential[cite: 1]
        SONAR_HOST_URL = 'http://34.14.196.151:9000' // Jenkins VM IP[cite: 1]
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Aditya22-smart/hello-python.git'  // GitHub Repository[cite: 1]
            }
        }
        stage('Install & Run Tests') {
            steps {
                sh '''
                  echo "Installing dependencies..."
                  python3 -m pip install --upgrade pip
                  pip3 install --user -r requirements.txt
                  
                  echo "Running tests..."
                  python3 -m pytest -q
                '''[cite: 1]
            }
        }
        stage('SonarQube Analysis (Async)') {
            steps {
                withSonarQubeEnv("${SONARQUBE}") {
                    withEnv(["PATH+SONAR=${tool SCANNER}/bin"]) {
                        sh '''
                          echo "Running SonarQube scan asynchronously..."
                          sonar-scanner \
                            -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=$SONAR_HOST_URL \
                            -Dsonar.login=$SONAR_API_TOKEN \
                            -Dsonar.python.version=3.10
                        '''[cite: 1]
                    }
                }
            }
        }
        stage('Deploy to App VM') {
            steps {
                sshagent(credentials: ['gce-ssh']) {
                    sh '''
                        echo "Deploying with systemd..."
                        ssh -o StrictHostKeyChecking=no adityalakhotia21@34.100.228.230 "mkdir -p /home/adityalakhotia21/app"
                        scp -o StrictHostKeyChecking=no -r * adityalakhotia21@34.100.228.230:/home/adityalakhotia21/app/
                        ssh -o StrictHostKeyChecking=no adityalakhotia21@34.100.228.230 "
                          sudo systemctl daemon-reload &&
                          sudo systemctl restart flaskapp &&
                          sudo systemctl enable flaskapp
                        "
                        echo "Deployment complete. Check: curl http://34.100.228.230:8080"
                    '''[cite: 1]
                }
            }
        }
        stage('Optional: Check SonarQube Quality Gate') {
            steps {
                script {
                    echo "Fetching SonarQube Quality Gate result (non-blocking)..."[cite: 1]
                    sh """
                      curl -s -u \$SONAR_API_TOKEN: \
                        "\$SONAR_HOST_URL/api/qualitygates/project_status?projectKey=\$SONAR_PROJECT_KEY" \
                        | jq '.projectStatus.status'
                    """[cite: 1]
                    echo "You can manually inspect the SonarQube dashboard for full details."[cite: 1]
                }
            }
        }
    }
    post {
        success {
            echo " Pipeline Succeeded"[cite: 1]
        }
        failure {
            echo " Pipeline Failed"[cite: 1]
        }
    }
}
