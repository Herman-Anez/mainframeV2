# 🏗️ HOCs: Higher-Order Components

Un **Higher-Order Component (HOC)** es una función que recibe un componente y devuelve un nuevo componente "mejorado". Es un patrón de diseño avanzado para reutilizar lógica entre componentes, extremadamente común antes de la llegada de los hooks y aún presente en muchas librerías.

---

## 🏗️ Estructura Fundamental

```jsx
const EnhancedComponent = withExtraLogic(BaseComponent);
```

### 🚀 Ejemplo 1: HOC de Logging
Ideal para monitorizar cuándo se montan y desmontan componentes de manera genérica.

```jsx
function withLogger(WrappedComponent) {
  return function(props) {
    useEffect(() => {
      console.log(`📊 Componente ${WrappedComponent.name} montado`);
      return () => console.log(`🗑️ Componente ${WrappedComponent.name} desmontado`);
    }, []);

    return <WrappedComponent {...props} />;
  };
}

const UserPageWithLogger = withLogger(UserPage);
```

---

## 🖇️ Inyección de Props

Los HOCs suelen usarse para "inyectar" datos o funcionalidades adicionales al componente envuelto.

```jsx
function withUser(WrappedComponent) {
  return function(props) {
    const [user, setUser] = useState(null);

    useEffect(() => {
      fetchUser(props.userId).then(setUser);
    }, [props.userId]);

    // Pasamos las props originales y el nuevo dato 'user'
    return <WrappedComponent {...props} user={user} />;
  };
}

const UserProfileWithData = withUser(UserProfile);
```

---

## 🌀 Composición de Múltiples HOCs

Puedes aplicar varios HOCs al mismo componente anidándolos.

```jsx
const Enhanced = withLogger(withTheme(withUser(MyComponent)));

// Con Redux o Lodash 'compose'
const Enhanced = compose(
  withLogger,
  withTheme,
  withUser
)(MyComponent);
```

---

## 📏 Reglas y Convenciones

1.  **Reenviar Props**: Usa el spread operator `{...props}` para asegurar que el componente final reciba todas las props originales.
2.  **Display Name**: Facilita el debugging añadiendo un nombre descriptivo para las React DevTools.
3.  **Ref Forwarding**: Si necesitas acceder a la instancia del componente envuelto, usa `React.forwardRef`.
4.  **No usar dentro del `render`**: Crea el componente mejorado **fuera** de la función del componente principal, o React lo recreará en cada renderizado (rompiendo el estado).

```jsx
// ✅ Correcto: Nombre descriptivo para debugging
WithLogger.displayName = `withLogger(${WrappedComponent.name})`;
```

---

## ⚖️ HOCs vs Hooks

| Característica | HOC | Hook |
| :--- | :--- | :--- |
| **Estructura** | Envuelve el componente (Wrapper) | Se llama dentro del componente |
| **Jerarquía** | Crea "Wrapper Hell" | Plana y limpia |
| **Lógica** | Ideal para inyectar props fijas | Ideal para lógica dinámica y local |
| **Composición** | Anidamiento complejo | Secuencial y sencilla |

---

## 💡 ¿Cuándo usar HOCs hoy?

Aunque la mayoría de los casos de uso han sido reemplazados por **Custom Hooks**, los HOCs siguen siendo útiles en:
*   **Librerías de Terceros**: Como `connect` de React-Redux o `withRouter` de versiones antiguas de React Router.
*   **Interceptación de Ciclo de Vida**: Cuando necesitas que un componente se comporte de cierta manera sin modificar su código interno.
*   **Mantenimiento**: En bases de código heredadas (Legacy Code).

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
