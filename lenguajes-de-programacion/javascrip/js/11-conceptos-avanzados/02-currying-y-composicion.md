# Currying y Composición

En la programación funcional, el **Currying** y la **Composición** son técnicas fundamentales para crear código modular, reutilizable y fácil de testear.

---

## Currying

Es la técnica de transformar una función que acepta múltiples argumentos en una secuencia de funciones que aceptan un único argumento cada una.

```js
// Sin currying
function suma(a, b, c) { return a + b + c; }

// Con currying manual
function sumaCurried(a) {
  return function(b) {
    return function(c) {
      return a + b + c;
    };
  };
}

console.log(sumaCurried(1)(2)(3)); // 6
```

### Currying genérico
Podemos automatizar este proceso con una función auxiliar:

```js
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return (...next) => curried(...args, ...next);
  };
}

const curriedSuma = curry(suma);
console.log(curriedSuma(1)(2)(3)); // 6
console.log(curriedSuma(1, 2)(3)); // 6
```

> [!TIP]
> El currying es extremadamente útil para crear **funciones parcialmente aplicadas**. Por ejemplo:
> `const multiplicar = curry((a, b) => a * b);`
> `const doble = multiplicar(2); // Función que siempre multiplica por 2`

---

## Composición de funciones

Consiste en combinar funciones simples para construir funciones complejas. La salida de una función se convierte directamente en la entrada de la siguiente.

```js
const trim = s => s.trim();
const mayusculas = s => s.toUpperCase();
const exclamar = s => s + '!';

// Composición manual (difícil de leer si hay muchas funciones)
const emocionarManual = (s) => exclamar(mayusculas(trim(s)));
```

### Funciones `compose` y `pipe`

Para manejar la composición de forma elegante, solemos usar utilidades:

- **`compose`**: Ejecuta las funciones de **derecha a izquierda** (matemático).
- **`pipe`**: Ejecuta las funciones de **izquierda a derecha** (flujo de datos).

```js
const compose = (...fns) => (x) => fns.reduceRight((acc, fn) => fn(acc), x);
const pipe = (...fns) => (x) => fns.reduce((acc, fn) => fn(acc), x);

const emocionar = compose(exclamar, mayusculas, trim);
console.log(emocionar('  hola  ')); // "HOLA!"
```

---

## Estilo "Punto Libre" (*Point-free style*)

Al componer funciones, podemos omitir los argumentos intermedios, centrándonos solo en la transformación de los datos.

- **Con argumentos:** `const procesar = (s) => pipe(trim, mayusculas)(s);`
- **Punto libre:** `const procesar = pipe(trim, mayusculas);`

---

## Beneficios y Limitaciones

### ✅ Beneficios
- **Reutilización:** Permite crear pequeñas piezas de lógica pura y combinarlas.
- **Legibilidad:** El código se lee como una serie de pasos de transformación.
- **Mantenibilidad:** Cada función pequeña es fácil de testear de forma aislada.

### ⚠️ Limitaciones
- **Depuración:** Puede ser más difícil seguir el flujo en el *stack trace* si ocurre un error dentro de una composición profunda.
- **Curva de aprendizaje:** Requiere un cambio de mentalidad hacia el paradigma funcional.

> [!NOTE]
> Muchas librerías modernas como **Ramda** o **Lodash/fp** traen estas utilidades integradas y optimizadas para su uso en producción.
