# 🚪 Portals: Rompiendo la Jerarquía del DOM

Los **Portals** proporcionan una forma de renderizar componentes hijos en un nodo del DOM que existe fuera de la jerarquía del componente padre, pero manteniendo todas las capacidades de React (eventos, props y contexto).

---

## 🏗️ Sintaxis Básica

Se utiliza la función `createPortal` de la librería `react-dom`.

```jsx
import { createPortal } from 'react-dom';

function MyPortal({ children }) {
  // 1. Contenido a renderizar
  // 2. Nodo del DOM donde se inyectará
  return createPortal(
    children,
    document.getElementById('portal-root')
  );
}
```

---

## 🤔 ¿Por qué usar Portals?

Existen casos donde un componente hijo necesita "escapar" visualmente de su padre debido a restricciones de CSS como `z-index`, `overflow: hidden` o `position: relative`.

*   **Modales y Diálogos**: Deben aparecer por encima de todo el contenido.
*   **Tooltips y Popovers**: No deben quedar cortados por contenedores con scroll.
*   **Toasts y Notificaciones**: Suelen vivir en una capa global de la interfaz.

---

## 🚀 Implementación de un Modal

### 1. Preparar el HTML
En tu archivo `public/index.html`, añade un nodo hermano al `root`.

```html
<body>
  <div id="root"></div>
  <div id="modal-root"></div> <!-- Destino del Portal -->
</body>
```

### 2. Crear el componente Modal
```jsx
const Modal = ({ children, onClose }) => {
  return createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {children}
        <button onClick={onClose}>Cerrar</button>
      </div>
    </div>,
    document.getElementById('modal-root')
  );
};
function Modal({ children, onClose }) {
  return createPortal(
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        {children}
        <button onClick={onClose}>Cerrar</button>
      </div>
    </div>,
    document.getElementById('modal-root')
  );
}
```
-----

Event bubbling en Portals

Los eventos (onClick, etc.) siguen el árbol virtual de React, no el DOM. Si haces clic en el modal, el evento burbujea hacia arriba en el árbol de componentes React, no en el DOM real. Esto permite manejar eventos en el padre aunque el DOM esté fuera.
Portales y Context API

El contexto funciona a través de portales sin problemas porque el contexto se basa en el árbol de componentes React, no en el DOM.
jsx

<ThemeContext.Provider value="dark">
  <Modal>
    <ConsumerComponent /> {/*Recibe "dark" correctamente*/}
  </Modal>
</ThemeContext.Provider>

Múltiples portales

Puedes tener varios nodos destino (ej. #modal-root, #tooltip-root, #toast-root).
Alternativas a Portals

- En algunos casos, position: fixed y z-index alto puede funcionar sin portal si no hay contenedores con transform/overflow.

- Librerías como react-modal usan portales por defecto.

Buenas prácticas

- Limpia el portal al desmontar (React lo hace automáticamente, pero si agregas listeners manuales, límpialos).

- No abuses de portales (solo para elementos que necesitan romper la jerarquía).

- Asegúrate de que el nodo destino exista en el DOM antes de renderizar.

Renderizado en servidor (SSR)

Los portales no pueden renderizarse en servidor porque document.getElementById no existe. En SSR, debes evitar renderizar el portal o usar condiciones:
jsx

if (typeof window === 'undefined') return null;
return createPortal(..., document.getElementById('modal-root'));
---

## ⚡ Burbujeo de Eventos (Event Bubbling)

Aunque un portal se renderice en un lugar diferente del DOM, se comporta como un hijo normal en el **árbol de componentes de React**.

> [!IMPORTANT]
> Un evento disparado desde dentro de un Portal burbujeará hacia los ancestros en el árbol de React, incluso si esos elementos no son ancestros en el árbol del DOM real.

---

## ⚖️ Ventajas y Limitaciones

### ✅ Ventajas
*   **CSS Limpio**: Evita peleas complejas con `z-index`.
*   **Contexto**: El componente en el portal sigue teniendo acceso a los Providers de la aplicación principal.

### ❌ Desventajas / Limitaciones
*   **Accesibilidad**: Debes manejar manualmente el foco del teclado (trap focus) dentro del modal.
*   **SSR**: Los portales no funcionan en el servidor (Node.js) porque dependen del objeto `document`. Debes renderizarlos solo en el cliente.

---

## 💡 Buenas Prácticas

1.  **Detección de Cliente**: Comprueba que el código se ejecuta en el navegador antes de intentar acceder al DOM.
2.  **Limpieza**: Asegúrate de que el portal no deje residuos en el DOM si el componente se desmonta de forma abrupta.
3.  **Fragmentos**: Puedes usar portales dentro de fragmentos para inyectar múltiples elementos en diferentes partes del DOM desde un solo componente.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>