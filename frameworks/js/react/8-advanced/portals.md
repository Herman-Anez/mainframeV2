

📄 8-advanced/portals.md
Concepto

Portals permiten renderizar un componente hijo en un nodo del DOM diferente al del componente padre, manteniendo el contexto de React (eventos, props, contexto).

Sintaxis

```jsx
import { createPortal } from 'react-dom';

function Modal({ children, isOpen }) {
  if (!isOpen) return null;
  return createPortal(
    <div className="modal-overlay">
      <div className="modal-content">{children}</div>
    </div>,
    document.getElementById('modal-root') // nodo destino
  );
}
```

¿Por qué usar Portals?

- Modales, tooltips, toasts, menús desplegables: deben romper la jerarquía visual (z-index, overflow hidden) pero mantener la lógica de React (props, eventos, contexto).

- Evitar problemas de CSS donde el padre tenga overflow: hidden o z-index limitado.

Configuración del nodo destino

En public/index.html:
html

<body>
  <div id="root"></div>
  <div id="modal-root"></div>
</body>

Ejemplo completo de Modal con Portal
jsx

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

function App() {
  const [showModal, setShowModal] = useState(false);
  return (
    <div style={{ overflow: 'hidden' }}> {/*No afecta al modal*/}
      <button onClick={() => setShowModal(true)}>Abrir modal</button>
      {showModal && (
        <Modal onClose={() => setShowModal(false)}>
          <h2>Contenido del modal</h2>
        </Modal>
      )}
    </div>
  );
}

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