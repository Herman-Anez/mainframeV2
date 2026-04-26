# Event Loop (Profundo)

Comprender el funcionamiento interno del **Event Loop** es crucial para escribir aplicaciones JavaScript de alto rendimiento y evitar bloqueos en la interfaz de usuario.

---

## Orden de Ejecución Exacto

El ciclo de vida de un "tick" en el navegador sigue un orden estrictamente definido:

1. **Macrotarea (Task):** Se ejecuta una sola macrotarea de la cola (ej: script inicial, eventos de usuario, `setTimeout`, `setInterval`, I/O).
2. **Microtareas (Microtasks):** Se vacía **completamente** la cola de microtareas (Promesas, `queueMicrotask`, `MutationObserver`). Si una microtarea genera nuevas microtareas, estas se ejecutan en este mismo paso.
3. **Renderizado:** El navegador decide si es necesario repintar la UI (típicamente cada 16.6ms para mantener 60fps).
   - Se ejecutan los callbacks de `requestAnimationFrame` (rAF) justo antes del repintado.
4. **Repetición:** El ciclo vuelve al punto 1 para tomar la siguiente macrotarea.

---

## Categorización de Tareas

### Macrotareas
- Scripts externos (`<script src="...">`).
- Eventos del DOM (click, scroll, etc.).
- `setTimeout` / `setInterval`.
- `setImmediate` (solo Node.js).
- `MessageChannel`.

### Microtareas
- Promesas (`.then`, `.catch`, `.finally`).
- `queueMicrotask()`.
- `MutationObserver`.
- `process.nextTick` (solo Node.js - es la de mayor prioridad).

---

## Ejemplo Práctico: El orden de consola

```js
console.log('1. Inicio');

setTimeout(() => console.log('2. Timeout'), 0);

Promise.resolve().then(() => console.log('3. Promesa'));

requestAnimationFrame(() => console.log('4. rAF'));

console.log('5. Fin');
```

**Orden de salida típico:**
1. `1. Inicio` (Síncrono)
2. `5. Fin` (Síncrono)
3. `3. Promesa` (Microtarea - se ejecuta antes del siguiente tick)
4. `4. rAF` (Antes del renderizado)
5. `2. Timeout` (Siguiente macrotarea)

---

## Consideraciones de Rendimiento

### El peligro del "Starvation"
> [!CAUTION]
> Si una microtarea añade continuamente nuevas microtareas (por ejemplo, una promesa que se resuelve y encadena otra infinitamente), el Event Loop **nunca** llegará a la fase de renderizado ni a la siguiente macrotarea. Esto congelará la interfaz de usuario por completo.

### Bloqueo del hilo principal
> [!IMPORTANT]
> JavaScript es monohilo. Una macrotarea que tarde demasiado en ejecutarse (ej: un cálculo matemático pesado) retrasará todas las microtareas y el renderizado, provocando una experiencia de usuario deficiente (*jank*).

### Recomendaciones
- **Tareas pesadas:** Divídelas en fragmentos pequeños usando `setTimeout` o delégalas a un **Web Worker**.
- **Animaciones:** Usa siempre `requestAnimationFrame` en lugar de `setTimeout` para asegurar la sincronización con el refresco de pantalla.
- **Lógica de Estado:** Las microtareas son ideales para coordinar cambios de estado que deben ser consistentes antes de que el usuario vea el próximo frame.

---
[back](../index)
