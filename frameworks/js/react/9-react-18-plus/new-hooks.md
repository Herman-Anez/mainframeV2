# ⚓ Nuevos Hooks: Especialización y Control

React 18 introdujo una serie de hooks técnicos diseñados para resolver problemas específicos relacionados con la hidratación, la sincronización con estados externos y la optimización de librerías de estilos.

---

## 🆔 `useId`

Genera identificadores únicos y, lo más importante, **estables** entre el servidor y el cliente. Es fundamental para la accesibilidad (ARIA).

```jsx
function FormField({ label }) {
  const id = useId();
  return (
    <>
      <label htmlFor={id}>{label}</label>
      <input id={id} type="text" />
    </>
  );
}
```

> [!IMPORTANT]
> **No lo uses** para generar `keys` en una lista. Las keys deben provenir de tus datos (ej: IDs de base de datos).

---

## 📡 `useSyncExternalStore`

Este hook permite suscribirse a fuentes de datos externas (como el estado de Redux, Zustand o incluso APIs del navegador como `localStorage`) de forma que sea totalmente compatible con el **Concurrent Rendering**.

// Store externa simple
let externalState = 0;
const listeners = new Set();

function subscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

function getSnapshot() {
  return externalState;
}

function updateState(newValue) {
  externalState = newValue;
  listeners.forEach(l => l());
}

function MiComponente() {
  const state = useSyncExternalStore(subscribe, getSnapshot);
  return <div>{state}</div>;
}

```

Uso típico:

- Integración con Redux (aunque Redux ya tiene hooks propios).

- Suscripción a APIs del navegador (localStorage, geolocalización, online/offline).

```jsx
```

const isOnline = useSyncExternalStore(
  (callback) => {
    window.addEventListener('online', callback);
    window.addEventListener('offline', callback);
    return () => {
      window.removeEventListener('online', callback);
      window.removeEventListener('offline', callback);
    };
  },
  () => navigator.onLine, // snapshot
  () => true // snapshot en servidor (SSR)
);

useInsertionEffect

Hook específico para librerías de CSS-in-JS que necesitan inyectar estilos antes de que React realice mutaciones del DOM. Su firma es igual a useEffect, pero se ejecuta antes de useLayoutEffect.

```jsx
function useCSS(rule) {
  useInsertionEffect(() => {
    const style = document.createElement('style');
    style.textContent = rule;
    document.head.appendChild(style);
    return () => style.remove();
  }, [rule]);
}
```

Diferencia con useLayoutEffect:

- useInsertionEffect se ejecuta antes de cualquier mutación del DOM.

- Ideal para inyectar estilos globales o dinámicos.

- No debe acceder a refs ni al DOM de los componentes (porque aún no se ha aplicado).

Nota: La mayoría de los desarrolladores no necesitan este hook directamente; está pensado para autores de librerías como styled-components o Emotion.
useDeferredValue (mencionado en transitions)

### Ejemplo: Detectar Estado de Conexión

```jsx
import { useSyncExternalStore } from 'react';

function useOnlineStatus() {
  return useSyncExternalStore(
    (callback) => {
      window.addEventListener('online', callback);
      window.addEventListener('offline', callback);
      return () => {
        window.removeEventListener('online', callback);
        window.removeEventListener('offline', callback);
      };
    },
    () => navigator.onLine, // Snapshot en cliente
    () => true // Snapshot inicial en servidor (SSR)
  );
}
```

---

## 🎨 `useInsertionEffect`

Un hook especializado para autores de librerías de **CSS-in-JS**. Se ejecuta **antes** de todas las mutaciones del DOM y antes de `useLayoutEffect`.

```jsx
useInsertionEffect(() => {
  const style = insertarReglaCSS(rule);
  return () => limpiarReglaCSS(style);
}, [rule]);
```

> [!TIP]
> Si no estás construyendo una librería de estilos, lo más probable es que debas usar `useEffect` o `useLayoutEffect` en su lugar.

---

## ⏳ `useDeferredValue`

Permite obtener una versión "retrasada" de un valor. React intentará renderizar primero con el valor actual y, si hay tiempo disponible, renderizará la parte pesada con el valor diferido.

```jsx
const [query, setQuery] = useState('');
const deferredQuery = useDeferredValue(query);

const isStale = query !== deferredQuery;

return (
  <div style={{ opacity: isStale ? 0.5 : 1 }}>
    <LargeList query={deferredQuery} />
  </div>
);
```

---

## 💡 Resumen de Casos de Uso

| Hook | Cuándo usarlo |
| :--- | :--- |
| **`useId`** | Para atributos `id` en formularios y tags de accesibilidad. |
| **`useSyncExternalStore`** | Para integrar estados que viven fuera de React (stores globales). |
| **`useInsertionEffect`** | Solo para inyectar `<style>` dinámicamente antes del renderizado. |
| **`useDeferredValue`** | Para retrasar la actualización de un valor pesado (como filtros). |

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
