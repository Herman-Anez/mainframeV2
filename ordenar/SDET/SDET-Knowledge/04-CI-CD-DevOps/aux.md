Profundizaré cada uno de los subtemas del módulo 04-CI-CD-DevOps. Como SDET, no solo ejecutas pruebas, sino que las integras en ciclos automáticos de entrega continua. Aquí verás el control de versiones avanzado, la construcción de pipelines robustos, la contenerización de entornos de prueba y la orquestación en Kubernetes; todo con un enfoque práctico y específico para testing.
Git para SDET

Git es la base de la colaboración en código, incluido el código de automatización. Un SDET maneja escenarios como sincronizar ramas de pruebas, aislar fallos introducidos en un commit específico y gestionar submódulos con utilidades compartidas.
Comandos esenciales

Más allá de add, commit, push, el arsenal avanzado de un SDET cubre:

    Gestión de ramas y estado:

        git fetch --prune: limpia referencias locales a ramas remotas eliminadas.

        git branch -a: lista todas las ramas locales y remotas.

        git checkout -b feature/test-123: crea y cambia a una rama nueva para una historia.

        git stash / git stash pop: guarda cambios rápidamente para cambiar de contexto sin hacer commit (útil cuando estás depurando una prueba y necesitas probar otra rama).

        git stash list / git stash drop: gestionar el stack de cambios temporales.

    Historial y depuración:

        git log --oneline --graph --decorate --all: visualiza el grafo de ramas y merges.

        git diff main...feature/rama o git diff --name-only: ver diferencias de archivos entre ramas.

        git blame <archivo>: identifica quién modificó cada línea; útil para rastrear cuándo un localizador o configuración cambió y empezó a fallar.

        git bisect start / git bisect bad / git bisect good: herramienta de búsqueda binaria para encontrar el commit exacto que introdujo una regresión en las pruebas. Flujo típico: marcas un commit malo (tests fallan) y uno bueno (tests pasan), y Git te va llevando a puntos intermedios para que ejecutes la suite y marques good o bad. Como SDET, puedes automatizar git bisect run con un script que lance el test fallido.

        git revert <commit> vs git reset: el primero crea un nuevo commit que deshace cambios; el segundo mueve el puntero. Para revertir un merge incorrecto, git revert -m 1 <commit>.

    Rebase y sincronización:

        git rebase main: reaplica tus commits de la rama actual sobre la punta de main, manteniendo un historial lineal. Preferible a merge en ramas de características para mantener limpio el historial de la suite de pruebas.

        git rebase --continue / --skip / --abort: control del proceso interactivo.

        git cherry-pick <commit>: trae un commit específico de otra rama sin fusionar toda la rama. Muy usado en automatización para portar una corrección de un flaky test entre ramas de release.

    Submódulos (submodules):

        Muchos equipos centralizan utilidades comunes (drivers, factories, reportes) en un repositorio aparte que se incluye como submódulo en el proyecto de pruebas.

        git submodule add <url> <path> y git submodule update --init --recursive.

        El SDET define la estrategia de versionado para que las pruebas no se rompan por una actualización no deseada del submódulo (apuntar a un tag específico).

    Tags y releases:

        git tag -a v1.2.3 -m "Suite de regresión release 1.2.3" y git push origin --tags: permite vincular exactamente la versión de las pruebas con la versión del producto bajo test. Las pipelines pueden ejecutar la suite etiquetada para una release concreta.

Estrategias de ramas y su impacto en testing

La estrategia de branching define cómo y cuándo se ejecutan las pruebas automáticas. El SDET debe alinear la automatización con estas políticas.

    Git Flow (ramos main, develop, feature, release, hotfix)

        Ramas feature: Las pruebas unitarias y de integración deben ejecutarse en cada push a la rama. El SDET asegura que en el PR se ejecuten suites rápidas (smoke, unit, API) con feedback < 5 min.

        Ramas release: Antes de fusionar en main, se ejecuta la suite completa de regresión (incluyendo UI y rendimiento). El SDET configura el pipeline para que ejecute en paralelo y genere reportes de cobertura y estabilidad.

        Hotfix: Requieren pruebas aceleradas focalizadas en el error corregido, más una suite de humo para no romper nada.

        Inconveniente: Las ramas de larga duración (develop) pueden acumular divergencias; las pruebas pueden fallar en release al mezclar features.

    GitHub Flow (ramas feature desde main con despliegue continuo)

        Es simple: una sola rama principal (main), ramas de feature cortas, y PR hacia main.

        Testing continuo: en el PR se lanza la suite completa. El SDET configura la ejecución según el contexto: si el cambio es solo documentación, se salta la batería de tests.

        El reto es garantizar que la suite no dure más de 10-15 minutos; si es más pesada, se aplica paralelismo extremo o se dividen las suites en required (bloqueantes) y optional (informativas, que no impiden merge si fallan pero se monitorizan).

    Trunk-Based Development (rama única trunk con feature flags)

        Los desarrolladores hacen commit directo a trunk (o ramas de vida <1 día). Esto exige una calidad extrema de las pruebas automáticas.

        El SDET implementa test gating: antes de que un commit llegue al repositorio central, se ejecuta una suite pre-commit (unit + integration ligeras) en el entorno del desarrollador.

        La suite completa se ejecuta post-commit en CI, y si falla, revierte automáticamente el cambio o alerta inmediatamente.

Estrategia de pruebas por rama y entorno:

    Archivos de configuración de pruebas por entorno (test-config-dev.yml, test-config-staging.yml) se versionan en el mismo repositorio o en un repo de configuración.

    Los tests deben ser agnósticos de la rama, pero sensibles al entorno; las variables se inyectan en la pipeline.

Jenkins para SDET

Jenkins sigue siendo el orquestador de pipelines más extendido en entornos empresariales. Como SDET, escribes pipelines para construir, empaquetar y probar el producto.
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

Integración con Slack

El feedback inmediato a todo el equipo cuando una suite falla es crítico. La integración se hace en la sección post del pipeline o mediante una shared library.

Paso a paso con el plugin de Slack:

    Instalar el plugin "Slack Notification" en Jenkins.

    Configurar en "Manage Jenkins > Configure System" el espacio de trabajo de Slack y el token (usando un secret text credential).

    En el Jenkinsfile, se usa slackSend:
    groovy

    post {
        success {
            slackSend (
                channel: '#qa-alerts',
                color: 'good',
                message: "Suite de tests pasó: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Ver>)"
            )
        }
        failure {
            slackSend (
                channel: '#qa-alerts',
                color: 'danger',
                message: "Suite de tests FALLÓ: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Ver>)"
            )
        }
    }

    Se puede personalizar para adjuntar un resumen de los test results (total, fallidos, saltados) extrayendo la información de los archivos junit o mediante slackUploadFile.

Mensajes condicionales avanzados:

    Notificar solo si falla en la rama main o en una rama de release.

    Incluir menciones a responsables (@canal) en casos críticos.

    Usar slackSend con attachments para dar formato estructurado (campos title, pretext, fields).

Alternativas: Microsoft Teams con el plugin Office 365 Connector, o webhooks genéricos.
GitHub Actions

GitHub Actions es la opción nativa de CI/CD integrada en GitHub que ha ganado mucha tracción porque el pipeline se define como código en .github/workflows/*.yml y se gestiona todo desde el repositorio.
Workflows y acciones para testing

Un workflow se compone de uno o más jobs con pasos que ejecutan acciones (scripts, comandos, o acciones reutilizables). El SDET lo ve como la herramienta para ejecutar baterías de test automáticas en cada push, PR y programación.

Estructura de un workflow de pruebas típico:
yaml

name: Test Suite
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 6 * * 1-5'  # ejecución diaria a las 6 AM

env:
  NODE_VERSION: 18

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run test:unit
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        if: success()

  integration-and-api-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - run: mvn -B verify -Pintegration

  e2e-tests:
    needs: integration-and-api-tests
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        browser: [chromium, firefox, webkit]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      - run: npx playwright install --with-deps ${{ matrix.browser }}
      - run: npx playwright test --project=${{ matrix.browser }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report-${{ matrix.browser }}
          path: playwright-report/

Características destacadas para el SDET:

    Matrix strategy: permite ejecutar tests en combinaciones de sistema operativo, versión de lenguaje, navegador. Ideal para cross-browser y cross-platform con un solo job.

    Service containers: bases de datos, Selenium Hub, wiremock. Se definen directamente en el workflow, facilitando entornos de integración reales sin necesidad de hosts externos.

    Caching: actions/cache para dependencias (Maven, npm) acelera las ejecuciones.

    Artifacts y reports: actions/upload-artifact permite guardar reportes, logs, screenshots para su revisión en caso de fallo.

    Reusabilidad: se pueden escribir acciones compuestas y workflows reusables que encapsulan pasos comunes (ej. "run-api-tests" que recibe como input el entorno).

    Condiciones y gates: con if se pueden ejecutar pruebas de rendimiento solo en horarios específicos, o saltar suites si el commit solo cambia documentación.

Consideraciones de seguridad:

    Los secretos (secrets.BROWSERSTACK_KEY) se configuran en GitHub y se evita exponerlos en logs.

    Los workflows que vienen de forks de PR pueden no tener acceso a secretos; se debe diseñar la suite para que no dependa de datos confidenciales en esos casos, o usar pull_request_target con precaución.

Para el SDET, Actions facilita la integración temprana de pruebas; permite que cualquier desarrollador pueda ver el resultado de los tests directamente en el PR, fomentando la propiedad compartida de calidad.
Docker para entornos de prueba

Docker proporciona entornos ligeros, idénticos en desarrollo, CI y producción. Para testing, resuelve el problema del “en mi máquina funciona” y permite una escalabilidad masiva.
Dockerfiles para testing

Un Dockerfile define la imagen que contiene todas las dependencias necesarias para ejecutar las pruebas. El SDET lo crea para encapsular la suite de automatización y sus herramientas.

Ejemplo de Dockerfile para un proyecto Java + Selenium:
dockerfile

FROM maven:3.9-eclipse-temurin-17

# Instalar dependencias de sistema para navegadores headless
RUN apt-get update && apt-get install -y \
    wget gnupg unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Chrome y ChromeDriver (usando script oficial)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Descargar ChromeDriver compatible (se puede automatizar con WebDriverManager en el código de test)

# Copiar el código de pruebas
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src

# Por defecto, ejecutar la suite completa
CMD ["mvn", "test", "-Denv=staging", "-Dheadless=true"]

Buenas prácticas para SDET:

    Multi-stage builds: Construir artefactos en una stage y copiar solo lo necesario a la imagen final, reduciendo tamaño y superficie de ataque.

    Ejecutar como non-root: crear un usuario tester con permisos limitados.

    Manejo de secretos: no incluir contraseñas en la imagen; pasarlas como variables de entorno en tiempo de ejecución (-e DB_PASS=$DB_PASS).

    Tagging: versionar las imágenes con el commit SHA o la versión de la suite, para auditar qué versión de pruebas se ejecutó.

Docker Compose para entornos de testing completos:
Un archivo docker-compose.test.yml puede levantar la aplicación bajo test, la base de datos, un mock de terceros, y el contenedor de pruebas, todo interconectado. El SDET lo usa para pruebas de integración que requieren todo el stack.
yaml

version: '3'
services:
  app:
    image: myapp:latest
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://db:5432/test
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: test
  tests:
    build: .
    environment:
      APP_URL: http://app:8080
    depends_on:
      - app
      - db
    volumes:
      - ./reports:/app/reports

El comando docker-compose -f docker-compose.test.yml run tests ejecuta las pruebas y extrae los reportes al host. En CI esto se convierte en un paso simple.
Selenium Grid con Docker

Ejecutar pruebas UI en paralelo requiere una granja de navegadores. Selenium Grid se puede desplegar con Docker de forma oficial y robusta.

Selenium Grid 4 con Docker (hub + nodos):

    Imagen oficial: selenium/hub:4.0 y selenium/node-chrome:4.0, etc.

    Docker Compose clásico (Grid independiente):

yaml

version: '3'
services:
  selenium-hub:
    image: selenium/hub:4.0
    container_name: selenium-hub
    ports:
      - "4444:4444"
  chrome:
    image: selenium/node-chrome:4.0
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
  firefox:
    image: selenium/node-firefox:4.0
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443

    El test se conecta a http://localhost:4444 usando RemoteWebDriver y especificando capacidades del navegador.

Modo dinámico (Selenium Grid 4): No se necesita declarar los nodos; los nodos se registran automáticamente en el hub usando el mismo network. Se puede usar el docker-compose de la documentación oficial.

Alternativas avanzadas:

    Selenoid: contenedores efímeros por sesión, velocidad y menor consumo de recursos. Tiene UI para ver las sesiones y grabar vídeo.

    Zalenium (deprecado): fue precursor, hoy reemplazado por Selenoid/Selenium Grid 4.

    Moon (comercial): para clústeres Kubernetes, con balanceo y gestión de cuotas.

Integración en CI:
En GitHub Actions o Jenkins, se levanta el Grid como services o en un stage previo. Luego la suite usa RemoteWebDriver para ejecutar en remoto. Ejemplo con GitHub Actions services:
yaml

services:
  selenium:
    image: selenium/standalone-chrome
    ports:
      - 4444:4444

Luego el código apunta a http://localhost:4444/wd/hub.

El SDET configura la infraestructura de Grid y se encarga de la escalabilidad: si se necesitan 50 sesiones concurrentes, diseñará la estrategia de nodos y recursos en el clúster (Docker Swarm o Kubernetes).
Kubernetes y pruebas

Cuando la escala y la orquestación superan a un simple Docker Compose, Kubernetes (K8s) es la plataforma donde se ejecutan tanto la aplicación como las pruebas.
Pods para pruebas

En K8s, la unidad mínima es el Pod (uno o más contenedores). Para ejecutar pruebas de automatización, se despliegan Jobs o Pods efímeros.

Job de Kubernetes para pruebas:
Un Job crea uno o varios Pods que se ejecutan hasta completar exitosamente (o fallar) un número de veces. Es ideal para suites de test que deben correr hasta el final y luego terminar.
yaml

apiVersion: batch/v1
kind: Job
metadata:
  name: api-test-run-{{ .Release.Name }}
spec:
  backoffLimit: 2  # reintentos en caso de fallo
  template:
    spec:
      containers:
        - name: tester
          image: registry/my-test-image:1.0
          env:
            - name: BASE_URL
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: api_url
            - name: DB_PASS
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: password
          command: ["pytest", "tests/api", "-v", "--junitxml=/results/report.xml"]
          volumeMounts:
            - name: results
              mountPath: /results
      restartPolicy: Never
      volumes:
        - name: results
          emptyDir: {}
  ttlSecondsAfterFinished: 86400  # autoeliminar tras 24h

Ventajas:

    Paralelismo: Se puede lanzar un Job por cada suite (API, UI) e incluso usar parallelism > 1 para que se ejecuten múltiples pods del mismo Job (p.ej., 10 pods para pruebas UI con un parámetro que distribuya los casos usando índices).

    Aislamiento: Cada prueba corre en su propio Pod, evitando contaminación de estado entre pruebas.

    Escalabilidad horizontal: Con herramientas como KEDA o Jobs programados, se pueden disparar miles de pruebas automáticamente ante eventos.

Selenium Grid en Kubernetes:
Desplegar un Grid escalable en K8s usando el Helm Chart oficial de Selenium. Incluye:

    Hub (Service y Deployment)

    Nodos como pods que se autoregistran.

    Ingress para acceder al Hub desde fuera del clúster.
    El SDET lanza las pruebas desde un Pod del mismo namespace, apuntando a http://selenium-hub:4444. Las sesiones se distribuyen entre los nodos disponibles.

Ephemeral test environments:
Con K8s, se pueden crear namespaces temporales que contengan la app bajo test, bases de datos, mocks, y el job de pruebas. Una vez finalizado, se destruye todo. Esto garantiza un entorno inmaculado para cada ejecución de regresión.

Pruebas de rendimiento en Kubernetes:
Herramientas como k6 operator ejecutan scripts de carga definiendo un recurso TestRun. El operador crea pods con k6 que inyectan carga y publican métricas.

Consideraciones para el SDET:

    Definir resources (CPU/memoria) tanto para los tests como para los servicios; un test que consume demasiada RAM puede ser matado por el scheduler.

    readinessProbe y livenessProbe en la app bajo prueba para que el Job de test espere hasta que el sistema esté disponible.

    Usar ConfigMaps para datos de configuración de pruebas (URLs, timeouts) y Secrets para credenciales.

El manejo de pruebas en Kubernetes cierra el círculo de la automatización moderna: desde el commit de código hasta la ejecución de suites en un entorno aislado, escalable y autogestionado.

Estos componentes del módulo CI/CD/DevOps te dan el control sobre cómo, cuándo y dónde se ejecutan las pruebas. Un SDET que domina Git, pipelines, Docker y Kubernetes se convierte en el habilitador de la calidad continua en toda la organización.
