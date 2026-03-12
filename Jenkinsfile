pipeline {
    agent any

    environment {
        OPENAI_API_KEY = credentials('openai-api-key') // Assuming you have this credential set up in Jenkins
    }

    stages {
        stage('Maven Build') {
            steps {
                sh 'mvn clean compile' // Adjust to your Maven goals
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t myapp .' // Adjust tag and context as needed
            }
        }
    }

    post {
        failure {
            script {
                // Capture the build logs and write to a file
                def logs = currentBuild.rawBuild.getLog(1000).join('\n')
                writeFile file: 'build_logs.txt', text: logs

                // Run the Python analyzer script
                sh '''
                    python3 pipeline_analyzer.py build_logs.txt
                '''
            }
        }
    }
}