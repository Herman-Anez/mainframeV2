# Eventos y Delegación

Los eventos son el puente entre la interacción del usuario y la lógica de nuestra aplicación. Permiten reaccionar a clics, pulsaciones de teclas, desplazamientos y cambios de estado en el navegador.

---

## Registro de Manejadores

### `addEventListener` (Recomendado)
Es el estándar moderno. Permite asociar múltiples funciones al mismo evento en un solo elemento sin sobrescribirlas.

```javascript
const boton = document.querySelector('#btn-accion');

function manejarClick(event) {
  console.log('Botón pulsado');
}

boton.addEventListener('click', manejarClick);

// Para removerlo, se requiere la referencia a la misma función
boton.removeEventListener('click', manejarClick);
```

> [!TIP]
> Puedes usar el objeto de opciones para configurar el comportamiento:
> *   `once: true`: El evento se dispara una sola vez y se elimina.
> *   `passive: true`: Mejora el rendimiento al indicar que no se usará `preventDefault()`.

---

## El Objeto de Evento (`event`)

Al dispararse un evento, el navegador pasa automáticamente un objeto con información detallada al manejador.

*   **`event.target`**: El elemento exacto que originó el evento.
*   **`event.currentTarget`**: El elemento al que se le asignó el listener.
*   **`event.preventDefault()`**: Cancela la acción por defecto (ej. evitar que un formulario se envíe).
*   **`event.stopPropagation()`**: Detiene el "burbujeo" del evento hacia los elementos padre.

---

## Propagación: Burbujeo y Captura

Cuando ocurre un evento en un elemento anidado, este viaja por el DOM en tres fases:

1.  **Fase de Captura (Capture):** El evento baja desde `window` hasta el elemento objetivo.
2.  **Fase de Objetivo (Target):** El evento se activa en el elemento real donde ocurrió la acción.
3.  **Fase de Burbujeo (Bubbling):** El evento sube desde el elemento objetivo hacia los ancestros hasta llegar a `window`.

> [!NOTE]
> Por defecto, `addEventListener` escucha en la fase de **burbujeo**. Para escuchar en captura, debes pasar `true` o `{ capture: true }` como tercer argumento.

---

## Delegación de Eventos

Esta técnica consiste en aprovechar el **burbujeo** para colocar un único listener en un elemento padre en lugar de múltiples listeners en sus hijos.

```javascript
const lista = document.querySelector('#mi-lista');

lista.addEventListener('click', (event) => {
  // Comprobamos si el clic fue en un botón de borrar
  if (event.target.classList.contains('btn-borrar')) {
    const item = event.target.closest('li');
    item.remove();
  }
});
```

### Ventajas de la Delegación
*   **Ahorro de Memoria:** Menos manejadores de eventos creados.
*   **Flexibilidad:** Funciona automáticamente con elementos añadidos al DOM en el futuro.
*   **Mantenibilidad:** El código está centralizado en un solo lugar.

---

## Eventos Personalizados

Podemos crear eventos propios para comunicar componentes o partes de nuestra aplicación de forma desacoplada.

```javascript
const loginEvent = new CustomEvent('app:login', {
  detail: { usuarioId: 123, rol: 'admin' }
});

document.dispatchEvent(loginEvent);

// Escuchando el evento
document.addEventListener('app:login', (e) => {
  console.log('Sesión iniciada por:', e.detail.usuarioId);
});
```

---

## Buenas Prácticas

1.  **Usa Delegación:** Siempre que gestiones listas dinámicas o muchos elementos similares.
2.  **Limpia Listeners:** Elimina los manejadores de eventos cuando destruyas elementos dinámicos o cambies de vista (especialmente en SPAs) para evitar fugas de memoria.
3.  **No abuses de `stopPropagation`:** Detener la propagación puede romper otras funcionalidades globales que dependan de detectar clics en el documento.
4.  **Eventos Pasivos:** Úsalos en eventos de alta frecuencia como `scroll` o `touchmove` para asegurar una experiencia de usuario fluida.

---
[Volver al Índice](../js-index.md)
