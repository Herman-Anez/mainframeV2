# 📡 forwardRef: Reenvío de Referencias

En React, las `refs` son tratadas de forma especial (al igual que las `keys`) y no se pasan automáticamente como una prop estándar a los componentes funcionales. `forwardRef` es la función que permite capturar una `ref` enviada por un componente padre y reenviarla a un elemento del DOM o a otro componente hijo interno.

---

## 🏗️ El Problema: Refs en Componentes Funcionales

Por defecto, si intentas pasar una `ref` a un componente funcional, React emitirá una advertencia y la `ref` será `null`.

```jsx
// ❌ Esto fallará
function MyInput(props) {
  return <input {...props} />;
}

const inputRef = useRef();
<MyInput ref={inputRef} />; // Error: ref no es una prop válida aquí
```

---

## 🚀 Solución con `forwardRef`

`forwardRef` envuelve el componente funcional y le proporciona la `ref` como un segundo argumento.

```jsx
import { forwardRef } from 'react';

const MyInput = forwardRef((props, ref) => {
  return (
    <div className="input-group">
      <label>{props.label}</label>
      {/* Reenviamos la ref al elemento real del DOM */}
      <input {...props} ref={ref} />
    </div>
  );
});

// Uso en el padre
function Parent() {
  const inputRef = useRef();

  const handleFocus = () => inputRef.current.focus();

  return (
    <>
      <MyInput ref={inputRef} label="Nombre" />
      <button onClick={handleFocus}>Enfocar Input</button>
    </>
  );
}
```

---

## 🖇️ Combinación con `useImperativeHandle`

A veces no quieres exponer todo el nodo del DOM, sino solo ciertos métodos de forma controlada.

```jsx
const CustomInput = forwardRef((props, ref) => {
  const localRef = useRef();

  useImperativeHandle(ref, () => ({
    focusAndSelect: () => {
      localRef.current.focus();
      localRef.current.select();
    },
    clear: () => {
      localRef.current.value = '';
    }
  }));

  return <input ref={localRef} {...props} />;
});
```

---

## 🛡️ Uso en HOCs (Higher-Order Components)

Si estás construyendo un HOC que envuelve a otros componentes, es una buena práctica usar `forwardRef` para asegurar que las `refs` lleguen al componente final y no se queden en el componente envoltorio.

---

## ⚖️ Ventajas y Limitaciones

### ✅ Ventajas
*   **Acceso al DOM**: Permite gestionar focos, selección de texto, animaciones y mediciones de tamaño desde el padre.
*   **Transparencia**: Hace que los componentes personalizados se comporten como elementos nativos del DOM respecto a las `refs`.

### ❌ Desventajas / Limitaciones
*   **Acoplamiento**: Rompe ligeramente el paradigma declarativo de React al permitir la manipulación directa del DOM desde fuera del componente.
*   **Complejidad**: Puede hacer que el código sea más difícil de seguir si se abusa de ello.

---

## 💡 Buenas Prácticas

1.  **Uso en Librerías**: Es casi obligatorio si estás construyendo una librería de componentes UI para que los usuarios puedan usar `refs`.
2.  **No abuses**: Si puedes resolver el problema mediante estado y props (flujo de datos hacia abajo), hazlo. La manipulación de `refs` debería ser el último recurso.
3.  **TypeScript**: Usa `forwardRef<TipoElemento, TipoProps>` para mantener la seguridad de tipos.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
