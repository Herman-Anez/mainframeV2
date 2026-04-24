
## Archivo: `02-currying-y-composicion.md`

Currying

Técnica de transformación de funciones que toman múltiples argumentos en una secuencia de funciones que toman un argumento cada una.
```js
// Sin currying
function suma(a, b, c) { return a + b + c; }

// Con currying manual
function sumaCurried(a) {
  return function(b) {
    return function(c) {
      return a + b + c;
    };
  };
}
sumaCurried(1)(2)(3); // 6
```

Permite crear funciones parcialmente aplicadas: const sumaUno = sumaCurried(1); sumaUno(2)(3).
Currying genérico

Se puede implementar un helper:
```js
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return (...next) => curried(...args, ...next);
  };
}
const curriedSuma = curry(suma);
curriedSuma(1)(2)(3); // 6
curriedSuma(1, 2)(3); // 6
```

### Aplicación práctica

    Crear funciones especializadas reutilizando lógica: const multiplicar = curry((a,b) => a*b); const doble = multiplicar(2);

    Configuración de manejadores de eventos, bibliotecas funcionales (Ramda, lodash/fp).

### Composición de funciones

Consiste en combinar funciones simples para formar funciones más complejas. La salida de una función se convierte en la entrada de la siguiente.
```js
const trim = s => s.trim();
const mayusculas = s => s.toUpperCase();
const exclamar = s => s + '!';

const emocionar = (s) => exclamar(mayusculas(trim(s)));
```

### Función compose y pipe

    compose ejecuta de derecha a izquierda (al estilo matemático).

    pipe ejecuta de izquierda a derecha.

```js
const compose = (...fns) => (x) => fns.reduceRight((acc, fn) => fn(acc), x);
const pipe = (...fns) => (x) => fns.reduce((acc, fn) => fn(acc), x);

const emocionar = compose(exclamar, mayusculas, trim);
emocionar('  hola  '); // 'HOLA!'
```

### Beneficios en programación funcional

    Mejora la legibilidad y la reutilización.

    Facilita el testing (cada función pequeña es pura y aislada).

    Promueve código declarativo.

### Punto libre (point-free style)

Al componer funciones, se omiten los argumentos intermedios. Ejemplo: const procesar = pipe(trim, mayusculas); en lugar de (s) => mayusculas(trim(s)).
Limitaciones

    Depuración más difícil (se pierde claridad en el stack trace).

    En js, la falta de tipos puede provocar errores silenciosos.

---
