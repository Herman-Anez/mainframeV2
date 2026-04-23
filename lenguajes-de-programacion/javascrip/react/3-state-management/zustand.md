# 🐻 Zustand: Estado Global Simplificado

Zustand es una librería de gestión de estado pequeña, rápida y escalable. Su principal ventaja es que elimina casi todo el boilerplate asociado a Redux, ofreciendo una API basada en Hooks extremadamente intuitiva.

---

## 🚀 Instalación y Setup

```bash
npm install zustand
```

### Crear un Store

A diferencia de Context, no necesitas un `Provider`. Creas el store y lo usas donde quieras.

```jsx
import { create } from 'zustand';

const useCounterStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));
```

---

## 🛠️ Uso en Componentes

### Acceso Básico

```jsx
function Counter() {
  const { count, increment } = useCounterStore();
  
  return (
    <>
      <h1>{count}</h1>
      <button onClick={increment}>+1</button>
    </>
  );
}
```

### ⚡ Selección Parcial (Optimización)

Para evitar que un componente se re-renderice por cambios en partes del estado que no usa, selecciona solo lo que necesitas:

```jsx
// Solo se re-renderiza si 'count' cambia
const count = useCounterStore((state) => state.count);
```

---

## 🌐 Estado Asíncrono

Zustand maneja acciones asíncronas de forma nativa sin necesidad de middlewares adicionales.

```jsx
const useUserStore = create((set) => ({
  user: null,
  loading: false,
  fetchUser: async (id) => {
    set({ loading: true });
    try {
      const res = await fetch(`https://api.example.com/user/${id}`);
      const user = await res.json();
      set({ user, loading: false });
    } catch (error) {
      set({ loading: false });
    }
  },
}));
```

---

## 🧩 Middlewares Potentes

Zustand incluye middlewares integrados para tareas comunes:

* **`persist`**: Guarda el estado en `localStorage` o `sessionStorage` automáticamente.
* **`devtools`**: Integración con Redux DevTools.

```jsx
import { persist, devtools } from 'zustand/middleware';

const useStore = create(
  devtools(
    persist(
      (set) => ({ count: 0, increment: () => set((s) => ({ count: s.count + 1 })) }),
      { name: 'app-storage' }
    )
  )
);
```

---

## 🤔 ¿Por qué elegir Zustand?

| Característica | Prop Drilling | Context API | Zustand |
| :--- | :---: | :---: | :---: |
| **Escalabilidad** | ❌ Baja | ⚠️ Media | ✅ Alta |
| **Boilerplate** | ✅ Ninguno | ⚠️ Medio | ✅ Mínimo |
| **Performance** | ⚠️ Pobre | ⚠️ Manual | ✅ Automática |
| **Facilidad** | ✅ Alta | ✅ Alta | ✅ Muy Alta |

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
