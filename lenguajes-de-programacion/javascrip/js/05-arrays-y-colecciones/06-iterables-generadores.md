
## Archivo: `06-iterables-generadores.md`

Protocolo iterable

Un objeto es iterable si implementa el método [Symbol.iterator], que devuelve un objeto iterador. Un iterador debe tener un método next() que retorna { value, done }.

Los bucles for...of, el spread (...), Array.from y otros consumen iterables.

Ejemplo manual:
```js
const iterable = {
  [Symbol.iterator]() {
    let i = 0;
    return {
      next() {
        i++;
        return { value: i, done: i > 3 };
      }
    };
  }
};
for (const v of iterable) { console.log(v); } // 1,2,3
```

### Iterables incorporados

    Arrays, Strings, Map, Set, NodeList, arguments (array-like pero iterable), TypedArrays.

    Object no es iterable, pero con Object.keys/values/entries podemos iterar.

### Consumo de iterables

### for...of

### [...iterable]

### Array.from(iterable)

    new Map(), new Set() reciben iterables.

    Promise.all, Promise.race, Promise.any, Promise.allSettled también aceptan iterables de promesas.

### Generadores (function*)

Son funciones especiales que permiten pausar y reanudar su ejecución, produciendo una secuencia de valores bajo demanda. Llamar a un generador no ejecuta su cuerpo, sino que devuelve un objeto iterador (que también es iterable).
```js
function* contador(max) {
  let i = 0;
  while (i < max) {
    yield i++;
  }
  return 'fin'; // value final que puede capturarse como último value con done:true
}
```
const gen = contador(3);
console.log(gen.next()); // { value: 0, done: false }
console.log(gen.next()); // { value: 1, done: false }
console.log(gen.next()); // { value: 2, done: false }
console.log(gen.next()); // { value: 'fin', done: true }

    yield pausa la ejecución y devuelve un valor al llamador.

    Dentro del generador se puede usar yield* otroIterable para delegar a otro iterable/generador.

    Se pueden pasar valores al generador con next(valor), que es recibido como resultado de la expresión yield.

```js
function* pregunta() {
  const nombre = yield '¿Cómo te llamas?';
  yield `Hola ${nombre}`;
}
const it = pregunta();
console.log(it.next().value); // ¿Cómo te llamas?
console.log(it.next('Juan').value); // Hola Juan
```

### Generadores asíncronos (async function*)

Combinan generadores con async/await. El objeto devuelto implementa el protocolo async iterable, usando for await...of.
```js
async function* fetchPages(urls) {
  for (const url of urls) {
    const res = await fetch(url);
    yield await res.json();
  }
}
for await (const data of fetchPages([...])) {
  console.log(data);
}
```

Producen { value, done } donde value es una promesa resuelta con el valor yieldado.
Aplicaciones

    Iteración de secuencias infinitas o perezosas (números fib, lecturas de archivos).

    Simplificar lógica asíncrona secuencial.

    Implementar comportamientos personalizados de for...of.

### 06-asincronia
---
