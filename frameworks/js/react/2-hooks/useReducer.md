# ⚖️ useReducer: Gestión de Estados Complejos

`useReducer` es una alternativa a `useState` para manejar estados con múltiples sub-valores o transiciones que dependen de acciones predefinidas. Sigue un patrón similar a Redux.

---

## 🏗️ Sintaxis Básica

```jsx
const [state, dispatch] = useReducer(reducer, initialState, init);
```

*   **`reducer`**: Función pura `(state, action) => newState`.
*   **`initialState`**: El valor inicial del estado.
*   **`dispatch`**: Función para enviar acciones al reducer.
*   **`init`**: (Opcional) Función para inicialización diferida.

---

## 🚀 Implementación y Flujo

### 1. Ejemplo Práctico: Contador

```jsx
const initialState = { count: 0 };

function reducer(state, action) {
  switch (action.type) {
    case 'increment': return { count: state.count + 1 };
    case 'decrement': return { count: state.count - 1 };
    case 'reset': return { count: 0 };
    default: throw new Error('Acción no soportada');
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </>
  );
}
```

### 2. Acciones con Payload
Útil para pasar datos adicionales a la lógica de actualización.

```jsx
dispatch({ type: 'set', payload: 10 });

// En el reducer
case 'set':
  return { count: action.payload };
```

### 3. Inicialización Diferida
Útil para resetear el estado o cuando el estado inicial depende de una prop.

```jsx
function init(initialCount) {
  return { count: initialCount };
}
const [state, dispatch] = useReducer(reducer, initialCount, init);
```

¿Cuándo usar useReducer sobre useState?

- Cuando el próximo estado depende del anterior de forma compleja.

- Cuando tienes múltiples campos que se actualizan juntos (ej. formulario grande).

- Cuando la lógica de actualización es difícil de seguir con varios useState.

- Prefieres un patrón de acciones predecible.


---

## 🎯 ¿Cuándo usar useReducer?

> [!TIP]
> Si tu estado tiene más de 3 variables que cambian juntas, o si la lógica del próximo estado depende fuertemente del anterior, `useReducer` es tu mejor amigo.

*   **Lógica Compleja**: Cuando el estado es un objeto con múltiples campos que se actualizan juntos (ej. formularios grandes).
*   **Predecibilidad**: Quieres centralizar la lógica de actualización fuera del cuerpo del componente.
*   **Rendimiento**: Evita pasar múltiples callbacks por props; puedes pasar un único `dispatch` que tiene referencia estable.
*   **Lógica de Negocio**: Cuando la transición de estado es difícil de seguir con múltiples `useState`.

---

## 🛡️ Patrón: Combinación con useContext (Mini-Redux)

Para aplicaciones medianas, este patrón es ideal para evitar el prop-drilling sin añadir una librería externa.

```jsx
const AppContext = createContext();

function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);
  
  // Memoizamos el valor para evitar re-renders innecesarios en consumidores
  const value = useMemo(() => ({ state, dispatch }), [state]);

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}
```

---

## 📏 Reglas y Buenas Prácticas

*   **Reducers Puros**: No hagas llamadas a APIs, mutaciones de variables externas ni uses `Math.random()` dentro del reducer.
*   **Inmutabilidad**: Nunca mutes el `state` directamente; devuelve siempre un nuevo objeto usando el spread operator (`...state`).
*   **Acciones Descriptivas**: Usa constantes para los tipos de acción (ej. `const INCREMENT = 'increment'`) y el estándar `{ type, payload }`.
*   **Separación de Lógica**: Para reducers muy grandes, sepáralos en archivos independientes para mejorar la legibilidad.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>

