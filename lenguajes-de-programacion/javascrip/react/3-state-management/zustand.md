# zustand.md

Zustand es una librería de estado global minimalista para React. Su API es muy simple, sin boilerplate, basada en hooks y sin necesidad de Provider (aunque opcional).
Instalación

```bash
npm install zustand
```

## Crear un store

```jsx
import { create } from 'zustand';

const useCounterStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));
```

## Usar en un componente

```jsx
function Contador() {
  const { count, increment, decrement } = useCounterStore();
  return (
    <div>
      {count}
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

## Selección parcial (evita re-renderizados innecesarios)

```jsx
const count = useCounterStore((state) => state.count);
const increment = useCounterStore((state) => state.increment);

```

## O con un selector

```jsx
const { count, increment } = useCounterStore((state) => ({
  count: state.count,
  increment: state.increment,
}), shallow); // comparación superficial
```

## Estado asíncrono

```jsx
const useUserStore = create((set) => ({
  user: null,
  loading: false,
  fetchUser: async (id) => {
    set({ loading: true });
    const res = await fetch(`/users/${id}`);
    const user = await res.json();
    set({ user, loading: false });
  },
}));
```

## Middlewares (persistencia, devtools, logger)

```jsx
import { persist } from 'zustand/middleware';

const useStore = create(
  persist(
    (set) => ({ count: 0, increment: () => set((s) => ({ count: s.count + 1 })) }),
    { name: 'counter-storage' } // localStorage key
  )
);
```

## Store con slices (modularización)

```jsx
const useBoundStore = create((...a) => ({
  ...counterSlice(...a),
  ...userSlice(...a),
}));
```

Ventajas sobre Redux

- Sin Provider (opcional).

- Menos código boilerplate.

- Rendimiento: solo re-renderiza componentes que usan datos específicos.

- Curva de aprendizaje baja.

Desventajas

- Menos tooling que Redux (aunque tiene DevTools).

- Menos estructura para equipos grandes (puede volverse desordenado).

Cuándo usar Zustand

- Proyectos pequeños a medianos.

- Necesitas estado global sin la complejidad de Redux.

- Prefieres una API de hooks simple.
