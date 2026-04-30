# ⚡ Executors y Futures

El framework Executors (desde Java 5) desacopla la definición de una tarea de la mecánica de ejecución. Permite manejar pools de hilos, programación periódica y obtener resultados de manera asincrónica.

---

## 🏛️ La interfaz `Executor`

```java
void execute(Runnable command);
```

La implementación más simple ejecuta el comando en un hilo nuevo o directamente en el invocador. No se usa casi nunca directamente; su subinterfaz `ExecutorService` es la relevante.

---

## ⚙️ `ExecutorService` y sus implementaciones

`ExecutorService` añade métodos para el ciclo de vida:

*   **`submit(Callable<T>)`** y **`submit(Runnable)`** devuelven un `Future`.
*   **`invokeAll()`**, **`invokeAny()`**.
*   **`shutdown()`** y **`shutdownNow()`**.

Obtenemos instancias mediante la clase `Executors` (factory methods):

*   **`Executors.newFixedThreadPool(int)`**: Pool con un número fijo de hilos.
*   **`Executors.newCachedThreadPool()`**: Crea hilos bajo demanda y los reutiliza.
*   **`Executors.newSingleThreadExecutor()`**: Un único hilo que ejecuta tareas secuencialmente.
*   **`Executors.newScheduledThreadPool(int)`**: Para tareas programadas o periódicas.
*   **`Executors.newWorkStealingPool()`**: Pool basado en `ForkJoinPool`.
*   **Java 21 - `Executors.newVirtualThreadPerTaskExecutor()`**: Crea un hilo virtual por cada tarea.

---

## 📦 `Callable` y `Future`

`Callable<V>` es como `Runnable` pero devuelve un resultado y puede lanzar excepciones comprobadas.

```java
Callable<Integer> tarea = () -> {
    Thread.sleep(100);
    return 42;
};
Future<Integer> futuro = executor.submit(tarea);
// ... hacer otras cosas
Integer resultado = futuro.get(); // bloquea hasta que esté disponible
```

`Future` ofrece:
*   `get()` con o sin timeout.
*   `cancel(boolean)`: Intenta cancelar la tarea.
*   `isDone()`, `isCancelled()`.

---

## ⚠️ Limitaciones de `Future`

> [!WARNING]
> *   No hay forma de componer múltiples futures sin bloqueos manuales.
> *   No se puede reaccionar a la finalización de una tarea de manera no bloqueante (salvo encuestas).
> *   Errores difíciles de manejar en cadenas.

---

## 🚀 `CompletableFuture` (Java 8+)

`CompletableFuture<T>` implementa `Future` y `CompletionStage`, proporcionando un modelo de programación asíncrona rico y no bloqueante.

### Creación
```java
CompletableFuture.supplyAsync(() -> calcular());
CompletableFuture.runAsync(() -> enviarMensaje());
```

> [!NOTE]
> Sin especificar `Executor` usan el `ForkJoinPool.commonPool()`; se puede pasar un `Executor`.

### Composición

*   **`thenApply(Function)`**: Transforma el resultado.
*   **`thenAccept(Consumer)`**: Consume el resultado.
*   **`thenRun(Runnable)`**: Ejecuta acción tras finalizar, sin usar el resultado.
*   **`thenCompose(Function)`**: Encadena otro `CompletableFuture` (flatMap).
*   **`thenCombine(other, BiFunction)`**: Combina dos futures independientes.

```java
CompletableFuture<String> futuro = CompletableFuture
    .supplyAsync(() -> obtenerId())
    .thenCompose(id -> CompletableFuture.supplyAsync(() -> buscarPorId(id)))
    .thenApply(entidad -> entidad.getNombre())
    .exceptionally(ex -> "Error: " + ex.getMessage());
```

### Métodos de coordinación

*   **`allOf(...)`**: Espera a que todos los futures especificados terminen.
*   **`anyOf(...)`**: Devuelve el resultado del primero que termine.

### Completado manual

*   **`complete(valor)`**: Completa el futuro con un valor si aún no se ha completado.
*   **`completeExceptionally(Throwable)`**: Completa con una excepción.

---

## 📅 `ScheduledExecutorService`

Permite programar tareas para ejecutarse tras un retraso o de forma periódica:

*   **`schedule(Callable, delay, unit)`**: Ejecución única diferida.
*   **`scheduleAtFixedRate(Runnable, delay, period, unit)`**: Tarea periódica a intervalos regulares, sin importar el tiempo de ejecución.
*   **`scheduleWithFixedDelay(Runnable, delay, delay, unit)`**: Tarea periódica con retraso entre finalización e inicio de la siguiente.

---

## 🌲 Fork/Join Framework

`ForkJoinPool` está optimizado para trabajo que se puede dividir recursivamente (divide y vencerás). Es la base del `parallelStream()`. Se programa con `RecursiveTask<V>` o `RecursiveAction`.

---

## 🧵 El nuevo Executor de hilos virtuales (Java 21)

`Executors.newVirtualThreadPerTaskExecutor()` devuelve un `ExecutorService` que crea un nuevo hilo virtual por cada tarea. Es una recomendación para la mayoría de las cargas de trabajo de alta concurrencia, ya que combina la facilidad de uso de un Executor con la escalabilidad de los hilos virtuales. 

> [!TIP]
> Internamente, cada tarea obtiene su propio hilo virtual; no hay pool de hilos virtuales (no es necesario).

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000; i++) {
        executor.submit(() -> procesarPeticion());
    }
}
```

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../../README.md)
- [☕ Java 21 Index](../../../index.md)
- [⬅️ Anterior: Hilos de Plataforma](./01-hilos-plataforma.md)
- [➡️ Siguiente: Hilos Virtuales y Concurrencia Estructurada](./03-virtual-threads-structured-concurrency-deep.md)
