
## Archivo: `05-event-loop-profundo.md`


Ya vimos la base del event loop. Ahora exploramos la interacción precisa entre microtareas, macrotareas y el renderizado, y las implicaciones prácticas.
Orden exacto de ejecución

Ciclo típico en el navegador:

    Ejecutar una macrotarea (task): script inicial, evento UI, setTimeout, setInterval, I/O, etc.

    Vaciar completamente la cola de microtareas (promesas, queueMicrotask, MutationObserver). Si durante esto se añaden nuevas microtareas, se ejecutan también en este mismo paso.

    Rendereizar (si es necesario): el navegador puede decidir repintar la UI. No ocurre en cada vuelta, sino cuando el agente de renderizado lo considera (normalmente cada 16ms para 60fps). Se ejecutan callbacks de requestAnimationFrame antes del repintado.

    Repetir: tomar la siguiente macrotarea.

### Macrotareas adicionales

    requestAnimationFrame(rAF): su callback se ejecuta justo antes del renderizado, pero después de las microtareas. Está sincronizado con el refresco de pantalla.

    requestIdleCallback: se ejecuta cuando el hilo principal está ocioso (entre frames). Prioridad baja.

    MessageChannel y setImmediate (solo Node) también son macrotareas.

### Ejemplo con rAF y microtareas
```js
setTimeout(() => console.log('timeout'), 0);
Promise.resolve().then(() => console.log('promise'));
requestAnimationFrame(() => console.log('rAF'));
// Orden típico: promise, rAF, timeout
```

Explicación: microtareas se vacían antes del render. rAF se ejecuta antes del render. Luego viene la macrotarea setTimeout.
¿Por qué setTimeout(fn, 0) no ejecuta inmediatamente?

Porque 0 es el tiempo mínimo, pero la callback se encola como macrotarea. El browser debe terminar la tarea actual, vaciar microtareas y posiblemente renderizar antes de despachar el timeout.
Starvation de macrotareas

Si una microtarea añade continuamente nuevas microtareas (bucle infinito de promesas), las macrotareas (y el renderizado) nunca se ejecutarán, congelando la UI. Evítalo.
Node.js vs Browsers

En Node.js, el event loop tiene varias fases: timers (setTimeout/setInterval), pending callbacks, idle, poll, check (setImmediate), close. Las microtareas se ejecutan entre fases y también después de cada fase. process.nextTick en Node es una microtarea incluso más prioritaria que las promesas.
Implicaciones de rendimiento

    Para tareas intensivas, dividir el trabajo en macrotareas pequeñas (setTimeout) permite que el navegador responda al usuario entre ellas.

    requestAnimationFrame es mejor para animaciones y cambios visuales que deban sincronizarse con el refresco.

    Las microtareas son el lugar ideal para ejecutar lógica que deba completarse antes del próximo renderizado (ej. actualizar el estado).

### Depuración

Entender el orden ayuda a depurar problemas asíncronos, como por qué un setTimeout(fn, 0) se ejecuta después de una promesa.
---
