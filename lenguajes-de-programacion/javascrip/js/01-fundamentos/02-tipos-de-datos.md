
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
