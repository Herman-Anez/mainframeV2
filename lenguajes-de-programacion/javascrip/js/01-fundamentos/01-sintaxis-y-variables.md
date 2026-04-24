## Archivo: `01-sintaxis-y-variables.md`

Declaración de variables: var, let, const

js ofrece tres formas de declarar variables. Cada una tiene reglas de ámbito, hoisting y reasignación distintas.
Palabra clave	Ámbito	Hoisting	Reasignable	Redeclarable en el mismo ámbito
var	Función	Sí (inicializa como undefined)	Sí	Sí
let	Bloque {}	Sí (pero no se inicializa, TDZ)	Sí	No
const	Bloque {}	Sí (TDZ)	No (debe inicializarse al declarar)	No
var

    Si se declara fuera de una función, es global y se convierte en propiedad del objeto window (en navegador).

    Las redeclaraciones son ignoradas (no lanzan error, simplemente se sobrescribe el valor).

    Su hoisting eleva la declaración y la inicializa automáticamente a undefined. Esto hace que se pueda acceder a la variable antes de su línea, pero con valor undefined.

```js
console.log(a); // undefined
var a = 5;
```

### let y const

    Tienen ámbito de bloque: existen solo dentro del {} más cercano (if, for, while, bloque independiente...).

    Están sujetos a la Zona Muerta Temporal (TDZ): desde el inicio del bloque hasta que se ejecuta la línea de declaración, cualquier acceso lanza ReferenceError.

    const exige inicialización en la misma sentencia. La variable no puede ser reasignada, pero si el valor es un objeto o array, sus propiedades/elementos sí pueden modificarse (la referencia es inmutable, no el contenido).

    En bucles, let crea un nuevo enlace para cada iteración, lo que evita problemas clásicos con closures dentro de for. Con var se comparte el mismo enlace en todo el ámbito.

### Ámbito léxico y scope chain

Cada función crea un nuevo ámbito; los bloques (con let/const) crean ámbitos anidados. La resolución de variables va del ámbito más interno al externo.
```js
const exterior = 'fuera';
function ejemplo() {
  const interior = 'dentro';
  if (true) {
    const bloque = 'bloque';
    console.log(bloque);   // 'bloque'
    console.log(interior); // 'dentro' — ámbito superior
    console.log(exterior); // 'fuera'  — ámbito global
  }
  console.log(bloque); // ReferenceError
}
```

### Buenas prácticas

    No usar var en código moderno; preferir const por defecto, y let solo si la variable va a ser reasignada.

    Minimizar el número de variables globales.

    Declarar las variables lo más cerca posible de su primer uso.

---
