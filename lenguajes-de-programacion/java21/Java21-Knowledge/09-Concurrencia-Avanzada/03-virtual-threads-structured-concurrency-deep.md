# 🚀 Virtual Threads y Concurrencia Estructurada

Los hilos virtuales y la concurrencia estructurada representan el nuevo estándar para aplicaciones concurrentes seguras y escalables en Java.

---

## 🏗️ Arquitectura interna de los hilos virtuales

Los hilos virtuales se implementan sobre una pequeña cantidad de hilos de plataforma llamados **carriers**. Cuando un hilo virtual ejecuta una operación que lo bloquearía (I/O, `sleep`, `park`), la JVM desmonta el hilo virtual del carrier y lo registra en un heap interno hasta que la condición se complete. El carrier queda libre para ejecutar otro hilo virtual.

*   El programador (**scheduler**) de hilos virtuales es `ForkJoinPool` con un modo de paralelismo que por defecto iguala al número de procesadores disponibles.
*   La pila del hilo virtual se almacena en el **heap** como objetos Java; al cambiar de contexto solo se intercambian referencias (muy eficiente).
*   Se puede monitorear con `jcmd` y `jstack`; los volcados muestran hilos virtuales sin coste adicional.

---

## 💡 Modelo de uso recomendado

*   **No reutilizar hilos virtuales:** Son desechables y muy baratos (~1 KB de sobrecarga inicial). Se crea uno por tarea.
*   **No usar pools:** Ni `Executors.newFixedThreadPool` con hilos virtuales; usar directamente el executor virtual.
*   **Cuidado con el pinning:** Si un hilo virtual ejecuta código que no se puede desmontar (por ejemplo, un bloque `synchronized` largo o un método nativo JNI que bloquea), el carrier queda ocupado. 

> [!TIP]
> En Java 21, muchas situaciones de pinning se han mitigado (por ejemplo, `Object.wait()` ahora libera el carrier). Para evitar pinning en secciones críticas largas, se recomienda usar `ReentrantLock` en lugar de `synchronized`.

*   **ThreadLocal:** Los hilos virtuales soportan `ThreadLocal`, pero su uso excesivo puede incrementar la memoria. Se recomiendan **Scoped Values** (preview) para datos de ámbito controlado.

---

## 💻 Ejemplo de migración de un servidor

### Antes (con pool de plataforma)
```java
ExecutorService pool = Executors.newFixedThreadPool(200);
while (true) {
    Socket s = server.accept();
    pool.submit(() -> manejar(s));
}
```

### Ahora (con hilos virtuales)
```java
while (true) {
    Socket s = server.accept();
    Thread.startVirtualThread(() -> manejar(s));
}
```

> [!NOTE]
> El código se simplifica y el límite pasa a ser la memoria general de la JVM en lugar de los hilos del SO.

---

## 🧩 Concurrencia Estructurada (Preview)

La concurrencia estructurada agrupa varias tareas relacionadas como una unidad de trabajo, confinando su ciclo de vida a un bloque léxico. Se implementa mediante `StructuredTaskScope`.

### `StructuredTaskScope.ShutdownOnFailure`

Si una subtarea falla, se cancelan las demás y se propaga la excepción.

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> pedido = scope.fork(() -> obtenerPedido(id));
    Future<Cliente> cliente = scope.fork(() -> obtenerCliente(idCliente));

    scope.join();           // espera a que todas las subtareas terminen o falle alguna
    scope.throwIfFailed();  // si alguna falló, lanza la excepción

    // Aquí ambas tareas han finalizado con éxito
    return new Factura(cliente.resultNow(), pedido.resultNow());
}
```

*   `fork(Callable)` devuelve un `Future` interno que **no debe salir del scope**.
*   `join()` bloquea al hilo virtual actual de manera eficiente.

### `StructuredTaskScope.ShutdownOnSuccess`

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
---

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

## 🔍 Observabilidad

*   Los hilos virtuales se integran con el sistema de monitoreo: `jcmd Thread.dump_to_file` captura todos los hilos sin overhead.
*   La concurrencia estructurada refleja las relaciones padre-hijo en los nombres de hilos y en los volcados, facilitando la depuración.

---

## 🌟 Buenas prácticas y transición

*   **Nuevas aplicaciones:** Usar hilos virtuales y concurrencia estructurada cuando sea posible.
*   **Código heredado:** Las bibliotecas con I/O bloqueante se benefician automáticamente.
*   **Frameworks:** Spring Boot 3.2+, Quarkus y Micronaut ya ofrecen soporte.

> [!CAUTION]
>Cuidado con la limitación de recursos:   Aunque los hilos virtuales son baratos, aún se pueden agotar recursos como conexiones de base de datos o memoria total.

---

# JVM Y RENDIMIENTO EN JAVA 21

La Máquina Virtual Java (JVM) es el entorno de ejecución que convierte el bytecode en instrucciones nativas y gestiona los recursos de la aplicación. Comprenderla a fondo es indispensable para escribir código eficiente, diagnosticar problemas de rendimiento y aprovechar al máximo las mejoras que trae Java 21. A continuación se desarrollan los tres ficheros de esta sección.


## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../../README.md)
- [☕ Java 21 Index](../../../index.md)
- [⬅️ Anterior: Executors y Futures](./02-executors-futures.md)
