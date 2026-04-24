# `this` Global y en Métodos

La palabra clave `this` es una de las más poderosas y confusas de JavaScript. Su valor no se determina en tiempo de escritura, sino en tiempo de ejecución, y depende de cómo se invoca la función que lo contiene.

## Reglas generales de determinación de `this`

Existen básicamente cuatro patrones que determinan a qué apunta `this`:

### 1. Invocación global o de función simple
### 2. Invocación como método de un objeto
### 3. Invocación con `new` (constructor)
### 4. Invocación explícita con `call`, `apply`, `bind`

---

## 1. `this` en el ámbito global

Fuera de cualquier función, `this` hace referencia al objeto global:

- **En el navegador:** `window` (o `globalThis`).
- **En Node.js:** `global` (o `globalThis`).
- **En módulos ES:** El ámbito global no tiene `this` apuntando al objeto global (es `undefined` en el nivel superior del módulo). Pero dentro de una función no ligada, sí.

```js
// Navegador (script normal)
console.log(this); // window

// En Node REPL o script CommonJS
console.log(this); // {}

// [!NOTE]
// En módulo CommonJS, this es el objeto module.exports (no global)
// En el ámbito de una función: this es global
```

## 2. `this` en una función normal

Cuando una función ordinaria (no flecha) es invocada sin un contexto explícito (no como método, no con `new`, sin `call`/`apply`/`bind`), su `this` depende del modo:

- **Modo no estricto:** `this` apunta al objeto global (`window` en navegadores, `global` en Node).
- **Modo estricto (`'use strict'` o módulos ES):** `this` es `undefined`.

```js
function mostrarThis() {
  console.log(this);
}

mostrarThis(); // window o global (no estricto), undefined (estricto)
```

> [!WARNING]
> Este comportamiento causa problemas cuando una función se pasa como callback y se espera que `this` tenga un valor particular.

## 3. `this` en un método de objeto

Cuando una función se llama como propiedad de un objeto (método), `this` se refiere al objeto que está antes del punto (o corchetes) en el momento de la invocación.

```js
const persona = {
  nombre: 'Carlos',
  saludar: function() {
    return `Hola, soy ${this.nombre}`;
  }
};

console.log(persona.saludar()); // Hola, soy Carlos
```

### El peligro de la pérdida de contexto

Si el método se extrae a una variable y se llama por separado, pierde su contexto original.

```js
const saludo = persona.saludar;
saludo(); // Hola, soy undefined (this es global/undefined)
```

### Excepción con la cadena de prototipos

Si el método se encuentra en el prototipo pero se invoca a través del objeto, `this` sigue siendo el objeto original.

```js
const base = { 
  decir() { 
    return this.valor; 
  } 
};

const hijo = Object.create(base);
hijo.valor = 10;
console.log(hijo.decir()); // 10
```

## 4. `this` en una función constructora (con `new`)

Cuando una función es llamada con `new`, se crea un objeto nuevo y `this` apunta a ese nuevo objeto dentro del constructor.

```js
function Cosa(nombre) {
  this.nombre = nombre;
}

const cosa = new Cosa('Ejemplo');
console.log(cosa.nombre); // Ejemplo
```

> [!TIP]
> Si accidentalmente se llama sin `new`, `this` se comportará según las reglas de función normal (posiblemente contaminando el objeto global). Para protegerse, se puede usar `new.target` o la sintaxis `class`, que fuerza el uso de `new`.

## 5. `this` en callbacks clásicos y event listeners

- **En `addEventListener`:** `this` dentro del callback apunta al elemento DOM que disparó el evento (excepto si se usa arrow function, que no tiene `this` propio).
- **En callbacks de temporizadores (`setTimeout`/`setInterval`):** Las funciones normales tienen `this` global/undefined.
- **En métodos de array como `.forEach`:** El segundo argumento opcional se convierte en el `this` del callback.

```js
const obj = { 
  factor: 10, 
  multiplicar(arr) { 
    arr.forEach(function(n) { 
      console.log(this.factor * n); 
    }, this); 
  } 
};
```

## Errores comunes

- Asumir que `this` dentro de una función anidada es el mismo que el de la función contenedora.
- Olvidar que `this` en callbacks se desvincula.

> [!IMPORTANT]
> La solución histórica era `var self = this;` o `var that = this;`. Hoy en día, las **arrow functions** resuelven esto de manera nativa (ver siguiente sección).