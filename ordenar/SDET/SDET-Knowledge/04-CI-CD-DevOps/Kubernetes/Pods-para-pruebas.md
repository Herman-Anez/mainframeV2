# Pods y Jobs para pruebas

En Kubernetes, la unidad mínima es el **Pod**. Para la automatización de pruebas, lo más común es desplegar **Jobs** o Pods efímeros que nacen, ejecutan la suite y mueren, liberando recursos.

## Job de Kubernetes para Pruebas

Un `Job` crea uno o varios Pods que se ejecutan hasta completar exitosamente (o fallar) la tarea encomendada. Es el recurso ideal para suites de regresión.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: api-test-run
spec:
  backoffLimit: 2  # Número de reintentos en caso de fallo
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
  ttlSecondsAfterFinished: 86400  # Eliminación automática tras 24h
```

## Ventajas del enfoque K8s

*   **Paralelismo**: Se puede lanzar un Job por cada suite (API, UI) e incluso usar el parámetro `parallelism > 1` para distribuir casos entre múltiples pods del mismo Job.
*   **Aislamiento Total**: Cada prueba corre en su propio Pod, eliminando cualquier riesgo de contaminación de estado entre ejecuciones concurrentes.
*   **Escalabilidad Horizontal**: Con herramientas como **KEDA**, se pueden disparar miles de pruebas automáticamente ante eventos específicos.

## Selenium Grid en Kubernetes

Desplegar un Grid escalable es posible mediante el *Helm Chart* oficial de Selenium, que incluye:
1.  **Hub**: Publicado mediante un Service y Deployment.
2.  **Nodos**: Pods que se autoregistran dinámicamente en el Hub.
3.  **Ingress**: Para acceder a la consola del Hub desde fuera del clúster.

## Entornos Efímeros (Ephemeral Environments)

Kubernetes permite crear `namespaces` temporales que contienen todo el stack (App + DB + Mocks + Tests). Al finalizar la ejecución, se destruye el namespace completo, garantizando un entorno inmaculado para cada regresión.

## Consideraciones para el SDET

*   **Gestión de Recursos**: Definir siempre `limits` y `requests` de CPU/RAM. Un test sin límites puede ser eliminado inesperadamente por el *OOM Killer*.
*   **Probes**: Configurar `readinessProbe` y `livenessProbe` en la aplicación bajo prueba para que los tests esperen a que el sistema esté realmente disponible.
*   **Configuración**: Usar `ConfigMaps` para URLs y timeouts, y `Secrets` para credenciales sensibles.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Kubernetes y pruebas](./index.md) | [Home](../../../index.md) | [Rendimiento y Seguridad](../05-Rendimiento-Seguridad/index.md) |