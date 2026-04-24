## Archivo: `05-temporizadores.md`


js provee funciones para ejecutar código después de un retraso o periódicamente. No son parte de ECMAScript, sino APIs del entorno (navegador y Node.js), pero son universales.
setTimeout(fn, delay, ...args)

Programa la ejecución única de fn después de delay milisegundos. Retorna un identificador numérico.
```js
const id = setTimeout(() => {
  console.log('Pasaron 2 segundos');
}, 2000);
```

    El tiempo no es garantizado: es el mínimo, pero la tarea se encolará y esperará su turno en el event loop.

    Si delay es 0, se ejecuta en la próxima macrotarea (después del código síncrono actual).

### clearTimeout(id)

Cancela un timeout pendiente.
setInterval(fn, delay, ...args)

Ejecuta fn repetidamente cada delay ms. Retorna un ID.
```js
const id = setInterval(() => console.log('tick'), 1000);
```

### clearInterval(id)

Detiene la repetición.
Precauciones con setInterval

    Si la función tarda más que el intervalo, las ejecuciones pueden solaparse o encolarse, lo que no es deseable. Es preferible usar setTimeout recursivo para intervalos seguros:

```js
function tarea() {
  console.log('ejecutar');
  setTimeout(tarea, 1000);
}
setTimeout(tarea, 1000);
```

De esta forma se garantiza un tiempo entre ejecuciones sin solapamiento.
setImmediate (Node.js) y queueMicrotask

No son temporizadores, pero están relacionados. En navegador no existe setImmediate; en su lugar se puede usar setTimeout(fn, 0) con precaución (es una macrotarea). queueMicrotask encola una microtarea, que se ejecuta antes de las macrotareas.
Uso con this

Si se pasa un método de objeto como callback, se pierde el contexto. Usar arrow function o bind.
Aplicaciones

    Debounce y throttle para eventos frecuentes (scroll, resize).

    Animaciones y retrasos.

    Timeout en peticiones (AbortController es preferible a veces).

---
