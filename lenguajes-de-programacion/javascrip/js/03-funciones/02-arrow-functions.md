## Archivo: `02-arrow-functions.md`


Las arrow functions (funciones flecha) introducidas en ES6 ofrecen una sintaxis más corta y un comportamiento especial en relación al this.
Sintaxis
```js
// Sin parámetros: paréntesis vacío obligatorio
const uno = () => 1;
// Un parámetro: paréntesis opcionales
const doble = x => x * 2;
// Múltiples parámetros o sin parámetros: paréntesis obligatorios
const suma = (a, b) => a + b;
// Cuerpo de bloque: return explícito necesario
const saludar = (nombre) => {
  const mensaje = `Hola ${nombre}`;
  return mensaje;
};
// Devolver un objeto literal: envolver entre paréntesis para evitar confusión con bloque
const crearUsuario = (nombre) => ({ nombre, id: Date.now() });
```

### Características clave

    No tienen su propio this: heredan el this del ámbito léxico en el que están definidas. Esto elimina la necesidad de const self = this o .bind(this) en callbacks.

    No se pueden usar como constructoras: lanzan error si se usan con new.

    No tienen arguments: dentro de una arrow function, arguments hace referencia al objeto de la función externa no flecha (o no existe en ámbito global). Para capturar argumentos se usa el parámetro rest (...args).

    No tienen propiedad prototype.

    No pueden ser usadas como generadores (no admiten yield dentro de ellas).

    Se pueden omitir las llaves y el return si el cuerpo es una única expresión (return implícito).

### this léxico
```js
const obj = {
  nombre: 'Ana',
  saludarNormal: function() {
    setTimeout(function() {
      console.log(this.nombre); // undefined (this es window/global)
    }, 100);
  },
  saludarArrow: function() {
    setTimeout(() => {
      console.log(this.nombre); // 'Ana' (this heredado del contexto de saludarArrow)
    }, 100);
  }
};
```

En el método saludarNormal, la función pasada a setTimeout es una función normal, por lo que su this es el objeto global (o undefined en strict mode). En saludarArrow, la arrow captura el this de saludarArrow (que es obj), por lo que funciona correctamente.
Cuándo no usar arrow functions

    Como métodos de un objeto si se espera que this haga referencia al objeto (porque usaría el this del ámbito superior, no el objeto).

    En funciones constructoras o definición de prototipos.

    Cuando se necesita el objeto arguments.

### Resumen

Las arrow functions simplifican callbacks y código funcional, y resuelven el eterno problema del this en contextos asíncronos. Son ideales para funciones cortas y puras.