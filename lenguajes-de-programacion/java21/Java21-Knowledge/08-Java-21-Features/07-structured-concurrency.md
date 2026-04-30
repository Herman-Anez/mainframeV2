# 🏗️ Structured Concurrency (Preview)

La **Concurrencia Estructurada** busca tratar varias tareas concurrentes como una unidad de trabajo, confinando su ciclo de vida a un bloque sintáctico. Esto facilita la cancelación, el manejo de errores y la observabilidad.

---

## 💡 Idea central

En lugar de lanzar hilos y unirlos manualmente, se usa un `StructuredTaskScope` que controla las subtareas. Cuando el bloque termina, el *scope* espera a que todas las tareas finalicen (o las cancela si falla alguna) antes de continuar. Se asemeja a un `try-with-resources`.

---

## 💻 Ejemplo con `ShutdownOnFailure`

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> tarea1 = scope.fork(() -> leerBaseDatos());
    Future<Integer> tarea2 = scope.fork(() -> calcularEstadisticas());

    scope.join();            // Espera a que todas las subtareas terminen o fallen
    scope.throwIfFailed();   // Si alguna falló, lanza la excepción

    String resultado1 = tarea1.resultNow();
    int resultado2 = tarea2.resultNow();
    return combinar(resultado1, resultado2);
}
```

### Métodos clave:
*   **`fork()`**: Lanza la tarea y devuelve un `Future`.
*   **`join()`**: Bloquea hasta que todas las tareas finalicen o alguna falle (según la política elegida).
*   **`throwIfFailed()`**: Propaga cualquier excepción ocurrida en las subtareas de forma automática.

---

## 🛠️ Políticas de manejo de errores

*   **`ShutdownOnFailure`**: Si cualquier subtarea falla, se cancelan las demás y la excepción se lanza en `throwIfFailed`.
*   **`ShutdownOnSuccess`**: Obtiene el primer resultado exitoso y cancela las otras (ideal para consultas redundantes o "racing").
*   **Personalización**: Se pueden crear políticas propias extendiendo `StructuredTaskScope`.

---

## 🌟 Ventajas

> [!TIP]
> *   **Árbol de tareas observable:** La relación padre‑hijo queda reflejada en los volcados de hilos (`thread dumps`) y herramientas de monitoreo.
> *   **Cancelación automática:** Al cerrar el *scope*, se cancelan automáticamente las subtareas aún en ejecución.
> *   **Simplicidad:** Código más limpio, sin necesidad de `CountDownLatch`, `ExecutorService` manual ni colecciones externas.
> *   **Escalabilidad:** Integración nativa con **hilos virtuales**.

---

## ⚠️ Consideraciones

> [!IMPORTANT]
> *   Al ser una característica en **preview**, puede haber cambios en la API final.
> *   Requiere habilitar `--enable-preview` tanto en compilación como en ejecución.
> *   Los `Future` devueltos por `fork` son específicos del *scope* y **no se deben pasar fuera** del bloque `try`.

> [!NOTE]
> **Estado:** Preview en Java 21.

---

## 🔗 Recursos y Enlaces

- [🏠 Inicio](../../../../../README.md)
- [☕ Java 21 Index](../../../index.md)

