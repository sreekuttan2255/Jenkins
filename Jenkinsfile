pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('gemini-api-key') // Assuming you have this credential set up in Jenkins
    }

    stages {
        stage('Python Test') {
            steps {
                // Here we run a command that is guaranteed to fail so we can test the AI agent!
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
                // Run the Python analyzer script directly
                sh '''
                    # Install the NEW required library for Gemini if not already present
                    #pip3 install google-genai --break-system-packages || true

                    # Run the analyzer script
                    python3 pipeline_analyzer.py build_logs.txt
                '''
            }
        }
    }
}
