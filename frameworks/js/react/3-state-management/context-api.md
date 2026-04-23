# 🌐 Context API: Gestión de Estado Global

Context API es una característica nativa de React que permite compartir datos globalmente sin tener que pasar props manualmente en cada nivel. Es la solución ideal para evitar el "Prop Drilling".

---

## ⚖️ Auditoría de Contenido

> [!REDUNDANT]
> Este archivo tiene un solapamiento del 90% con [useContext (Hook)](../2-hooks/useContext.md).
> **Conveniencia**: Conviene **combinar** estas secciones en un solo archivo "Arquitectura de Contexto" para evitar inconsistencias. Este archivo es superior en cuanto a la comparación con Redux y arquitectura.

---

## 🏗️ Flujo de Implementación

### 1. Creación del Contexto

```jsx
import { createContext } from 'react';
const UserContext = createContext(null);
```

### 2. Proveedor (Provider)

```jsx
function App() {
  const [user, setUser] = useState(null);
  
  // Optimizamos el valor con useMemo
  const value = useMemo(() => ({ user, setUser }), [user]);

  return (
    <UserContext.Provider value={value}>
      <Dashboard />
    </UserContext.Provider>
  );
}
```

### 3. Consumo (useContext)

```jsx
import { useContext } from 'react';
function Avatar() {
  const { user } = useContext(UserContext);
  return <img src={user?.avatar} alt="User Avatar" />;
}
```

----
ontexto con estado complejo y reducción de re-renderizados

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

---

## ⚔️ Context API vs Redux

| Característica | Context API | Redux / Zustand |
| :--- | :--- | :--- |
| **Nativo** | ✅ Sí | ❌ No |
| **Complejidad** | Baja | Media / Alta |
| **Rendimiento** | Re-renderiza todos los consumidores | Actualizaciones selectivas |
| **Uso Ideal** | Datos estáticos o poco frecuentes | Lógica compleja, alto rendimiento |

---

## 💡 Buenas Prácticas

1. **Contextos Atómicos**: No creas un "AppContext" gigante. Divide por dominios (`UserContext`, `ThemeContext`, `CartContext`).
2. **Custom Hooks**: Siempre expón un hook como `useUser()` para consumir el contexto de forma segura.
3. **Seguridad**: Valida siempre que el hook se use dentro de su Provider correspondiente.

```jsx
export function useUser() {
  const context = useContext(UserContext);
  if (!context) throw new Error('useUser debe usarse dentro de UserProvider');
  return context;
}
```

---

## ⚠️ Limitaciones

- **Rendimiento**: No es adecuado para datos que cambian miles de veces por segundo (como la posición del ratón en un canvas).
- **Depuración**: No tiene herramientas de inspección tan potentes como Redux DevTools.

- No es adecuado para rendimiento crítico con miles de actualizaciones por segundo (usa Zustand o Jotai).

- El provider debe envolver todo el árbol que necesite acceso.

---

[⬅️ Volver al Índice](../README.md)
