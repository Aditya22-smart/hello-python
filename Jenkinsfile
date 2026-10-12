pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/<your-username>/mlops-iris-demo.git'
      }
    }
    stage('Install Dependencies') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Retrain Model') {
      steps {
        sh 'python3 retrain.py'
      }
    }
    stage('Deploy Model') {
      steps {
        sh 'cp iris_model.pkl /home/ubuntu/app/'
      }
    }
  }
}
