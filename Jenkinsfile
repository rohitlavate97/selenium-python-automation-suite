pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest -n 3 --env=qa'
            }
        }

        stage('Generate Allure Report with History') {
            steps {
                sh '''
                echo "Preserving Allure history (if exists)..."

                if [ -d allure-report/history ]; then
                    cp -r allure-report/history allure-results/ || true
                fi

                echo "Generating Allure report..."
                allure generate allure-results -o allure-report --clean
                '''
            }
        }
    }

    post {
        always {
            echo "Archiving artifacts..."

            archiveArtifacts artifacts: '**/screenshots/*.png', fingerprint: true
            archiveArtifacts artifacts: '**/logs/*.log', fingerprint: true
            archiveArtifacts artifacts: '**/reports/*.json', fingerprint: true
            archiveArtifacts artifacts: '**/allure-report/**', fingerprint: true
        }

        success {
            echo "Build succeeded"
        }

        failure {
            echo "Build failed"
        }
    }
}
