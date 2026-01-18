pipeline {
    agent any

    stages {
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest -n 3 --env=qa'
            }
        }

        stage('Allure') {
            steps {
                sh 'allure generate allure-results -o allure-report --clean'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/screenshots/*.png'
            archiveArtifacts artifacts: '**/logs/*.log'
        }
    }
}
