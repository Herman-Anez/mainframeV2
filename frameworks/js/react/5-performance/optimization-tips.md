optimization-tips.md

Este archivo compila técnicas prácticas de optimización de rendimiento en React.

## Evitar renderizados innecesarios

Usar React.memo, useMemo, useCallback

Ya vistos en detalle.
Mover el estado hacia abajo (State colocation)

```jsx
// ❌ Mal: estado en el padre, causa re-render de toda la lista
function App() {
  const [texto, setTexto] = useState('');
  return (
    <div>
      <input value={texto} onChange={e => setTexto(e.target.value)} />
      <ListaGrande /> {/* se re-renderiza cada vez que cambia texto */}
    </div>
  );
}

// ✅ Bien: estado en el componente que lo necesita
function App() {
  return (
    <div>
      <InputControlado />
      <ListaGrande />
    </div>
  );
}
```

Extraer componentes que cambian frecuentemente

Mantén los componentes estables separados de los que cambian.

## Optimizar listas grandes

Virtualización (react-window, react-virtualized)

Renderiza solo los elementos visibles en la ventana.

```jsx
import { FixedSizeList as List } from 'react-window';

function ListaVirtualizada({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>{items[index]}</div>
  );
  return (
    <List
      height={400}
      itemCount={items.length}
      itemSize={35}
      width={300}
    >
      {Row}
    </List>
  );
}
```

Paginación o carga infinita

No cargues 10,000 elementos de una vez.

## Evitar funciones anónimas en props (cuando sea posible)

```jsx
// ❌ Mal (crea nueva función en cada render)
<button onClick={() => handleClick(id)}>Eliminar</button>

// ✅ Bien (usar useCallback o definir función fuera)
const handleClickMemo = useCallback(() => handleClick(id), [id]);
<button onClick={handleClickMemo}>Eliminar</button>
```

Si el componente hijo no está memoizado, la diferencia es mínima. Solo es crítica con React.memo.

## Memoizar valores costosos

```jsx
// ❌ Mal: recalcula en cada render
const total = items.reduce((sum, i) => sum + i.price, 0);

// ✅ Bien: solo cuando items cambia
const total = useMemo(() => items.reduce((sum, i) => sum + i.price, 0), [items]);
```

## Usar useTransition para actualizaciones no urgentes (React 18)

```jsx
const [isPending, startTransition] = useTransition();
const [query, setQuery] = useState('');

const handleChange = (e) => {
  const value = e.target.value;
  startTransition(() => {
    setQuery(value); // no urgente
  });
};
```

## Evitar la propagación de contextos grandes

Si usas Context API, divide contextos por dominio y memoiza el value.

```jsx
// ❌ Mal: contexto gigante que cambia todo el tiempo
<AppContext.Provider value={{ user, theme, notifications, ... }}>

// ✅ Bien: contextos separados
<UserProvider>
  <ThemeProvider>
    <NotificationsProvider>
      ...
    </NotificationsProvider>
  </ThemeProvider>
</UserProvider>
```

## Evitar objetos literales en dependencias de efectos

```jsx
// ❌ Mal: objeto nuevo en cada render
useEffect(() => {
  fetchData({ page, limit });
}, [{ page, limit }]); // siempre diferente

// ✅ Bien: desestructurar dependencias
useEffect(() => {
  fetchData({ page, limit });
}, [page, limit]);
```

## Imágenes optimizadas

- Usar loading="lazy" en <img> (nativo del navegador).

- Usar formatos modernos (WebP, AVIF).

- Pre-dimensionar imágenes (evitar reflow).

## Web Workers para tareas pesadas

Si tienes procesamiento intensivo (ordenar 1M de registros, cálculos criptográficos), muévelo a un Web Worker.
1## Medir y monitorear

- React DevTools Profiler: graba interacciones y muestra qué componentes se renderizan.

- Lighthouse: mide rendimiento general.

- Web Vitals: Core Web Vitals de Google.

Herramientas de análisis de bundles
bash

npm install --save-dev webpack-bundle-analyzer

# o para Vite

npm install --save-dev rollup-plugin-visualizer

Checklist de optimización (antes de optimizar)

- ¿Hay re-renderizados innecesarios visibles? (Profiler)

- ¿El bundle inicial es demasiado grande? (Bundle analyzer)

- ¿Hay operaciones costosas en el hilo principal? (Performance tab de Chrome)

- ¿Las imágenes están optimizadas?

- ¿Se puede dividir el código por rutas?

- ¿Se puede virtualizar una lista larga?

Principio fundamental

- "Las optimizaciones tempranas son la raíz de todos los males" – Donald Knuth.

Optimiza solo cuando tengas un problema medible. La legibilidad y mantenibilidad del código son más importantes que micro-optimizaciones sin impacto real.
