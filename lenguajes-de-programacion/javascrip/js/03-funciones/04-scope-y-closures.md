
## Archivo: `04-scope-y-closures.md`

Scope (ámbito)

El ámbito determina dónde una variable es accesible. En js, hasta ES6 el ámbito solo era de función y global. Con let y const se añadió el ámbito de bloque.

    Ámbito global: variables declaradas fuera de cualquier función (o con var sin función). Son propiedades del objeto global (ventana en navegador).

    Ámbito de función: cada función crea su propio ámbito, las variables declaradas dentro con var, let o const son locales a esa función.

    Ámbito de bloque: let y const limitan la variable al bloque {} (if, for, while, etc.).

La resolución de nombres sigue la cadena de ámbitos (scope chain): el motor busca la variable en el ámbito actual, si no la encuentra sube al ámbito superior, y así hasta el global. Si no existe, se crea una variable global en modo no estricto (error en estricto).
Closure (clausura)

Un closure se produce cuando una función "recuerda" y puede acceder a variables de su ámbito léxico incluso cuando la función se ejecuta fuera de ese ámbito. En otras palabras, una función interna que referencia variables de una función externa "cierra sobre" esas variables.
```js
function crearContador() {
  let cuenta = 0;
  return function() {
    cuenta++;
    return cuenta;
  };
}
const contador1 = crearContador();
console.log(contador1()); // 1
console.log(contador1()); // 2
```

Aquí la función anónima retornada mantiene viva la variable cuenta (que pertenece al ámbito de crearContador) a través del closure. Cada llamada a crearContador() genera un nuevo ámbito con su propia variable cuenta.
Aplicaciones prácticas de closures

    Encapsulación y datos privados: simular propiedades privadas (antes de los campos #).

    Fábricas de funciones y partial application.

    Manejo de eventos asíncronos que necesitan contexto (similar a cómo las arrow functions capturan this, pero para variables).

    Memoización (cache de resultados).

### Ejemplo con bucles (clásico)
```js
for (var i = 0; i < 3; i++) {
  setTimeout(function() { console.log(i); }, 100);
}
// Imprime 3, 3, 3 (porque i es compartida en el ámbito global/función)
```

Solución con closure (IIFE) o con let:
```js
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // 0,1,2 (cada iteración tiene su propio i)
}
```

### Importante

Los closures no copian los valores en el momento de su creación, capturan la referencia a la variable. Si la variable cambia antes de que la función se ejecute, verá el valor actualizado.
Rendimiento

Los closures mantienen referencias al ámbito exterior, lo que puede impedir que el garbage collector libere memoria si no se usan con cuidado. Sin embargo, son una herramienta fundamental y no deben evitarse por razones prematuras de rendimiento.