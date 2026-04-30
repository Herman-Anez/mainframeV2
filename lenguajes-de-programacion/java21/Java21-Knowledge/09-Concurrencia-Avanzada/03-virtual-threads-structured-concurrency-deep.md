
# VIRTUAL THREADS Y CONCURRENCIA ESTRUCTURADA EN PROFUNDIDAD
1. Arquitectura interna de los hilos virtuales

Los hilos virtuales se implementan sobre una pequeña cantidad de hilos de plataforma llamados carriers. Cuando un hilo virtual ejecuta una operación que lo bloquearía (I/O, sleep, park), la JVM desmonta el hilo virtual del carrier y lo registra en un heap interno hasta que la condición se complete. El carrier queda libre para ejecutar otro hilo virtual.

    El programador (scheduler) de hilos virtuales es ForkJoinPool con un modo de paralelismo que por defecto iguala al número de procesadores disponibles.

    La pila del hilo virtual se almacena en el heap como objetos Java; al cambiar de contexto solo se intercambian referencias (muy eficiente).

    Se puede monitorear con jcmd y jstack; los volcados muestran hilos virtuales sin coste adicional.

2. Modelo de uso recomendado

    No reutilizar hilos virtuales: son desechables y muy baratos (~1 KB de sobrecarga inicial). Se crea uno por tarea.

    No usar pools: ni Executors.newFixedThreadPool con hilos virtuales; usar directamente el executor virtual.

    Cuidado con el pinning: si un hilo virtual ejecuta código que no se puede desmontar (por ejemplo, un bloque synchronized que no se libera pronto, o un método nativo JNI que bloquea), el carrier queda ocupado y puede reducir la capacidad de concurrencia. En Java 21, algunas situaciones comunes de pinning se han eliminado o mitigado (p.ej., Object.wait() libera el carrier). Para evitar pinning en secciones críticas largas, usar ReentrantLock en lugar de synchronized.

    ThreadLocal: los hilos virtuales soportan ThreadLocal, pero su uso excesivo puede incrementar la memoria porque cada hilo virtual mantiene su copia. En su lugar, se recomiendan Scoped Values (preview) para datos de ámbito controlado.

3. Ejemplo de migración de un servidor

Antes (con pool de plataforma):
```java
ExecutorService pool = Executors.newFixedThreadPool(200);
while (true) {
    Socket s = server.accept();
    pool.submit(() -> manejar(s));
}
```

Ahora (con hilos virtuales):
```java
while (true) {
    Socket s = server.accept();
    Thread.startVirtualThread(() -> manejar(s));
}
```

El código se simplifica, el límite pasa a ser la memoria general de la JVM en lugar de los hilos del SO.
4. Concurrencia estructurada (Structured Concurrency, preview)

La concurrencia estructurada extiende el concepto de hilos virtuales al agrupar varias tareas relacionadas como una unidad de trabajo, confinando su ciclo de vida a un bloque léxico. Se implementa mediante StructuredTaskScope (en java.util.concurrent, preview en Java 21).
StructuredTaskScope.ShutdownOnFailure

El más común: si una subtarea falla, se cancelan las demás y se propaga la excepción.
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> pedido = scope.fork(() -> obtenerPedido(id));
    Future<Cliente> cliente = scope.fork(() -> obtenerCliente(idCliente));

    scope.join();           // espera a que todas las subtareas terminen o falle alguna
    scope.throwIfFailed();  // si alguna falló, lanza la excepción

    // Aquí ambas tareas han finalizado con éxito
    return new Factura(cliente.resultNow(), pedido.resultNow());
}

    fork(Callable) devuelve un Future interno que NO debe salir del scope.

    join() bloquea al hilo virtual actual de manera eficiente. Internamente, la JVM puede desmontar el hilo virtual mientras espera.
```

    Si lanza ThrowIfFailed, las excepciones de las subtareas se agrupan adecuadamente.

### StructuredTaskScope.ShutdownOnSuccess

Útil para obtener el primer resultado exitoso de un conjunto de tareas redundantes y cancelar las otras.
```java
try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
    scope.fork(() -> consultarApi1());
    scope.fork(() -> consultarApi2());

    scope.join();
    String resultado = scope.result();  // obtiene el resultado del primero exitoso
    // las demás tareas se cancelaron automáticamente
}
```

### Custom policies

Podemos extender StructuredTaskScope y sobrescribir handleComplete(Future) para decidir cuándo detener otras tareas.
Integración con Scoped Values

Los valores de ámbito se heredan automáticamente dentro de las subtareas lanzadas por el scope.
```java
ScopedValue.where(TRACE_ID, trace).run(() -> {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        scope.fork(() -> logWithTrace());
        ...
    }
});
```

La combinación de hilos virtuales, scoped values y concurrencia estructurada representa el nuevo estándar para aplicaciones concurrentes seguras y escalables en Java.
5. Observabilidad

    Los hilos virtuales se integran con el sistema de monitoreo: jcmd Thread.dump_to_file captura todos los hilos sin overhead.

    La concurrencia estructurada refleja las relaciones padre-hijo en los nombres de hilos y en los volcados, facilitando la depuración de fallos en cascada.

### 6. Buenas prácticas y transición

    Nuevas aplicaciones: usar hilos virtuales y concurrencia estructurada cuando sea posible.

    Código heredado: las bibliotecas que realizan I/O bloqueante (p.ej., JDBC antiguo) se benefician automáticamente sin cambios; miles de hilos virtuales pueden estar bloqueados en lectura de base de datos sin agotar los hilos del SO.

    Frameworks: Spring Boot 3.2+ ofrece opción para hilos virtuales en Tomcat; Quarkus y Micronaut también.

    Cuidado con la limitación de recursos: aunque los hilos virtuales son baratos, aún se pueden agotar recursos como conexiones de base de datos o memoria total.

# JVM Y RENDIMIENTO EN JAVA 21

La Máquina Virtual Java (JVM) es el entorno de ejecución que convierte el bytecode en instrucciones nativas y gestiona los recursos de la aplicación. Comprenderla a fondo es indispensable para escribir código eficiente, diagnosticar problemas de rendimiento y aprovechar al máximo las mejoras que trae Java 21. A continuación se desarrollan los tres ficheros de esta sección.
