# 🎁 Props: Comunicación entre Componentes

Las **props** (propiedades) son el mecanismo principal para pasar datos de un componente padre a un componente hijo. Son la base de la arquitectura unidireccional de React.

> [!IMPORTANT]
> Las props son **de solo lectura** (inmutables). Un componente hijo nunca debe intentar modificar las props que recibe.

---

## 🚀 Uso Básico

```jsx
// Componente Padre
const App = () => {
  return <UserCard name="Elena" age={28} isAdmin={true} />;
};

// Componente Hijo
const UserCard = (props) => {
  return (
    <div className="card">
      <h3>{props.name}</h3>
      <p>Edad: {props.age}</p>
      {props.isAdmin && <span>⭐ Administrador</span>}
    </div>
  );
};
```

---

## ⚡ Desestructuración (Recomendado)

En lugar de usar `props.algo`, es una mejor práctica desestructurar directamente en los argumentos de la función para mayor claridad.

```jsx
const UserCard = ({ name, age, isAdmin }) => {
  return (
    <div>
      <h3>{name}</h3>
      <p>{age}</p>
    </div>
  );
};
```

---

## 🧩 Props Especiales: `children`

La prop `children` permite pasar contenido anidado a un componente, permitiendo crear "envoltorios" (wrappers).

```jsx
const Modal = ({ children, title }) => (
  <div className="modal">
    <h2>{title}</h2>
    <div className="modal-body">
      {children}
    </div>
  </div>
);

// Uso
<Modal title="Confirmación">
  <p>¿Estás seguro de que quieres borrar este archivo?</p>
  <button>Sí, borrar</button>
</Modal>
```

---

## 🛠️ Validación con PropTypes

Aunque hoy se suele usar **TypeScript**, `prop-types` es una librería estándar para validar que un componente reciba los datos correctos durante el desarrollo.

```jsx
import PropTypes from 'prop-types';

UserCard.propTypes = {
  name: PropTypes.string.isRequired,
  age: PropTypes.number,
  isAdmin: PropTypes.bool
};

UserCard.defaultProps = {
  isAdmin: false
};
```

----

## Props por defecto (defaultProps)

```tsx
```

function Boton({ texto = "Click" }) { ... }
// o externamente:
Boton.defaultProps = { texto: "Click" };

---

----

## 📏 Reglas de Oro

1. **Flujo Unidireccional**: Los datos viajan de padres a hijos. Si un hijo necesita enviar datos al padre, el padre debe pasar una **función callback** como prop.
2. **Inmutabilidad**: Si necesitas "cambiar" una prop, debe ser el padre quien actualice su estado y lo vuelva a pasar.
3. **Spread Operator (`...props`)**: Úsalos con precaución. Pasar demasiadas props automáticamente puede ocultar dependencias y causar bugs.

---

[⬅️ Volver al Índice](../README.md)
