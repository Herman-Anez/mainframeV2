# useContext.md

## Concepto

useContext permite consumir un contexto creado con React.createContext sin necesidad de usar Context.Consumer o anidar componentes.

## Creación del contexto

```jsx
// TemaContext.js
import { createContext } from 'react';
export const TemaContext = createContext('claro'); // valor por defecto
```

## Proveer el contexto

```jsx
import { TemaContext } from './TemaContext';

function App() {
  return (
    <TemaContext.Provider value="oscuro">
      <ComponenteHijo />
    </TemaContext.Provider>
  );
}
```

## Consumir con useContext

```jsx
import { useContext } from 'react';
import { TemaContext } from './TemaContext';

function ComponenteHijo() {
  const tema = useContext(TemaContext);
  return <div className={`tema-${tema}`}>Contenido</div>;
}
```

## Contexto con estado mutable

```jsx
const AuthContext = createContext(null);

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const login = (userData) => setUser(userData);
  const logout = () => setUser(null);
  
  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
```

### Ventajas

- Evita props drilling (pasar props por muchos niveles).

- Centraliza datos globales: tema, autenticación, idioma, etc.

### Desventajas y limitaciones

- No es un sistema de gestión de estado completo: los cambios en el contexto causan re-render de todos los consumidores, sin mecanismo de memoización por defecto.

- Para rendimiento, combínalo con useMemo en el valor del provider.

```jsx
<AuthContext.Provider value={value}>
const value = useMemo(() => ({ user, login, logout }), [user]);
```

## Contexto múltiple

Puedes anidar varios providers. Cada useContext obtiene el contexto más cercano en el árbol.
Uso con useReducer (mini Redux)

```jsx
const StoreContext = createContext();

function StoreProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <StoreContext.Provider value={{ state, dispatch }}>
      {children}
    </StoreContext.Provider>
  );
}
```

## Buenas prácticas

- Crear contextos específicos (no un solo contexto gigante).

- Exportar un custom hook para consumir el contexto (más limpio):

```jsx
```

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth debe usarse dentro de AuthProvider');
  return context;
