
📄 9-react-18-plus/automatic-batching.md
Concepto

Automatic Batching es la capacidad de React de agrupar múltiples actualizaciones de estado en un solo re-render, incluso si ocurren dentro de promesas, setTimeout, eventos nativos, etc.
Antes de React 18 (solo batching en eventos de React)

```jsx
function handleClick() {
  setCount(c => c + 1); // No re-renderiza inmediatamente
  setFlag(f => !f);     // React agrupa y hace un solo render
}
// ✅ Sí había batching

setTimeout(() => {
  setCount(c => c + 1); // Re-render
  setFlag(f => !f);     // Otro re-render (2 renders)
}, 1000);
// ❌ No batching fuera de eventos de React
```

Después de React 18 (con createRoot)

```jsx
// Todo lo que esté dentro del mismo callback síncrono se agrupa
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  // Un solo re-render
}, 1000);

// También funciona con promesas, fetch, etc.
fetch('/api').then(() => {
  setData(data);
  setLoading(false); // Un solo render
});
```

Cómo deshabilitar el batching (casos raros)

```jsx
import { flushSync } from 'react-dom';

flushSync(() => {
  setCount(c => c + 1); // Fuerza render inmediato
});
// Aquí ya se renderizó
setFlag(f => !f); // Otro render
```

Impacto en el rendimiento

- Reduce renders innecesarios.

- Código más simple (no necesitas usar unstable_batchedUpdates manualmente).

- Mejor experiencia porque los estados intermedios no se muestran al usuario.

Buenas prácticas

- Confía en el batching automático; no intentes optimizar manualmente.

- Si necesitas leer el DOM después de una actualización, usa flushSync.

- Recuerda que el batching solo funciona si las actualizaciones están dentro del mismo event loop tick.
