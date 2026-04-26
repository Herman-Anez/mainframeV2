
## Archivo: `06-event-loop.md`


El Event Loop es el mecanismo que permite a js ejecutar código asíncrono de manera no bloqueante a pesar de tener un solo hilo de ejecución principal.
Componentes

    Call Stack (Pila de ejecución): donde se apilan las funciones llamadas síncronamente. Cada función se retira al finalizar.

    Web APIs / Background Tasks: en el navegador, funciones como setTimeout, fetch, eventos del DOM son manejadas por el entorno fuera del motor JS. Cuando terminan, insertan callbacks en las colas.

    Colas de tareas (Task Queues):

        Macrotareas (Task Queue): setTimeout, setInterval, eventos de UI, I/O, setImmediate (Node). Solo se procesa una macrotarea a la vez por ciclo del event loop.

        Microtareas (Microtask Queue): promesas (.then, .catch, .finally), queueMicrotask, MutationObserver. Se procesan por completo al final de cada macrotarea y antes de la siguiente.

    Event Loop: ciclo continuo que verifica la pila. Si está vacía, toma tareas de las colas:

        Primero vacía completamente la cola de microtareas (incluso las que se generen durante ese procesamiento).

        Luego toma la siguiente macrotarea (una sola) y la ejecuta.

        Repite.

### Orden de ejecución típico
```js
console.log('1');
setTimeout(() => console.log('2'), 0);
Promise.resolve().then(() => console.log('3'));
console.log('4');
// Resultado: 1, 4, 3, 2
```

Explicación:

    '1' y '4' son código síncrono, van directo a consola.

    setTimeout encola una macrotarea (futura).

    Promise.then encola una microtarea.

    Al terminar lo síncrono, la pila queda vacía. Se procesan microtareas: '3'.

    Luego se toma la macrotarea: '2'.

### Renderizado

En navegadores, el renderizado de la página suele ocurrir entre macrotareas, después de procesar las microtareas pendientes. Por eso cambios en microtareas pueden afectar el renderizado antes de que el usuario vea algo inconsistente.
Consecuencias prácticas

    Las microtareas pueden ejecutarse infinitamente si dentro de una microtarea se añade otra microtarea (bloqueo de la UI).

    setTimeout(fn, 0) no ejecuta inmediatamente, cede el control al event loop; se usa para posponer al final de la pila actual.

    async/await convierten el código que sigue al await en una microtarea.

    Para tareas intensivas, dividir el trabajo y ceder el control con setTimeout para mantener la UI responsiva.

### Node.js vs Navegadores

El concepto es similar, pero Node tiene más tipos de colas (timer, poll, check, close) y setImmediate que se comporta distinto de setTimeout(fn,0) según el momento.
Visualización gráfica

Se puede imaginar:
```text
Call Stack -> (vacía) -> Event Loop:
  - Vaciar Microtask Queue
  - Tomar 1 Macrotask
  - Renderizar (si es necesario)
  - Repetir
```

Comprender el event loop es crucial para depurar problemas de orden de ejecución y rendimiento en aplicaciones asíncronas.


---
[back](../index)
