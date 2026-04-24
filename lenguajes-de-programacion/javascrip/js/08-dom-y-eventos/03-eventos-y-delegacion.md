# Eventos y Delegación

Los eventos permiten que nuestras aplicaciones reaccionen a las interacciones del usuario o a cambios en el estado del navegador.

---

## Registrar manejadores de eventos

### Propiedades *on-event* (`onclick`, `onchange`)

```js
elemento.onclick = function(evento) { 
  // lógica aquí 
};
```

- **Limitación:** Solo permiten un manejador por evento (el último sobrescribe al anterior).
- **Recomendación:** No se recomienda su uso en aplicaciones modernas.

### `addEventListener` y `removeEventListener`

Es la forma estándar y recomendada de gestionar eventos.

```js
function manejarClick(e) {
  console.log('Elemento clickeado:', e.target);
}

// Registro
elemento.addEventListener('click', manejarClick);

// Eliminación (requiere la referencia a la función original)
elemento.removeEventListener('click', manejarClick);
```

- **Ventajas:** Permite múltiples escuchadores para el mismo evento.
- **Opciones avanzadas:** Acepta un tercer argumento opcional (`options` o un booleano `useCapture`).
    - `once: true`: El listener se elimina automáticamente tras ejecutarse una vez.
    - `passive: true`: Indica que el listener no llamará a `preventDefault()`, mejorando el rendimiento en eventos de alta frecuencia como `scroll`.

---

## El objeto de evento (`e`)

Cada manejador recibe automáticamente un objeto con información detallada:

- **`e.target`**: El elemento exacto que originó el evento (el más profundo en el árbol).
- **`e.currentTarget`**: El elemento al que se ha asociado el listener (muy útil en delegación).
- **`e.type`**: El nombre del evento (ej: `'click'`).
- **`e.preventDefault()`**: Cancela el comportamiento por defecto del navegador (ej: evitar que un link navegue o un form se envíe).
- **`e.stopPropagation()`**: Detiene la propagación del evento hacia los ancestros (burbujeo).
- **`e.stopImmediatePropagation()`**: Detiene la propagación y evita que se ejecuten otros listeners del mismo tipo en el elemento actual.

---

## Fases de propagación

Cuando ocurre un evento, este recorre tres fases:

1. **Fase de captura:** Desde `window` hacia el elemento objetivo (*target*).
2. **Fase de target:** El evento llega al elemento donde ocurrió la acción.
3. **Fase de burbujeo (Bubbling):** El evento sube desde el elemento objetivo de vuelta hacia `window`.

> [!NOTE]
> Por defecto, los listeners se registran en la **fase de burbujeo**. Para usar la fase de captura, se debe pasar `true` o `{ capture: true }` como tercer argumento.

---

## Delegación de eventos

Es una técnica optimizada que consiste en colocar un único listener en un ancestro común en lugar de muchos listeners en elementos hijos individuales. Se utiliza `e.target` para identificar qué hijo disparó el evento.

```js
lista.addEventListener('click', (e) => {
  if (e.target.matches('li button')) {
    const item = e.target.closest('li');
    console.log('Botón clickeado en el elemento:', item);
  }
});
```

- **Esencial para:** Elementos creados dinámicamente.
- **Ventajas:** Menor uso de memoria (menos listeners) y código más limpio.

---

## Eventos comunes

- **Ratón:** `click`, `dblclick`, `mousedown`, `mouseup`, `mousemove`, `mouseover`, `mouseout`, `mouseenter`, `mouseleave`.
- **Teclado:** `keydown`, `keyup` (usar `e.key` o `e.code`).
- **Formulario:** `submit`, `change`, `input`, `focus`, `blur`, `focusin`, `focusout`.
- **Documento/Ventana:** `DOMContentLoaded` (DOM listo), `load` (todo cargado), `resize`, `scroll`, `beforeunload`.
- **Táctil:** `touchstart`, `touchmove`, `touchend`.

---

## Eventos personalizados

Podemos crear y disparar nuestros propios eventos mediante `CustomEvent`.

```js
const loginEvent = new CustomEvent('user-login', { 
  detail: { id: 1, name: 'Admin' } 
});

elemento.addEventListener('user-login', e => console.log(e.detail));
elemento.dispatchEvent(loginEvent);
```

---

## Buenas prácticas

- **Delegación:** Úsala siempre que gestiones múltiples elementos similares o dinámicos.
- **Prevención:** Prefiere `e.preventDefault()` sobre `return false`.
- **Limpieza:** Remueve los listeners cuando ya no sean necesarios para evitar fugas de memoria (*memory leaks*).
- **Rendimiento:** Usa `{ passive: true }` en eventos de `scroll` y `resize` para una experiencia más fluida.
