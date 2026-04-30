01-fundamentos
---

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

## Archivo: `02-tipos-de-datos.md`

Tipos primitivos (7)

Los tipos primitivos son inmutables (no se pueden modificar sus valores, toda operación devuelve un nuevo valor) y se comparan por valor.

    string: Cadenas de texto. Se pueden usar comillas simples, dobles o backticks (template literals).

    number: Números en coma flotante de 64 bits (IEEE 754). Valor especial NaN, Infinity, -Infinity. No hay distinción entero/decimal.

        NaN es el único valor que no es igual a sí mismo (NaN !== NaN). Se comprueba con Number.isNaN().

    bigint: Enteros de precisión arbitraria. Se crean añadiendo n al final del literal (123n) o con BigInt().

        No se pueden mezclar directamente con number en operaciones aritméticas.

    boolean: true o false.

    undefined: Valor que tiene una variable no inicializada o un parámetro no pasado. Debería ser el propio lenguaje quien lo asigna, no forzarlo manualmente.

    null: Representa la ausencia intencionada de valor. Se asigna explícitamente. typeof null devuelve por error histórico "object".

    symbol: Valor único e inmutable, usado como identificador de propiedades de objeto. Creado con Symbol('descripcion'). No se convierten automáticamente a string.

### typeof y sus trampas

    typeof null → "object" (bug histórico).

    typeof NaN → "number".

    typeof function(){} → "function" (aunque las funciones son objetos).

    typeof array → "object" (para detectar array usar Array.isArray()).

### Tipos de referencia (objetos)

Los objetos son colecciones de propiedades y se comparan por referencia (dos objetos distintos con el mismo contenido no son iguales). Mutables por defecto.

    Object: literal {}, new Object().

    Array: [], new Array().

    Function: cualquier función.

    Date, RegExp, Map, Set, etc.

La asignación de objetos copia la referencia, no el valor. Para copiar superficialmente se usa spread (...) o Object.assign. Para copia profunda, structuredClone() (moderno) o JSON.parse(JSON.stringify(...)) (con limitaciones).
Wrappers primitivos

Al acceder a una propiedad de un primitivo como "hola".length, js crea temporalmente un objeto String, ejecuta la operación y lo descarta. Por eso no se pueden añadir propiedades a primitivos.
Coerción implícita de tipos (vista rápida)

Los operadores y las comparaciones pueden disparar conversiones automáticas. Se detallará en el siguiente punto.
---

## Archivo: `03-operadores-y-coercion.md`

Operadores más importantes
Categoría	Operadores
Aritméticos	+, -, *, /, %, ** (exponenciación)
Asignación	=, +=, -=, etc.
Comparación	==, !=, ===, !==, >, <, >=, <=
Lógicos	&&, ||, ?? (nullish coalescing)
Ternario	condición ? valorVerdadero : valorFalso
Unarios	!, ++, --, typeof, void
Relacionales	in, instanceof
Coerción de tipos

La coerción es la conversión automática o manual de un tipo a otro.
Coerción explícita (recomendada)

### String(valor)

### Number(valor), parseInt(), parseFloat()

### Boolean(valor)

### BigInt(valor)

### Symbol(valor)

### Coerción implícita

Muchos operadores fuerzan la conversión. Reglas básicas:

    Suma +:

        Si algún operando es string, el otro se convierte a string y se concatenan.

        En otro caso, ambos se convierten a number (si es posible) y se suman.

        null se convierte a 0, undefined a NaN en contexto numérico.

    Resta -, multiplicación *, división /, etc.: Ambos operandos se convierten a número.

    Comparación débil ==:

        Compara sin verificar tipo. Aplica un algoritmo complejo de coerción.

        Si los tipos son distintos, se fuerza la conversión de uno o ambos lados a número, string o booleano.

        Evitarla siempre que sea posible; usar === (igualdad estricta).

    Booleanos en contexto lógico: Todos los valores tienen un valor verdadero/falso asociado. Valores falsy: false, 0, "", null, undefined, NaN. Todo lo demás es truthy (incluyendo [], {}, "false").

    Operador lógico && y ||: No necesariamente devuelven booleanos; devuelven uno de los operandos.

        a || b: si a es truthy, devuelve a; si no, devuelve b.

        a && b: si a es falsy, devuelve a; si no, devuelve b.

    Operador de fusión nula ??: Devuelve el operando derecho solo si el izquierdo es null o undefined (no por falsy general). Ideal para valores por defecto.
```js
    const valor = 0 ?? 'default'; // 0 (porque 0 no es null/undefined)
    const valor2 = 0 || 'default'; // 'default' (porque 0 es falsy)
```

### Ejemplo de trampas con coerción
```js
[] + []        // ""  (ambos se convierten a string vacío)
[] + {}        // "[object Object]"
{} + []        // 0 (si se interpreta como bloque + [])
true + true    // 2
'5' - 3        // 2
'5' + 3        // "53"
```

### Recomendaciones

    Usar siempre === y !==.

    Convertir explícitamente antes de operar si hay incertidumbre.

    Preferir ?? para valores por defecto cuando 0 o "" son válidos.

---

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

---
[back](../index)
