# Declaración vs. Expresión de Funciones

Las funciones en JavaScript se pueden definir de dos formas principales: mediante declaración y mediante expresión. Ambas crean objetos de tipo `function`, pero se comportan de manera diferente en cuanto al **hoisting** y al momento en que están disponibles en el ciclo de ejecución.

---

## 1. Declaración de Función (Function Declaration)

Una declaración de función define una función con los parámetros especificados.

```javascript
function saludar(nombre) {
  return `Hola, ${nombre}`;
}
```

### Características Principales

*   **Hoisting:** La declaración completa (nombre y cuerpo) se eleva al inicio del ámbito. Esto permite llamar a la función antes de su línea de definición sin errores.
*   **Nombre Obligatorio:** Debe tener un identificador obligatoriamente.
*   **Ámbito:** Puede ser utilizada en cualquier lugar dentro del ámbito en que se declaró.

> [!IMPORTANT]
> En bloques `if` o bucles, su comportamiento puede ser inconsistente en modo no estricto. En modo estricto (`"use strict"`), el ámbito de bloque se respeta correctamente.

### Ejemplo de Hoisting
```javascript
console.log(suma(3, 4)); // Output: 7 (funciona por hoisting)

function suma(a, b) {
  return a + b;
}
```

---

## 2. Expresión de Función (Function Expression)

Se produce cuando se asigna una función (anónima o con nombre) a una variable o constante.

```javascript
const despedir = function(nombre) {
  return `Adiós, ${nombre}`;
};
```

### Características Principales

*   **Sin Hoisting de Valor:** La variable se eleva según su declaración (`var`, `let`, `const`), pero la asignación de la función no ocurre hasta que se ejecuta la línea.
*   **Acceso Restringido:** No se puede invocar antes de la línea de asignación. Con `let`/`const` se produce un `ReferenceError` debido a la Zona Muerta Temporal (TDZ).
*   **Anonimato:** La función puede ser anónima. Si es nombrada, el nombre solo es visible dentro del cuerpo de la función.

```javascript
// console.log(multiplicar); // undefined (si es var) o ReferenceError (si es let/const)
// multiplicar(5, 5);       // Error: multiplicar is not a function

var multiplicar = function(a, b) {
  return a * b;
};
```

---

## 3. Expresión de Función Nombrada (Named Function Expression)

Es una expresión de función donde se le asigna un nombre interno a la función.

```javascript
const factorial = function fact(n) {
  return n <= 1 ? 1 : n * fact(n - 1);
};

// console.log(fact); // ReferenceError: fact is not defined (fuera de la función)
```

> [!TIP]
> **Ventaja:** El nombre `fact` solo existe dentro del cuerpo, lo que facilita la recursión y mejora la depuración, ya que el nombre aparecerá en los *stack traces*.

---

## 4. Comparativa Rápida

| Característica | Declaración | Expresión |
| :--- | :--- | :--- |
| **Hoisting** | Sí (cuerpo completo) | Solo la variable (si es `var`) |
| **Disponibilidad** | Antes de su línea | Después de la asignación |
| **Puede ser anónima** | No | Sí |
| **Ámbito en bloques** | Según contexto (evitar sin `strict`) | Respetado (bloque) |

---

## Recomendaciones

> [!NOTE]
> *   Usa **declaraciones** para funciones utilitarias que se usan en cualquier parte del módulo.
> *   Prefiere **expresiones** asignadas a `const` para evitar redeclaraciones accidentales y forzar un flujo de código más predecible (definir antes de usar).

---
