
# Modo Estricto (`"use strict"`)

## ¿Qué es?

El modo estricto es una funcionalidad que permite ejecutar JavaScript bajo un conjunto de restricciones más rigurosas. Su objetivo es corregir malas prácticas comunes y convertir errores que antes fallaban silenciosamente en excepciones explícitas.

## Activación

*   **A nivel de script:** Añadir `"use strict";` al principio del archivo (antes de cualquier otra sentencia).
*   **A nivel de función:** Colocar la directiva dentro de una función, justo al inicio del cuerpo.

> [!NOTE]
> Los **módulos de ES6** y las **clases** siempre se ejecutan en modo estricto de forma automática; no es necesario declararlo explícitamente en estos casos.

---

## Cambios Principales

### 1. Prohibición de variables globales implícitas
Asignar un valor a una variable no declarada lanza un `ReferenceError` en lugar de crear una variable global accidentalmente.

```javascript
"use strict";
x = 5; // ReferenceError: x is not defined
```

### 2. Comportamiento de `this`
Elimina la coerción de `this` al objeto global. En una función normal invocada sin contexto, `this` será `undefined` en lugar de `window` o `global`.

```javascript
"use strict";
function normal() {
  return this;
}
console.log(normal()); // undefined
```

### 3. Parámetros duplicados
Prohíbe el uso de parámetros con el mismo nombre en la declaración de una función.

```javascript
"use strict";
function suma(a, a, b) { // SyntaxError
  return a + a + b;
}
```

### 4. Restricciones con `delete`
Bloquea el intento de eliminar variables, funciones o argumentos mediante el operador `delete` (lo cual antes fallaba de forma silenciosa).

```javascript
"use strict";
var x = 1;
delete x; // SyntaxError: Delete of an unqualified identifier in strict mode.
```

### 5. Otras restricciones técnicas
*   **Literales Octales:** Prohíbe el uso de octales antiguos (ej. `010`). Se debe usar el formato moderno `0o10`.
*   **`eval` y `arguments`:** Impide que estas palabras se usen como nombres de variable o parámetros. Además, `eval` no puede introducir variables nuevas en el ámbito que lo rodea.
*   **Seguridad de Objetos:** Lanza un error al intentar escribir en propiedades de solo lectura o en objetos no extensibles.

---

## Consecuencias Prácticas

*   **Seguridad:** Previene fugas accidentales al objeto global.
*   **Predictibilidad:** Obliga a una declaración de variables correcta y explícita.
*   **Depuración:** Facilita la detección de errores al lanzar excepciones inmediatas.

> [!IMPORTANT]
> **¿Cuándo usarlo?**
> La recomendación es usarlo **siempre**. Aunque herramientas modernas como ESLint o TypeScript ya incorporan estas reglas, y los módulos ES lo activan por defecto, mantener la costumbre de usarlo en scripts clásicos garantiza un código más robusto y profesional.

---