# Closures Aplicados

Aunque ya cubrimos los conceptos básicos de los **closures**, en esta sección profundizamos en los patrones avanzados y casos de uso prácticos en el desarrollo profesional.

---

## Patrones de Diseño con Closures

### 1. Módulo Revelador Clásico (*Revealing Module Pattern*)

Antes de la llegada de los módulos nativos en ES6, se utilizaban IIFEs (*Immediately Invoked Function Expressions*) y closures para encapsular estado privado y exponer solo lo necesario.

```js
const contador = (function() {
  let cuenta = 0; // Variable privada

  return {
    incrementar: () => ++cuenta,
    valor: () => cuenta
  };
})();

contador.incrementar();
console.log(contador.valor()); // 1
console.log(contador.cuenta);  // undefined (privacidad real)
```

### 2. Fábricas de Funciones (*Function Factories*)

Los closures permiten crear funciones especializadas basadas en una configuración inicial o contexto.

```js
function crearMultiplicador(factor) {
  return (n) => n * factor;
}

const duplicar = crearMultiplicador(2);
const triplicar = crearMultiplicador(3);

console.log(duplicar(5));  // 10
console.log(triplicar(5)); // 15
```

---

## Optimizaciones: Memoización

Los closures son fundamentales para implementar **memoización**, una técnica de optimización que consiste en cachear los resultados de funciones costosas.

```js
function memoizar(fn) {
  const cache = {};

  return function(...args) {
    const key = JSON.stringify(args);
    if (key in cache) return cache[key];

    const resultado = fn(...args);
    cache[key] = resultado;
    return resultado;
  };
}

const fibonacciMemo = memoizar((n) => {
  if (n <= 1) return n;
  return fibonacciMemo(n - 1) + fibonacciMemo(n - 2);
});
```

---

## Privacidad y Manejo de Estado

### Simulación de variables privadas

Antes de la sintaxis oficial de campos privados (`#propiedad`), los closures eran la única forma de garantizar la integridad de los datos en clases u objetos.

```js
function crearPersona(nombre) {
  let _edad = 0; // Realmente privada e inaccesible desde fuera

  return {
    getEdad: () => _edad,
    cumplirAnios: () => _edad++
  };
}
```

### Temporizadores y closures

Clásico problema del for con var. Los closures permiten capturar el valor en cada iteración (aunque con let ya no es necesario).

```js
for (var i = 0; i < 3; i++) {
  ((indice) => {
    setTimeout(() => console.log(indice), 100);
  })(i);
}

### Manejadores de eventos con estado

Un closure puede mantener el estado interno de un componente o interfaz sin necesidad de recurrir a variables globales.

```js
function crearManejador() {
  let contador = 0;
  return () => console.log(`Click número: ${++contador}`);
}

const boton = document.getElementById('btn');
boton.addEventListener('click', crearManejador());
```

---

## Consideraciones Técnicas

> [!CAUTION]
> **Gestión de Memoria:** Los closures mantienen referencias a las variables de su ámbito exterior. Si no se gestionan correctamente, pueden retener objetos grandes en memoria y causar **fugas de memoria** (*memory leaks*).

> [!NOTE]
> Con la introducción de `let` y `const`, muchos problemas clásicos de closures (como el valor de `i` en un bucle `for` con `setTimeout`) han quedado resueltos de forma más sencilla, pero el entendimiento profundo de los closures sigue siendo esencial para patrones funcionales.

- **Testing:** El estado encapsulado en un closure puede ser difícil de testear directamente si no se proporcionan métodos de inspección.
- **Depuración:** El seguimiento del estado en múltiples niveles de closures puede aumentar la complejidad cognitiva del código.
