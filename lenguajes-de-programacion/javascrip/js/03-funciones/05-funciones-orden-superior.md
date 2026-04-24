## Archivo: `05-funciones-orden-superior.md`


Una función de orden superior (higher-order function) es aquella que cumple al menos una de estas condiciones:

    Recibe una función como argumento.

    Retorna una función como resultado.

Este concepto es central en la programación funcional y está muy presente en js.
Funciones que reciben callbacks

Los callbacks son funciones pasadas como argumentos para ser ejecutadas más tarde. Ejemplos: Array.prototype.map, filter, reduce, forEach, setTimeout, manejadores de eventos.
```js
const numeros = [1,2,3];
const dobles = numeros.map(n => n * 2); // map recibe una función
```

### Funciones que retornan funciones

Permiten crear configuraciones personalizadas y reutilizar lógica.
```js
function multiplicarPor(factor) {
  return function(numero) {
    return numero * factor;
  };
}
const duplicar = multiplicarPor(2);
duplicar(5); // 10
```

### Composición de funciones

Se pueden combinar funciones de orden superior para crear pipelines de procesamiento. Por ejemplo:
```js
const compose = (f, g) => x => f(g(x));
const añadirExclamación = s => s + '!';
const gritar = s => s.toUpperCase();
const emocionar = compose(añadirExclamación, gritar);
emocionar('hola'); // 'HOLA!'
```

### Métodos funcionales de Array como funciones de orden superior

    map(fn): transforma cada elemento.

    filter(fn): selecciona elementos según predicado.

    reduce(fn, initial): acumula valor.

    forEach(fn): ejecuta efecto secundario.

    some(fn), every(fn): pruebas booleanas.

    find(fn): primer elemento que cumple condición.

Todos ellos reciben una función con una firma típica (elemento, índice?, array?).
Beneficios

    Separación de responsabilidades (la lógica de iteración se abstrae).

    Código más declarativo y legible.

    Reutilización de callbacks.

### Ejemplo práctico: encadenamiento
```js
const usuarios = [
  { nombre: 'Ana', edad: 25 },
  { nombre: 'Luis', edad: 17 },
  { nombre: 'Marta', edad: 30 }
];
const nombresAdultos = usuarios
  .filter(u => u.edad >= 18)
  .map(u => u.nombre);
// ['Ana', 'Marta']
```

### Funciones puras e impuras

En este contexto conviene recordar que las funciones que no modifican estado externo y siempre devuelven lo mismo para los mismos argumentos se llaman puras. Son ideales como callbacks porque son predecibles y facilitan la composición.