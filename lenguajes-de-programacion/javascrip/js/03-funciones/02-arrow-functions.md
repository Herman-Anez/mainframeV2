# Arrow Functions (Funciones Flecha)

Las *arrow functions*, introducidas en ES6 (ECMAScript 2015), ofrecen una sintaxis más concisa y un comportamiento especial en relación al contexto de ejecución (`this`).

---

## 1. Sintaxis

```javascript
// Sin parámetros: paréntesis vacíos obligatorios
const uno = () => 1;

// Un solo parámetro: paréntesis opcionales
const doble = x => x * 2;

// Múltiples parámetros: paréntesis obligatorios
const suma = (a, b) => a + b;

// Cuerpo con bloque: requiere llaves y return explícito
const saludar = (nombre) => {
  const mensaje = `Hola ${nombre}`;
  return mensaje;
};

// Retornar un objeto literal: envolver entre paréntesis
const crearUsuario = (nombre) => ({ nombre, id: Date.now() });
```

---

## 2. Características Clave

*   **`this` Léxico:** No tienen su propio `this`. Heredan el `this` del ámbito léxico en el que fueron definidas.
*   **No Constructoras:** No se pueden usar con el operador `new`. Lanzarán un error si se intenta.
*   **Sin Objeto `arguments`:** No tienen su propio objeto `arguments`. Acceden al de la función externa más cercana. Se recomienda usar parámetros *rest* (`...args`).
*   **Sin Propiedad `prototype`:** Al no ser constructoras, carecen de esta propiedad.
*   **No Generadores:** No pueden ser usadas como funciones generadoras (no admiten `yield`).
*   **Return Implícito:** Si el cuerpo es una única expresión, se pueden omitir las llaves y la palabra clave `return`.

---

## 3. Comportamiento de `this`

El comportamiento del `this` es la diferencia más significativa respecto a las funciones tradicionales.

```javascript
const obj = {
  nombre: 'Ana',
  saludarNormal: function() {
    setTimeout(function() {
      console.log(this.nombre); // undefined (this apunta al objeto global/window)
    }, 100);
  },
  saludarArrow: function() {
    setTimeout(() => {
      console.log(this.nombre); // 'Ana' (this heredado del contexto de obj)
    }, 100);
  }
};
```

> [!NOTE]
> En `saludarNormal`, la función dentro de `setTimeout` pierde el contexto. En `saludarArrow`, la flecha captura el `this` de su entorno (el método `saludarArrow` cuyo `this` es `obj`).

---

## 4. Cuándo No Usar Arrow Functions

> [!WARNING]
> Evita el uso de funciones flecha en los siguientes escenarios:
> 1.  **Métodos de Objetos:** Si necesitas que `this` haga referencia al propio objeto.
> 2.  **Funciones Constructoras:** No funcionan con `new`.
> 3.  **Prototipos:** Al definir métodos en `prototype` que dependan del contexto de la instancia.
> 4.  **Uso de `arguments`:** Si dependes estrictamente de este objeto en lugar de parámetros *rest*.

---

## Resumen

Las *arrow functions* simplifican enormemente los *callbacks* y el código funcional, resolviendo el problema histórico del `this` en contextos asíncronos. Son la elección ideal para funciones cortas, puras y de transformación de datos.

---
---
[back](../index)
