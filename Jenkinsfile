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
                    #echo 'print("Hello World)' > bad_script.py
                    #python3 bad_script.py > build_logs.txt 2>&1 || true
                    set -o pipefail
                    python3 function.py 2>&1 | tee build.log 
                '''
            }
        }

        // You can add more stages here as needed, for example, stages for building, deploying, etc.
    }

    post {
        failure {
            script {
                def log=currentBuild.rawBuild.getLog(1000)
                writeFile file: 'jenkins.log', text: log.join('\n')
            }   
            sh '''
                # Install the NEW required library for Gemini if not already present
                #pip3 install google-genai --break-system-packages || true

                # Run the analyzer script
                python3 pipeline_analyzer.py build.log jenkins.log
                '''
        }
    }
}
