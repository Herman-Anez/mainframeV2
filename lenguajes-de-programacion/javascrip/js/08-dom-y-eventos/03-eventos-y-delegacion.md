## Archivo: `03-eventos-y-delegacion.md`


Los eventos permiten reaccionar a interacciones del usuario o cambios en el navegador.
Registrar manejadores
Propiedades on-event (onclick, onchange)
```js
elemento.onclick = function(evento) { ... };
```

    Solo un manejador por evento (sobrescribe anterior).

    No recomendado en aplicaciones modernas.

### addEventListener y removeEventListener
```js
function manejarClick(e) {
  console.log('Clicked', e.target);
}
elemento.addEventListener('click', manejarClick);
// eliminar después
elemento.removeEventListener('click', manejarClick);
```

    Permite múltiples escuchadores para el mismo evento.

    Tercer argumento opcional: options (capture, once, passive) o booleano useCapture.

    once: true elimina el listener automáticamente tras la primera ejecución.

    passive: true indica que el listener no llamará a preventDefault(), importante para rendimiento en scroll.

### El objeto evento e

Cada manejador recibe un objeto Event con propiedades clave:

    e.target: el elemento que originó el evento (más profundo).

    e.currentTarget: el elemento al que se ha enlazado el listener (útil en delegación).

    e.type: nombre del evento.

    e.preventDefault(): cancela el comportamiento por defecto (ej. envío de formulario, link).

    e.stopPropagation(): detiene la propagación del evento.

    e.stopImmediatePropagation(): detiene la propagación y evita que se ejecuten otros listeners en el mismo elemento.

### Fases de propagación

Cuando ocurre un evento, atraviesa tres fases:

    Fase de captura: desde window hacia el target (rara vez usada).

    Fase de target: el elemento donde ocurrió.

    Fase de burbuja: del target sube hacia window.

Por defecto, los listeners se registran en fase de burbuja. Para captura, pasa true como tercer argumento o { capture: true }.
Delegación de eventos

Técnica que consiste en poner un único listener en un ancestro común y usar e.target para determinar qué elemento hijo lo disparó. Esencial cuando los elementos se crean dinámicamente.
```js
lista.addEventListener('click', (e) => {
  if (e.target.matches('li button')) {
    console.log('Botón clickeado en elemento', e.target.closest('li'));
  }
});
```

    Ventajas: menos listeners, mejor rendimiento, maneja elementos añadidos posteriormente.

    Siempre verificar que e.target sea el deseado usando matches o closest.

### Eventos comunes

    Ratón: click, dblclick, mousedown, mouseup, mousemove, mouseover, mouseout, mouseenter, mouseleave (estos dos no burbujean).

    Teclado: keydown, keyup, keypress (obsoleto), con propiedades e.key, e.code.

    Formulario: submit, change, input, focus, blur, focusin, focusout (estos dos sí burbujean).

    Documento: DOMContentLoaded, load, beforeunload.

    Ventana: resize, scroll, storage (ver siguiente sección).

    Táctil: touchstart, touchmove, touchend.

### Eventos personalizados

new CustomEvent('nombre', { detail: { ... } }) y dispatchEvent permiten crear sistemas de comunicación propios.
```js
elemento.addEventListener('user-login', e => console.log(e.detail));
elemento.dispatchEvent(new CustomEvent('user-login', { detail: { id: 1 } }));
```

### Buenas prácticas

    Usa delegación siempre que puedas.

    Prefiere e.preventDefault() sobre return false (que además detiene propagación).

    Remueve listeners cuando ya no sean necesarios para evitar memory leaks.

    Para scroll y resize, usa { passive: true } para mejorar el rendimiento.

---
