# STRUCTURED CONCURRENCY (PREVIEW)

La Concurrencia Estructurada busca tratar varias tareas concurrentes como una unidad de trabajo, confinando su ciclo de vida a un bloque sintáctico. Esto facilita la cancelación, el manejo de errores y la observabilidad.
Idea central

En lugar de lanzar hilos y unirlos manualmente, se usa un StructuredTaskScope que controla las subtareas. Cuando el bloque termina, el scope espera a que todas las tareas finalicen (o las cancela si falla alguna) antes de continuar. Se asemeja a un try-with-resources.
Ejemplo con ShutdownOnFailure
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> tarea1 = scope.fork(() -> leerBaseDatos());
    Future<Integer> tarea2 = scope.fork(() -> calcularEstadisticas());

    scope.join();            // espera a que todas las subtareas terminen o fallen
    scope.throwIfFailed();   // si alguna falló, lanza la excepción

    String resultado1 = tarea1.resultNow();
    int resultado2 = tarea2.resultNow();
    return combinar(resultado1, resultado2);
}

    fork lanza la tarea y devuelve un Future.

    join() bloquea hasta que todas las tareas finalicen o alguna falle (según política).

    throwIfFailed() propaga cualquier excepción ocurrida en las subtareas.
```

### Políticas de manejo de errores

    ShutdownOnFailure: si cualquier subtarea falla, se cancelan las demás y la excepción se lanza en throwIfFailed.

    ShutdownOnSuccess: obtiene el primer resultado exitoso y cancela las otras (útil para consultas redundantes).

    Se pueden crear políticas propias extendiendo StructuredTaskScope.

### Ventajas

    Árbol de tareas observable: la relación padre‑hijo queda reflejada en los volcados de hilos y herramientas de monitoreo.

    Cancelación automática: al cerrar el scope, se cancelan las subtareas aún en ejecución.

    Código más simple: sin CountDownLatch, ExecutorService manual ni colecciones externas para recolectar resultados.

    Integración con hilos virtuales para máxima escalabilidad.

### Consideraciones

    Al ser preview, puede haber cambios en la API final.

    Requiere habilitar --enable-preview.

    Los Future devueltos por fork no son los mismos Future de java.util.concurrent (son internos del scope), y no se deben pasar fuera del bloque del scope.

    Estado: Preview en Java 21.

