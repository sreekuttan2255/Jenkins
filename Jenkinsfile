pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('gemini-api-key') // Assuming you have this credential set up in Jenkins
    }

    stages {
        stage('Maven Build') {
            steps {
                // Redirect standard output and error to build_logs.txt
                // We use || true to ensure the pipeline continues to the post block
                // even if the maven build fails
                sh 'mvn clean compile > build_logs.txt 2>&1 || true' 
                
                // Then we check if the build actually succeeded by reading the log
                // If it contains BUILD FAILURE, we explicitly fail the stage
                sh '''
                    if grep -q "BUILD FAILURE" build_logs.txt; then
                        echo "Maven build failed."
                        exit 1
                    fi
                '''
            }
        }

        // Temporarily comment out Docker build so we can test the AI script first
        // stage('Docker Build') {
        //     steps {
        //         sh 'docker build -t myapp .' // Adjust tag and context as needed
        //     }
        // }
    }

    post {
        failure {
            script {
                // Run the Python analyzer script INSIDE a Python container!
                docker.image('python:3.9').inside {
                    sh '''
                        # Install the required library for Gemini
                        pip install google-generativeai

                        # Run the analyzer script
                        python3 pipeline_analyzer.py build_logs.txt
                    '''
                }
            }
        }
    }
}
