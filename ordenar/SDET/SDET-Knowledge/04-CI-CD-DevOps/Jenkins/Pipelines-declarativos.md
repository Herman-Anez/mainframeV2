# Pipelines declarativos en Jenkins

Frente a los pipelines scripted (Groovy puro), el modelo **declarativo** impone una estructura más predecible, legible y fácil de mantener. Se define en un archivo llamado `Jenkinsfile` que reside en la raíz del repositorio.

## Estructura básica de un pipeline de pruebas

```groovy
pipeline {
    agent any  // Define el nodo de ejecución (puede ser una etiqueta como 'linux && docker')
    
    environment {
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
            cleanWs() // Limpiar el espacio de trabajo
        }
        success {
            echo 'Todos los tests han pasado satisfactoriamente.'
        }
        failure {
            echo 'Se detectaron fallos en la suite de pruebas.'
        }
    }
}
```

## Elementos clave para el SDET

*   **`agent`**: Define dónde se ejecuta el pipeline. Puede ser `any`, un contenedor Docker, una etiqueta de nodo específica o `none` (para asignar agentes por stage).
*   **`tools`**: Referencias a herramientas preconfiguradas en el sistema (Maven, JDK, Gradle, Node).
*   **`environment`**: Gestión de variables de entorno. Soporta inyección de secretos mediante `credentials('id')`.
*   **`when`**: Condiciona la ejecución de un `stage` según la rama (`branch 'main'`), parámetros o estado previo de la construcción.
*   **`parallel`**: Permite ejecutar sub-stages simultáneamente.
    > [!TIP]
    > Ideal para ejecutar suites de UI en diferentes navegadores al mismo tiempo para reducir el tiempo total de feedback.

```groovy
stage('Cross-Browser Tests') {
    parallel {
        stage('Chrome') { steps { sh 'mvn test -Dbrowser=chrome' } }
        stage('Firefox') { steps { sh 'mvn test -Dbrowser=firefox' } }
    }
}
```

## Buenas prácticas

1.  **Pipeline as Code**: Mantener siempre el `Jenkinsfile` en el repositorio de código.
2.  **Externalización de Lógica**: Evitar incrustar lógica compleja en el pipeline; es preferible llamar a scripts externos (`./run_tests.sh`).
3.  **Shared Libraries**: Reutilizar funciones comunes (notificaciones, subida a S3, etc.) mediante librerías compartidas de Jenkins.
4.  **Gestión de Datos**: Usar `stash`/`unstash` para pasar archivos de resultados entre diferentes nodos de ejecución.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Jenkins para SDET](./index.md) | [Home](../../../index.md) | [Integración con Slack](./Integracion-Slack.md) |