# higher-order-components.md

Un Higher-Order Component (HOC) es una función que recibe un componente y devuelve un nuevo componente mejorado. Es un patrón para reutilizar lógica entre componentes, común antes de los hooks.
Firma

```jsx
const EnhancedComponent = higherOrderComponent(WrappedComponent);
```

Ejemplo básico: HOC de logging

```jsx
function withLogger(WrappedComponent) {
  return function(props) {
    useEffect(() => {
      console.log(`Componente ${WrappedComponent.name} montado`);
      return () => console.log(`Componente ${WrappedComponent.name} desmontado`);
    }, []);
    return <WrappedComponent {...props} />;
  };
}
const UserPageWithLogger = withLogger(UserPage);
```

HOC que añade props

```jsx
function withUser(WrappedComponent) {
  return function(props) {
    const [user, setUser] = useState(null);
    useEffect(() => {
      fetchUser(props.userId).then(setUser);
    }, [props.userId]);
    return <WrappedComponent {...props} user={user} />;
  };
}

const UserProfileWithData = withUser(UserProfile);
```

Composición de HOCs

```jsx
const EnhancedComponent = withLogger(withUser(withTheme(BaseComponent)));
// o con una función compose (Redux)
import compose from 'lodash/fp/compose';
const EnhancedComponent = compose(withLogger, withUser, withTheme)(BaseComponent);
```

HOCs con configuración (fábrica de HOCs)

```jsx
function withFetch(url) {
  return function(WrappedComponent) {
    return function(props) {
      const [data, setData] = useState(null);
      useEffect(() => {
        fetch(url).then(res => res.json()).then(setData);
      }, []);
      return <WrappedComponent {...props} data={data} />;
    };
  };
}

const UserListWithFetch = withFetch('/api/users')(UserList);

```

Convenciones importantes

- Pasar props no relacionadas al componente envuelto (usar spread).

- Display name para debugging: WrappedComponent.displayName || 'Component'.

- No usar HOCs dentro de render (causa desmontado/montado constante).

- Ref forwarding con forwardRef.

```jsx
function withLogger(WrappedComponent) {
  const WithLogger = React.forwardRef((props, ref) => {
    // ... lógica
    return <WrappedComponent {...props} ref={ref} />;
  });
  WithLogger.displayName = `withLogger(${getDisplayName(WrappedComponent)})`;
  return WithLogger;
}

function getDisplayName(WrappedComponent) {
  return WrappedComponent.displayName || WrappedComponent.name || 'Component';
}
```

Ventajas

- Reutilización de lógica (antes de hooks).

- Composición de múltiples comportamientos.

- Aislamiento de lógica compleja.

Desventajas

- Wrapper hell (muchos niveles de componentes en React DevTools).

- Colisiones de props (dos HOCs pueden añadir la misma prop).

- Dificultad para tipar (TypeScript mejora, pero no es trivial).

- Menos legible que los hooks.

HOCs vs Hooks

|HOC|Hook|
|-|-|
|Envuelve el componente|Se llama dentro del componente|
|Puede causar wrapper hell|No añade componentes extra|
|Más difícil de componer|Fácil de componer funciones|
|Ideal para librerías (react-redux connect)|Ideal para lógica de aplicación|

¿Cuándo usar HOCs hoy?

- Librerías consolidadas (react-redux, react-router v5).

- Necesitas interceptar el ciclo de vida de un componente de manera no intrusiva.

- Código legacy que ya usa HOCs.

En proyectos nuevos, los custom hooks son la opción preferida.
