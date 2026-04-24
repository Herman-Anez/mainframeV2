
## Archivo: `01-history-api.md`


La History API permite manipular el historial del navegador sin recargar la página, base de las SPA (Single Page Applications) para el enrutamiento del lado del cliente.
Objeto window.history

Proporciona métodos para navegar y modificar la pila de historial.
history.back(), history.forward(), history.go()

    history.back(): equivale a presionar el botón atrás.

    history.forward(): botón adelante.

    history.go(delta): -1 atrás, 1 adelante, 0 recarga la página actual.

### history.pushState(state, title, url)

Añade una nueva entrada al historial y cambia la URL en la barra de direcciones sin recargar la página. Es el núcleo del enrutamiento moderno.
```js
const nuevoEstado = { page: 'about', userId: 42 };
history.pushState(nuevoEstado, '', '/about');

    state: objeto js asociado a la entrada del historial (hasta 640KB por entrada en la mayoría de navegadores). Se recupera luego con history.state o en el evento popstate.

    title: actualmente ignorado por la mayoría de navegadores, se pasa string vacío.

    url: nueva URL (mismo origen). El navegador no verifica que exista el recurso; solo se actualiza la barra.
```

### history.replaceState(state, title, url)

Similar a pushState pero reemplaza la entrada actual del historial en lugar de añadir una nueva. Útil para corregir la URL sin generar historial adicional (ej. al redirigir después de login).
Evento popstate

Se dispara en window cuando el usuario navega por el historial (atrás/adelante). No se dispara con pushState o replaceState.
```js
window.addEventListener('popstate', (event) => {
  if (event.state) {
    // restaurar la vista según event.state
    console.log('Volviendo a estado:', event.state);
  }
});
```

En el manejador, location.pathname ya se ha actualizado; podemos leer la ruta y renderizar el contenido correspondiente.
Integración con SPA

Un enrutador cliente típico:

    Intercepta clics en enlaces internos, llama a pushState y renderiza la vista.

    Escucha popstate para navegación hacia atrás.

    En carga inicial (o refresco), el servidor debe responder con el HTML base y el enrutador cliente toma el control.

### Seguridad y restricciones

    La nueva URL debe ser del mismo origen; de lo contrario lanza una excepción.

    El estado se serializa mediante la API de Structured Clone (soporta objetos, arrays, etc., pero no funciones, DOM nodes).

    El estado no persiste tras cerrar la pestaña (a diferencia de sessionStorage).

---
