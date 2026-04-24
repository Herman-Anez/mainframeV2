## Archivo: `01-closures-aplicados.md`


Ya cubrimos closures en fundamentos. Aquí profundizamos con patrones avanzados.
Módulo revelador clásico

Antes de ES6 se usaban closures para encapsular estado:
```js
const contador = (function() {
  let cuenta = 0;
  return {
    incrementar: () => ++cuenta,
    valor: () => cuenta
  };
})();
contador.incrementar();
console.log(contador.valor()); // 1
console.log(contador.cuenta); // undefined
```

### Fábricas de funciones

Crean funciones especializadas basadas en configuración:
```js
function crearMultiplicador(factor) {
  return (n) => n * factor;
}
const duplicar = crearMultiplicador(2);
duplicar(5); // 10
```

### Caché y memoización

Los closures permiten almacenar resultados previos para evitar cálculos repetidos.
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
  return fibonacciMemo(n-1) + fibonacciMemo(n-2);
});
```

### Simulación de variables privadas en clases ES6

Antes de los campos #, los closures permitían privacidad:
```js
function crearPersona(nombre) {
  let _edad = 0; // privada
  return {
    getEdad: () => _edad,
    cumplirAños: () => _edad++
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
```

### Manejadores de eventos con estado

Un closure puede mantener estado entre eventos sin variables globales.
```js
function crearManejador() {
  let contador = 0;
  return () => console.log(`Click #${++contador}`);
}
document.getElementById('btn').addEventListener('click', crearManejador());
```

### Posibles desventajas

    Pueden retener referencias grandes y causar fugas de memoria si no se limpian.

    Dificultan el testing si el estado no es accesible.

---
