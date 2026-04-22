pipeline {
   agent any
   environment {
       GEMINI_API_KEY = credentials('gemini-api-key')
   }
   stages {
       stage('Install Dependencies') {
           steps {
               sh '''
                   set -o pipefail
                   pip install -r requirements.txt 2>&1 | tee install.log
               '''
           }
       }
       stage('Dependency Validation') {
           steps {
               sh '''
                   set -o pipefail
                   python3 dependency_checker.py 2>&1 | tee validation.log
               '''
           }
       }
       stage('Run Application') {
           steps {
               sh '''
                   set -o pipefail
                   python3 function.py 2>&1 | tee app.log
               '''
           }
       }
   }
   post {
       failure {
           script {
               def log = currentBuild.rawBuild.getLog(1000)
               writeFile file: 'jenkins.log', text: log.join('\n')
           }
           sh '''
               python3 pipeline_analyzer.py jenkins.log install.log validation.log app.log
           '''
       }
   }
}