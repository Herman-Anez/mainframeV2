## Archivo: `01-callbacks.md`


Un callback es una función que se pasa como argumento a otra función y se ejecuta más tarde, generalmente al completarse una operación (síncrona o asíncrona).
Callback síncrono vs asíncrono

    Síncrono: la función externa ejecuta el callback inmediatamente (ej. array.forEach, array.map). Bloquea el hilo.

    Asíncrono: la función registra el callback para ejecutarse en el futuro, cuando ocurra un evento o finalice una tarea larga (ej. setTimeout, lectura de archivo). No bloquea.

### Ejemplo con temporizador
```js
console.log('Inicio');
setTimeout(() => {
  console.log('Timeout');
}, 1000);
console.log('Fin');
// Imprime: Inicio, Fin, Timeout (después de 1s)
```

### Callback pattern en Node.js (error-first)

Tradicionalmente en Node, los callbacks asíncronos reciben un error como primer argumento o null si todo fue bien.
```js
fs.readFile('/archivo.txt', 'utf8', (err, data) => {
  if (err) {
    console.error('Error:', err);
    return;
  }
  console.log(data);
});
```

Esto normaliza el manejo de errores.
Inconveniente: Callback Hell

Cuando se anidan muchos callbacks para secuencias de operaciones asíncronas, el código se vuelve difícil de leer y mantener:
```js
obtenerUsuario(id, (usuario) => {
  obtenerPedidos(usuario, (pedidos) => {
    procesarPedido(pedidos[0], (resultado) => {
      // más anidamiento...
    });
  });
});
```

Las soluciones modernas incluyen Promesas y async/await.
Errores comunes

    Olvidar que la ejecución continúa después de setTimeout sin esperar.

    No capturar errores lanzados dentro de callbacks asíncronos con try/catch (no funcionan porque el stack original ya no existe).

    Perder el contexto de this si pasamos un método como callback sin atar (bind o arrow function).

### Aún se usan

    APIs antiguas en Node (fs callback-style) y navegadores (IndexedDB, etc.).

    Event listeners (addEventListener).

    Muchos módulos han migrado a promesas: fs.promises.

---
