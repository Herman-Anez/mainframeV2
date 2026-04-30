# Sintaxis y Variables: `var`, `let` y `const`

JavaScript ofrece tres formas de declarar variables. Cada una tiene reglas de ámbito, hoisting y reasignación distintas.

### Comparativa de Declaraciones

| Palabra clave | Ámbito | Hoisting | Reasignable | Redeclarable (mismo ámbito) |
| :--- | :--- | :--- | :--- | :--- |
| **`var`** | Función | Sí (inicializa como `undefined`) | Sí | Sí |
| **`let`** | Bloque `{}` | Sí (pero no se inicializa, TDZ) | Sí | No |
| **`const`** | Bloque `{}` | Sí (TDZ) | No (debe inicializarse) | No |

---

### Detalles de `var`

> [!NOTE]
> `var` es la forma tradicional de declarar variables en JavaScript, pero tiene comportamientos que pueden inducir a errores.

* **Ámbito Global:** Si se declara fuera de una función, es global y se convierte en propiedad del objeto `window` (en el navegador).
* **Redeclaración:** Las redeclaraciones son ignoradas; no lanzan error, simplemente se sobrescribe el valor.
* **Hoisting:** Su hoisting eleva la declaración y la inicializa automáticamente a `undefined`. Esto permite acceder a la variable antes de su línea de declaración, pero con valor `undefined`.

```javascript
console.log(a); // undefined
var a = 5;
```

### `let` y `const`

* **Ámbito de Bloque:** Tienen ámbito de bloque; existen solo dentro del `{}` más cercano (`if`, `for`, `while`, bloque independiente...).
* **Zona Muerta Temporal (TDZ):** Están sujetos a la TDZ desde el inicio del bloque hasta que se ejecuta la línea de declaración. Cualquier acceso previo lanza `ReferenceError`.
* **Inmutabilidad en `const`:** `const` exige inicialización en la misma sentencia. La variable no puede ser reasignada, pero si el valor es un objeto o array, sus propiedades o elementos sí pueden modificarse (la referencia es inmutable, no el contenido).
* **Gestión en Bucles:** En bucles, `let` crea un nuevo enlace para cada iteración, lo que evita problemas clásicos con closures dentro de un `for`. Con `var` se comparte el mismo enlace en todo el ámbito.

### Ámbito Léxico y *Scope Chain*

Cada función crea un nuevo ámbito; los bloques (con `let`/`const`) crean ámbitos anidados. La resolución de variables va del ámbito más interno al externo.

```javascript
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

> [!IMPORTANT]
>
> ### Buenas Prácticas
>
> * **Evitar `var`:** No usar `var` en código moderno; preferir `const` por defecto, y `let` solo si la variable va a ser reasignada.
> * **Variables Globales:** Minimizar el número de variables globales para evitar colisiones.
> * **Proximidad:** Declarar las variables lo más cerca posible de su primer uso.

---

---
[back](../index)
