pipeline {
    agent any
    
    stages {
        stage('Clonar repositorio') {
              agent { 
            node{
              label "slave1"; 
              }
          }      
            steps {
                script {
                    git credentialsId: 'github-token',
                        url: 'https://github.com/richifor/ventabus.git',
                        branch: 'main'
                }
            }
        }
        
        stage('Instalar dependencias') {
               agent { 
            node{
              label "slave1"; 
              }
          }         
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }
        
        stage('Verificación de calidad de código') {
               agent { 
            node{
              label "slave1"; 
              }
          }         
            steps {
                sh 'echo "Control de calidad de código. Evaluando el porcentaje con pylint"'
                sh 'python3 -m pylint --generate-rcfile > .pylintrc'

                sh 'python3 -m pylint --rcfile=.pylintrc bus/srv_bus.py registro/registro.py cajero/caja.py tienda/tienda.py | tee pylint_report.txt'
                script {
                    def pylintReport = readFile('pylint_report.txt')
                    def match = pylintReport =~ /Your code has been rated at ([-+]?[0-9]*\.?[0-9]+)\/10/
                    def pylintScore = match[0][1].toDouble() * 10
                    echo "Puntuación de pylint: ${pylintScore}%"
                    if (pylintScore < 70) {
                        echo "La puntuación de pylint es inferior al 70%. Enviando notificación al desarrollador."
                        // Analizar método de notificación para que no falle ... falta el smtp para el mail.. hay que pensarlo. 
                        error('Pylint score es inferior al 70%')
                    }
                }
            }
        }
        
        stage('Ejecutar Docker Compose') {
               agent { 
            node{
              label "slave1"; 
              }
          }         
            steps {
                sh 'docker compose up -d'
            }
        }
        
        stage('Ejecutar pruebas unitarias') {
               agent { 
            node{
              label "slave1"; 
              }
          }         
            steps {
                sh 'python3 -m unittest testunitarios.test_srv_bus'
                sh 'python3 -m unittest testunitarios.test_registro'
                sh 'python3 -m unittest testunitarios.test_caja'
                sh 'python3 -m unittest testunitarios.test_tienda'
            }
        }
        
        stage('Pruebas de integración') {
               agent { 
            node{
              label "slave1"; 
              }
          }         
            steps {
                sh 'python3 -m unittest testunitarios.test_integracion'
            }
        }
        
        stage('Limpieza') {
               agent { 
            node{
              label "slave1"; 
              }
          }         
            steps {
                sh 'docker compose down'
                sh 'docker rmi -f $(docker images -q)'
            }
        }
        
        stage('Despliegue') {
               agent { 
            node{
              label "slave2"; 
              }
          }         
            steps {
                 script {
                    git credentialsId: 'github-token',
                        url: 'https://github.com/richifor/ventabus.git',
                        branch: 'main'
                }
                sh 'python3 -m pip install -r requirements.txt'
                sh 'docker compose up -d'
            }
        }
    }
}
