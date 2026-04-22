# useReducer.md

Concepto

useReducer es una alternativa a useState para manejar estados complejos con múltiples sub-valores o transiciones que dependen de acciones. Está inspirado en Redux.
Sintaxis

```jsx
const [state, dispatch] = useReducer(reducer, initialState, init);
```

- reducer: función pura (state, action) => newState.

- initialState: valor inicial.

- init (opcional): función para inicialización diferida.

Ejemplo básico: contador

```jsx
```

const initialState = { count: 0 };

function reducer(state, action) {
  switch (action.type) {
    case 'increment': return { count: state.count + 1 };
    case 'decrement': return { count: state.count - 1 };
    case 'reset': return initialState;
    default: throw new Error();
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <>
      Count: {state.count}
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
    </>
  );
}

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

Combinación con useContext (mini Redux)

```jsx
const AppContext = createContext();

function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);
  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}
```

Tipado con TypeScript (útil aunque no obligatorio)

```tsx
type State = { count: number };
type Action = { type: 'increment' } | { type: 'decrement' };

const reducer = (state: State, action: Action): State => { ... };
```

Buenas prácticas

- Los reducers deben ser puros (sin efectos secundarios, sin mutar state).

- Usa constantes para los tipos de acción (ej. const INCREMENT = 'increment').

- Separa reducers en archivos diferentes para lógica compleja.

Comparación de rendimiento

useReducer evita pasar callbacks por muchos niveles (en lugar de setState puedes pasar dispatch). Es más eficiente para actualizaciones profundas.
