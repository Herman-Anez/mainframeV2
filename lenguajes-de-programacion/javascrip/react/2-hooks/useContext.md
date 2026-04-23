# ⚓ useContext: Consumo de Estado Global

El hook `useContext` permite suscribirse a un contexto de React sin necesidad de anidamientos complejos o componentes de tipo "Consumer".

> [!IMPORTANT]
> `useContext` solo sirve para **consumir** el contexto. Para crear y proveer los datos, sigues necesitando `createContext` y un `Provider`.

---

## ⚖️ Auditoría de Contenido

> [!REDUNDANT]
> Este archivo tiene un solapamiento del 90% con [Context API (Gestión de Estado)](../3-state-management/context-api.md). 
> **Recomendación**: Mantener este archivo como una referencia rápida del **Hook** y usar el de Gestión de Estado para explicar la arquitectura completa y comparaciones con Redux.

---

## 🏗️ Implementación en 3 Pasos

### 1. Crear el Contexto

```jsx
// TemaContext.js
import { createContext } from 'react';
export const TemaContext = createContext('claro');
```

### 2. Proveer el Valor

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

### 3. Consumir con el Hook

```jsx
import { useContext } from 'react';
import { TemaContext } from './TemaContext';

function ComponenteHijo() {
  const tema = useContext(TemaContext);
  return <div className={`tema-${tema}`}>El tema actual es: {tema}</div>;
}
```

---

## 📊 Ventajas y Limitaciones

* **Ventaja**: Evita el "Prop Drilling" (pasar datos por niveles intermedios que no los necesitan).
* **Limitación**: Los cambios en el contexto re-renderizan a **todos** los consumidores. No es un sistema de gestión de estado optimizado para alta frecuencia de cambios.

---

## 💡 Buenas Prácticas

### Custom Hooks para Consumo

En lugar de importar el contexto en cada componente, exporta un hook personalizado para un código más limpio y seguro:

```jsx
export function useTema() {
  const context = useContext(TemaContext);
  if (!context) {
    throw new Error('useTema debe usarse dentro de un TemaProvider');
  }
  return context;
}
```

### Memoización del Valor

Para evitar re-renders innecesarios en los hijos cuando el proveedor se actualiza, memoiza el valor:

```jsx
const value = useMemo(() => ({ user, login }), [user]);
return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
```

---

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
----

[⬅️ Volver al Índice](../README.md)
