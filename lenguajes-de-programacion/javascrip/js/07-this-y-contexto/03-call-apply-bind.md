# `call`, `apply` y `bind`

Estos tres métodos, pertenecientes a `Function.prototype`, permiten controlar explícitamente el valor de `this` en una función y proveen mecanismos para "prestar" funciones entre diferentes objetos.

---

## .call(): Invocación con Lista de Argumentos

El método `.call()` invoca una función inmediatamente, estableciendo `this` al objeto proporcionado como primer argumento y pasando los argumentos restantes de forma individual.

```javascript
function presentar(saludo, signo) {
  console.log(`${saludo}, soy ${this.nombre}${signo}`);
}

const usuario = { nombre: 'Lucía' };

presentar.call(usuario, 'Hola', '!'); // "Hola, soy Lucía!"
```

*   **Uso común:** Herencia de constructores en patrones antiguos de JavaScript: `Padre.call(this, ...args)`.

---

## .apply(): Invocación con Array de Argumentos

`.apply()` funciona de forma idéntica a `.call()`, con la diferencia de que los argumentos de la función se pasan como un **único array** (o un objeto similar a un array).

```javascript
const numeros = [5, 10, 15, 20];

// Encontrar el máximo prestando el método Math.max
const maximo = Math.max.apply(null, numeros); 
console.log(maximo); // 20
```

> [!TIP]
> En el JavaScript moderno (ES6+), el **operador spread** (`...`) suele ser preferible al uso de `.apply()` para pasar arrays como argumentos: `Math.max(...numeros)`.

---

## .bind(): Creación de una Función Vinculada

A diferencia de los anteriores, `.bind()` **no ejecuta la función de inmediato**. En su lugar, devuelve una **nueva función** que tiene el `this` fijado permanentemente al valor proporcionado.

### Aplicación Parcial (Partial Application)
También permite preestablecer algunos argumentos de la función original.

```javascript
function multiplicar(a, b) {
  return a * b;
}

const duplicar = multiplicar.bind(null, 2);
console.log(duplicar(10)); // 20
```

### Preservación de Contexto en Callbacks
Es la herramienta clásica para evitar que un método pierda su contexto al ser pasado como callback.

```javascript
const app = {
  mensaje: 'Cargando...',
  mostrar() {
    console.log(this.mensaje);
  }
};

// Error: this se perdería. Solución: bind
setTimeout(app.mostrar.bind(app), 1000);
```

> [!IMPORTANT]
> Una vez que una función ha sido vinculada mediante `.bind()`, su contexto de `this` es **inmutable**. No puede ser sobrescrito por llamadas posteriores a `.call()` o `.apply()`.

---

## Tabla Comparativa

| Método | ¿Ejecuta la función? | Paso de Argumentos | Valor de Retorno |
| :--- | :--- | :--- | :--- |
| **`.call()`** | Sí | Lista (uno a uno) | El resultado de la función |
| **`.apply()`** | Sí | Array / Iterable | El resultado de la función |
| **`.bind()`** | No | Lista (uno a uno) | Una nueva función vinculada |

---

## Interacción con Arrow Functions

Las funciones de flecha **ignoran** el cambio de contexto de estos tres métodos porque no poseen un `this` propio. Si intentas usar `call`, `apply` o `bind` sobre una Arrow Function, el valor de `this` seguirá siendo el de su ámbito léxico original.

```javascript
const flecha = () => console.log(this);
flecha.call({ id: 1 }); // 'this' seguirá siendo el contexto exterior (ej. window)
```

---
[Volver al Índice](../js-index.md)
