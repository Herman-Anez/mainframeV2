
## Archivo: `03-call-apply-bind.md`


Estos tres métodos permiten controlar explícitamente el valor de this y proveen una forma de "prestar" funciones.

Todos pertenecen a Function.prototype y están disponibles en cualquier función (excepto arrows, que ignoran estos métodos porque no tienen this propio).
call(thisArg, arg1, arg2, ...)

Invoca la función inmediatamente, estableciendo this al primer argumento, y pasando los argumentos restantes de forma individual.
```js
function saludar(signo) {
  console.log(`Hola ${this.nombre}${signo}`);
}
const persona = { nombre: 'Lucía' };
saludar.call(persona, '!'); // Hola Lucía!

    thisArg puede ser null o undefined (en ese caso se reemplaza por el objeto global en no estricto, o se mantiene en estricto).

    Muy usado para herencia constructora: Padre.call(this, ...args).
```

### apply(thisArg, [argsArray])

Similar a call, pero los argumentos se pasan como un array (o iterable).
```js
function sumar(a, b, c) {
  return a + b + c;
}
const numeros = [1, 2, 3];
sumar.apply(null, numeros); // 6
```

    Útil cuando tienes los argumentos en un array y quieres pasarlos dinámicamente.

    Hoy en día, el operador spread (...) cubre muchos casos: fn(...args).

### bind(thisArg, arg1, arg2, ...)

No ejecuta la función de inmediato. Devuelve una nueva función con el this fijado permanentemente al valor dado, y los argumentos opcionales preestablecidos (partial application).
```js
function multiplicar(factor, n) {
  return factor * n;
}
const duplicar = multiplicar.bind(null, 2);
console.log(duplicar(5)); // 10

    Una vez hecho bind, el this no puede ser sobrescrito ni siquiera con call/apply/new (aunque new ignora el this vinculado y usa el nuevo objeto).
```

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

### Tabla comparativa
Método	¿Ejecuta?	Argumentos	Devuelve
call	Sí	Lista individual	Resultado de fn
apply	Sí	Array	Resultado de fn
bind	No	Lista individual	Nueva función
Casos comunes

    Préstamo de métodos: usar Array.prototype.slice.call sobre objetos array-like (arguments, NodeList) para convertirlos en array. (Hoy reemplazado por Array.from).

    Establecer this en callbacks de eventos cuando necesitas otro objeto.

    Partial application: const fn = funcion.bind(null, predefinido).

    Encadenamiento con setTimeout: setTimeout(objeto.metodo.bind(objeto), 100).

### Consideraciones con Arrow Functions

Como se mencionó, las arrow functions no pueden ser vinculadas; call, apply, bind no producen error pero no alteran this. Solo los argumentos adicionales se pasan (si los acepta).
```js
const flecha = () => console.log(this);
flecha.call({a:1}); // this sigue siendo el del ámbito léxico
```
Dominar this y sus métodos de control es esencial para escribir código robusto y evitar bugs de contexto.