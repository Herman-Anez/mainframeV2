# Callbacks en JavaScript

Un callback es una función que se pasa como argumento a otra función y se ejecuta más tarde, generalmente al completarse una operación (síncrona o asíncrona).

---

## Callback Síncrono vs Asíncrono

*   **Síncrono:** La función externa ejecuta el callback inmediatamente (ej. `array.forEach`, `array.map`). Bloquea el hilo de ejecución hasta terminar.
*   **Asíncrono:** La función registra el callback para ejecutarse en el futuro, cuando ocurra un evento o finalice una tarea larga (ej. `setTimeout`, lectura de archivo). No bloquea el hilo principal.

### Ejemplo con Temporizador
```javascript
console.log('Inicio');

setTimeout(() => {
  console.log('Timeout');
}, 1000);

console.log('Fin');

// Imprime: Inicio, Fin, Timeout (después de 1s)
```

---

## Callback Pattern en Node.js (Error-First)

Tradicionalmente en Node.js, los callbacks asíncronos reciben un error como primer argumento o `null` si la operación fue exitosa.

```javascript
const fs = require('fs');

fs.readFile('/archivo.txt', 'utf8', (err, data) => {
  if (err) {
    console.error('Error al leer el archivo:', err);
    return;
  }
  console.log('Contenido:', data);
});
```

> [!NOTE]
> Este patrón normaliza el manejo de errores en toda la plataforma, obligando al desarrollador a verificar si ocurrió un fallo antes de procesar los datos.

---

## Inconveniente: Callback Hell

Cuando se anidan muchos callbacks para secuencias de operaciones asíncronas, el código se vuelve difícil de leer y mantener, expandiéndose horizontalmente en lo que se conoce como "Pyramid of Doom".

```javascript
obtenerUsuario(id, (usuario) => {
  obtenerPedidos(usuario, (pedidos) => {
    procesarPedido(pedidos[0], (resultado) => {
      // El anidamiento continúa...
    });
  });
});
```

> [!TIP]
> Las soluciones modernas para mitigar este problema incluyen el uso de **Promesas** y la sintaxis **async/await**.

---

## Errores Comunes

> [!WARNING]
> Ten especial cuidado con los siguientes puntos al trabajar con callbacks:
> 1.  **Continuidad de ejecución:** Olvidar que el código sigue ejecutándose después de un `setTimeout` sin esperar al callback.
> 2.  **Captura de errores:** Los bloques `try/catch` tradicionales no capturan errores lanzados dentro de callbacks asíncronos porque el stack original ya no existe.
> 3.  **Contexto de `this`:** Se puede perder el contexto original si se pasa un método de un objeto como callback sin usar `.bind()` o funciones de flecha.

---

## Vigencia de los Callbacks

A pesar de las alternativas modernas, los callbacks siguen siendo fundamentales en:
*   **APIs de Navegadores:** Event listeners (`addEventListener`).
*   **APIs Heredadas:** Muchas funciones nativas de Node.js siguen ofreciendo versiones basadas en callbacks (aunque ahora existan `fs.promises`).
*   **Programación Funcional:** Métodos de arrays como `map`, `filter` y `reduce`.

---
[Volver al Índice](../js-index.md)
