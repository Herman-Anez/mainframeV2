# El Event Loop en JavaScript

El **Event Loop** (Bucle de Eventos) es el mecanismo fundamental que permite a JavaScript realizar operaciones asíncronas de manera no bloqueante, a pesar de ser un lenguaje de un solo hilo (single-threaded).

---

## Componentes del Sistema

Para entender el Event Loop, debemos visualizar cómo interactúa el motor de JavaScript con el entorno (Navegador o Node.js):

1.  **Call Stack (Pila de Ejecución):** Donde se apilan las funciones llamadas de forma síncrona. Sigue el principio LIFO (*Last In, First Out*). Una función se retira de la pila solo cuando termina su ejecución.
2.  **Web APIs / Background Tasks:** Funciones proporcionadas por el entorno (como `setTimeout`, `fetch`, o eventos del DOM) que se ejecutan fuera del motor de JavaScript para no bloquearlo.
3.  **Task Queues (Colas de Tareas):** Donde se guardan los callbacks de las tareas finalizadas esperando ser ejecutados por el motor de JS.

---

## Colas de Tareas: Macro y Micro

Existen dos tipos de colas con distintas prioridades:

### Microtareas (Microtask Queue)
*   **Contenido:** Promesas (`.then`, `.catch`, `.finally`), `queueMicrotask`, y `MutationObserver`.
*   **Prioridad:** Máxima. Se procesan **todas** las microtareas pendientes antes de que el Event Loop pase a la siguiente fase.

### Macrotareas (Task Queue)
*   **Contenido:** `setTimeout`, `setInterval`, eventos de usuario (click, scroll), operaciones de I/O, y `setImmediate` (en Node.js).
*   **Prioridad:** Menor. El Event Loop procesa **solo una** macrotarea por ciclo.

---

## Funcionamiento del Ciclo

El Event Loop sigue un algoritmo constante:

1.  Verifica si la **Call Stack** está vacía.
2.  Si está vacía, procesa **toda la cola de microtareas** hasta que no quede ninguna (incluso las que se añadan durante este proceso).
3.  Si es necesario, el navegador realiza el **renderizado** de la interfaz.
4.  Toma la **primera macrotarea** de la cola y la mueve a la Call Stack para ejecutarla.
5.  Repite el proceso.

---

## Ejemplo de Orden de Ejecución

```javascript
console.log('1: Síncrono');

setTimeout(() => console.log('2: Macrotarea'), 0);

Promise.resolve().then(() => console.log('3: Microtarea'));

console.log('4: Síncrono');

// RESULTADO: 1, 4, 3, 2
```

> [!NOTE]
> **Explicación:** '1' y '4' se ejecutan inmediatamente. Al terminar lo síncrono, la pila está vacía. El motor revisa las microtareas y ejecuta '3' (promesa). Finalmente, toma la macrotarea '2' (timeout).

---

## Consecuencias Prácticas

> [!WARNING]
> **Bloqueo de la UI:** Si creas una cadena infinita de microtareas (por ejemplo, una promesa que se llama a sí misma recursivamente), la cola de microtareas nunca se vaciará y el navegador nunca llegará al paso de renderizado o macrotareas, congelando la aplicación.

### Optimizaciones
*   **`setTimeout(fn, 0)`**: Se utiliza para "posponer" una tarea al final de la cola actual, permitiendo que el navegador respire y procese otros eventos antes de ejecutar la función.
*   **Tareas intensivas:** Para cálculos pesados, es recomendable dividirlos en trozos pequeños y usar `setTimeout` para ceder el control al Event Loop entre fragmentos, manteniendo la interfaz responsiva.

---

## Diferencias: Navegador vs Node.js

Aunque el concepto base es el mismo, Node.js utiliza la librería **libuv** y tiene fases más complejas (timers, poll, check, close). Sin embargo, la distinción entre microtareas (como `process.nextTick`) y macrotareas sigue siendo el principio rector para entender el orden de ejecución.

---
[Volver al Índice](../js-index.md)
