# ⚡ Eventos: Interactividad en React

El manejo de eventos en React es muy similar al manejo de eventos en elementos del DOM, pero con algunas diferencias sintácticas clave para alinearse con JavaScript y JSX.

---

## 🏗️ Sintaxis Básica

Los eventos en React se nombran usando **camelCase** (ej: `onClick`) en lugar de minúsculas, y se pasa una **función** como manejador en lugar de un string.

```jsx
<button onClick={handleClick}>Click</button>
```

---

## 🚀 Definir Manejadores

```jsx
function MiComponente() {
  function handleClick(e) {
    e.preventDefault();  // Previene el comportamiento por defecto (ej: recarga de página)
    console.log('Botón clickeado');
  }

  return <button onClick={handleClick}>Click aquí</button>;
}
```

---

## ⚖️ Diferencias con HTML Nativo

*   **Declarativo**: No se usa `addEventListener`. El evento se declara directamente en el JSX.
*   **Evento Sintético**: El objeto `e` es un **SyntheticEvent**. React envuelve el evento nativo para garantizar que funcione exactamente igual en todos los navegadores.

---

## 🖇️ Paso de Parámetros

Si necesitas pasar un argumento extra a la función manejadora, usa una función flecha:

```jsx
<button onClick={() => eliminarItem(id)}>Eliminar</button>
```

> [!WARNING]
> Crear funciones flecha directamente en el render puede afectar el rendimiento en componentes de gran tamaño. Para casos críticos, considera usar el hook `useCallback`.

---

## 📋 Eventos en Formularios

En React, los formularios suelen ser **Componentes Controlados**, donde el estado de React es la "única fuente de verdad".

```jsx
const [texto, setTexto] = useState('');

function handleChange(e) {
  setTexto(e.target.value);
}

<input type="text" value={texto} onChange={handleChange} />;
```

---

## 💡 Eventos Comunes

React soporta casi todos los eventos nativos:
*   **Mouse**: `onClick`, `onMouseEnter`, `onMouseLeave`.
*   **Teclado**: `onKeyDown`, `onKeyUp`, `onFocus`, `onBlur`.
*   **Formularios**: `onChange`, `onSubmit`, `onInput`.

---

## 🛡️ Propagación y Acción por Defecto

Los métodos `e.preventDefault()` y `e.stopPropagation()` funcionan exactamente igual que en el DOM nativo para detener el comportamiento del navegador o la burbuja del evento.

---

## 💡 Buenas Prácticas

*   **Extraer Lógica**: Mantén el JSX limpio extrayendo los manejadores de eventos a funciones con nombre antes del `return`.
*   **Eventos Personalizados**: React no permite eventos personalizados nativos; en su lugar, se pasan **props callback** (ej: `onUserLogin={handleLogin}`).

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>

