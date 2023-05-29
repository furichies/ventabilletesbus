pipeline {
    agent any
    
    stages {
        stage('Clonar Repositorio') {
            steps {
                git branch: 'quality', credentialsId: 'github-credentials', url: 'https://github.com/richifor/ventabus.git'
            }
        }
        
        stage('Construir y Probar Aplicación Bus') {
            steps {
                dir('bus') {
                    sh 'docker-compose build'
                    sh 'docker-compose up -d'
                    sh 'docker-compose exec app python -m unittest discover testunitarios'
                    sh 'docker-compose down'
                }
            }
        }
        
        stage('Construir y Probar Aplicación Registro') {
            steps {
                dir('registro') {
                    sh 'docker-compose build'
                    sh 'docker-compose up -d'
                    sh 'docker-compose exec app python -m unittest discover testunitarios'
                    sh 'docker-compose down'
                }
            }
        }
        
        stage('Construir y Probar Aplicación Caja') {
            steps {
                dir('cajero') {
                    sh 'docker-compose build'
                    sh 'docker-compose up -d'
                    sh 'docker-compose exec app python -m unittest discover testunitarios'
                    sh 'docker-compose down'
                }
            }
        }
        
        stage('Construir y Probar Aplicación Tienda') {
            steps {
                dir('tienda') {
                    sh 'docker-compose build'
                    sh 'docker-compose up -d'
                    sh 'docker-compose exec app python -m unittest discover testunitarios'
                    sh 'docker-compose down'
                }
            }
        }
        
        stage('Ejecutar pylint') {
            steps {
                sh 'pylint bus/srv_bus.py'
                sh 'pylint registro/registro.py'
                sh 'pylint cajero/caja.py'
                sh 'pylint tienda/tienda.py'
            }
        }
        
        stage('Construir Imágenes Docker') {
            steps {
                dir('bus') {
                    sh 'docker build -t bus-app .'
                }
                
                dir('registro') {
                    sh 'docker build -t registro-app .'
                }
                
                dir('cajero') {
                    sh 'docker build -t caja-app .'
                }
                
                dir('tienda') {
                    sh 'docker build -t tienda-app .'
                }
            }
        }
    }
}
