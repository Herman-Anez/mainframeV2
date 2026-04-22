# redux.md

Redux es una librería de gestión de estado global predecible basada en el patrón Flux. Se usa frecuentemente con React a través de react-redux.

## Principios fundamentales

- Única fuente de verdad: el estado global vive en un solo store.

- El estado es de solo lectura: solo se modifica emitiendo acciones.

- Los cambios se hacen con funciones puras (reducers).

## Flujo básico de Redux

text

Componente → dispatch(action) → Reducer → Nuevo estado → Componente se actualiza

Núcleo de Redux (sin React)

```jsx
import { createStore } from 'redux';

// Reducer
const contadorReducer = (state = 0, action) => {
  switch (action.type) {
    case 'INCREMENTAR': return state + 1;
    case 'DECREMENTAR': return state - 1;
    default: return state;
  }
};
// Store
const store = createStore(contadorReducer);

// Dispatch
store.dispatch({ type: 'INCREMENTAR' });

// Suscripción
store.subscribe(() => console.log(store.getState()));
```

## Redux con React (react-redux)

### Proveer el store

```jsx
import { Provider } from 'react-redux';
import { store } from './store';

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);
```


### Conectar un componente (hooks modernos)

```jsx
import { useSelector, useDispatch } from 'react-redux';

function Contador() {
  const count = useSelector(state => state.contador);
  const dispatch = useDispatch();
  return (
    <div>
      {count}
      <button onClick={() => dispatch({ type: 'INCREMENTAR' })}>+</button>
    </div>
  );
}
```


Redux Toolkit (recomendado hoy)

Simplifica la configuración, reduce boilerplate.

```jsx
import { configureStore, createSlice } from '@reduxjs/toolkit';

const contadorSlice = createSlice({
  name: 'contador',
  initialState: 0,
  reducers: {
    incrementar: state => state + 1,
    decrementar: state => state - 1,
    incrementarPor: (state, action) => state + action.payload,
  },
});

export const { incrementar, decrementar, incrementarPor } = contadorSlice.actions;
export const store = configureStore({ reducer: contadorSlice.reducer });
```


En el componente:

```jsx
import { incrementar } from './store';
dispatch(incrementar());
```


## Middleware (ej. Redux Thunk para acciones asíncronas)

```jsx
const fetchUser = (id) => async (dispatch) => {
  dispatch({ type: 'FETCH_USER_REQUEST' });
  try {
    const response = await fetch(`/users/${id}`);
    const data = await response.json();
    dispatch({ type: 'FETCH_USER_SUCCESS', payload: data });
  } catch (error) {
    dispatch({ type: 'FETCH_USER_FAILURE', error });
  }
};
```


Buenas prácticas

- Usa Redux Toolkit siempre.

- Mantén los reducers planos y combínalos con combineReducers.

- No guardes datos derivados o no serializables (clases, funciones) en el store.

- Usa Selectors memoizados con createSelector (Reselect) para evitar cálculos innecesarios.

Cuándo usar Redux

- Estado global muy complejo y compartido por muchos componentes.

- Actualizaciones frecuentes (colaboración en tiempo real, juegos).

- Necesitas time-travel debugging o persistencia avanzada.

- Equipo grande que requiere patrones estrictos.

Alternativas modernas más ligeras

- Zustand (siguiente archivo), Jotai, Recoil.
