# Temporizadores en JavaScript

JavaScript proporciona funciones para ejecutar código después de un retraso específico o de forma periódica. Aunque no son parte del estándar oficial de ECMAScript, son APIs universales disponibles en prácticamente todos los entornos (Navegadores y Node.js).

---

## `setTimeout()`

Programa la ejecución única de una función después de que transcurra un tiempo determinado en milisegundos.

```javascript
const timerId = setTimeout((nombre) => {
  console.log(`Hola, ${nombre}`);
}, 2000, 'Usuario');
```

> [!IMPORTANT]
> El tiempo especificado es el **mínimo garantizado**, no el exacto. La ejecución real dependerá de la carga de trabajo en el **Event Loop**. Un `setTimeout` con retraso `0` se ejecutará en la siguiente macrotarea, justo después de que termine el código síncrono actual.

---

## `setInterval()`

Ejecuta una función de forma repetida, esperando un intervalo de tiempo específico entre cada inicio de ejecución.

```javascript
let contador = 0;
const intervalId = setInterval(() => {
  contador++;
  console.log(`Tick ${contador}`);
  if (contador === 5) clearInterval(intervalId);
}, 1000);
```

---

## Cancelación de Temporizadores

Ambas funciones devuelven un identificador numérico (ID) que permite cancelar la ejecución antes de que ocurra o se repita.

*   **`clearTimeout(id)`**: Cancela un `setTimeout`.
*   **`clearInterval(id)`**: Detiene un `setInterval`.

---

## Buenas Prácticas y Precauciones

### `setInterval` vs `setTimeout` Recursivo
Si la tarea dentro de un `setInterval` tarda más que el propio intervalo, las ejecuciones pueden solaparse o acumularse, provocando problemas de rendimiento.

> [!TIP]
> Para garantizar un tiempo de espera constante **entre el fin de una tarea y el inicio de la siguiente**, es preferible usar un `setTimeout` recursivo:
> ```javascript
> function realizarTarea() {
>   // ... lógica de la tarea ...
>   setTimeout(realizarTarea, 1000); // Se programa la siguiente tras terminar la actual
> }
> setTimeout(realizarTarea, 1000);
> ```

---

## Alternativas y Microtareas

Existen otras formas de programar tareas con diferentes prioridades:

1.  **`setImmediate(fn)`**: (Solo Node.js) Ejecuta la función inmediatamente después de que termine el ciclo actual de eventos.
2.  **`queueMicrotask(fn)`**: Encola una **microtarea**. Estas se ejecutan con mayor prioridad que los temporizadores, justo después del código síncrono y antes de que el navegador vuelva a renderizar.

---

## Manejo del Contexto (`this`)

Al pasar un método de un objeto como callback a un temporizador, se pierde el contexto original de `this` (apuntará al objeto global o será `undefined` en modo estricto).

```javascript
const usuario = {
  nombre: 'Ana',
  saludar() {
    console.log(`Hola, soy ${this.nombre}`);
  }
};

// INCORRECTO: Perderá el contexto
setTimeout(usuario.saludar, 1000); 

// CORRECTO: Usando arrow function o bind
setTimeout(() => usuario.saludar(), 1000);
setTimeout(usuario.saludar.bind(usuario), 1000);
```

---
[Volver al Índice](../js-index.md)
