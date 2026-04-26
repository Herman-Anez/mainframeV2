# `call`, `apply` y `bind`

Estos tres métodos permiten controlar explícitamente el valor de `this` y proveen una forma de "prestar" funciones entre objetos.

Todos pertenecen a `Function.prototype` y están disponibles en cualquier función (excepto arrows, que ignoran estos métodos porque no tienen `this` propio).

---

## `call(thisArg, arg1, arg2, ...)`

Invoca la función inmediatamente, estableciendo `this` al primer argumento, y pasando los argumentos restantes de forma individual.

```js
function saludar(signo) {
  console.log(`Hola ${this.nombre}${signo}`);
}

const persona = { nombre: 'Lucía' };
saludar.call(persona, '!'); // Hola Lucía!
```

- **`thisArg`:** Puede ser `null` o `undefined` (en ese caso se reemplaza por el objeto global en modo no estricto, o se mantiene como tal en modo estricto).
- **Uso común:** Muy usado para herencia constructora: `Padre.call(this, ...args)`.

---

## `apply(thisArg, [argsArray])`

Similar a `call`, pero los argumentos se pasan como un **array** (o un objeto iterable).

```js
function sumar(a, b, c) {
  return a + b + c;
}

const numeros = [1, 2, 3];
sumar.apply(null, numeros); // 6
```

- **Cuándo usarlo:** Útil cuando tienes los argumentos en un array y quieres pasarlos dinámicamente.
- **Alternativa moderna:** Hoy en día, el operador **spread** (`...`) cubre muchos casos: `fn(...args)`.

---

## `bind(thisArg, arg1, arg2, ...)`

No ejecuta la función de inmediato. Devuelve una **nueva función** con el `this` fijado permanentemente al valor dado, y los argumentos opcionales preestablecidos (*partial application*).

```js
function multiplicar(factor, n) {
  return factor * n;
}

const duplicar = multiplicar.bind(null, 2);
console.log(duplicar(5)); // 10
```

> [!IMPORTANT]
> Una vez hecho `bind`, el `this` no puede ser sobrescrito ni siquiera con `call`/`apply` (aunque `new` ignora el `this` vinculado y usa el nuevo objeto).

### Paso de métodos como callbacks

Es fundamental para pasar métodos de objeto como callbacks sin perder el contexto.

```js
const boton = {
  texto: 'Click me',
  manejarClick: function() {
    console.log(this.texto);
  }
};

document.querySelector('button').addEventListener('click', boton.manejarClick.bind(boton));
// Sin bind, this sería el button, no boton.
```

---

## Tabla comparativa

| Método | ¿Ejecuta? | Argumentos | Devuelve |
| :--- | :--- | :--- | :--- |
| **`call`** | Sí | Lista individual | Resultado de la función |
| **`apply`** | Sí | Array | Resultado de la función |
| **`bind`** | No | Lista individual | Una nueva función |

---

## Casos comunes

1. **Préstamo de métodos:** Usar `Array.prototype.slice.call` sobre objetos *array-like* (`arguments`, `NodeList`) para convertirlos en array. (Hoy reemplazado por `Array.from`).
2. **Establecer `this` en callbacks:** Especialmente en eventos cuando necesitas referenciar otro objeto.
3. **Partial application:** `const fn = funcion.bind(null, predefinido)`.
4. **Encadenamiento con temporizadores:** `setTimeout(objeto.metodo.bind(objeto), 100)`.

---

## Consideraciones con Arrow Functions

Como se mencionó, las arrow functions **no pueden ser vinculadas**; `call`, `apply` y `bind` no producen error pero no alteran su `this`. Solo los argumentos adicionales se pasan (si los acepta).

```js
const flecha = () => console.log(this);
flecha.call({a: 1}); // this sigue siendo el del ámbito léxico
```

> [!TIP]
> Dominar `this` y sus métodos de control es esencial para escribir código robusto y evitar bugs de contexto difíciles de rastrear.
---
[back](../index)
