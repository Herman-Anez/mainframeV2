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