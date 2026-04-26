# History API

La **History API** permite manipular el historial de navegación del usuario sin recargar la página completa. Es la base tecnológica de las **SPA** (*Single Page Applications*) para gestionar el enrutamiento en el lado del cliente.

---

## El objeto `window.history`

Proporciona métodos esenciales para navegar y modificar la pila del historial del navegador.

- **`history.back()`**: Equivale a presionar el botón "Atrás" del navegador.
- **`history.forward()`**: Equivale al botón "Adelante".
- **`history.go(delta)`**: Permite saltar posiciones en el historial (`-1` atrás, `1` adelante, `0` recarga la página).

---

## Manipulación del estado

### `history.pushState(state, title, url)`

Añade una nueva entrada al historial y cambia la URL en la barra de direcciones sin provocar una recarga. Es el núcleo del enrutamiento moderno.

```js
const nuevoEstado = { page: 'about', userId: 42 };
history.pushState(nuevoEstado, '', '/about');
```

- **`state`**: Objeto JavaScript serializable asociado a la entrada. Se recupera mediante `history.state` o en el evento `popstate`. (Límite aproximado: 640KB).
- **`title`**: Actualmente ignorado por la mayoría de navegadores (se recomienda pasar un string vacío `''`).
- **`url`**: La nueva URL que se mostrará en la barra. Debe ser del mismo origen que la actual.

### `history.replaceState(state, title, url)`

Similar a `pushState`, pero **reemplaza** la entrada actual del historial en lugar de añadir una nueva. Es ideal para actualizar la URL sin generar historial adicional (ej: después de una redirección de login).

---

## El evento `popstate`

Se dispara en el objeto `window` cuando el usuario navega a través del historial (botones atrás/adelante).

```js
window.addEventListener('popstate', (event) => {
  if (event.state) {
    // Restaurar la vista o el estado de la aplicación
    console.log('Restaurando estado:', event.state);
    renderizarPagina(event.state.page);
  }
});
```

> [!NOTE]
> El evento `popstate` **no** se dispara al llamar a `pushState()` o `replaceState()`. Solo ocurre mediante acciones del usuario o métodos de navegación como `back()`, `forward()` y `go()`.

---

## Integración en SPAs

Un enrutador cliente (*Client-side Router*) típico funciona siguiendo este flujo:

1. **Intercepción:** Captura los clics en enlaces internos (`<a>`) y previene la navegación por defecto.
2. **Navegación:** Llama a `pushState()` para actualizar la URL y el historial.
3. **Renderizado:** Actualiza el DOM para mostrar la nueva vista sin recargar.
4. **Sincronización:** Escucha `popstate` para reaccionar cuando el usuario usa los botones del navegador.

---

## Seguridad y Restricciones

- **Mismo Origen:** La nueva URL debe pertenecer al mismo origen (protocolo, dominio y puerto). De lo contrario, se lanzará una excepción de seguridad.
- **Serialización:** El estado se guarda mediante el algoritmo de *Structured Clone* (soporta objetos complejos y arrays, pero no funciones o nodos del DOM).
- **Persistencia:** A diferencia de `sessionStorage`, el estado de la History API no persiste necesariamente tras cerrar y volver a abrir la pestaña en todos los navegadores.

> [!IMPORTANT]
> Cuando se usa History API para enrutamiento, el servidor debe estar configurado para devolver el `index.html` base para cualquier ruta desconocida, permitiendo que el JavaScript del cliente tome el control del renderizado.

---
[back](../index)
