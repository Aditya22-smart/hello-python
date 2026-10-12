pipeline {
  agent any
  stages {
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
        sh 'cp iris_model.pkl /home/adityalakhotia21/app/'
      }
    }
  }
}
