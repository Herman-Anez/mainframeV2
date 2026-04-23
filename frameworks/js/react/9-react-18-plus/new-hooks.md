
📄 9-react-18-plus/new-hooks.md
useId

Genera identificadores únicos y estables para accesibilidad (evita conflictos en SSR e hidratación).

```jsx
function FormField() {
  const id = useId();
  return (
    <>
      <label htmlFor={id}>Nombre:</label>
      <input id={id} type="text" />
    </>
  );
}
```

Características:

- Los IDs son consistentes en servidor y cliente (evita advertencias de hidratación).

- Cada llamada produce un ID diferente.

- No usar para keys en listas.

useSyncExternalStore

Hook para suscribirse a fuentes de datos externas (stores de Redux, Zustand, estado global de otras librerías) de forma segura con concurrencia.

```jsx
import { useSyncExternalStore } from 'react';

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

```jsx
const deferredValue = useDeferredValue(value);
```

Recibe un valor y devuelve una versión que se actualiza con menor prioridad. Útil para mantener responsivo el UI mientras se renderiza contenido pesado basado en ese valor.

```jsx
function App() {
  const [text, setText] = useState('');
  const deferredText = useDeferredValue(text);
  
  const list = useMemo(() => {
    return expensiveFilter(hugeList, deferredText);
  }, [deferredText]);
  
  return (
    <>
      <input value={text} onChange={e => setText(e.target.value)} />
      {deferredText !== text && <Spinner />}
      <List items={list} />
    </>
  );
}
```
