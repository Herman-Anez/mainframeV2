# 🧵 Virtual Threads (Project Loom)

Los hilos virtuales son la respuesta de Java para la programación concurrente masiva de una manera sencilla y eficiente. Se integran sin cambios en la gran mayoría del código existente.

---

## ❓ ¿Qué son?

Los hilos del sistema operativo (hilos de plataforma) son recursos costosos (típicamente ~1 MB de pila por hilo). Los hilos virtuales son hilos ligeros gestionados por la JVM que se multiplexan sobre un pequeño número de hilos de plataforma (**carriers**). Cuando un hilo virtual se bloquea (por I/O, sleep, espera en un lock), su carrier puede ejecutar otro hilo virtual, liberando el recurso del SO.

Esto permite el modelo «un hilo por petición» escalando a millones de tareas concurrentes sin el coste de memoria ni de cambio de contexto.

---

## 🛠️ Creación y uso

### Mediante `Thread.startVirtualThread`

```java
Thread.startVirtualThread(() -> {
    System.out.println("Ejecutando en hilo virtual: " + Thread.currentThread());
});
```

### Con `Executors.newVirtualThreadPerTaskExecutor()`

Devuelve un `ExecutorService` que asigna un nuevo hilo virtual a cada tarea:

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> procesar());
    executor.submit(() -> recuperar());
} // se cierra el executor tras las tareas
```

### Con el nuevo `Thread.Builder` (API más flexible)

```java
Thread.Builder builder = Thread.ofVirtual()
        .name("worker-", 0)
        .uncaughtExceptionHandler((t, e) -> e.printStackTrace());
Thread hilo = builder.start(() -> { ... });
```

---

## 🔑 Características importantes

> [!NOTE]
> *   Los hilos virtuales son **daemon** por defecto y no tienen prioridad (no aplica).
> *   **No se deben agrupar en pools:** crear un hilo virtual es tan barato (~1 KB) que se crean y descartan según necesidad. La API del executor proporciona un pool conceptual que genera uno nuevo por tarea.
> *   No hay problema si un hilo virtual bloquea (con `sleep`, `LockSupport.park()`, I/O síncrona). La JVM desacopla el carrier.

> [!IMPORTANT]
> Los problemas tradicionales con `ThreadLocal` y `synchronized` son más evidentes con millones de hilos: `synchronized` en grano grueso puede causar **pinning** (el hilo virtual se ancla al carrier, impidiendo su liberación). Se recomienda sustituir `synchronized` por `ReentrantLock` en nuevos desarrollos de alta concurrencia.

---

## 💻 Ejemplo de servicio web

```java
try (var serverSocket = new ServerSocket(8080)) {
    while (true) {
        Socket socket = serverSocket.accept();
        Thread.startVirtualThread(() -> handleRequest(socket));
    }
}
```

Con miles de conexiones simultáneas, este código sigue funcionando con un consumo mínimo de recursos.

---

## 🚀 Migración

No es necesario reescribir código legacy. Cualquier aplicación que use `ExecutorService`, `Thread` o frameworks como **Spring Boot 3.2+** (activando `spring.threads.virtual.enabled=true`) puede aprovechar los hilos virtuales casi de inmediato.

> [!TIP]
> **Estado:** Definitivo en Java 21. Sin necesidad de flags adicionales.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../../README.md)
- [☕ Java 21 Index](../../../index.md)

