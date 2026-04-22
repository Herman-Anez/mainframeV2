# context-api.md

Context API es una característica nativa de React que permite compartir datos globalmente sin tener que pasar props manualmente en cada nivel.
Creación y uso (repaso pero más profundo)

## Crear contexto

```jsx
import { createContext } from 'react';
const UserContext = createContext(null);
```

## Proveedor

```jsx
function App() {
  const [user, setUser] = useState(null);
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Dashboard />
    </UserContext.Provider>
  );
}
```

## Consumir en cualquier componente hijo

```jsx
import { useContext } from 'react';
function Avatar() {
  const { user } = useContext(UserContext);
  return <img src={user?.avatar} />;
}
```

Contexto con estado complejo y reducción de re-renderizados

Por defecto, cualquier cambio en el value del provider provoca que todos los consumidores se re-rendericen. Para evitarlo:

- Contextos separados para datos que cambian independientemente.

- Memoizar el value con useMemo:

```jsx
const value = useMemo(() => ({ user, setUser }), [user]);
<UserContext.Provider value={value}>...</UserContext.Provider>
```

Contexto múltiple (anidado)

Puedes tener contextos de tema, autenticación, preferencias, etc., anidados.
Contexto + useReducer (mini Redux)

```jsx
const StoreContext = createContext();
function StoreProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  const value = useMemo(() => ({ state, dispatch }), [state]);
  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>;
}
// Uso
const { state, dispatch } = useContext(StoreContext);
```

Contexto vs Redux

|Contexto|Redux|
|-|-|
|Nativo de React|Librería externa|
|Bueno para datos estáticos o poco frecuentes|Para lógica compleja y actualizaciones frecuentes|
|Re-renderiza todos los consumidores por defecto|Actualizaciones selectivas|
|Sin herramientas de debugging avanzadas|DevTools potentes|

## Buenas prácticas

- Crear custom hooks para consumir contexto (ej. useUser()).

- Validar que el hook se use dentro del provider:

```jsx
export function useUser() {
 const context = useContext(UserContext);
  if (!context) throw new Error('useUser must be used within UserProvider');
  return context;
}
```

- No meter datos que cambian muy rápido (ej. posición del mouse) en un contexto grande.

- Dividir contextos por dominio (UserContext, ThemeContext, etc.).

Limitaciones

- No es adecuado para rendimiento crítico con miles de actualizaciones por segundo (usa Zustand o Jotai).

- El provider debe envolver todo el árbol que necesite acceso.
