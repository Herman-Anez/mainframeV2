# `this` Global y en Métodos

La palabra clave `this` es una de las más potentes y, a la vez, confusas de JavaScript. Su valor no se determina en tiempo de escritura (estáticamente), sino en **tiempo de ejecución** (dinámicamente), y depende estrictamente de **cómo se invoca** la función que lo contiene.

---

## Patrones de Determinación de `this`

Existen cuatro patrones principales que definen el valor de `this`:

1.  **Invocación Global o de Función Simple:** Contexto por defecto.
2.  **Invocación como Método:** El objeto que contiene la función.
3.  **Invocación con `new`:** El nuevo objeto creado por el constructor.
4.  **Invocación Explícita:** Uso de `call`, `apply` o `bind`.

---

## 1. El Contexto Global

Fuera de cualquier función, `this` hace referencia al objeto global del entorno de ejecución:

*   **En el Navegador:** `window` o `globalThis`.
*   **En Node.js:** `global` o `globalThis`.
*   **En Módulos ES:** `this` en el nivel superior es `undefined`.

```javascript
// Navegador (script estándar)
console.log(this === window); // true

// Node.js (ámbito de archivo)
console.log(this); // En CommonJS es {} (referencia a module.exports)
```

> [!NOTE]
> `globalThis` es la forma estándar y moderna de acceder al objeto global independientemente del entorno (Navegador, Worker o Node.js).

---

## 2. `this` en Funciones Normales

Cuando una función ordinaria (no flecha) se invoca de forma simple (ej. `miFuncion()`), su `this` depende del modo de ejecución:

*   **Modo No Estricto:** `this` apunta al objeto global.
*   **Modo Estricto (`'use strict'`):** `this` es `undefined`.

```javascript
function mostrar() {
  'use strict';
  console.log(this);
}

mostrar(); // undefined
```

> [!WARNING]
> Confiar en el objeto global para `this` suele ser fuente de errores difíciles de depurar y contaminación del espacio de nombres global.

---

## 3. `this` en Métodos de Objeto

Cuando una función se invoca como propiedad de un objeto (un método), `this` se refiere al objeto que está "antes del punto" en el momento de la llamada.

```javascript
const usuario = {
  nombre: 'Carlos',
  saludar() {
    console.log(`Hola, soy ${this.nombre}`);
  }
};

usuario.saludar(); // "Hola, soy Carlos"
```

### Pérdida de Contexto
Si extraemos el método del objeto, la conexión con `this` se rompe:

```javascript
const funcionSuelta = usuario.saludar;
funcionSuelta(); // "Hola, soy undefined" (this ya no es usuario)
```

---

## 4. Funciones Constructoras (`new`)

Al invocar una función con el operador `new`, ocurren cuatro pasos:
1. Se crea un nuevo objeto vacío `{}`.
2. `this` se vincula a ese nuevo objeto.
3. Se ejecuta el código de la función.
4. Se devuelve automáticamente el objeto (a menos que la función retorne explícitamente otro objeto).

```javascript
function Persona(nombre) {
  this.nombre = nombre;
}

const juan = new Persona('Juan');
console.log(juan.nombre); // "Juan"
```

> [!TIP]
> Si olvidas el `new`, `this` se comportará como en una función normal (global o undefined), lo que puede romper tu código. Usa `class` de ES6 para evitar este error, ya que las clases exigen el uso de `new`.

---

## 5. `this` en Callbacks y Eventos

*   **Event Listeners:** En un `addEventListener`, `this` apunta al elemento DOM que recibió el evento (salvo si usas una *arrow function*).
*   **Temporizadores:** En `setTimeout`, la función de callback pierde el contexto original y `this` vuelve a ser el objeto global o `undefined`.

```javascript
const boton = document.querySelector('#miBoton');
boton.addEventListener('click', function() {
  console.log(this); // El elemento <button>
});
```

---

## Errores Comunes y Mitigación

Un error clásico es intentar acceder a `this` dentro de una función anidada (como un `forEach` o un callback):

```javascript
const tienda = {
  productos: ['Pan', 'Leche'],
  listar() {
    this.productos.forEach(function(p) {
      // ERROR: this aquí es undefined (modo estricto) o global
      console.log(`${this.nombre} vende ${p}`);
    });
  }
};
```

> [!IMPORTANT]
> Históricamente se solucionaba con `const self = this;`. Actualmente, la solución preferida es usar **Arrow Functions** (que heredan el `this` del ámbito superior) o el método **`.bind(this)`**.

---
[Volver al Índice](../js-index.md)
