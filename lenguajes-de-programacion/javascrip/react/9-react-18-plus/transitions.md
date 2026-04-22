

📄 9-react-18-plus/transitions.md
Concepto

Transitions son una característica de React 18+ que permiten marcar actualizaciones de estado como no urgentes, permitiendo que el UI siga siendo responsivo durante actualizaciones pesadas.
useTransition hook
jsx

const [isPending, startTransition] = useTransition();

- isPending: booleano que indica si la transición está activa (útil para mostrar un spinner).

- startTransition(callback): función que envuelve la actualización de estado no urgente.

Ejemplo práctico

```jsx
function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();
  
  const handleChange = (e) => {
    const value = e.target.value;
    setQuery(value); // Urgente: actualiza el input inmediatamente

    startTransition(() => {
      // No urgente: búsqueda pesada
      const filtered = hugeList.filter(item => item.includes(value));
      setResults(filtered);
    });
  };
  
  return (
    <div>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <ResultList items={results} />
    </div>
  );
}
```

startTransition como función independiente

```jsx
import { startTransition } from 'react';

startTransition(() => {
  setResults(heavyComputation(query));
});

useDeferredValue (alternativa)
```

Recibe un valor y devuelve una versión "desfasada" que se actualiza en segundo plano.

```jsx
const [query, setQuery] = useState('');
const deferredQuery = useDeferredValue(query);
const results = useMemo(() => filterList(hugeList, deferredQuery), [deferredQuery]);
```

// El input se actualiza inmediatamente con query, los resultados con deferredQuery (más lento)

Diferencia entre useTransition y useDeferredValue

|useTransition|useDeferredValue|
|-|-|
|Controlas dónde se aplica la transición|Aplica a un valor específico|
|Tienes isPending para feedback|No hay indicador de pendiente (aunque puedes comparar valor vs deferred)|
|Útil para actualizaciones de estado que son costosas|Útil cuando el valor viene de props o de fuera|

## Reglas importantes

- Solo se pueden usar con estado (setState, dispatch). No para efectos secundarios.

- Si el dispositivo es rápido, la transición ocurre de forma síncrona (no se nota).

- En React 18, las actualizaciones dentro de startTransition son interrumpibles.

## Transiciones con Suspense

Las transiciones evitan que Suspense muestre un fallback indeseado durante la carga de datos:

```jsx
startTransition(() => {
  setResource(fetchNewData()); // si suspende, no muestra fallback, mantiene la UI antigua
});
```

Buenas prácticas

- Toda actualización que no sea inmediata (cambio de ruta, filtros, búsquedas) debe ir dentro de startTransition.

- No uses transiciones para inputs de texto (ahí la prioridad es máxima).

- Muestra isPending para dar feedback al usuario (spinner, skeleton).
