# ⚖️ useReducer: Gestión de Estados Complejos

`useReducer` es una alternativa a `useState` para manejar estados con múltiples sub-valores o transiciones que dependen de acciones predefinidas. Sigue un patrón similar a Redux.

---

## 🏗️ Sintaxis Básica

```jsx
const [state, dispatch] = useReducer(reducer, initialState, init);
```

* **`reducer`**: Función pura `(state, action) => newState`.
* **`initialState`**: El valor inicial del estado.
* **`dispatch`**: Función para enviar acciones al reducer.

---

## 🚀 Ejemplo Práctico: Contador

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

Acciones con payload

```jsx
function reducer(state, action) {
  switch (action.type) {
    case 'set':
      return { count: action.payload };
    default:
      return state;
  }
}
// uso
dispatch({ type: 'set', payload: 10 });
```

Inicialización diferida

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

1. **Lógica compleja**: Cuando el estado es un objeto con múltiples campos.
2. **Acciones predecibles**: Quieres centralizar la lógica de actualización fuera del componente.
3. **Optimización**: Al pasar `dispatch` a componentes hijos, no cambia entre renders (referencia estable).

---

## 🔗 Combinación con useContext (Mini-Redux)

Este es un patrón muy común para evitar el prop-drilling en aplicaciones medianas.

```jsx
const AppContext = createContext();

function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);
  
  // Memoizamos el valor para evitar re-renders innecesarios
  const value = useMemo(() => ({ state, dispatch }), [state]);

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}
```

---

## 📏 Reglas de Oro

* **Reducers Puros**: No hagas llamadas a APIs ni uses `Math.random()` dentro del reducer.
* **Inmutabilidad**: Nunca mutes el `state` directamente; siempre devuelve un objeto nuevo (usa el spread operator `...state`).
* **Acciones Descriptivas**: Usa el estándar `{ type: 'ACTION_NAME', payload: data }`.

---
Buenas prácticas

- Los reducers deben ser puros (sin efectos secundarios, sin mutar state).

- Usa constantes para los tipos de acción (ej. const INCREMENT = 'increment').

- Separa reducers en archivos diferentes para lógica compleja.

Comparación de rendimiento

useReducer evita pasar callbacks por muchos niveles (en lugar de setState puedes pasar dispatch). Es más eficiente para actualizaciones profundas.

---

[⬅️ Volver al Índice](../README.md)
