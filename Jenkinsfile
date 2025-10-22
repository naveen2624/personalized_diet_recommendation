pipeline {
    agent any

    stages {
        // Checkout the entire repo
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/your-username/your-repo.git'
            }
        }

        // Frontend build
        stage('Frontend Install & Build') {
            steps {
                dir('frontend') {
                    bat 'npm install'
                    bat 'npm run build'
                    bat 'npm test'
                }
            }
        }

        // Backend install & test
        stage('Backend Install & Test') {
            steps {
                dir('backend') {
                    bat 'python -m venv venv'
                    bat '.\\venv\\Scripts\\activate && pip install -r requirements.txt'
                    bat '.\\venv\\Scripts\\activate && pytest'
                }
            }
        }
    }
}
