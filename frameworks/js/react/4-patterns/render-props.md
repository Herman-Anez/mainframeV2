# render-props.md

Render Props es un patrón donde un componente recibe una función como prop (generalmente llamada render o children) que retorna JSX. El componente llama a esa función con sus propios datos internos, permitiendo al padre definir cómo renderizar.
Origen

Popularizado antes de los hooks. Sigue siendo útil, aunque muchos casos se resuelven con custom hooks.
Ejemplo básico

```jsx
// Componente que maneja el ratón
function MouseTracker({ children }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const handleMouseMove = (e) => setPosition({ x: e.clientX, y: e.clientY });
  
  return (
    <div onMouseMove={handleMouseMove}>
      {children(position)}
    </div>
  );
}

// Uso
<MouseTracker>
  {({ x, y }) => (
    <p>La posición del ratón es ({x}, {y})</p>
  )}
</MouseTracker>
```

Patrón con prop render (alternativa a children)

```jsx
function MouseTracker({ render }) {
  // ... mismo estado
  return <div onMouseMove={handleMouseMove}>{render(position)}</div>;
}

<MouseTracker render={({ x, y }) => <p>{x},{y}</p>} />
```

Ejemplo real: componente de solicitud de datos

```jsx
function Fetch({ url, children }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => { setData(data); setLoading(false); });
  }, [url]);
  
  return children({ data, loading });
}
// Uso
<Fetch url="/api/user">
  {({ data, loading }) => (
    loading ? <Spinner /> : <UserInfo user={data} />
  )}
</Fetch>
```

Ventajas

- Máxima flexibilidad: el componente padre decide completamente el renderizado.

- Reutilización de lógica sin necesidad de herencia.

- Composición dinámica.

Desventajas

- Callback hell si se anidan muchos render props.

- Legibilidad reducida en comparación con hooks.

- Rendimiento porque se crea una nueva función en cada render (aunque es manejable).

Render props vs Hooks

Con la llegada de los custom hooks, los render props han perdido popularidad:

```jsx
// Con hook
function useMousePosition() {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  useEffect(() => {
    const handler = (e) => setPos({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);
  return pos;
}

// Uso
function MiComponente() {
  const { x, y } = useMousePosition();
  return <p>{x},{y}</p>;
}
```

¿Cuándo usar render props hoy?

- En librerías que aún lo soportan (ej. react-router v5).

- Cuando necesitas que un componente controle el ciclo de vida y múltiples puntos de renderizado.

- Para mantener compatibilidad con código antiguo.

Buenas prácticas

- Nombra la prop children o render según el caso.

- Si usas children, asegúrate de documentar que espera una función.

- Combínalo con React.memo para evitar renders innecesarios.
