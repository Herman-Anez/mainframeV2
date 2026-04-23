# react-memo.md

React.memo es una función de orden superior (HOC) que evita que un componente funcional se re-renderice si sus props no han cambiado (comparación superficial por defecto).
Sintaxis

```jsx
const ComponenteMemoizado = React.memo(ComponenteOriginal);
```

¿Cuándo usar React.memo?

- Componentes que reciben las mismas props frecuentemente.

- Componentes que se renderizan muchas veces (listas grandes, tablas).

- Componentes pesados (con cálculos costosos o muchos elementos DOM).

Ejemplo básico

```jsx
const Hijo = React.memo(({ valor }) => {
  console.log('Hijo renderizado');
  return <div>{valor}</div>;
});

function Padre() {
  const [contador, setContador] = useState(0);
  const [texto, setTexto] = useState('Hola');
  
  return (
    <div>
      <button onClick={() => setContador(c => c + 1)}>Contador: {contador}</button>
      <input value={texto} onChange={(e) => setTexto(e.target.value)} />
      <Hijo valor="Este texto no cambia" />
    </div>
  );
}
```

El componente Hijo solo se renderizará una vez, aunque el padre se re-renderice al cambiar contador o texto.
Personalización de la comparación

Por defecto, React.memo hace una comparación superficial (shallow compare) de las props. Si necesitas control personalizado, pasa una función como segundo argumento:

```jsx
const MemoComponent = React.memo(
  Componente,
  (prevProps, nextProps) => {
    // Devuelve true si son iguales (NO debe re-renderizar)
    return prevProps.usuario.id === nextProps.usuario.id;
  }
);
```

Cuidado: la función debe ser pura y rápida.
Limitaciones importantes

## Las funciones como props siempre cambian (a menos que uses useCallback)

```jsx
// ❌ Mal: handleClick se recrea en cada render
<HijoMemo onClick={() => console.log('click')} />

// ✅ Bien: con useCallback
const handleClick = useCallback(() => console.log('click'), []);
<HijoMemo onClick={handleClick} />
```

## Los objetos/arrays literales también cambian cada vez

```jsx
// ❌ Mal: objeto nuevo cada vez
<HijoMemo config={{ tema: 'oscuro' }} />

// ✅ Bien: usar useMemo o definir fuera
const config = useMemo(() => ({ tema: 'oscuro' }), []);
<HijoMemo config={config} />
```

## React.memo solo mira las props, no el estado interno ni el contexto

Si el componente usa useContext y el contexto cambia, se re-renderizará igualmente.
¿Cuándo NO usar React.memo?

- Componentes que casi siempre reciben props diferentes (ej. inputs controlados).

- Componentes muy ligeros (el costo de la comparación supera el beneficio).

- En toda la aplicación sin medir (optimización prematura).

Medir antes de optimizar

Usa React DevTools → Profiler para identificar componentes que se re-renderizan innecesariamente. Solo entonces aplica React.memo.
React.memo vs PureComponent

- React.memo para componentes funcionales.

- PureComponent para componentes de clase (implementa shouldComponentUpdate con shallow compare).

Buenas prácticas

- Envuelve solo los componentes que realmente lo necesitan.

- Combínalo con useCallback y useMemo para props estables.

- Prefiere la composición para evitar pasar props innecesarias.
