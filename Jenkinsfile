pipeline {
    agent any
    
    stages {
        stage('Clonar repositorio') {
            steps {
                script {
                    git credentialsId: 'github-token',
                        url: 'https://github.com/richifor/ventabus.git',
                        branch: 'main'
                }
            }
        }
        
        stage('Instalar dependencias') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Verificación de calidad de código') {
            steps {
                sh 'echo "Control de calidad de código. Evaluando el porcentaje con pylint"'
                sh 'pylint --rcfile=.pylintrc bus/srv_bus.py registro/registro.py cajero/caja.py tienda/tienda.py | tee pylint_report.txt'
                script {
                    def pylintReport = readFile('pylint_report.txt')
                    def match = pylintReport =~ /Your code has been rated at ([-+]?[0-9]*\.?[0-9]+)\/10/
                    def pylintScore = match[0][1].toDouble() * 10
                    echo "Puntuación de pylint: ${pylintScore}%"
                    if (pylintScore < 70) {
                        echo "La puntuación de pylint es inferior al 70%. Enviando notificación al desarrollador."
                        // Agrega el código para enviar la notificación al desarrollador aquí
                        error('Pylint score es inferior al 70%')
                    }
                }
            }
        }
        
        stage('Ejecutar Docker Compose') {
            steps {
                sh 'docker-compose up -d'
            }
        }
        
        stage('Ejecutar pruebas unitarias') {
            steps {
                sh 'python -m unittest testunitarios.test_srv_bus'
                sh 'python -m unittest testunitarios.test_registro'
                sh 'python -m unittest testunitarios.test_caja'
                sh 'python -m unittest testunitarios.test_tienda'
            }
        }
        
        stage('Pruebas de integración') {
            steps {
                sh 'python -m unittest testunitarios.test_integracion'
            }
        }
        
        stage('Limpieza') {
            steps {
                sh 'docker-compose down'
                sh 'docker rmi $(docker images -q)'
            }
        }
        
        stage('Despliegue') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
