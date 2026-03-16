pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('gemini-api-key') // Assuming you have this credential set up in Jenkins
    }

    stages {
        stage('Python Test') {
            steps {
                // Here we run a command that is guaranteed to fail so we can test the AI agent!
                // We use a script block because docker.image().inside must run inside a script block in Declarative Pipelines
                script {
                    docker.image('python:3.9').inside {
                        // This creates a deliberate SyntaxError by missing a closing quote
                        sh '''
                            echo 'print("Hello World)' > bad_script.py
                            python3 bad_script.py > build_logs.txt 2>&1 || true

                            if grep -q "SyntaxError" build_logs.txt; then
                                echo "Python test failed as expected."
                                exit 1
                            fi
                        '''
                    }
                }
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
