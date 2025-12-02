pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Restore Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Build Project') {
            steps {
                bat 'dotnet build -c Release --no-restore'
            }
        }

        stage('Run Tests UNITARY') {
            steps {
                bat 'pytest -v '
            }
        }

        stage('Run Tests coverage') {
            steps {
                bat 'pytest --cov=Domain/Entities/Editorial   --cov-report=html ./Test/ '
            }
        }


        stage('Stop IIS AppPool') {
            steps {
                script {
                    // Verificar el estado del AppPool
                    def state = bat(script: 'C:\\Windows\\System32\\inetsrv\\appcmd list apppool /name:CardonIV /text:state', returnStdout: true).trim()

                    if (state.equalsIgnoreCase('Started')) {
                        echo "AppPool CardonIV est� activo. Deteni�ndolo..."
                        bat 'C:\\Windows\\System32\\inetsrv\\appcmd stop apppool /apppool.name:CardonIV'
                    } else {
                        echo "AppPool CardonIV no est� activo. Continuando con el siguiente paso..."
                        bat 'C:\\Windows\\System32\\inetsrv\\appcmd stop apppool /apppool.name:CardonIV'
                    }
                }
            }
        }

        stage('Publish Project') {
            steps {
                bat 'dotnet publish CardonIV.Front/CardonIV.Front.csproj -c Release -o publish_output'
            }
        }

        stage('Deploy to IIS') {
            steps {
                bat 'xcopy /E /Y /I publish_output\\* C:\\inetpub\\wwwroot\\CardonIV\\'
            }
        }

        stage('Start IIS AppPool') {
            steps {
                bat 'C:\\Windows\\System32\\inetsrv\\appcmd start apppool /apppool.name:CardonIV'
            }
        }
    }
}