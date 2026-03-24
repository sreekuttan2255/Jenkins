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
                    #python3 bad_script.py > build_logs.txt 2>&1 || true
                    python3 bad_script.py 2>&1 | tee build.log 
                    
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

                    # Extract error lines to error_logs.txt
                    #grep -E "ERROR|FAIL|Exception|Traceback|SyntaxError" build_logs.txt > error_logs.txt || true

                    # Run the analyzer script
                    python3 pipeline_analyzer.py build.log
                '''
            }
        }
    }
}
