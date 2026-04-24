
## Archivo: `06-iife-y-recursividad.md`

IIFE (Immediately Invoked Function Expression)

Una IIFE es una función que se define y se ejecuta inmediatamente. Sintaxis básica:
```js
(function() {
  // código aislado
})();
```

o
```js
(function() {
  // código aislado
}());
```

    Se usa para crear un ámbito privado y evitar contaminar el ámbito global.

    Muy común antes de la llegada de módulos ES6 para encapsular código.

### Puede tener parámetros: (function(global) { ... }(window));

### Casos de uso

    Módulo revelador (revealing module pattern): retornar un objeto con métodos públicos que acceden a variables privadas del closure.

```js
const modulo = (function() {
  let privada = 0;
  return {
    incrementar() { privada++; },
    valor() { return privada; }
  };
})();
modulo.incrementar();
console.log(modulo.valor()); // 1
console.log(modulo.privada); // undefined

    Bucles y closures (antes de let): capturar valor de iterador.
```

js

### for (var i = 0; i < 3; i++) {
  (function(indice) {
    setTimeout(() => console.log(indice), 100);
  })(i);
}

    Evitar colisiones de nombres en scripts concatenados.

### Recursividad

Una función recursiva es aquella que se llama a sí misma para resolver un problema dividiéndolo en subproblemas más pequeños, hasta llegar a un caso base que detiene la recursión.
```js
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}
```

### Componentes esenciales

    Caso base: condición que termina la recursión (sin ella hay desbordamiento de pila).

    Llamada recursiva: con argumentos que convergen hacia el caso base.

### Recursión de cola (tail recursion)

Si la llamada recursiva es la última operación que realiza la función (está en posición de cola), algunos motores pueden optimizarla para evitar acumulación de stack (TCO, Tail Call Optimization). No todos los entornos lo implementan, pero es buena práctica escribir funciones recursivas de cola cuando sea posible.
```js
function factorial(n, acum = 1) {
  if (n <= 1) return acum;
  return factorial(n - 1, n * acum); // llamada de cola
}
```

### Aplicaciones clásicas

    Recorridos de estructuras de árbol o grafo.

    Algoritmos como ordenamiento (quicksort, mergesort).

    Cálculo de secuencias (Fibonacci).

    Procesamiento de estructuras anidadas (JSON, DOM).

### Precauciones

    Cada llamada recursiva consume memoria en la pila de ejecución; si la profundidad es excesiva, se produce un stack overflow.

    A veces una solución iterativa es más eficiente y clara; pero la recursividad puede ser más natural para problemas auto-similares.

### 04-objetos-y-clases
---
