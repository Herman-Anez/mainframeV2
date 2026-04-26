# Tipos de Datos

## Tipos Primitivos (7)

Los tipos primitivos son inmutables (no se pueden modificar sus valores; toda operación devuelve un nuevo valor) y se comparan por valor.

*   **`string`:** Cadenas de texto. Se pueden usar comillas simples, dobles o *backticks* (template literals).
*   **`number`:** Números en coma flotante de 64 bits (IEEE 754). Valores especiales: `NaN`, `Infinity`, `-Infinity`. No hay distinción entre entero y decimal.
    *   `NaN` es el único valor que no es igual a sí mismo (`NaN !== NaN`). Se comprueba con `Number.isNaN()`.
*   **`bigint`:** Enteros de precisión arbitraria. Se crean añadiendo `n` al final del literal (`123n`) o con `BigInt()`.
    *   No se pueden mezclar directamente con `number` en operaciones aritméticas.
*   **`boolean`:** `true` o `false`.
*   **`undefined`:** Valor que tiene una variable no inicializada o un parámetro no pasado. Debería ser el propio lenguaje quien lo asigna, no forzarlo manualmente.
*   **`null`:** Representa la ausencia intencionada de valor. Se asigna explícitamente. `typeof null` devuelve por error histórico `"object"`.
*   **`symbol`:** Valor único e inmutable, usado como identificador de propiedades de objeto. Creado con `Symbol('descripcion')`. No se convierten automáticamente a `string`.

---

### `typeof` y sus trampas

> [!WARNING]
> El operador `typeof` tiene comportamientos heredados que pueden ser confusos.

| Expresión | Resultado | Nota |
| :--- | :--- | :--- |
| `typeof null` | `"object"` | Bug histórico del lenguaje. |
| `typeof NaN` | `"number"` | `NaN` es técnicamente un número "No Numérico". |
| `typeof function(){}` | `"function"` | Aunque las funciones son objetos. |
| `typeof []` | `"object"` | Para detectar arrays, usar `Array.isArray()`. |

---

## Tipos de Referencia (Objetos)

Los objetos son colecciones de propiedades y se comparan por referencia (dos objetos distintos con el mismo contenido no son iguales). Son mutables por defecto.

*   **Object:** literal `{}`, `new Object()`.
*   **Array:** `[]`, `new Array()`.
*   **Function:** cualquier función.
*   **Otros:** `Date`, `RegExp`, `Map`, `Set`, etc.

> [!IMPORTANT]
> La asignación de objetos copia la **referencia**, no el valor.
> *   **Copia Superficial:** Se usa el operador *spread* (`...`) o `Object.assign`.
> *   **Copia Profunda:** Se recomienda `structuredClone()` (moderno) o `JSON.parse(JSON.stringify(...))` (con limitaciones).

---

### *Wrappers* Primitivos

Al acceder a una propiedad de un primitivo como `"hola".length`, JavaScript crea temporalmente un objeto `String`, ejecuta la operación y lo descarta. Por eso no se pueden añadir propiedades a los primitivos.

### Coerción Implícita de Tipos (Vista Rápida)

Los operadores y las comparaciones pueden disparar conversiones automáticas. Se detallará en el siguiente apartado.

---


---
[back](../index)
