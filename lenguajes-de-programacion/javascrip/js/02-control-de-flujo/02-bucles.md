
# Estructuras de Control: Bucles e Iteración

## Bucle `for` Clásico

Es la estructura de repetición más común cuando se conoce de antemano el número de iteraciones.

```javascript
for (inicialización; condición; expresión final) {
  // cuerpo del bucle
}
```

*   **Flexibilidad:** Se puede omitir cualquiera de las tres partes (por ejemplo, `for(;;)` crea un bucle infinito).
*   **Ámbito:** Las variables declaradas con `var` comparten ámbito; con `let` se crea un nuevo enlace en cada iteración, lo cual es fundamental al trabajar con *closures*.

---

## `while` y `do...while`

*   **`while`:** Evalúa la condición **antes** de cada iteración. Es posible que el cuerpo no se ejecute nunca si la condición es falsa desde el inicio.
*   **`do...while`:** Ejecuta el cuerpo **al menos una vez** y luego evalúa la condición para decidir si continúa.

```javascript
while (hayDatos()) {
  procesar();
}

do {
  intentar();
} while (reintentar);
```

---

## `for...in`

Recorre las **claves enumerables** de un objeto, incluyendo aquellas heredadas a través de la cadena de prototipos.

```javascript
for (const key in objeto) {
  if (Object.hasOwn(objeto, key)) {
    console.log(key, objeto[key]);
  }
}
```

> [!WARNING]
> **No usar para arrays.** `for...in` recorre los índices como cadenas de texto (`strings`) y puede incluir propiedades adicionales añadidas al prototipo, lo que genera resultados inesperados.
> *   El orden de iteración no está garantizado para propiedades no numéricas.
> *   Se recomienda filtrar siempre con `Object.hasOwn()` para evitar propiedades heredadas.

---

## `for...of`

Introducido en ES6, recorre los **valores** de un objeto iterable (arrays, strings, Map, Set, generadores, NodeList, etc.).

```javascript
for (const valor of iterable) {
  console.log(valor);
}
```

*   **Orden:** Respeta el orden natural del iterable.
*   **Objetos Planos:** No funciona sobre objetos planos (`{}`) a menos que implementen `Symbol.iterator`.
*   **Índices:** Es ideal para arrays cuando no se necesita el índice, aunque se puede combinar con `.entries()` si es necesario: `for (const [i, v] of arr.entries())`.

---

## Control de Flujo: `break` y `continue`

*   **`break`:** Termina inmediatamente la ejecución del bucle.
*   **`continue`:** Salta el resto del cuerpo y pasa directamente a la siguiente iteración.

> [!NOTE]
> Ambos afectan al bucle más cercano. Se pueden usar **etiquetas** (*labels*) para controlar bucles anidados exteriores.

```javascript
exterior: for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    if (i === j) continue exterior; // Salta a la siguiente iteración del bucle 'i'
    console.log(i, j);
  }
}
```

---

> [!TIP]
> ### Buenas Prácticas
> 
> *   **Preferencia:** Preferir `for...of` o métodos funcionales (`.forEach`, `.map`) para arrays sobre el `for` clásico.
> *   **Objetos:** Para iterar objetos, es mejor usar `Object.keys()`, `Object.values()` o `Object.entries()` junto con `for...of`.
> *   **Mutación:** Tener precaución al modificar la longitud de un array mientras se itera con un `for` clásico para evitar saltos de elementos o bucles infinitos.

---


---
[back](../index)
