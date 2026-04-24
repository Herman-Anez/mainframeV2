    
## Archivo: `01-declaracion-vs-expresion.md`


Las funciones en js se pueden definir de dos formas principales: mediante declaración y mediante expresión. Ambas crean objetos de tipo function, pero se comportan de manera diferente en cuanto al hoisting y al momento en que están disponibles.
Declaración de función (Function Declaration)
```js
function saludar(nombre) {
  return `Hola, ${nombre}`;
}

    La declaración completa (nombre y cuerpo) se eleva al inicio del ámbito por el hoisting. Esto significa que se puede llamar a la función antes de la línea donde aparece definida, sin error.

    Debe tener un nombre obligatoriamente (aunque puede ser redefinida en modo no estricto).
```

    Puede ser utilizada en cualquier lugar dentro del ámbito en que se declaró, incluso antes de su definición.

    En bloques if o bucles, su comportamiento puede ser inconsistente en modo no estricto; en modo estricto o con let/const el ámbito de bloque se respeta, pero sigue siendo una declaración.

```js
console.log(suma(3,4)); // 7, funciona por hoisting
function suma(a,b) { return a+b; }
```

### Expresión de función (Function Expression)
```js
const despedir = function(nombre) {
  return `Adiós, ${nombre}`;
};

    Se asigna una función (anónima o con nombre) a una variable o constante. La variable se eleva según su declaración (var, let, const), pero la asignación del valor no ocurre hasta la ejecución de esa línea.

    Por tanto, no se puede invocar antes de la línea de asignación (con let/const se produce ReferenceError por la TDZ; con var la variable existe pero es undefined).

    La función puede ser anónima (sin nombre) o nombrada. Si se le da nombre, este solo es visible dentro del cuerpo de la función, útil para recursión o trazas de pila.
```

js

### console.log(multiplicar); // undefined (si var) o ReferenceError (si let/const)
// multiplicar(5,5); // Error
var multiplicar = function(a,b) { return a*b; };

### Expresión de función nombrada (Named Function Expression)
```js
const factorial = function fact(n) {
  return n <= 1 ? 1 : n * fact(n-1);
};
console.log(fact); // ReferenceError: fact is not defined (fuera de la función)

    El nombre fact solo existe dentro del cuerpo de la función; fuera, la variable factorial es la referencia. Ventaja: mejor depuración (stack trace mostrará fact) y posibilidad de recursión incluso si la variable externa se reasigna.
```

### Comparativa rápida
Característica	Declaración	Expresión
Hoisting	Sí, cuerpo completo	Solo la variable (si var)
Momento de disponibilidad	Antes de su línea	Después de la asignación
Puede ser anónima	No	Sí
Ámbito en bloques	Según contexto (problemático sin strict mode)	Respetado (bloque)
Recomendación

    Usa declaraciones para funciones utilitarias que se usan en cualquier parte del módulo.

    Prefiere expresiones asignadas a const cuando el valor no va a cambiar. Esto evita redeclaraciones accidentales y obliga a definirlas antes de usarlas (código más predecible).

    En general, con módulos ES y buenas prácticas, ambas formas son válidas; la elección depende del estilo.

---
