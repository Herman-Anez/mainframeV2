Pipelines declarativos

Frente a los pipelines scripted (Groovy puro), el declarativo impone una estructura más predecible y fácil de mantener. Se define en un Jenkinsfile dentro del repositorio.

Estructura básica de un pipeline de pruebas declarativo:
groovy

pipeline {
    agent any  // o un nodo con etiqueta como 'linux && docker'
    
    environment {
        // Variables globales
        MAVEN_HOME = tool 'Maven 3.8'
        TEST_ENV = 'staging'
    }

    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Navegador para pruebas UI')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://repo.git'
            }
        }
        stage('Build & Unit Tests') {
            steps {
                sh 'mvn clean test -DskipITs'
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }
        stage('Integration Tests') {
            steps {
                sh 'mvn verify -Pintegration'
            }
        }
        stage('UI Tests') {
            when {
                expression { params.BROWSER != null }
            }
            steps {
                sh 'mvn test -Dsuite=ui -Dbrowser=${BROWSER}'
            }
        }
        stage('Performance Tests') {
            when {
                branch 'main'
            }
            steps {
                sh 'jmeter -n -t stress.jmx ...'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: '**/reports/**', allowEmptyArchive: true
            // limpiar espacio de trabajo si es necesario
            cleanWs()
        }
        success {
            echo 'Todos los tests han pasado.'
        }
        failure {
            echo 'Hay fallos en la suite.'
        }
    }
}

Elementos clave:

    agent: define dónde se ejecuta. Puede ser any, un nodo Docker, una etiqueta específica, o incluso none para asignar agentes por stage.

    tools: referencias a herramientas configuradas en Jenkins (Maven, JDK, Gradle, Node).

    environment: variables de entorno, soporta credenciales con credentials('id').

    when: condiciona la ejecución de un stage según rama (branch 'main'), parámetros o estado de la construcción.

    parallel: dentro de un stage se puede definir un bloque parallel con sub-stages. Así se ejecutan suites de UI en distintos navegadores simultáneamente:
    groovy

    stage('Cross-Browser Tests') {
        parallel {
            stage('Chrome') { steps { sh 'mvn test -Dbrowser=chrome' } }
            stage('Firefox') { steps { sh 'mvn test -Dbrowser=firefox' } }
        }
    }

Buenas prácticas:

    Mantener el Jenkinsfile en el repositorio (Pipeline as Code).

    Externalizar scripts complejos a sh que llamen a un script específico (./run_tests.sh) para no incrustar lógica en el pipeline.

    Usar shared libraries para reutilizar funciones frecuentes como sendSlackNotification, uploadToS3, etc.

    Gestionar los datos de prueba con stash/unstash cuando necesitas pasar archivos entre stages en diferentes nodos.