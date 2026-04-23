# ⚛️ Redux & Redux Toolkit (RTK)

Redux es una librería para la gestión del estado global de las aplicaciones. Es conocida por su arquitectura predecible y estricta, basada en el patrón **Flux**.

> [!IMPORTANT]
> Hoy en día, **Redux Toolkit (RTK)** es la forma oficial y recomendada de escribir lógica de Redux. Elimina el "boilerplate" excesivo del Redux clásico.

---

## 🏗️ Principios Fundamentales

1. **Única fuente de verdad**: Todo el estado de tu aplicación vive en un solo objeto (Store).
2. **El estado es de solo lectura**: La única forma de cambiar el estado es emitiendo una **Acción**.
3. **Cambios con funciones puras**: Los **Reducers** especifican cómo cambian las acciones al estado.

---

## 🏗️ Flujo básico de Redux

```text
Componente → dispatch(action) → Reducer → Nuevo estado → Componente se actualiza
```

---

## 🏛️ Núcleo de Redux (Vanilla / Sin React)

> [!NOTE]
> Este es el núcleo conceptual. Aunque hoy se usa RTK, entender el `createStore` y el `dispatch` manual es vital para comprender cómo funciona Redux bajo el capó.

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

---

## 🛠️ Redux Toolkit (La forma moderna)

RTK simplifica radicalmente la creación de Redux. Usa `createSlice` para definir reducers y acciones en un solo lugar.

```jsx
import { createSlice, configureStore } from '@reduxjs/toolkit';

// 1. Definir un "Slice"
const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => {
      // RTK permite "mutar" el estado internamente gracias a Immer.js
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    }
  }
});

// 2. Exportar acciones y el store
export const { increment, decrement } = counterSlice.actions;
export const store = configureStore({
  reducer: {
    counter: counterSlice.reducer
  }
});
```

> [!REDUNDANT]
> El siguiente bloque repite la lógica de Redux Toolkit pero añade una acción parametrizada (`incrementarPor`). Se mantiene como complemento del anterior.

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

---

## 🚀 Uso en React (react-redux)

Necesitas `react-redux` para conectar tu Store con los componentes.

### 1. Proveer el store

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

### 2. Conectar un componente (Hooks Modernos)

> [!REDUNDANT]
> Se presentan dos ejemplos de conexión similares. El segundo es más específico usando las acciones exportadas del Slice, lo cual es la práctica recomendada.

**Ejemplo A (Dispatch manual):**

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

**Ejemplo B (Uso recomendado con Actions):**

```jsx
import { useSelector, useDispatch } from 'react-redux';
import { increment } from './counterSlice';

function Counter() {
  const count = useSelector((state) => state.counter.value);
  const dispatch = useDispatch();

  return (
    <div>
      <span>{count}</span>
      <button onClick={() => dispatch(increment())}>+1</button>
    </div>
  );
}
```

----

## ⚡ ¿Cuándo elegir Redux?

| Situación | Recomendación |
| :--- | :--- |
| **App Giga-Escalable** | ✅ Redux es imbatible por sus herramientas de debugging y consistencia. |
| **Muchos Estados Cruzados** | ✅ Si muchos componentes no relacionados necesitan los mismos datos. |
| **Lógica de Negocio Compleja** | ✅ Redux permite separar la lógica de la UI de forma muy clara. |
| **Proyectos Pequeños** | ❌ Considera **Zustand** o **Context API** para evitar complejidad innecesaria. |

---

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

---

## ⏳ Middleware (Acciones Asíncronas)

Redux Toolkit incluye `thunk` por defecto. Aquí un ejemplo de cómo se estructuran las llamadas asíncronas:

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

---

## 📊 ¿Cuándo elegir Redux?

| Situación | Recomendación |
| :--- | :--- |
| **App Giga-Escalable** | ✅ Redux es imbatible por sus herramientas de debugging y consistencia. |
| **Muchos Estados Cruzados** | ✅ Si muchos componentes no relacionados necesitan los mismos datos. |
| **Lógica de Negocio Compleja** | ✅ Redux permite separar la lógica de la UI de forma muy clara. |
| **Proyectos Pequeños** | ❌ Considera **Zustand** o **Context API** for simplicity. |

> [!REDUNDANT]
> El siguiente listado complementa con criterios específicos de equipo y herramientas.

* **Rendimiento**: Actualizaciones frecuentes (colaboración en tiempo real, juegos).
* **Time-travel**: Necesitas debugging avanzado o persistencia.
* **Equipo**: Equipos grandes que requieren patrones estrictos y uniformes.

---

## 💡 Buenas Prácticas

* **Usa Redux Toolkit** siempre; olvida el Redux clásico para proyectos nuevos.
* **Mantén los reducers planos** y combínalos con `combineReducers`.
* **Datos no serializables**: No guardes clases o funciones en el store.
* **Selectors**: Usa selectores memoizados (`createSelector`) para evitar re-renders costosos.

---

Buenas prácticas

* Usa Redux Toolkit siempre.

* Mantén los reducers planos y combínalos con combineReducers.

* No guardes datos derivados o no serializables (clases, funciones) en el store.

* Usa Selectors memoizados con createSelector (Reselect) para evitar cálculos innecesarios.

Cuándo usar Redux

* Estado global muy complejo y compartido por muchos componentes.

* Actualizaciones frecuentes (colaboración en tiempo real, juegos).

* Necesitas time-travel debugging o persistencia avanzada.

* Equipo grande que requiere patrones estrictos.

----

## 🛠️ Alternativas modernas más ligeras

* **Zustand**: Más simple y sin Providers. (Ver [Zustand](./zustand.md))
* **Jotai / Recoil**: Estado basado en átomos.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
