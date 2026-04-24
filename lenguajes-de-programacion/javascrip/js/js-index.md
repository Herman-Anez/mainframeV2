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
02-control-de-flujo
---

## Archivo: `01-condicionales.md`

if / else if / else

La estructura básica de toma de decisiones.
```js
if (condición) {
  // bloque si verdadero
} else if (otraCondición) {
  // bloque si la anterior es falsa y esta es verdadera
} else {
  // bloque si todas las anteriores son falsas
}

    La condición se evalúa y se fuerza a booleano (truthy/falsy).
```

    Se pueden anidar sin límite, pero un exceso de else if se puede sustituir por switch o un objeto de mapeo.

### Operador ternario

Forma concisa de devolver un valor u otro según condición.
```js
const access = edad >= 18 ? 'Permitido' : 'Denegado';
```

    Se puede anidar, pero pierde legibilidad rápidamente; mejor evitarlo en casos complejos.

### Switch

Evalúa una expresión y compara su valor con cada caso usando comparación estricta (===).
```js
switch (fruta) {
  case 'manzana':
    precio = 1;
    break;
  case 'pera':
  case 'uva':   // ambos casos comparten el mismo bloque
    precio = 2;
    break;
  default:
    precio = 0;
}

    Fall-through: si no se coloca break, la ejecución continúa con el siguiente caso hasta encontrar un break o el final. A veces se usa a propósito (como en el ejemplo), pero debe documentarse.
```

    El default es opcional; se ejecuta si ningún caso coincide.

    La expresión del switch y los case pueden ser cualquier valor (no solo números o strings).

### Condicionales de cortocircuito

Uso de && y || para ejecutar código condicionalmente.
```js
isLogged && mostrarDashboard();  // equivale a if (isLogged) mostrarDashboard();
config = opciones || {};         // asigna opciones si es truthy, si no, {}
```

### Patrones recomendados

    Preferir if para condiciones binarias simples.

    Usar switch cuando hay múltiples valores discretos a comparar (más legible que muchos else if).

    Evaluar las condiciones de la más específica a la más general, o usar early returns en funciones.

---

## Archivo: `02-bucles.md`

Bucle for clásico
```js
for (inicialización; condición; expresión final) {
  // cuerpo
}

    Se puede omitir cualquiera de las tres partes (por ejemplo, for(;;) es un bucle infinito).

    Todas las variables declaradas con var comparten ámbito; con let se crea un nuevo enlace en cada iteración (muy útil con closures).

while y do...while

    while: evalúa la condición antes de cada iteración. Puede no ejecutarse nunca.

    do...while: ejecuta el cuerpo al menos una vez y luego evalúa la condición.
```

js

### while (hayDatos()) { procesar(); }
do { intentar(); } while (reintentar);

### for...in

Recorre las claves enumerables de un objeto (incluyendo las heredadas a través de la cadena de prototipos).
```js
for (const key in objeto) {
  if (Object.hasOwn(objeto, key)) {
    console.log(key, objeto[key]);
  }
}

    No usar para arrays (recorre índices como strings y puede incluir propiedades añadidas).
```

    El orden no está garantizado para propiedades no numéricas.

    Para evitar propiedades heredadas, filtrar con Object.hasOwn() (o Object.prototype.hasOwnProperty.call()).

### for...of

Introducido en ES6, recorre los valores de un objeto iterable (arrays, strings, mapas, sets, generadores, NodeList, etc.).
```js
for (const valor of iterable) {
  console.log(valor);
}
```

    No funciona sobre objetos planos a menos que implementen Symbol.iterator.

    Sí respeta el orden natural del iterable.

    Muy útil para arrays cuando no se necesita el índice.

    Se puede combinar con entries(): for (const [i, v] of arr.entries()).

### Control de flujo dentro de bucles: break y continue

    break: termina inmediatamente el bucle.

    continue: salta a la siguiente iteración.

    Ambos afectan al bucle más cercano. Se pueden usar etiquetas (label:) para saltar de un bucle anidado exterior.

```js
exterior: for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    if (i === j) continue exterior; // salta a la siguiente iteración de 'i'
    console.log(i, j);
  }
}
```

### Buenas prácticas

    Preferir for...of (o métodos funcionales como .forEach, .map) para arrays sobre el for clásico.

    No usar for...in en arrays; para objetos, considerar Object.keys()/Object.values()/Object.entries() con for...of.

    Cuidado con modificar la longitud de un array mientras se itera con un for clásico.

---

## Archivo: `03-excepciones-trycatch.md`

Estructura básica
```js
try {
  // código que puede lanzar una excepción
} catch (error) {
  // manejo del error
} finally {
  // se ejecuta siempre, haya o no error
}
```

    Si ocurre un error en try, la ejecución salta inmediatamente al bloque catch. Luego, pase lo que pase, se ejecuta finally.

    El objeto error en catch puede ser cualquier cosa lanzada, pero se recomienda que sea una instancia de Error o sus subclases.

    catch puede omitir el paréntesis y la variable si no se necesita la información del error (ES2019+): catch { ... }.

### Lanzar errores: throw
```js
throw new Error('Mensaje descriptivo');
throw new TypeError('valor inválido');
throw 'esto no es buena práctica'; // evítalo
```

El motor crea un objeto Error con información de pila de llamadas (stack trace).
Copy constructor: new Error(message)

    Error, TypeError, RangeError, SyntaxError, ReferenceError, URIError, EvalError.

    Se pueden crear errores personalizados extendiendo Error:

```js
class ValidationError extends Error {
  constructor(message, campo) {
    super(message);
    this.name = 'ValidationError';
    this.field = campo;
  }
}
throw new ValidationError('Campo requerido', 'email');
```

¿Qué sucede si no se captura un error?

El error se propaga hacia arriba en la pila de llamadas. Si llega al ámbito global sin ser capturado, el script se detiene y se muestra en consola (navegador) o se termina el proceso (Node.js, a menos que haya un listener de uncaughtException). Esto provoca una mala experiencia de usuario.
Finally y return

El bloque finally se ejecuta incluso si try o catch tienen una sentencia return. La única forma de evitarlo es un cierre forzado del proceso (ej. process.exit()) o un bucle infinito. Si finally también tiene un return, ese valor sobreescribe cualquier return anterior. Se recomienda que finally no devuelva valores.
Patrones de uso

    Capturar errores en operaciones de entrada/salida (fetch, lectura de archivos) y mostrar mensajes amigables.

    En entornos asíncronos con async/await, usar try/catch alrededor del await.

    En promesas, el equivalente es .catch().

    En frameworks frontend, a menudo se usan barreras globales de error (componentDidCatch en React, o manejadores de ventana).

### Ejemplo robusto
```js
async function getUsers() {
  try {
    const response = await fetch('/api/users');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Fallo al obtener usuarios:', error.message);
    // Opcional: relanzar o devolver valor por defecto
    return [];
  } finally {
    console.log('Petición finalizada');
  }
}
```

### 03-funciones
---

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
---

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

## Archivo: `04-scope-y-closures.md`

Scope (ámbito)

El ámbito determina dónde una variable es accesible. En js, hasta ES6 el ámbito solo era de función y global. Con let y const se añadió el ámbito de bloque.

    Ámbito global: variables declaradas fuera de cualquier función (o con var sin función). Son propiedades del objeto global (ventana en navegador).

    Ámbito de función: cada función crea su propio ámbito, las variables declaradas dentro con var, let o const son locales a esa función.

    Ámbito de bloque: let y const limitan la variable al bloque {} (if, for, while, etc.).

La resolución de nombres sigue la cadena de ámbitos (scope chain): el motor busca la variable en el ámbito actual, si no la encuentra sube al ámbito superior, y así hasta el global. Si no existe, se crea una variable global en modo no estricto (error en estricto).
Closure (clausura)

Un closure se produce cuando una función "recuerda" y puede acceder a variables de su ámbito léxico incluso cuando la función se ejecuta fuera de ese ámbito. En otras palabras, una función interna que referencia variables de una función externa "cierra sobre" esas variables.
```js
function crearContador() {
  let cuenta = 0;
  return function() {
    cuenta++;
    return cuenta;
  };
}
const contador1 = crearContador();
console.log(contador1()); // 1
console.log(contador1()); // 2
```

Aquí la función anónima retornada mantiene viva la variable cuenta (que pertenece al ámbito de crearContador) a través del closure. Cada llamada a crearContador() genera un nuevo ámbito con su propia variable cuenta.
Aplicaciones prácticas de closures

    Encapsulación y datos privados: simular propiedades privadas (antes de los campos #).

    Fábricas de funciones y partial application.

    Manejo de eventos asíncronos que necesitan contexto (similar a cómo las arrow functions capturan this, pero para variables).

    Memoización (cache de resultados).

### Ejemplo con bucles (clásico)
```js
for (var i = 0; i < 3; i++) {
  setTimeout(function() { console.log(i); }, 100);
}
// Imprime 3, 3, 3 (porque i es compartida en el ámbito global/función)
```

Solución con closure (IIFE) o con let:
```js
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // 0,1,2 (cada iteración tiene su propio i)
}
```

### Importante

Los closures no copian los valores en el momento de su creación, capturan la referencia a la variable. Si la variable cambia antes de que la función se ejecute, verá el valor actualizado.
Rendimiento

Los closures mantienen referencias al ámbito exterior, lo que puede impedir que el garbage collector libere memoria si no se usan con cuidado. Sin embargo, son una herramienta fundamental y no deben evitarse por razones prematuras de rendimiento.
---

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
---

## Archivo: `06-iife-y-recursividad.md`

IIFE (Immediately Invoked Function Expression)

Una IIFE es una función que se define y se ejecuta inmediatamente. Sintaxis básica:
```js
(function() {
  // código aislado
})();
```

o
```js
(function() {
  // código aislado
}());
```

    Se usa para crear un ámbito privado y evitar contaminar el ámbito global.

    Muy común antes de la llegada de módulos ES6 para encapsular código.

### Puede tener parámetros: (function(global) { ... }(window));

### Casos de uso

    Módulo revelador (revealing module pattern): retornar un objeto con métodos públicos que acceden a variables privadas del closure.

```js
const modulo = (function() {
  let privada = 0;
  return {
    incrementar() { privada++; },
    valor() { return privada; }
  };
})();
modulo.incrementar();
console.log(modulo.valor()); // 1
console.log(modulo.privada); // undefined

    Bucles y closures (antes de let): capturar valor de iterador.
```

js

### for (var i = 0; i < 3; i++) {
  (function(indice) {
    setTimeout(() => console.log(indice), 100);
  })(i);
}

    Evitar colisiones de nombres en scripts concatenados.

### Recursividad

Una función recursiva es aquella que se llama a sí misma para resolver un problema dividiéndolo en subproblemas más pequeños, hasta llegar a un caso base que detiene la recursión.
```js
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}
```

### Componentes esenciales

    Caso base: condición que termina la recursión (sin ella hay desbordamiento de pila).

    Llamada recursiva: con argumentos que convergen hacia el caso base.

### Recursión de cola (tail recursion)

Si la llamada recursiva es la última operación que realiza la función (está en posición de cola), algunos motores pueden optimizarla para evitar acumulación de stack (TCO, Tail Call Optimization). No todos los entornos lo implementan, pero es buena práctica escribir funciones recursivas de cola cuando sea posible.
```js
function factorial(n, acum = 1) {
  if (n <= 1) return acum;
  return factorial(n - 1, n * acum); // llamada de cola
}
```

### Aplicaciones clásicas

    Recorridos de estructuras de árbol o grafo.

    Algoritmos como ordenamiento (quicksort, mergesort).

    Cálculo de secuencias (Fibonacci).

    Procesamiento de estructuras anidadas (JSON, DOM).

### Precauciones

    Cada llamada recursiva consume memoria en la pila de ejecución; si la profundidad es excesiva, se produce un stack overflow.

    A veces una solución iterativa es más eficiente y clara; pero la recursividad puede ser más natural para problemas auto-similares.

### 04-objetos-y-clases
---

## Archivo: `01-objetos-literales.md`


En js, un objeto es una colección de pares clave-valor. La notación literal es la forma más común de crearlos.
Sintaxis básica
```js
const persona = {
  nombre: 'Carlos',
  edad: 30,
  saludar: function() {
    return `Hola, soy ${this.nombre}`;
  }
};
```

### Nombres de propiedades

    Pueden ser cadenas (con comillas si contienen espacios o caracteres especiales) o identificadores válidos.

    También pueden ser números, que se convierten a cadena automáticamente: { 0: 'valor' } es válido.

    Desde ES6, se pueden definir propiedades computadas con []:

```js
const campo = 'edad';
const obj = { [campo]: 25 };
```

### Métodos abreviados

ES6 permite definir métodos sin la palabra clave function:
```js
const obj = {
  saludar() { console.log('hola'); }
};
```

### Propiedades shorthand

Si el nombre de la variable y la propiedad coinciden, se omite el valor:
```js
const nombre = 'Ana', edad = 28;
const user = { nombre, edad }; // { nombre: 'Ana', edad: 28 }
```

### Prototipo

Todo objeto literal tiene como prototipo Object.prototype, del que hereda métodos como toString(), hasOwnProperty(), etc. Puede ser modificado con Object.create() o Object.setPrototypeOf() (desaconsejado por rendimiento).
Acceso a propiedades

### Notación punto: objeto.propiedad

    Notación corchetes: objeto['propiedad'] – útil cuando el nombre es dinámico o contiene caracteres especiales.

### Comparación

Dos objetos literales distintos siempre son diferentes aunque tengan el mismo contenido, porque se comparan por referencia.
```js
const a = {x:1};
const b = {x:1};
console.log(a === b); // false
```

### Mutabilidad

Los objetos son mutables: se pueden añadir, modificar o eliminar propiedades en cualquier momento.
---

## Archivo: `02-propiedades-y-metodos.md`

Propiedades

Las propiedades de un objeto asocian una clave (nombre) con un valor. Además del valor, cada propiedad tiene atributos (descriptores):

    writable: si el valor puede cambiarse.

    enumerable: si aparece en bucles for...in y Object.keys().

    configurable: si la propiedad puede eliminarse o cambiar sus descriptores.

Por defecto, las propiedades definidas de forma literal son writable, enumerable y configurable.
Definición de propiedades con control preciso

Object.defineProperty(obj, prop, descriptor) permite establecer esos atributos.
```js
const obj = {};
Object.defineProperty(obj, 'id', {
  value: 123,
  writable: false,
  enumerable: true,
  configurable: false
});
obj.id = 456; // no tiene efecto (o lanza error en strict mode)
```

Object.defineProperties para múltiples propiedades.
Métodos

Son funciones almacenadas como propiedades del objeto. Pueden referirse al objeto a través de this. En métodos definidos con sintaxis abreviada, this apunta al objeto sobre el que se invoca el método.
Getters y Setters

Se definen con las palabras clave get y set, permitiendo ejecutar lógica al leer o escribir una propiedad.
```js
const persona = {
  nombre: 'Juan',
  apellido: 'Perez',
  get nombreCompleto() {
    return `${this.nombre} ${this.apellido}`;
  },
  set nombreCompleto(val) {
    const partes = val.split(' ');
    this.nombre = partes[0];
    this.apellido = partes[1];
  }
};
console.log(persona.nombreCompleto); // Juan Perez
persona.nombreCompleto = 'Ana Lopez';
console.log(persona.nombre); // Ana
```

### Método this en métodos

El valor de this depende de cómo se invoca la función:

    Llamada directa como método: obj.metodo() → this es obj.

    Función extraída: const fn = obj.metodo; fn() → this es objeto global (o undefined en estricto).

    Arrow functions: no tienen this propio, heredan el del contexto.

### Borrado de propiedades

El operador delete elimina la propiedad del objeto. Fallará si la propiedad es no configurable.
Verificación de existencia

    prop in obj (verifica cadena de prototipos).

    obj.hasOwnProperty(prop) (solo propiedades propias).

    obj[prop] !== undefined (puede fallar si el valor es undefined).

---

## Archivo: `03-prototipos.md`


js es un lenguaje basado en prototipos. Cada objeto tiene un enlace interno a otro objeto llamado su prototipo, y de él hereda propiedades.
Propiedad __proto__ y Object.getPrototypeOf()

    __proto__ es un accessor heredado de Object.prototype (no recomendado en producción, pero expuesto en la mayoría de navegadores).

    La forma estándar es Object.getPrototypeOf(obj) y Object.setPrototypeOf(obj, proto).

### Cadena de prototipos

Cuando accedemos a una propiedad, el motor la busca primero en el propio objeto. Si no existe, sube al prototipo, y así sucesivamente hasta llegar a Object.prototype (cuyo prototipo es null). Este es el mecanismo de herencia en js.
```js
const animal = { tipo: 'desconocido' };
const perro = Object.create(animal);
perro.ladrar = function() { return 'guau'; };
console.log(perro.tipo); // 'desconocido' (heredado)
console.log(perro.ladrar()); // 'guau'
console.log(perro.toString()); // método heredado de Object.prototype
```

### Propiedad constructor

Las funciones (que pueden actuar como constructor) tienen una propiedad prototype que es un objeto con una propiedad constructor que apunta de vuelta a la función. Cuando creamos un objeto con new, su prototipo se establece a ese prototype. Así, los objetos creados con new Func() heredan métodos definidos en Func.prototype.
Herencia prototípica clásica (antes de clases)

Los desarrolladores manipulaban prototype para simular herencia:
```js
function Animal(nombre) { this.nombre = nombre; }
Animal.prototype.hablar = function() { return '...'; };

function Perro(nombre) { Animal.call(this, nombre); }
Perro.prototype = Object.create(Animal.prototype);
Perro.prototype.constructor = Perro;
Perro.prototype.ladrar = function() { return 'guau'; };
```

Este patrón es engorroso y fue reemplazado por la sintaxis class (azúcar sintáctico sobre prototipos).
Impacto en el rendimiento

Recorrer la cadena de prototipos es rápido, pero modificar __proto__ o Object.setPrototypeOf es una operación lenta que debe evitarse en código de alto rendimiento. Lo recomendable es establecer el prototipo al crear el objeto con Object.create().
---

## Archivo: `04-funciones-constructoras.md`


Una función constructora es una función normal que se invoca con el operador new. Su propósito es crear e inicializar un objeto.
Convención

    Nombre en PascalCase (primera letra mayúscula) para distinguirla de funciones normales.

    Internamente usa this para asignar propiedades al nuevo objeto.

    No debe devolver explícitamente un objeto (si devuelve un valor primitivo, se ignora; si devuelve un objeto, ese objeto será el resultado en lugar de la instancia).

```js
function Coche(marca, modelo) {
  this.marca = marca;
  this.modelo = modelo;
}
Coche.prototype.arrancar = function() {
  return `${this.marca} ${this.modelo} arrancado`;
};

const coche1 = new Coche('Toyota', 'Yaris');
console.log(coche1.arrancar()); // Toyota Yaris arrancado
```

### Qué ocurre al usar new

    Se crea un nuevo objeto vacío.

    El prototipo del nuevo objeto se enlaza a Func.prototype.

    Dentro de la función, this apunta al nuevo objeto.

    Se ejecuta el cuerpo de la función (normalmente para añadir propiedades).

    Si la función no retorna un objeto, se devuelve el nuevo objeto creado.

### Cómo detectar si una función fue llamada con new

    new.target: dentro de la función, si fue llamada con new es una referencia a la función constructora; si no, es undefined.

    Con eso se puede lanzar un error si se omite new.

### Problemas

    Requiere manejar el prototype para métodos, lo que puede ser confuso.

    No es obvio que deba usarse new; se puede invocar sin new, causando efectos laterales en el ámbito global.

    La sintaxis de clases resuelve estos problemas con un diseño más claro.

---

## Archivo: `05-clases-es6.md`


La sintaxis class introduce una manera más clara y familiar de crear objetos y manejar la herencia, basada internamente en prototipos.
Declaración de clase
```js
class Persona {
  constructor(nombre, edad) {
    this.nombre = nombre;
    this.edad = edad;
  }
  saludar() {
    return `Hola, soy ${this.nombre}`;
  }
  static especie() {
    return 'humano';
  }
}

    El método constructor se ejecuta al hacer new Persona(...). Si no se define, se usa uno vacío por defecto.

    Los métodos definidos en el cuerpo de la clase van al prototype (no son propios de cada instancia).

    static define un método en la propia clase (no en las instancias).
```

### Herencia con extends y super
```js
class Estudiante extends Persona {
  constructor(nombre, edad, curso) {
    super(nombre, edad); // debe llamarse a super antes de usar this
    this.curso = curso;
  }
  saludar() {
    return `${super.saludar()}. Estudio ${this.curso}`;
  }
}

    extends establece la cadena de prototipos (tanto Estudiante.prototype como Estudiante.__proto__).

    super dentro del constructor invoca al constructor padre.

    super.metodo() llama a la versión del padre de un método.
```

### Miembros privados (ES2022)

Se prefijan con #. No son accesibles fuera de la clase.
```js
class Cuenta {
  #saldo = 0;
  depositar(monto) {
    this.#saldo += monto;
  }
  getSaldo() {
    return this.#saldo;
  }
}

    No pueden ser accedidos ni desde subclases (a menos que se expongan mediante métodos protegidos, no nativos).
```

### Campos públicos (class fields)

Las propiedades pueden declararse directamente en el cuerpo de la clase (sin this en el constructor) y se inicializan antes del constructor:
```js
class Rectangulo {
  alto = 10;
  ancho = 5;
  area = this.alto * this.ancho; // cuidado: se evalúa cuando se crea la instancia
}
```

Estos campos son propios de la instancia.
Getters y setters en clases

Igual que en objetos literales, con get y set.
Diferencias con funciones constructoras

    El código de una clase siempre se ejecuta en modo estricto.

    Las clases no se pueden llamar sin new (error TypeError).

    Las declaraciones de clase no son izadas (hoisting temporal pero con TDZ, a diferencia de las funciones que si se elevan).

### Resumen

Las clases no reemplazan los prototipos; son un envoltorio sintáctico que facilita la programación orientada a objetos en js, especialmente para desarrolladores que vienen de lenguajes basados en clases.
---

## Archivo: `06-metodos-de-object.md`


El objeto global Object proporciona métodos estáticos muy útiles para trabajar con objetos.
Métodos de iteración y conversión

    Object.keys(obj): devuelve un array con las claves propias enumerables.

    Object.values(obj): array con los valores propios enumerables.

    Object.entries(obj): array de pares [clave, valor].

```js
const obj = { a: 1, b: 2 };
Object.entries(obj); // [['a',1], ['b',2]]
```

Estos ignoran propiedades no enumerables y las heredadas.
Métodos para control de propiedades

    Object.defineProperty(obj, prop, descriptor) y Object.defineProperties: ya vistos.

    Object.getOwnPropertyDescriptor(obj, prop): devuelve el descriptor de una propiedad propia.

    Object.getOwnPropertyNames(obj): array de todas las claves propias (incluyendo no enumerables, excluyendo Symbols).

    Object.getOwnPropertySymbols(obj): array de símbolos propios.

    Object.hasOwn(obj, prop) (ES2022): método más seguro que obj.hasOwnProperty para verificar propiedad propia.

### Protección de objetos (inmutabilidad)

    Object.preventExtensions(obj): impide añadir nuevas propiedades.

    Object.seal(obj): preventExtensions + configura configurable: false para todas las propiedades existentes (no se pueden eliminar).

    Object.freeze(obj): seal + configura writable: false (objeto completamente inmutable de forma superficial). Las subpropiedades si son objetos pueden seguir modificándose.
    Para cada uno existen sus comprobadores: Object.isExtensible, Object.isSealed, Object.isFrozen.

```js
const config = Object.freeze({ api: 'https://...' });
config.api = 'otra'; // falla silenciosamente o lanza error en estricto
```

### Creación y manipulación de prototipos

    Object.create(proto, [descriptors]): crea un nuevo objeto con el prototipo especificado.

    Object.getPrototypeOf(obj) y Object.setPrototypeOf(obj, proto).

    Object.setPrototypeOf es lento; mejor usar Object.create.

### Métodos de copia y composición

    Object.assign(target, ...sources): copia las propiedades propias enumerables de los objetos fuente al objeto destino (copia superficial). Retorna el destino. Muy usado para combinar objetos.

```js
const base = { a: 1 };
const copia = Object.assign({}, base, { b: 2 }); // { a:1, b:2 }
```

    No copia getters/setters, sino sus valores evaluados.

### De objeto a otros formatos

    Object.fromEntries(iterable): inverso de Object.entries, construye un objeto a partir de pares clave-valor.

```js
Object.fromEntries([['nombre','Juan'], ['edad',30]]); // {nombre:'Juan', edad:30}
```

    JSON.stringify y JSON.parse para serialización, aunque no son métodos de Object, son indispensables.

---

## Archivo: `07-destructuring.md`


La desestructuración (destructuring) permite extraer valores de arrays u objetos y asignarlos a variables de forma concisa.
Desestructuración de objetos
```js
const persona = { nombre: 'Elena', edad: 28, ciudad: 'Madrid' };
const { nombre, edad } = persona;
console.log(nombre); // Elena
```

    Los nombres de las variables deben coincidir con las claves.

    Se pueden usar alias: { nombre: name, edad: age }.

    Se pueden asignar valores por defecto: { pais = 'España' }.

    También se puede extraer en parámetros de función:

```js
function presentar({ nombre, edad }) {
  return `${nombre} tiene ${edad} años`;
}
```

    Se puede anidar:

```js
const usuario = { datos: { email: 'a@b.com' } };
const { datos: { email } } = usuario;

    Se puede combinar con el operador rest para agrupar el resto de propiedades: const { nombre, ...resto } = obj;.
```

### Desestructuración de arrays
```js
const colores = ['rojo', 'verde', 'azul'];
const [primero, segundo] = colores;
console.log(primero); // rojo

    Se pueden omitir elementos con comas: const [,, tercero] = colores;.

    Rest en arrays: const [primero, ...demas] = colores;.

    Valores por defecto: const [a = 10] = [].

    Intercambio de variables: [a, b] = [b, a];.
```

### Casos de uso comunes

    Extraer propiedades de objetos de configuración.

    Múltiples valores de retorno emulados con arrays u objetos.

    Iteración con for...of y entries(): for (const [indice, valor] of arr.entries()).

### Desestructuración anidada y compleja

Se pueden mezclar objetos y arrays en una misma sentencia:
```js
const datos = { id: 1, items: ['a', 'b'] };
const { id, items: [x, y] } = datos;
console.log(x); // 'a'
```

### Errores comunes

    Intentar desestructurar null o undefined lanza TypeError; se puede proteger con valor por defecto: const { prop } = obj || {};.

    La desestructuración siempre crea nuevas variables, no modifica el original.

### 05-arrays-y-colecciones
---

## Archivo: `01-arrays-basicos.md`


Los arrays en js son objetos de alto nivel que permiten almacenar colecciones ordenadas de elementos. Internamente son objetos con claves numéricas (índices) y una propiedad length especial.
Creación
```js
const arr1 = [1, 2, 3];          // literal
const arr2 = new Array(1, 2, 3); // constructor (no recomendado si se pasa un solo número, crea array con ese tamaño)
const arr3 = Array.of(5);        // crea [5] (soluciona ambigüedad)
const arr4 = Array.from('hola'); // convierte iterable/array-like en array: ['h','o','l','a']
```

### Índices y propiedad length

    Los índices son enteros no negativos. Se puede acceder con arr[indice].

    length es siempre uno más que el mayor índice existente (no es el número real de elementos si hay huecos).

    Modificar length directamente trunca o extiende el array. Si se asigna un valor más pequeño, se eliminan elementos sobrantes. Si se hace más grande, los huecos se llenan con empty (comportamiento de índice inexistente).

```js
const a = [10, 20, 30];
a.length = 2;      // ahora es [10, 20]
a.length = 5;      // [10, 20, , , ] -> los últimos tres son empty
console.log(a[3]); // undefined
```

### Arrays dispersos (sparse arrays)

Los arrays pueden tener "agujeros" si se asignan índices no consecutivos.
```js
const sparse = [];
sparse[100] = 'a';
console.log(sparse.length); // 101
```

Los métodos que iteran (forEach, map, etc.) ignoran los índices vacíos. Los bucles for tradicionales acceden a ellos devolviendo undefined. El operador in devuelve false para esos índices.
Detectar un array

Dado que typeof devuelve "object", la forma correcta es:

    Array.isArray(valor) (ES5) – recomendado.

    valor instanceof Array (falla entre iframes o dominios diferentes).

### Iteración básica

    for (let i = 0; i < arr.length; i++) – clásico, pero maneja índices manualmente.

    for...of – recorre valores (recomendado).

    for...in – recorre índices como strings (incluye propiedades no numéricas si las hay, no recomendado para arrays).

    Métodos funcionales como forEach.

### Comparación y mutabilidad

Los arrays son objetos, por lo que dos arrays con el mismo contenido son diferentes referencias. La comparación por valor requiere iterar manualmente o usar JSON.stringify (limitado).
---

## Archivo: `02-metodos-modificadores.md`


Estos métodos mutan el array original. Es importante reconocerlos para evitar efectos laterales no deseados.
Agregar y eliminar al final

    push(...items): añade uno o más elementos al final y devuelve la nueva longitud.

    pop(): elimina el último elemento y lo devuelve (o undefined si el array está vacío).

### Agregar y eliminar al inicio

    unshift(...items): añade al inicio, devuelve nueva longitud.

    shift(): elimina el primer elemento y lo devuelve.

Coste: shift y unshift deben reindexar todos los elementos, por lo que son más lentos que push/pop.
splice(indice, cantidadAEliminar, ...itemsAAgregar)

Método todoterreno para modificar un array en cualquier posición.

    Elimina cantidadAEliminar elementos desde indice.

    Inserta itemsAAgregar en esa misma posición.

    Devuelve un array con los elementos eliminados.

    Con cantidadAEliminar = 0 se usa como inserción pura.

    Con ...itemsAAgregar vacío se usa como eliminación pura.

    Los índices negativos cuentan desde el final.

```js
const arr = [1,2,3,4,5];
arr.splice(2, 2); // elimina 3,4 → arr = [1,2,5]
arr.splice(1, 0, 'a', 'b'); // arr = [1,'a','b',2,5]
```

### Relleno y copia dentro del array

    fill(valor, inicio?, fin?): rellena los índices de inicio a fin (exclusivo) con valor. Si no se pasan, rellena todo. Muta el array.

    copyWithin(target, start, end?): copia una porción del propio array a otra posición, sobrescribiendo. Útil para desplazamientos. Muta el array.

```js
[1,2,3,4,5].copyWithin(0, 3); // [4,5,3,4,5]
```

### Ordenamiento y reversa

    sort(fnComparacion?): ordena in-place y devuelve el array. Por defecto, convierte elementos a string y compara por código UTF-16. Para orden numérico pasar (a, b) => a - b.

    reverse(): invierte el orden in-place.

```js
const nums = [3,1,10];
nums.sort(); // [1, 10, 3] (orden léxico)
nums.sort((a,b) => a - b); // [1,3,10]
```

### Otros

    flat() y flatMap() no son mutadores (devuelven nuevo array, ver en otra sección), pero se pueden usar.

### Importante

Todos estos métodos modifican el array original. Si se necesita inmutabilidad, se deben hacer copias previas (con spread, slice, etc.).
---

## Archivo: `03-metodos-funcionales.md`


Estos métodos no modifican el array original (a excepción de forEach que no devuelve nada, pero puede modificar elementos si el callback lo hace). Son la base de la programación funcional con arrays.
forEach(fn)

Ejecuta fn(elemento, indice, array) para cada elemento. Ignora índices vacíos. No devuelve nada, no se puede encadenar. Útil para efectos secundarios controlados.
```js
[1,2,3].forEach(n => console.log(n));
```

No se puede detener con break; si se necesita interrumpir, usar for...of o some/every.
map(fn)

Transforma cada elemento y devuelve un nuevo array con los resultados.
```js
const dobles = [1,2,3].map(n => n * 2); // [2,4,6]
```

La longitud del nuevo array siempre es igual a la original, aunque los índices vacíos permanecen vacíos.
filter(fn)

Devuelve un nuevo array con los elementos para los que fn devuelve un valor truthy.
```js
const mayores = [5, 10, 3, 15].filter(n => n > 7); // [10,15]
```

Si ningún elemento pasa, devuelve array vacío.
reduce(fn, valorInicial?) y reduceRight

Acumula los elementos en un solo valor. fn recibe (acumulador, elemento, indice, array).
```js
const suma = [1,2,3,4].reduce((acc, n) => acc + n, 0); // 10
```

    Si no se da valorInicial, el primer elemento se usa como acumulador inicial y la iteración empieza desde el segundo.

    reduceRight itera de derecha a izquierda.

### find(fn) y findIndex(fn)

    find devuelve el primer elemento que cumple la condición, o undefined.

    findIndex devuelve el índice de ese elemento, o -1.

### some(fn) y every(fn)

    some: ¿al menos un elemento cumple? → booleano.

    every: ¿todos cumplen? → booleano.

Ambos detienen la iteración tan pronto como se conoce el resultado.
flat(depth?) y flatMap(fn)

    flat(depth): "aplana" sub-arrays hasta la profundidad indicada (por defecto 1). Devuelve nuevo array.

```js
[1, [2, [3]]].flat(2); // [1,2,3]

    flatMap(fn): es un map() seguido de flat(1). Ideal cuando el callback devuelve un array y queremos un solo array como resultado.
```

### Encadenamiento

Debido a que estos métodos devuelven nuevos arrays (excepto forEach), se pueden encadenar para crear pipelines de procesamiento legibles:
```js
const resultado = usuarios
  .filter(u => u.activo)
  .map(u => u.nombre)
  .sort();

---

## Archivo: `04-spread-y-rest.md`

```

Se trata del operador ... usado tanto en arrays como en objetos (ya visto), pero aquí lo enfocamos en su uso con arrays y colecciones.
Spread en arrays (expansión)

Convierte los elementos de un iterable (array, string, Set, Map, etc.) en elementos individuales.
Creación de copias superficiales
```js
const original = [1,2,3];
const copia = [...original];
copia.push(4); // original sigue siendo [1,2,3]
```

Solo copia un nivel de profundidad (las referencias a objetos internos se comparten).
Combinar arrays
```js
const a = [1,2], b = [3,4];
const combinado = [...a, ...b, 5]; // [1,2,3,4,5]
```

### Insertar elementos en posición arbitraria sin splice
```js
const arr = [10, 50];
const nuevo = [0, ...arr, 100]; // [0,10,50,100]
```

### Pasar argumentos a funciones
```js
Math.max(...[1,5,3,9,2]); // 9
```

### Convertir NodeList u otros array-like a array
```js
const divs = document.querySelectorAll('div');
const arrDivs = [...divs];
```

Alternativa moderna: Array.from.
Rest en arrays (agrupación)

En desestructuración o en parámetros de función, ... recoge el resto de elementos en un array.
Destructuring rest
```js
const [primero, segundo, ...resto] = [10,20,30,40,50];
console.log(resto); // [30,40,50]
```

Debe ser el último elemento. Si no hay más elementos, resto será [].
Ignorar elementos

También se puede omitir la variable [a,,b] = [1,2,3] (a=1, b=3).
Rest en parámetros (ya visto en funciones)
```js
function sumar(...numeros) {
  return numeros.reduce((a,b) => a+b, 0);
}
```

Reemplaza a arguments.
Nota sobre rendimiento

El spread es una operación que itera el iterable completo; con grandes volúmenes puede ser costoso. Para operaciones pesadas considerar alternativas como push.apply o bucles, aunque normalmente no es un problema.
---

## Archivo: `05-set-y-map.md`


ES6 introdujo nuevas estructuras de datos eficientes para casos específicos.
Set

Colección de valores únicos, de cualquier tipo, sin claves. Permite inserción, búsqueda y eliminación rápidas (normalmente mejor rendimiento que con arrays para grandes colecciones).
Creación y métodos básicos
```js
const set = new Set([1,2,3,2,1]);
console.log(set); // Set(3) {1,2,3}
set.add(4);
set.has(2); // true
set.delete(3);
set.size; // 3
set.clear();

    add retorna el propio Set, permite encadenamiento.

    has es más rápido que indexOf en arrays cuando hay muchos elementos.

    Convierte a array: [...set] o Array.from(set).
```

### Iteración

### set.forEach(valor => ...)

### for (const valor of set)

    set.keys(), set.values(), set.entries() (estos dos últimos retornan el mismo iterador, con valor como clave y valor).

### Casos de uso

    Eliminar duplicados de un array: [...new Set(arr)].

    Conjuntos para operaciones de álgebra de conjuntos: unión, intersección, diferencia (usando spread y filter).

    Seguimiento de visitas únicas, IDs.

### WeakSet

Similar a Set pero solo acepta objetos y mantiene referencias débiles (si el objeto no tiene otras referencias, puede ser recolectado por el GC).

    No es iterable, no tiene propiedad size.

    Útil para marcar objetos sin prevenir su eliminación (ej. seguimiento de visitas DOM sin fugas de memoria).

### Map

Colección de pares clave-valor donde las claves pueden ser cualquier tipo (objetos, funciones, primitivos). A diferencia de objetos, mantiene el orden de inserción y tiene un mejor rendimiento en inserciones/eliminaciones frecuentes.
Creación y métodos
```js
const map = new Map();
map.set('nombre', 'Ana');
map.set(42, 'edad');
const objKey = { id: 1 };
map.set(objKey, 'datos');
```

### map.get('nombre'); // 'Ana'
map.has(42);       // true
map.size;          // 3
map.delete('edad');
map.clear();

### Iteración

### for (const [clave, valor] of map) (entries por defecto)

### map.forEach((valor, clave) => ...)

    map.keys(), map.values(), map.entries().

### Ventajas sobre objetos

    Las claves no se limitan a strings/symbols; pueden ser objetos.

    Propiedad size fácil de consultar.

    Mejor rendimiento en adiciones/eliminaciones frecuentes.

    No tiene claves heredadas por prototipo, es seguro iterar sin hasOwnProperty.

    Preserva el orden de inserción.

### Conversión con objetos y arrays

    De objeto a Map: new Map(Object.entries(obj)).

    De Map a objeto: Object.fromEntries(map).

    De array de pares a Map: new Map([['a',1], ['b',2]]).

### WeakMap

    Solo acepta objetos como claves y las referencias son débiles.

    No iterable, sin size.

    Ideal para almacenar datos asociados a objetos sin prevenir su recolección (metadatos privados, cachés).

    Uso común: cachear resultados de cálculo para objetos que pueden desaparecer.

---

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

## Archivo: `01-callbacks.md`


Un callback es una función que se pasa como argumento a otra función y se ejecuta más tarde, generalmente al completarse una operación (síncrona o asíncrona).
Callback síncrono vs asíncrono

    Síncrono: la función externa ejecuta el callback inmediatamente (ej. array.forEach, array.map). Bloquea el hilo.

    Asíncrono: la función registra el callback para ejecutarse en el futuro, cuando ocurra un evento o finalice una tarea larga (ej. setTimeout, lectura de archivo). No bloquea.

### Ejemplo con temporizador
```js
console.log('Inicio');
setTimeout(() => {
  console.log('Timeout');
}, 1000);
console.log('Fin');
// Imprime: Inicio, Fin, Timeout (después de 1s)
```

### Callback pattern en Node.js (error-first)

Tradicionalmente en Node, los callbacks asíncronos reciben un error como primer argumento o null si todo fue bien.
```js
fs.readFile('/archivo.txt', 'utf8', (err, data) => {
  if (err) {
    console.error('Error:', err);
    return;
  }
  console.log(data);
});
```

Esto normaliza el manejo de errores.
Inconveniente: Callback Hell

Cuando se anidan muchos callbacks para secuencias de operaciones asíncronas, el código se vuelve difícil de leer y mantener:
```js
obtenerUsuario(id, (usuario) => {
  obtenerPedidos(usuario, (pedidos) => {
    procesarPedido(pedidos[0], (resultado) => {
      // más anidamiento...
    });
  });
});
```

Las soluciones modernas incluyen Promesas y async/await.
Errores comunes

    Olvidar que la ejecución continúa después de setTimeout sin esperar.

    No capturar errores lanzados dentro de callbacks asíncronos con try/catch (no funcionan porque el stack original ya no existe).

    Perder el contexto de this si pasamos un método como callback sin atar (bind o arrow function).

### Aún se usan

    APIs antiguas en Node (fs callback-style) y navegadores (IndexedDB, etc.).

    Event listeners (addEventListener).

    Muchos módulos han migrado a promesas: fs.promises.

---

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

## Archivo: `03-async-await.md`


async/await es azúcar sintáctico sobre las promesas, que permite escribir código asíncrono como si fuera síncrono, mejorando la legibilidad.
Función async

Una función precedida por async siempre devuelve una promesa. Si la función retorna un valor (no promesa), la promesa se resuelve con ese valor. Si lanza una excepción, la promesa se rechaza.
```js
async function obtenerDatos() {
  return 42;
}
obtenerDatos().then(console.log); // 42
```

### Palabra clave await

Solo se puede usar dentro de funciones async. Pausa la ejecución de la función hasta que la promesa se resuelva, y devuelve el valor resuelto.
```js
async function mostrarUsuario(id) {
  const response = await fetch(`/api/user/${id}`);
  const user = await response.json();
  console.log(user);
}
```

    Si la promesa se rechaza, await lanza una excepción, que se puede capturar con try/catch.

    No bloquea el hilo principal; el runtime puede atender otras tareas mientras espera.

### Manejo de errores con try/catch
```js
async function tarea() {
  try {
    const datos = await funcionQuePuedeFallar();
    return datos;
  } catch (error) {
    console.error('Falló:', error);
    // Podemos devolver valor por defecto o relanzar
    throw error;
  }
}
```

### Uso de await fuera de async (top-level await)

En módulos ES, el estándar permite await a nivel de cuerpo del módulo sin necesidad de función async (ES2022). Facilita la inicialización asíncrona de módulos.
Combinación con Promise.all

Como await detiene la ejecución secuencialmente, si necesitamos lanzar varias operaciones concurrentes debemos iniciar las promesas sin esperar y luego usar await Promise.all(...).
```js
async function cargarEnParalelo() {
  const [usr, posts] = await Promise.all([
    fetch('/user').then(r => r.json()),
    fetch('/posts').then(r => r.json())
  ]);
}
```

### Cuidado con bucles

    for...of funciona bien con await si se necesita secuencialidad.

    No usar forEach con await porque el callback de forEach no es async y no esperará realmente.

### Errores comunes

    Olvidar que async hace que la función siempre retorne una promesa, lo que puede cambiar la interfaz de la función.

    No manejar errores, dejando promesas rechazadas silenciosas (en Node las advertencias, en navegador eventos unhandledrejection).

    No aprovechar la concurrencia y usar await secuencial para tareas independientes.

---

## Archivo: `04-fetch-api.md`


fetch es la API moderna para realizar peticiones HTTP en el navegador (y disponible globalmente en Node 18+). Retorna una Promesa que resuelve un objeto Response.
Sintaxis básica
```js
fetch(url, options)
  .then(response => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error('Error de red o parseo', error));

```
    url: string o URL.

    options: objeto de configuración opcional (method, headers, body, mode, etc.).

    Por defecto realiza GET.

### El objeto Response

Propiedades principales:

    response.ok: booleano, true si status entre 200-299.

    response.status: código HTTP (200, 404...).

    response.headers: objeto Headers.

    response.url: URL final después de redirecciones.
    Métodos para leer el cuerpo (solo uno puede ser llamado, el cuerpo se consume):

    response.json(): parsea JSON.

    response.text(): texto plano.

    response.blob(): datos binarios (imágenes, archivos).

    response.arrayBuffer(): buffer de bytes.

    response.formData(): para datos de formulario.

### Configuración de peticiones
```js
fetch('/api/item', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token'
  },
  body: JSON.stringify({ nombre: 'Producto' })
})
```

Otras opciones: mode ('cors', 'no-cors', 'same-origin'), credentials ('include', 'same-origin', 'omit'), cache, redirect.
Manejo de errores

fetch solo rechaza la promesa por errores de red (no se pudo conectar). Un status HTTP 404 o 500 NO es un error de red, la promesa se resuelve normalmente. Por eso es necesario verificar response.ok.
Cancelación con AbortController

Se puede cancelar una petición fetch usando AbortController.
```js
const controller = new AbortController();
setTimeout(() => controller.abort(), 5000);
fetch(url, { signal: controller.signal })
  .then(...)
  .catch(err => {
    if (err.name === 'AbortError') console.log('Cancelada');
  });
```

### Subida de archivos

body puede ser un FormData para subir archivos:
```js
const formData = new FormData();
formData.append('archivo', fileInput.files[0]);
fetch('/upload', { method: 'POST', body: formData });
```

### Streaming

El cuerpo de la respuesta puede ser leído como stream usando response.body.getReader(), útil para grandes descargas.
Fetch vs Axios

Fetch es nativo, no necesita dependencias, pero carece de algunas comodidades como interceptores, timeout nativo (se puede con AbortController) o manejo automático de JSON. Axios sigue siendo popular en proyectos grandes.
---

## Archivo: `05-temporizadores.md`


js provee funciones para ejecutar código después de un retraso o periódicamente. No son parte de ECMAScript, sino APIs del entorno (navegador y Node.js), pero son universales.
setTimeout(fn, delay, ...args)

Programa la ejecución única de fn después de delay milisegundos. Retorna un identificador numérico.
```js
const id = setTimeout(() => {
  console.log('Pasaron 2 segundos');
}, 2000);
```

    El tiempo no es garantizado: es el mínimo, pero la tarea se encolará y esperará su turno en el event loop.

    Si delay es 0, se ejecuta en la próxima macrotarea (después del código síncrono actual).

### clearTimeout(id)

Cancela un timeout pendiente.
setInterval(fn, delay, ...args)

Ejecuta fn repetidamente cada delay ms. Retorna un ID.
```js
const id = setInterval(() => console.log('tick'), 1000);
```

### clearInterval(id)

Detiene la repetición.
Precauciones con setInterval

    Si la función tarda más que el intervalo, las ejecuciones pueden solaparse o encolarse, lo que no es deseable. Es preferible usar setTimeout recursivo para intervalos seguros:

```js
function tarea() {
  console.log('ejecutar');
  setTimeout(tarea, 1000);
}
setTimeout(tarea, 1000);
```

De esta forma se garantiza un tiempo entre ejecuciones sin solapamiento.
setImmediate (Node.js) y queueMicrotask

No son temporizadores, pero están relacionados. En navegador no existe setImmediate; en su lugar se puede usar setTimeout(fn, 0) con precaución (es una macrotarea). queueMicrotask encola una microtarea, que se ejecuta antes de las macrotareas.
Uso con this

Si se pasa un método de objeto como callback, se pierde el contexto. Usar arrow function o bind.
Aplicaciones

    Debounce y throttle para eventos frecuentes (scroll, resize).

    Animaciones y retrasos.

    Timeout en peticiones (AbortController es preferible a veces).

---

## Archivo: `06-event-loop.md`


El Event Loop es el mecanismo que permite a js ejecutar código asíncrono de manera no bloqueante a pesar de tener un solo hilo de ejecución principal.
Componentes

    Call Stack (Pila de ejecución): donde se apilan las funciones llamadas síncronamente. Cada función se retira al finalizar.

    Web APIs / Background Tasks: en el navegador, funciones como setTimeout, fetch, eventos del DOM son manejadas por el entorno fuera del motor JS. Cuando terminan, insertan callbacks en las colas.

    Colas de tareas (Task Queues):

        Macrotareas (Task Queue): setTimeout, setInterval, eventos de UI, I/O, setImmediate (Node). Solo se procesa una macrotarea a la vez por ciclo del event loop.

        Microtareas (Microtask Queue): promesas (.then, .catch, .finally), queueMicrotask, MutationObserver. Se procesan por completo al final de cada macrotarea y antes de la siguiente.

    Event Loop: ciclo continuo que verifica la pila. Si está vacía, toma tareas de las colas:

        Primero vacía completamente la cola de microtareas (incluso las que se generen durante ese procesamiento).

        Luego toma la siguiente macrotarea (una sola) y la ejecuta.

        Repite.

### Orden de ejecución típico
```js
console.log('1');
setTimeout(() => console.log('2'), 0);
Promise.resolve().then(() => console.log('3'));
console.log('4');
// Resultado: 1, 4, 3, 2
```

Explicación:

    '1' y '4' son código síncrono, van directo a consola.

    setTimeout encola una macrotarea (futura).

    Promise.then encola una microtarea.

    Al terminar lo síncrono, la pila queda vacía. Se procesan microtareas: '3'.

    Luego se toma la macrotarea: '2'.

### Renderizado

En navegadores, el renderizado de la página suele ocurrir entre macrotareas, después de procesar las microtareas pendientes. Por eso cambios en microtareas pueden afectar el renderizado antes de que el usuario vea algo inconsistente.
Consecuencias prácticas

    Las microtareas pueden ejecutarse infinitamente si dentro de una microtarea se añade otra microtarea (bloqueo de la UI).

    setTimeout(fn, 0) no ejecuta inmediatamente, cede el control al event loop; se usa para posponer al final de la pila actual.

    async/await convierten el código que sigue al await en una microtarea.

    Para tareas intensivas, dividir el trabajo y ceder el control con setTimeout para mantener la UI responsiva.

### Node.js vs Navegadores

El concepto es similar, pero Node tiene más tipos de colas (timer, poll, check, close) y setImmediate que se comporta distinto de setTimeout(fn,0) según el momento.
Visualización gráfica

Se puede imaginar:
```text
Call Stack -> (vacía) -> Event Loop:
  - Vaciar Microtask Queue
  - Tomar 1 Macrotask
  - Renderizar (si es necesario)
  - Repetir
```

Comprender el event loop es crucial para depurar problemas de orden de ejecución y rendimiento en aplicaciones asíncronas.

### 07-this-y-contexto
---

## Archivo: `01-this-global-y-metodo.md`


La palabra clave this es una de las más poderosas y confusas de js. Su valor no se determina en tiempo de escritura, sino en tiempo de ejecución, y depende de cómo se invoca la función que lo contiene.
Reglas generales de determinación de this

Existen básicamente cuatro patrones que determinan a qué apunta this:

### Invocación global o de función simple

### Invocación como método de un objeto

### Invocación con new (constructor)

### Invocación explícita con call, apply, bind

1. this en el ámbito global

Fuera de cualquier función, this hace referencia al objeto global:

    En el navegador: window (o globalThis).

    En Node.js: global (o globalThis).

    En módulos ES, el ámbito global no tiene this apuntando al objeto global (es undefined en el nivel superior del módulo). Pero dentro de una función no ligada, sí.

```js
// Navegador (script normal)
console.log(this); // window

// En Node REPL o script CommonJS
console.log(this); // {}
// Nota: en módulo CommonJS, this es el objeto module.exports (no global)
// En el ámbito de una función: this es global
```

2. this en una función normal (no método, no new, sin call/apply/bind)

Cuando una función ordinaria (no flecha) es invocada sin un contexto explícito, su this depende del modo:

    Modo no estricto: this apunta al objeto global (window en navegadores, global en Node).

    Modo estricto ('use strict' o módulos ES): this es undefined.

```js
function mostrarThis() {
  console.log(this);
}
mostrarThis(); // window o global (no estricto), undefined (estricto)
```

Este comportamiento causa problemas cuando una función se pasa como callback y se espera que this tenga un valor particular.
3. this en un método de objeto

Cuando una función se llama como propiedad de un objeto (método), this se refiere al objeto que está antes del punto (o corchetes) en el momento de la invocación.
```js
const persona = {
  nombre: 'Carlos',
  saludar: function() {
    return `Hola, soy ${this.nombre}`;
  }
};
```

### console.log(persona.saludar()); // Hola, soy Carlos

Peligro: si el método se extrae a una variable y se llama por separado, pierde su contexto.
```js
const saludo = persona.saludar;
saludo(); // Hola, soy undefined (this es global/undefined)
```

Excepción con la cadena de prototipos: si el método se encuentra en el prototipo pero se invoca a través del objeto, this sigue siendo el objeto original.
```js
const base = { decir() { return this.valor; } };
const hijo = Object.create(base);
hijo.valor = 10;
console.log(hijo.decir()); // 10
```

### 4. this en una función constructora (con new)

Cuando una función es llamada con new, se crea un objeto nuevo y this apunta a ese nuevo objeto dentro del constructor.
```js
function Cosa(nombre) {
  this.nombre = nombre;
}
const cosa = new Cosa('Ejemplo');
console.log(cosa.nombre); // Ejemplo
```

Si accidentalmente se llama sin new, this se comportará según las reglas de función normal (posiblemente contaminando el objeto global). Para protegerse, se puede usar new.target o la sintaxis class, que fuerza el uso de new.
5. this en callbacks clásicos y event listeners

    En addEventListener, this dentro del callback apunta al elemento DOM que disparó el evento (excepto si se usa arrow function, que no tiene this propio).

    En callbacks de temporizadores (setTimeout/setInterval), las funciones normales tienen this global/undefined.

    En métodos de array como .forEach, el segundo argumento opcional se convierte en el this del callback.

```js
const obj = { factor: 10, multiplicar(arr) { arr.forEach(function(n) { console.log(this.factor * n); }, this); } };
```

### Errores comunes

    Asumir que this dentro de una función anidada es el mismo que el de la función contenedora.

    Olvidar que this en callbacks se desvincula.

La solución histórica era var self = this; o that = this;. Hoy las arrow functions resuelven esto (ver siguiente sección).
---

## Archivo: `02-arrow-functions-y-this.md`


Las arrow functions (funciones flecha) se diferencian radicalmente de las funciones normales en el manejo de this: no tienen su propio this. En lugar de eso, capturan el valor de this del ámbito léxico que las envuelve en el momento de su definición.
No vinculan this propio

Dentro de una arrow function, this se resuelve exactamente igual que cualquier otra variable del ámbito exterior. Si la arrow se define en un ámbito donde this es un objeto, ese objeto será this dentro de la arrow, sin importar cómo se invoque.
```js
const obj = {
  nombre: 'Ana',
  saludar: function() {
    // this es obj
    const arrow = () => {
      console.log(this.nombre);
    };
    arrow();
  }
};
obj.saludar(); // Ana
```

Si definimos la arrow directamente como método del objeto, NO funcionará como esperamos, porque la arrow captura this del ámbito de definición (que podría ser global/undefined), no el objeto.
```js
const obj = {
  nombre: 'Error',
  saludar: () => {
    console.log(this.nombre); // undefined o error
  }
};
obj.saludar(); // No imprime 'Error'
```

Por eso, no uses arrow functions como métodos de objetos si necesitas acceder a this del objeto.
Ventajas en callbacks

Donde las arrows brillan es en callbacks y funciones anidadas, evitando la necesidad de bind o self = this.
```js
function Temporizador() {
  this.segundos = 0;
  setInterval(() => {
    this.segundos++; // this se refiere a la instancia de Temporizador
  }, 1000);
}
```

Con una función normal, this.segundos estaría creando una propiedad en el objeto global.
Arrow functions y addEventListener

Si usas una arrow en addEventListener, this NO apuntará al elemento que disparó el evento, sino al this del ámbito exterior. Si necesitas el elemento, utiliza event.currentTarget o event.target.
```js
element.addEventListener('click', (e) => {
  console.log(this); // no es el elemento
  console.log(e.currentTarget); // el elemento
});
```

### Arrow functions y constructores

Las arrows no pueden ser usadas con new. Carecen de propiedad prototype y lanzarán un TypeError si se intenta.
Puntos a recordar

    this en arrow function es léxico: se define dónde se escribe la función, no cómo se llama.

    No tienen arguments, super ni new.target propios; los heredan del contexto contenedor.

    Son extremadamente útiles para preservar el contexto de this en callbacks, promesas y programación funcional.

    No adecuadas para métodos de objetos (salvo que el método no use this).

---

## Archivo: `03-call-apply-bind.md`


Estos tres métodos permiten controlar explícitamente el valor de this y proveen una forma de "prestar" funciones.

Todos pertenecen a Function.prototype y están disponibles en cualquier función (excepto arrows, que ignoran estos métodos porque no tienen this propio).
call(thisArg, arg1, arg2, ...)

Invoca la función inmediatamente, estableciendo this al primer argumento, y pasando los argumentos restantes de forma individual.
```js
function saludar(signo) {
  console.log(`Hola ${this.nombre}${signo}`);
}
const persona = { nombre: 'Lucía' };
saludar.call(persona, '!'); // Hola Lucía!

    thisArg puede ser null o undefined (en ese caso se reemplaza por el objeto global en no estricto, o se mantiene en estricto).

    Muy usado para herencia constructora: Padre.call(this, ...args).
```

### apply(thisArg, [argsArray])

Similar a call, pero los argumentos se pasan como un array (o iterable).
```js
function sumar(a, b, c) {
  return a + b + c;
}
const numeros = [1, 2, 3];
sumar.apply(null, numeros); // 6
```

    Útil cuando tienes los argumentos en un array y quieres pasarlos dinámicamente.

    Hoy en día, el operador spread (...) cubre muchos casos: fn(...args).

### bind(thisArg, arg1, arg2, ...)

No ejecuta la función de inmediato. Devuelve una nueva función con el this fijado permanentemente al valor dado, y los argumentos opcionales preestablecidos (partial application).
```js
function multiplicar(factor, n) {
  return factor * n;
}
const duplicar = multiplicar.bind(null, 2);
console.log(duplicar(5)); // 10

    Una vez hecho bind, el this no puede ser sobrescrito ni siquiera con call/apply/new (aunque new ignora el this vinculado y usa el nuevo objeto).
```

    Es fundamental para pasar métodos de objeto como callbacks sin perder el contexto.

```js
const boton = {
  texto: 'Click me',
  manejarClick: function() {
    console.log(this.texto);
  }
};
document.querySelector('button').addEventListener('click', boton.manejarClick.bind(boton));
// Sin bind, this sería el button, no boton.
```

### Tabla comparativa
Método	¿Ejecuta?	Argumentos	Devuelve
call	Sí	Lista individual	Resultado de fn
apply	Sí	Array	Resultado de fn
bind	No	Lista individual	Nueva función
Casos comunes

    Préstamo de métodos: usar Array.prototype.slice.call sobre objetos array-like (arguments, NodeList) para convertirlos en array. (Hoy reemplazado por Array.from).

    Establecer this en callbacks de eventos cuando necesitas otro objeto.

    Partial application: const fn = funcion.bind(null, predefinido).

    Encadenamiento con setTimeout: setTimeout(objeto.metodo.bind(objeto), 100).

### Consideraciones con Arrow Functions

Como se mencionó, las arrow functions no pueden ser vinculadas; call, apply, bind no producen error pero no alteran this. Solo los argumentos adicionales se pasan (si los acepta).
```js
const flecha = () => console.log(this);
flecha.call({a:1}); // this sigue siendo el del ámbito léxico
```

Dominar this y sus métodos de control es esencial para escribir código robusto y evitar bugs de contexto.
08-dom-y-eventos
---

## Archivo: `01-seleccion-del-dom.md`


El DOM (Document Object Model) es la representación en árbol de los documentos HTML/XML. Para interactuar con él, primero hay que seleccionar los nodos.
Métodos clásicos del objeto document
getElementById

Devuelve un único elemento (o null) cuyo atributo id coincida exactamente. Sensible a mayúsculas. Método más rápido.
```js
const el = document.getElementById('main');
```

### getElementsByClassName

Devuelve una HTMLCollection viva de elementos con la clase especificada. Se actualiza automáticamente si el DOM cambia.
```js
const items = document.getElementsByClassName('item');
```

### getElementsByTagName

Devuelve HTMLCollection viva de elementos con el nombre de etiqueta dado.
```js
const divs = document.getElementsByTagName('div');
```

### getElementsByName

Devuelve NodeList viva de elementos con name dado (muy usado en formularios).
```js
const radios = document.getElementsByName('genero');
```

### Métodos modernos: querySelector y querySelectorAll

Usan selectores CSS, mucho más flexibles.

    querySelector(selector): devuelve el primer elemento que coincida o null.

    querySelectorAll(selector): devuelve una NodeList estática (no viva) de todos los elementos que coinciden.

```js
const primerItem = document.querySelector('.item');
const todosItems = document.querySelectorAll('.item');
const input = document.querySelector('#form input[type="text"]');
```

Las NodeList estáticas no se actualizan si el DOM cambia después de la consulta. Se pueden iterar con forEach (moderno), pero no son arrays completos; hay que convertirlos con Array.from para usar map, filter, etc.
Diferencias entre colecciones vivas y estáticas

    HTMLCollection (viva): refleja cambios dinámicos. No tiene forEach (aunque puede usarse con índices).

    NodeList estática: snapshot del momento, más predecible. querySelectorAll la devuelve; childNodes devuelve una NodeList viva.

### Selección relativa a un elemento

Una vez obtenido un elemento, podemos buscar dentro de él:

### element.querySelector/All

    element.getElementsBy...

    Propiedades de navegación: parentNode, children, firstChild, lastChild, nextSibling, previousSibling, closest(selector).

closest recorre hacia arriba (ancestros) buscando la primera coincidencia, muy práctico para delegación de eventos.
Selección de elementos especiales

### document.body, document.head, document.documentElement (html)

### document.forms, document.images, document.links, etc. (colecciones HTML)

### Buenas prácticas

    Prefiere querySelector para búsquedas complejas.

    Usa getElementById cuando solo necesites un ID por rendimiento.

    Convierte NodeList a array si necesitas métodos funcionales: [...lista] o Array.from.

    Guarda referencias a elementos seleccionados frecuentemente para no reconsultar el DOM.

---

## Archivo: `02-manipulacion-del-dom.md`


Manipular el DOM implica crear, modificar o eliminar nodos y sus atributos.
Crear elementos y texto

    document.createElement('tag'): crea un elemento del tipo dado.

    document.createTextNode('texto'): crea un nodo de texto. También se puede simplemente asignar a textContent o usar innerHTML.

```js
const p = document.createElement('p');
p.textContent = 'Hola mundo';
```

### Insertar nodos en el árbol

    parent.appendChild(nodo): añade como último hijo.

    parent.insertBefore(nuevo, referencia): inserta antes del nodo referencia existente.

    parent.replaceChild(nuevo, viejo): reemplaza un hijo.

    element.remove(): elimina el propio elemento.

    parent.removeChild(hijo): elimina un hijo.

Métodos modernos (más flexibles):

    parent.append(...nodosOstrings): inserta al final, acepta múltiples nodos y texto.

    parent.prepend(...nodosOstrings): inserta al principio.

    element.before(...): hermano anterior.

    element.after(...): hermano posterior.

    element.replaceWith(...): reemplaza el elemento.

```js
const div = document.createElement('div');
div.append('Texto', document.createElement('br'), 'más texto');
```

### Manipulación de contenido

    element.textContent: obtiene/establece el texto plano de todo el subárbol. Más seguro y eficiente que innerHTML si no necesitas HTML.

    element.innerHTML: obtiene/establece el contenido HTML como string. ¡Cuidado con XSS! No insertar contenido de usuario sin sanitizar.

    element.outerHTML: incluye el propio elemento en la cadena HTML.

    element.innerText: similar a textContent pero tiene en cuenta estilos y devuelve solo el texto visible; puede ser más lento.

### Atributos y propiedades

    Atributo HTML: definido en la etiqueta, accedible con getAttribute('nombre') y setAttribute('nombre', 'valor'). Siempre son strings.

    Propiedad de DOM: los elementos tienen propiedades en js que reflejan algunos atributos, pero pueden tener tipos distintos (ej. checked es booleano, value de input es el actual).

```js
input.getAttribute('value'); // valor inicial
input.value; // valor actual
```

    element.hasAttribute('attr'), element.removeAttribute('attr').

    data-* atributos: acceso mediante element.dataset.propiedad.

    Clases: element.classList permite add('clase'), remove('clase'), toggle('clase'), contains('clase'). Preferible a manipular className.

### Estilos

    element.style.propiedad = 'valor' para estilos en línea. Las propiedades se escriben en camelCase: backgroundColor.

    element.style.cssText para asignar varias a la vez.

    getComputedStyle(element) devuelve el objeto de estilos computados (solo lectura).

```js
const estilos = window.getComputedStyle(elemento);
console.log(estilos.marginTop);
```

### Fragmentos y rendimiento

Si necesitas hacer muchas inserciones, usa un DocumentFragment para evitar múltiples reflows. El fragmento se construye en memoria y luego se inserta de una vez.
```js
const frag = document.createDocumentFragment();
for (let i=0; i<1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  frag.appendChild(li);
}
ul.appendChild(frag);
```

### Clonar y eliminar

    element.cloneNode(true): copia profunda; false copia superficial.

    element.remove(): desaparece el nodo del DOM.

### Cuidado con XSS

Nunca uses innerHTML o outerHTML con contenido no confiable. Utiliza textContent o sanitizadores como DOMPurify.
---

## Archivo: `03-eventos-y-delegacion.md`


Los eventos permiten reaccionar a interacciones del usuario o cambios en el navegador.
Registrar manejadores
Propiedades on-event (onclick, onchange)
```js
elemento.onclick = function(evento) { ... };
```

    Solo un manejador por evento (sobrescribe anterior).

    No recomendado en aplicaciones modernas.

### addEventListener y removeEventListener
```js
function manejarClick(e) {
  console.log('Clicked', e.target);
}
elemento.addEventListener('click', manejarClick);
// eliminar después
elemento.removeEventListener('click', manejarClick);
```

    Permite múltiples escuchadores para el mismo evento.

    Tercer argumento opcional: options (capture, once, passive) o booleano useCapture.

    once: true elimina el listener automáticamente tras la primera ejecución.

    passive: true indica que el listener no llamará a preventDefault(), importante para rendimiento en scroll.

### El objeto evento e

Cada manejador recibe un objeto Event con propiedades clave:

    e.target: el elemento que originó el evento (más profundo).

    e.currentTarget: el elemento al que se ha enlazado el listener (útil en delegación).

    e.type: nombre del evento.

    e.preventDefault(): cancela el comportamiento por defecto (ej. envío de formulario, link).

    e.stopPropagation(): detiene la propagación del evento.

    e.stopImmediatePropagation(): detiene la propagación y evita que se ejecuten otros listeners en el mismo elemento.

### Fases de propagación

Cuando ocurre un evento, atraviesa tres fases:

    Fase de captura: desde window hacia el target (rara vez usada).

    Fase de target: el elemento donde ocurrió.

    Fase de burbuja: del target sube hacia window.

Por defecto, los listeners se registran en fase de burbuja. Para captura, pasa true como tercer argumento o { capture: true }.
Delegación de eventos

Técnica que consiste en poner un único listener en un ancestro común y usar e.target para determinar qué elemento hijo lo disparó. Esencial cuando los elementos se crean dinámicamente.
```js
lista.addEventListener('click', (e) => {
  if (e.target.matches('li button')) {
    console.log('Botón clickeado en elemento', e.target.closest('li'));
  }
});
```

    Ventajas: menos listeners, mejor rendimiento, maneja elementos añadidos posteriormente.

    Siempre verificar que e.target sea el deseado usando matches o closest.

### Eventos comunes

    Ratón: click, dblclick, mousedown, mouseup, mousemove, mouseover, mouseout, mouseenter, mouseleave (estos dos no burbujean).

    Teclado: keydown, keyup, keypress (obsoleto), con propiedades e.key, e.code.

    Formulario: submit, change, input, focus, blur, focusin, focusout (estos dos sí burbujean).

    Documento: DOMContentLoaded, load, beforeunload.

    Ventana: resize, scroll, storage (ver siguiente sección).

    Táctil: touchstart, touchmove, touchend.

### Eventos personalizados

new CustomEvent('nombre', { detail: { ... } }) y dispatchEvent permiten crear sistemas de comunicación propios.
```js
elemento.addEventListener('user-login', e => console.log(e.detail));
elemento.dispatchEvent(new CustomEvent('user-login', { detail: { id: 1 } }));
```

### Buenas prácticas

    Usa delegación siempre que puedas.

    Prefiere e.preventDefault() sobre return false (que además detiene propagación).

    Remueve listeners cuando ya no sean necesarios para evitar memory leaks.

    Para scroll y resize, usa { passive: true } para mejorar el rendimiento.

---

## Archivo: `04-web-storage.md`


El almacenamiento web permite guardar datos en el navegador de forma sencilla, sin cookies y con mayor capacidad.
localStorage

    Almacenamiento persistente: los datos sobreviven cierres del navegador y reinicios.

    Espacio típico: ~5-10 MB por origen.

    API síncrona y sencilla.

```js
// Guardar
localStorage.setItem('usuario', JSON.stringify({ nombre: 'Ana' }));
// Leer
const usuario = JSON.parse(localStorage.getItem('usuario'));
// Eliminar uno
localStorage.removeItem('usuario');
// Limpiar todo
localStorage.clear();
// Iterar
for (let i = 0; i < localStorage.length; i++) {
  const clave = localStorage.key(i);
  const valor = localStorage.getItem(clave);
}
```

    Solo almacena strings. Para objetos usa JSON.stringify/parse.

    Acceso por origen (protocolo + dominio + puerto).

    Las operaciones son síncronas, no bloquean significativamente porque leen/escriben en disco rápido. Para grandes cantidades puede bloquear, mejor usar IndexedDB.

### sessionStorage

Idéntico a localStorage en API, pero los datos se eliminan al cerrar la pestaña o ventana. Cada pestaña tiene su propio almacenamiento aislado (incluso si comparten origen).

Útil para datos de sesión, como formularios temporales, pasos de wizard, etc.
Evento storage

Se dispara en todas las demás pestañas/orígenes (no en la que realizó el cambio) cuando localStorage o sessionStorage es modificado. Permite sincronizar estado entre pestañas.
```js
window.addEventListener('storage', (e) => {
  console.log(`Clave ${e.key} cambió de ${e.oldValue} a ${e.newValue}`);
  console.log('Origen:', e.url);
});
```

sstorageArea distingue si el cambio fue en localStorage o sessionStorage.
Capacidades y límites

    Almacenamiento por origen (~5-10MB, variable).

    Exceder el límite lanza QuotaExceededError.

    No apto para datos sensibles (no está cifrado, XSS puede acceder).

    No es un sustituto de bases de datos, para datos estructurados complejos usar IndexedDB.

    No bloquea el hilo en exceso pero puede ralentizar si se abusa.

### Buenas prácticas

    Siempre usar JSON.stringify y JSON.parse.

    Capturar excepciones de cuota (try/catch).

    Prefijar las claves para evitar colisiones.

    No almacenar tokens de sesión o información sensible; preferir cookies HttpOnly y Secure.

    Para datos que cambian muy frecuentemente, considerar usar en memoria y persistir solo ocasionalmente.

### Cookies vs Web Storage
Característica	Cookies	Web Storage
Capacidad	~4KB	~5-10MB
Envío al servidor	Sí (automático en cada petición)	No (solo accesible por JS)
Persistencia	Configurable (expira)	localStorage persiste, sessionStorage no
Accesibilidad	document.cookie	API sencilla

Para estado de interfaz y datos no críticos, web storage es ideal.

### 09-módulos
---

## Archivo: `01-es6-modules.md`


Los módulos ES6 (ECMAScript 2015) son el sistema de módulos nativo de js. Permiten encapsular código, exportar e importar funcionalidades y cargar dependencias de forma declarativa.
Conceptos básicos

    Cada archivo .js que use import/export es un módulo.

    Los módulos se ejecutan en modo estricto automáticamente.

    El ámbito de un módulo es propio: las variables, funciones y clases definidas no se filtran al ámbito global a menos que se exporten y se importen expresamente.

    Los módulos se cargan de forma asíncrona y diferida (como <script type="module">), lo que evita bloqueos del HTML.

### Exportaciones

Se puede exportar cualquier declaración (variables, funciones, clases) o valores directamente.
Exportaciones nombradas (named exports)

Permiten exportar varias cosas desde un módulo.
```js
// matematicas.js
export const PI = 3.1416;
export function suma(a, b) { return a + b; }
export class Calculadora { /* ... */ }
```

También se puede exportar al final con una sola sentencia:
```js
const PI = 3.1416;
function suma(a, b) { return a + b; }
export { PI, suma };
```

Se pueden renombrar con as:
```js
export { suma as sumar };
```

### Exportación por defecto (default export)

Un módulo puede tener una única exportación por defecto. Se suele usar para exportar la entidad principal del módulo (una función, una clase, un objeto).
```js
// calculadora.js
export default class Calculadora {
  // ...
}
// o bien:
// export { Calculadora as default };
```

También se puede exportar una función anónima o un valor directamente:
```js
export default function() { /* ... */ }
```

No se debe abusar de las exportaciones por defecto; tienden a hacer menos explícita la importación.
Importaciones
Importación nombrada
```js
import { PI, suma, Calculadora } from './matematicas.js';

    Las rutas deben ser completas (incluyendo extensión) en muchos entornos (navegador, Deno). En Node con módulos ES se puede omitir .js si el empaquetador lo resuelve.
```

    Los nombres deben coincidir con los exportados, a menos que se use alias:

```js
import { suma as add } from './matematicas.js';
```

### Importación por defecto
```js
import Calculadora from './calculadora.js';
```

Puede tener cualquier nombre (no está ligado sintácticamente).
Importación combinada
```js
import React, { useState, useEffect } from 'react';
```

### Importación de todo el módulo (namespace)
```js
import * as Mat from './matematicas.js';
console.log(Mat.PI, Mat.suma(2,3));
```

Crea un objeto módulo con todas las exportaciones nombradas (no incluye la exportación por defecto, o la incluye como .default).
Importación solo para efectos secundarios
```js
import './estilos.css'; // ejecuta el módulo sin importar nada
```

Se usa para cargar CSS, polyfills o configurar librerías.
Ejecución de módulos

    Las importaciones son estáticas: el motor resuelve todas las dependencias en tiempo de compilación (no se puede usar import dentro de condicionales).

    Para importación dinámica existe la función import().

    Los módulos se evalúan solo la primera vez que se importan; las exportaciones son enlazadas (no copiadas): si el módulo exporta una variable y la modifica internamente, los importadores ven el nuevo valor (referencia viva, solo para exportaciones nombradas).

### import() dinámico

Devuelve una promesa del módulo completo. Permite cargar módulos bajo demanda (code splitting).
```js
const modulo = await import('./utilidades.js');
modulo.funcion();
```

Se puede usar en cualquier contexto, no solo en el nivel superior. Es común en SPA para lazy loading de rutas.
Compatibilidad en navegadores

Para usar módulos en un HTML:
```html
<script type="module" src="app.js"></script>
```

Los módulos se cargan con CORS, así que no funcionan desde file:// (necesitan un servidor). Se pueden usar importmap para controlar la resolución de módulos.
Tree shaking y agrupadores

Los bundlers (Webpack, Vite, Rollup) analizan las importaciones estáticas para eliminar código no usado (tree shaking). Por eso las exportaciones nombradas suelen facilitar este proceso.
Buenas prácticas

    Prefiere exportaciones nombradas para APIs claras.

    Usa default solo para componentes principales (un componente React, por ejemplo).

    Mantén los módulos pequeños y cohesivos.

    No mezcles lógica y efectos secundarios; los módulos con efectos secundarios dificultan el testing y el tree-shaking.

---

## Archivo: `02-commonjs.md`


CommonJS (CJS) es el sistema de módulos utilizado históricamente por Node.js (y otros entornos como Electron, Webpack, etc.). Es síncrono y está pensado para cargas en el servidor.
Exportar con module.exports y exports

En cada archivo CJS, las variables module, exports, require y __filename, __dirname están inyectadas.

    module.exports es el objeto (o valor) que realmente se exporta.

    exports es una referencia a module.exports; si se reasigna exports = {}, se rompe la referencia y no se exporta nada. Para exportar varias cosas, se asignan propiedades: exports.foo = ... o se usa directamente module.exports.

```js
// matematicas.cjs
function suma(a, b) { return a + b; }
const PI = 3.1416;
module.exports = { suma, PI };
```

También se puede exportar una sola función:
```js
// calculadora.cjs
class Calculadora {}
module.exports = Calculadora;
```

### Importar con require()
```js
const mate = require('./matematicas.cjs');
console.log(mate.suma(2,3));

    require es una función síncrona que devuelve el valor de module.exports del módulo requerido.
```

    El módulo se evalúa y cachea: una misma referencia devuelta en subsecuentes require.

    Las extensiones .js, .json y .node se resuelven automáticamente.

    Se pueden requerir directorios con un archivo index.js dentro.

### Carga cíclica

CommonJS maneja dependencias circulares devolviendo el objeto module.exports en el estado que tenga hasta ese momento (parcialmente cargado). Esto puede causar comportamientos inesperados; es mejor evitar ciclos.
Diferencias con ES Modules
Característica	CJS	ESM
Carga	Síncrona	Asíncrona (estática) / Dinámica con import()
Sintaxis	require / module.exports	import / export
Resolución en Node	Extensiones automáticas	Debe especificar extensión (si no se usa paquete)
Modo estricto	No por defecto	Sí, automático
Tree shaking	Difícil	Soportado nativamente
this en top-level	apunta a exports	undefined
Temporalidad	En tiempo de ejecución	Estática (salvo dinámica)
Interoperabilidad

Node.js permite importar módulos CJS desde ESM usando:
```js
import mod from 'modulo-cjs'; // toma el default export de CJS
import { nombrado } from 'modulo-cjs'; // falla si no se ha exportado nombrado explícitamente
```

Para importar ESM desde CJS se puede usar import() dinámica (asíncrono). No se puede usar require para módulos ESM.
¿Cuándo usar cada uno?

    Nuevos proyectos en Node: preferir ESM ("type": "module" en package.json).

    Proyectos legacy: CJS. Muchos paquetes npm aún distribuyen CJS.

    Bibliotecas: conviene publicar dual CJS/ESM para máxima compatibilidad.

### 10-apis-web
---

## Archivo: `01-history-api.md`


La History API permite manipular el historial del navegador sin recargar la página, base de las SPA (Single Page Applications) para el enrutamiento del lado del cliente.
Objeto window.history

Proporciona métodos para navegar y modificar la pila de historial.
history.back(), history.forward(), history.go()

    history.back(): equivale a presionar el botón atrás.

    history.forward(): botón adelante.

    history.go(delta): -1 atrás, 1 adelante, 0 recarga la página actual.

### history.pushState(state, title, url)

Añade una nueva entrada al historial y cambia la URL en la barra de direcciones sin recargar la página. Es el núcleo del enrutamiento moderno.
```js
const nuevoEstado = { page: 'about', userId: 42 };
history.pushState(nuevoEstado, '', '/about');

    state: objeto js asociado a la entrada del historial (hasta 640KB por entrada en la mayoría de navegadores). Se recupera luego con history.state o en el evento popstate.

    title: actualmente ignorado por la mayoría de navegadores, se pasa string vacío.

    url: nueva URL (mismo origen). El navegador no verifica que exista el recurso; solo se actualiza la barra.
```

### history.replaceState(state, title, url)

Similar a pushState pero reemplaza la entrada actual del historial en lugar de añadir una nueva. Útil para corregir la URL sin generar historial adicional (ej. al redirigir después de login).
Evento popstate

Se dispara en window cuando el usuario navega por el historial (atrás/adelante). No se dispara con pushState o replaceState.
```js
window.addEventListener('popstate', (event) => {
  if (event.state) {
    // restaurar la vista según event.state
    console.log('Volviendo a estado:', event.state);
  }
});
```

En el manejador, location.pathname ya se ha actualizado; podemos leer la ruta y renderizar el contenido correspondiente.
Integración con SPA

Un enrutador cliente típico:

    Intercepta clics en enlaces internos, llama a pushState y renderiza la vista.

    Escucha popstate para navegación hacia atrás.

    En carga inicial (o refresco), el servidor debe responder con el HTML base y el enrutador cliente toma el control.

### Seguridad y restricciones

    La nueva URL debe ser del mismo origen; de lo contrario lanza una excepción.

    El estado se serializa mediante la API de Structured Clone (soporta objetos, arrays, etc., pero no funciones, DOM nodes).

    El estado no persiste tras cerrar la pestaña (a diferencia de sessionStorage).

---

## Archivo: `02-clipboard.md`


La Clipboard API permite leer y escribir en el portapapeles del sistema de forma asíncrona y segura, reemplazando al antiguo document.execCommand('copy').
Escritura en portapapeles
```js
await navigator.clipboard.writeText('Texto a copiar');
```

O para datos binarios:
```js
const blob = new Blob(['<h1>HTML</h1>'], { type: 'text/html' });
const item = new ClipboardItem({ 'text/html': blob });
await navigator.clipboard.write([item]);
```

ClipboardItem permite múltiples representaciones (texto plano + HTML, por ejemplo) para que el destino pegue la que prefiera.
Lectura del portapapeles
```js
const texto = await navigator.clipboard.readText();
```

Para leer otros formatos:
```js
const items = await navigator.clipboard.read();
for (const item of items) {
  for (const type of item.types) {
    const blob = await item.getType(type);
    // procesar blob (texto, imagen, etc.)
  }
}
```

### Permisos y seguridad

    La escritura requiere interacción del usuario (clic, tecla) o permiso clipboard-write. En páginas seguras (HTTPS) normalmente se concede implícitamente en respuesta a un gesto del usuario.

    La lectura requiere el permiso clipboard-read, solicitado con la API Permissions:

```js
const permiso = await navigator.permissions.query({ name: 'clipboard-read' });
if (permiso.state === 'granted' || permiso.state === 'prompt') {
  const texto = await navigator.clipboard.readText();
}

    Ambas requieren contexto seguro (HTTPS o localhost).
```

### Eventos copy, cut, paste

Se pueden interceptar en el documento para modificar los datos que se copian o pegan. Ejemplo para añadir información extra al copiar:
```js
document.addEventListener('copy', (e) => {
  e.preventDefault();
  const seleccion = document.getSelection().toString();
  e.clipboardData.setData('text/plain', seleccion + '\n\nFuente: mi web');
});
```

### Consideraciones

    La API asíncrona no está disponible en todos los navegadores antiguos.

    Siempre manejar excepciones: el acceso puede ser denegado.

    No dependas de que el portapapeles esté accesible; ofrece alternativas.

---

## Archivo: `03-geolocation.md`


La Geolocation API permite obtener la ubicación del dispositivo con el consentimiento del usuario.
Objeto navigator.geolocation

Disponible solo en contextos seguros (HTTPS). Métodos principales:
getCurrentPosition(success, error?, options?)

Obtiene la posición una sola vez.
```js
navigator.geolocation.getCurrentPosition(
  (position) => {
    console.log(position.coords.latitude, position.coords.longitude);
  },
  (error) => {
    console.error('Error:', error.message);
  },
  { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
);
```

Propiedades del objeto position.coords:

### latitude, longitude (grados decimales)

### accuracy (metros), altitude, altitudeAccuracy, heading, speed

### watchPosition(success, error?, options?)

Registra un vigilante que llama al callback cada vez que la posición cambia. Devuelve un watchId.
clearWatch(watchId)

Detiene el seguimiento iniciado con watchPosition.
Opciones

    enableHighAccuracy: booleano, solicita GPS más preciso (puede consumir más batería).

    timeout: ms máximos para obtener posición.

    maximumAge: tiempo máximo en ms de una caché permitida (0 = siempre nueva).

### Errores

El callback de error recibe un objeto GeolocationPositionError con:

    code: 1 (PERMISSION_DENIED), 2 (POSITION_UNAVAILABLE), 3 (TIMEOUT).

    message: texto descriptivo.

### Permisos

El navegador pide permiso explícito al usuario. Con la API Permissions se puede consultar el estado (pero no se puede solicitar programáticamente sin un gesto del usuario previo).
Limitaciones

    Solo funciona en HTTPS.

    La precisión varía (GPS en exteriores, WiFi/móvil en interiores).

    No disponible en todos los dispositivos (siempre verificar if ('geolocation' in navigator)).

### Casos de uso

    Mapas y servicios basados en localización.

    Búsqueda de lugares cercanos.

    Registro de rutas.

---

## Archivo: `04-canvas-basico.md`


El elemento <canvas> proporciona un área de dibujo de píxeles mediante scripts (API de Canvas 2D, WebGL para 3D). Aquí veremos los fundamentos del contexto 2D.
Obtener el contexto
```html
<canvas id="lienzo" width="400" height="300"></canvas>
```

```js
const canvas = document.getElementById('lienzo');
const ctx = canvas.getContext('2d');
```

### Dibujo de formas

    Rectángulos:

        fillRect(x, y, width, height): rectángulo relleno.

        strokeRect(x, y, w, h): rectángulo contorneado.

        clearRect(x, y, w, h): borra píxeles.

    Caminos (paths):
```js
    ctx.beginPath();
    ctx.moveTo(50, 50);
    ctx.lineTo(100, 100);
    ctx.lineTo(50, 100);
    ctx.closePath(); // cierra la figura
    ctx.stroke(); // dibuja la línea
    ctx.fill(); // rellena el interior
```

    Arcos/círculos:
    ctx.arc(x, y, radius, startAngle, endAngle, anticlockwise?).
    Ángulos en radianes. Ej: ctx.arc(100, 100, 50, 0, Math.PI * 2).

### Estilos de trazo y relleno

### ctx.fillStyle = 'red' | '#00FF00' | 'rgba(...)' | gradiente | patrón

    ctx.strokeStyle = ...

### ctx.lineWidth = 5

### ctx.lineCap, ctx.lineJoin

### Gradientes y patrones

    Lineal: const grad = ctx.createLinearGradient(x0,y0, x1,y1); grad.addColorStop(0, 'white'); grad.addColorStop(1, 'black');

### Radial: ctx.createRadialGradient(x0,y0,r0, x1,y1,r1)

### Patrón: ctx.createPattern(imagen, 'repeat')

### Texto

### ctx.font = '20px Arial'

### ctx.fillText('texto', x, y) (relleno)

### ctx.strokeText('texto', x, y) (contorno)

### ctx.textAlign, ctx.textBaseline

### Transformaciones

    ctx.translate(x, y): desplaza el origen.

    ctx.rotate(rad): rota el lienzo.

    ctx.scale(sx, sy): escala.

    ctx.save() y ctx.restore(): apilan y restauran el estado (transformaciones, estilos).

### Imágenes
```js
const img = new Image();
img.onload = () => ctx.drawImage(img, x, y, width?, height?);
img.src = 'ruta.png';
```

También se puede recortar con drawImage(img, sx, sy, sw, sh, dx, dy, dw, dh).
Animaciones

Canvas no mantiene estado entre fotogramas; hay que redibujar todo en cada frame. Típico bucle:
```js
function animar() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // actualizar y dibujar
  requestAnimationFrame(animar);
}
animar();
```

### Pixel manipulation

ctx.getImageData(x,y,w,h) devuelve un objeto ImageData con .data (Uint8ClampedArray en formato RGBA). Permite leer y escribir píxeles directamente. ctx.putImageData(imageData, x, y) para escribir.
Buenas prácticas

    Especificar width y height en el elemento o en js; no modificar con CSS (distorsiona).

    Limpiar el lienzo al inicio de cada frame.

    Usar requestAnimationFrame para animaciones suaves.

    Para gráficos complejos, considerar librerías como Fabric.js, PixiJS, Konva.

### 11-conceptos-avanzados
---

## Archivo: `01-closures-aplicados.md`


Ya cubrimos closures en fundamentos. Aquí profundizamos con patrones avanzados.
Módulo revelador clásico

Antes de ES6 se usaban closures para encapsular estado:
```js
const contador = (function() {
  let cuenta = 0;
  return {
    incrementar: () => ++cuenta,
    valor: () => cuenta
  };
})();
contador.incrementar();
console.log(contador.valor()); // 1
console.log(contador.cuenta); // undefined
```

### Fábricas de funciones

Crean funciones especializadas basadas en configuración:
```js
function crearMultiplicador(factor) {
  return (n) => n * factor;
}
const duplicar = crearMultiplicador(2);
duplicar(5); // 10
```

### Caché y memoización

Los closures permiten almacenar resultados previos para evitar cálculos repetidos.
```js
function memoizar(fn) {
  const cache = {};
  return function(...args) {
    const key = JSON.stringify(args);
    if (key in cache) return cache[key];
    const resultado = fn(...args);
    cache[key] = resultado;
    return resultado;
  };
}
const fibonacciMemo = memoizar((n) => {
  if (n <= 1) return n;
  return fibonacciMemo(n-1) + fibonacciMemo(n-2);
});
```

### Simulación de variables privadas en clases ES6

Antes de los campos #, los closures permitían privacidad:
```js
function crearPersona(nombre) {
  let _edad = 0; // privada
  return {
    getEdad: () => _edad,
    cumplirAños: () => _edad++
  };
}
```

### Temporizadores y closures

Clásico problema del for con var. Los closures permiten capturar el valor en cada iteración (aunque con let ya no es necesario).
```js
for (var i = 0; i < 3; i++) {
  ((indice) => {
    setTimeout(() => console.log(indice), 100);
  })(i);
}
```

### Manejadores de eventos con estado

Un closure puede mantener estado entre eventos sin variables globales.
```js
function crearManejador() {
  let contador = 0;
  return () => console.log(`Click #${++contador}`);
}
document.getElementById('btn').addEventListener('click', crearManejador());
```

### Posibles desventajas

    Pueden retener referencias grandes y causar fugas de memoria si no se limpian.

    Dificultan el testing si el estado no es accesible.

---

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

## Archivo: `03-proxy-y-reflect.md`

Proxy

Permite interceptar y redefinir operaciones fundamentales sobre un objeto (get, set, delete, has, enumerate, construct, apply...). Se crea con new Proxy(target, handler).
```js
const persona = { nombre: 'Ana', edad: 28 };
const manejador = {
  get(target, prop) {
    if (prop === 'edad') return `${target.edad} años`;
    return Reflect.get(target, prop);
  },
  set(target, prop, valor) {
    if (prop === 'edad' && valor < 0) throw new Error('Edad no válida');
    target[prop] = valor;
    return true;
  }
};
const proxy = new Proxy(persona, manejador);
console.log(proxy.edad); // '28 años'
proxy.edad = -5; // lanza Error
```

### Métodos interceptables (trampas)

    get, set, deleteProperty, has (operador in), ownKeys, getOwnPropertyDescriptor, defineProperty, preventExtensions, isExtensible, apply (para funciones), construct (para new).

### Casos de uso

    Validación y saneamiento de datos.

    PropTypes en tiempo de ejecución.

    Observadores reactivos: frameworks como Vue 3 utilizan Proxy para la reactividad.

    Logging y profiling.

    APIs de objetos negativos (ej. valores por defecto: const cero = new Proxy({}, { get: (t,p) => p in t ? t[p] : 0 })).

    Virtualización de objetos (simular propiedades que no existen realmente).

### Reflect

Objeto incorporado con métodos estáticos que replican las operaciones internas del lenguaje (las mismas trampas de Proxy). Su propósito es normalizar la manipulación de objetos y proporcionar una forma segura de invocar la operación predeterminada dentro de un proxy.

    Reflect.get(obj, prop, receiver?) en lugar de obj[prop].

    Reflect.set(...), Reflect.deleteProperty, Reflect.apply, etc.

Dentro de un proxy, en lugar de target[prop] se recomienda Reflect.get(target, prop, receiver) para respetar la cadena de prototipos y posibles proxies anidados.
Relación Proxy y Reflect

Han sido diseñados para trabajar juntos; cada trampa de Proxy tiene un método correspondiente en Reflect que ejecuta el comportamiento por defecto.
```js
const manejador = {
  set(target, prop, value, receiver) {
    // alguna validación
    return Reflect.set(target, prop, value, receiver);
  }
};
```

### Precauciones

    Los proxies no son totalmente transparentes: proxy !== target, typeof, comparaciones pueden fallar.

    El rendimiento de proxies es inferior al acceso directo (aunque para la mayoría de aplicaciones es aceptable).

    No se pueden polifillar; requieren soporte nativo ES6.

---

## Archivo: `04-symbols-iteradores.md`

Symbol

Tipo de dato primitivo introducido en ES6. Cada símbolo es único e inmutable. Se crea con Symbol('descripcion'), donde la descripción es solo para depuración. Los símbolos pueden ser propiedades de objetos, evitando colisiones de nombres.
```js
const id = Symbol('id');
const user = { [id]: 123, nombre: 'Juan' };
console.log(user[id]); // 123
Object.keys(user); // ['nombre'] — no incluye símbolos
Object.getOwnPropertySymbols(user); // [Symbol(id)]
```

### Símbolos conocidos (Well-known Symbols)

Son propiedades estáticas de Symbol que representan protocolos internos del lenguaje. Permiten personalizar comportamientos de objetos.
Symbol.iterator

Define el iterador por defecto de un objeto. Se usa en for...of, spread, Array.from, etc.
```js
const rango = {
  inicio: 1,
  fin: 5,
  [Symbol.iterator]() {
    let actual = this.inicio;
    const fin = this.fin;
    return {
      next() {
        if (actual <= fin) return { value: actual++, done: false };
        return { value: undefined, done: true };
      }
    };
  }
};
for (const n of rango) console.log(n); // 1 2 3 4 5
```

También se puede implementar como generador:
```js
*[Symbol.iterator]() {
  for (let i = this.inicio; i <= this.fin; i++) yield i;
}
```

### Symbol.asyncIterator

Define el iterador asíncrono por defecto, usado en for await...of. Retorna un objeto con next() que devuelve Promise<{value, done}>.
```js
const paginador = {
  pagina: 1,
  async *[Symbol.asyncIterator]() {
    while (this.pagina <= 3) {
      yield await fetch(`/api/pagina/${this.pagina++}`).then(r => r.json());
    }
  }
};
```

### Otros well-known symbols

    Symbol.toPrimitive: controla la conversión a primitivo (hint: 'string' | 'number' | 'default').

    Symbol.toStringTag: define el resultado de Object.prototype.toString() (ej. [object MiClase]).

    Symbol.hasInstance: personaliza el comportamiento de instanceof.

    Symbol.species: usado por constructores para determinar qué clase usar al crear objetos derivados.

    Symbol.match, Symbol.replace, Symbol.search, Symbol.split: personalizan métodos de strings con expresiones regulares.

### Iteradores y objetos array-like

Implementar Symbol.iterator convierte un objeto en iterable. Para ser array-like además debe tener length y propiedades numéricas, pero no garantiza ser iterable.
Uso práctico

    Estructuras de datos personalizadas: listas enlazadas, árboles, que soporten for...of.

    Colecciones que cargan bajo demanda (lazy evaluation).

    Integración con spread y Array.from.

---

## Archivo: `05-event-loop-profundo.md`


Ya vimos la base del event loop. Ahora exploramos la interacción precisa entre microtareas, macrotareas y el renderizado, y las implicaciones prácticas.
Orden exacto de ejecución

Ciclo típico en el navegador:

    Ejecutar una macrotarea (task): script inicial, evento UI, setTimeout, setInterval, I/O, etc.

    Vaciar completamente la cola de microtareas (promesas, queueMicrotask, MutationObserver). Si durante esto se añaden nuevas microtareas, se ejecutan también en este mismo paso.

    Rendereizar (si es necesario): el navegador puede decidir repintar la UI. No ocurre en cada vuelta, sino cuando el agente de renderizado lo considera (normalmente cada 16ms para 60fps). Se ejecutan callbacks de requestAnimationFrame antes del repintado.

    Repetir: tomar la siguiente macrotarea.

### Macrotareas adicionales

    requestAnimationFrame(rAF): su callback se ejecuta justo antes del renderizado, pero después de las microtareas. Está sincronizado con el refresco de pantalla.

    requestIdleCallback: se ejecuta cuando el hilo principal está ocioso (entre frames). Prioridad baja.

    MessageChannel y setImmediate (solo Node) también son macrotareas.

### Ejemplo con rAF y microtareas
```js
setTimeout(() => console.log('timeout'), 0);
Promise.resolve().then(() => console.log('promise'));
requestAnimationFrame(() => console.log('rAF'));
// Orden típico: promise, rAF, timeout
```

Explicación: microtareas se vacían antes del render. rAF se ejecuta antes del render. Luego viene la macrotarea setTimeout.
¿Por qué setTimeout(fn, 0) no ejecuta inmediatamente?

Porque 0 es el tiempo mínimo, pero la callback se encola como macrotarea. El browser debe terminar la tarea actual, vaciar microtareas y posiblemente renderizar antes de despachar el timeout.
Starvation de macrotareas

Si una microtarea añade continuamente nuevas microtareas (bucle infinito de promesas), las macrotareas (y el renderizado) nunca se ejecutarán, congelando la UI. Evítalo.
Node.js vs Browsers

En Node.js, el event loop tiene varias fases: timers (setTimeout/setInterval), pending callbacks, idle, poll, check (setImmediate), close. Las microtareas se ejecutan entre fases y también después de cada fase. process.nextTick en Node es una microtarea incluso más prioritaria que las promesas.
Implicaciones de rendimiento

    Para tareas intensivas, dividir el trabajo en macrotareas pequeñas (setTimeout) permite que el navegador responda al usuario entre ellas.

    requestAnimationFrame es mejor para animaciones y cambios visuales que deban sincronizarse con el refresco.

    Las microtareas son el lugar ideal para ejecutar lógica que deba completarse antes del próximo renderizado (ej. actualizar el estado).

### Depuración

Entender el orden ayuda a depurar problemas asíncronos, como por qué un setTimeout(fn, 0) se ejecuta después de una promesa.
---

## Archivo: `06-web-workers.md`


Los Web Workers permiten ejecutar código js en un hilo separado del hilo principal (UI), evitando bloqueos. Se comunican con el hilo principal mediante mensajes.
Tipos de workers

    Dedicated Worker: dedicado al script que lo crea. La comunicación es 1:1.

    Shared Worker: puede ser compartido por varias pestañas/orígenes del mismo origen. Comunicación a través de puertos.

    Service Worker: funciona como proxy de red, permite offline, notificaciones push. Sigue un ciclo de vida especial y actúa a nivel de dominio.

Aquí nos centramos en el Dedicated Worker.
Crear un worker
```js
// main.js
const worker = new Worker('worker.js');
worker.postMessage({ type: 'start', data: [1,2,3] });
```

### worker.onmessage = (e) => {
  console.log('Resultado:', e.data);
};

### worker.onerror = (e) => {
  console.error('Error en worker:', e.message);
};

### // worker.js
self.onmessage = (e) => {
  const result = e.data.data.reduce((a,b) => a+b, 0);
  self.postMessage(result);
};

### Intercambio de mensajes

    postMessage permite pasar datos que son copiados (structured clone algorithm).

    Se pueden transferir ciertos objetos (ArrayBuffer, MessagePort, ImageBitmap) mediante transferencia de propiedad (movimiento, no copia), liberando el original en el emisor. Esto se logra pasando un segundo argumento: worker.postMessage(buffer, [buffer]).

### APIs disponibles en Workers

Los workers tienen acceso limitado:

    No pueden manipular el DOM, ni acceder a window, document, parent.

    Disponen de self, importScripts() (para cargar otros scripts), fetch, XMLHttpRequest, WebSocket, IndexedDB.

    Pueden usar navigator, location (solo lectura), setTimeout/setInterval.

    Pueden crear otros workers (subworkers).

### Terminación

    worker.terminate() desde el hilo principal finaliza el worker inmediatamente.

    self.close() desde dentro del worker lo cierra.

### Casos de uso

    Operaciones de CPU intensiva: procesamiento de imágenes, cálculos matemáticos, criptografía.

    Parseo y manipulación de grandes datos (CSV, JSON).

    Simulaciones y motores de juego.

    Prefetching y procesamiento de datos en segundo plano.

### Errores y depuración

    Los errores no capturados en el worker no afectan al hilo principal; se reportan mediante onerror.

    Las herramientas de desarrollo del navegador pueden inspeccionar workers y ver sus consolas.

### Consideraciones

    La creación de muchos workers puede consumir mucha memoria; cada worker tiene su propio heap.

    La comunicación mediante serialización puede ser costosa para grandes volúmenes; usar transferencia de buffers para datos binarios.

    Para tareas pequeñas, el coste de crear un worker puede superar el beneficio; evaluar con medidas de rendimiento.

### Shared Workers y Service Workers

    Shared Workers: mismo script accedido por múltiples conexiones (pestañas). Cada conexión usa un MessagePort.

    Service Workers: actúan como proxy de red, interceptan peticiones fetch, manejan caché, notificaciones push y sincronización en fondo. Tienen ciclo de vida (instalación, activación) y requieren HTTPS.
