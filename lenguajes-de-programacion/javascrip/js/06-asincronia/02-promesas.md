
## Archivo: `02-promesas.md`


Una Promise (promesa) es un objeto que representa la eventual finalización (o falla) de una operación asíncrona y su valor resultante.
Estados

    pending: estado inicial, ni cumplida ni rechazada.

    fulfilled: la operación se completó con éxito, tiene un valor.

    rejected: la operación falló, tiene un motivo (error).

Una vez que está en fulfilled o rejected, no puede cambiar de estado (se dice que está settled).
Creación
```js
const promesa = new Promise((resolve, reject) => {
  // operación asíncrona
  const exito = true;
  if (exito) resolve('datos obtenidos');
  else reject(new Error('falló'));
});

    resolve(valor) devuelve un valor (que puede ser otra promesa, se asimila automáticamente).

    reject(razon) suele ser un error.
```

### Consumo

    .then(onFulfilled, onRejected): programa callbacks para cuando la promesa se resuelva o rechace. Retorna una nueva promesa, permitiendo encadenamiento.

    .catch(onRejected): equivalente a .then(null, onRejected), para manejo de errores.

    .finally(onFinally): se ejecuta independientemente del resultado, sin modificar el valor/rechazo.

```js
fetch('/api/data')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error))
  .finally(() => console.log('Petición terminada'));
```

### Encadenamiento

Cada .then retorna una nueva promesa cuyo valor será el retorno del callback. Si el callback devuelve un valor, la promesa se resuelve con ese valor; si devuelve una promesa, la promesa externa espera a que se resuelva (flattening).
Promesificación y utilidades

    Promise.resolve(valor): devuelve una promesa resuelta con valor. Si valor es una promesa, la devuelve tal cual. Útil para empezar una cadena.

    Promise.reject(razon): promesa rechazada.

    Promise.all(iterable): espera a que todas las promesas se resuelvan y devuelve array de resultados. Si alguna falla, rechaza inmediatamente con ese error.

    Promise.allSettled(iterable): espera a que todas terminen (cumplan o rechacen) y devuelve array de objetos {status, value/reason}.

    Promise.race(iterable): se resuelve/rechaza con la primera promesa que se establezca.

    Promise.any(iterable): se resuelve con la primera que se cumpla; si todas fallan, rechaza con un AggregateError.

### Manejo de errores

Los errores lanzados dentro de callbacks se convierten automáticamente en rechazos. Siempre es necesario propagar el manejo con un .catch al final de la cadena para no tener promesas rechazadas no manejadas.
Microtareas

Los callbacks de .then/.catch/.finally se ejecutan como microtareas (prioritarias) después de que el código síncrono termine pero antes de macrotareas (setTimeout, eventos). Esto es relevante para el event loop.
---
