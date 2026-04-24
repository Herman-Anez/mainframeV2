
## Archivo: `04-strict-mode.md`

¿Qué es?

El modo estricto ("use strict") es una forma de ejecutar js bajo un conjunto de restricciones que corrigen malas prácticas y convierten algunos errores silenciosos en excepciones.
Activación

    A nivel de script: añadir "use strict"; al principio del archivo (antes de cualquier otra sentencia).

    A nivel de función: dentro de una función, al inicio del cuerpo.

    Los módulos ES6 y las clases automáticamente corren en modo estricto; no hace falta declararlo.

### Cambios principales que introduce

    Prohíbe variables implícitas globales. Asignar a una variable no declarada lanza ReferenceError.
```js
    "use strict";
    x = 5; // ReferenceError: x is not defined
```

    Elimina la coerción de this a objeto global. En una función normal, this es undefined en lugar de window/global.
```js
    function normal() { return this; }
    normal(); // undefined
```

    Prohíbe parámetros duplicados en funciones.
```js
    function sum(a, a) { "use strict"; } // SyntaxError

    Bloquea la eliminación de variables, funciones o argumentos con delete (antes fallaba silenciosamente).
    js

    var x = 1;
    delete x; // SyntaxError

    Prohíbe los octales literales, como var num = 010;. Se debe usar 0o10.
```

    Impide que eval y arguments se usen como nombres de variable o parámetro y limita su manipulación.

    eval y arguments no introducen variables en el ámbito circundante.

    Lanza error al escribir propiedades de solo lectura o sobre objetos no extensibles.

### Consecuencias prácticas

    Obliga a declarar variables correctamente.

    Previene fugas accidentales al objeto global.

    Hace que el código sea más seguro y predecible.

    Herramientas modernas (ESLint, TypeScript) ya incorporan estas reglas, pero "use strict" da garantía en tiempo de ejecución.

¿Cuándo usarlo?

Siempre. En proyectos modernos con módulos ES no es necesario explícitamente, pero en scripts clásicos es obligatorio colocarlo al inicio.