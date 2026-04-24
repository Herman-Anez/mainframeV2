
## Archivo: `03-parametros-y-spread.md`

Parámetros por defecto

Se puede asignar un valor por defecto a un parámetro que será usado si el argumento es undefined (no se aplica para null u otros valores falsy).
```js
function saludar(nombre = 'invitado') {
  return `Hola, ${nombre}`;
}
saludar();       // Hola, invitado
saludar(undefined); // Hola, invitado
saludar(null);   // Hola, null (no se reemplaza)

    Las expresiones de los valores por defecto se evalúan en cada llamada (no en la definición), y pueden referenciar parámetros anteriores.
```

js

### function suma(a, b = a * 2) {
  return a + b;
}
suma(3); // 9 (b = 3*2)

### Parámetros rest (...)

Permite representar un número indefinido de argumentos como un array.
```js
function concatenar(separador, ...palabras) {
  return palabras.join(separador);
}
concatenar('-', 'a', 'b', 'c'); // 'a-b-c'
```

    Solo puede haber un parámetro rest y debe ser el último.

    Sustituye al objeto arguments (que no es un array real) de manera más clara.

    En arrow functions es la única forma de capturar todos los argumentos.

### Operador spread en funciones (invocación)

El mismo operador ... permite expandir un array (o cualquier iterable) en argumentos individuales en una llamada.
```js
const numeros = [5, 10, 15];
console.log(Math.max(...numeros)); // 15

const fecha = [2025, 4, 12];
new Date(...fecha); // similar a new Date(2025, 4, 12)
```

Se puede combinar con argumentos normales.
El objeto arguments (solo funciones no flecha)

Es un objeto similar a un array (no tiene métodos como forEach) que contiene todos los argumentos pasados a la función. Está disponible en funciones clásicas, pero no en arrow functions.
```js
function test() {
  console.log(arguments[0]); // primer argumento
  console.log(arguments.length);
}
test(1,2,3); // 1 y 3

    Convertir a array: Array.from(arguments) o [...arguments].
```

### Buenas prácticas

    Prefiere parámetros rest sobre arguments (más legible y seguro).

    Usa valores por defecto para evitar comprobaciones manuales de undefined.

    El spread simplifica mucho la invocación de funciones variádicas.

---
