useMemo-useCallback.md
Concepto

Ambos hooks memorizan valores/funciones para evitar recrearlos en cada render, optimizando el rendimiento.
useMemo – Memoriza valores

```jsx
const valorMemoizado = useMemo(() => computoCostoso(a, b), [a, b]);
```

- Devuelve el resultado de la función.

- Solo se recalcula cuando cambian las dependencias.

Ejemplo práctico

```jsx
function Lista({ items, filtro }) {
  const itemsFiltrados = useMemo(() => {
    return items.filter(item => item.includes(filtro));
  }, [items, filtro]);
  
  return <ul>{itemsFiltrados.map(...)}</ul>;
}
```

useCallback – Memoriza funciones

```jsx
const funcionMemoizada = useCallback(() => {
  hacerAlgo(a, b);
}, [a, b]);
```

- Devuelve la misma referencia de función entre renders si las dependencias no cambian.

- Evita que componentes hijos (optimizados con React.memo) se re-rendericen innecesariamente.

Ejemplo

```jsx
const handleClick = useCallback(() => {
  console.log(count);
}, [count]);

<BotonMemo onClick={handleClick} />
```

Diferencia clave

|Hook|Qué memoriza|Uso típico|
|-|-|-|
|useMemo|Valor calculado|Operaciones costosas, objetos/arrays derivados|
|useCallback|Función Pasar callbacks a hijos memoizados|

¿CuándoNO usarlos?

- No los uses en todos lados (la optimización prematura es mala).

- Si el cálculo es barato (sumas, concatenaciones), no vale la pena.

- Si el componente no tiene problemas de rendimiento, evita complejidad.

Trampa común

```jsx
// ❌ Mal: useCallback para una función que se pasa a un div nativo (no memoizado)
const handleClick = useCallback(() => {}, []);
<div onClick={handleClick} />

// ✅ Bien: solo cuando el hijo está envuelto en React.memo
const HijoMemo = React.memo(({ onClick }) => ...);
```

useMemo para objetos que son dependencia de otros hooks

```jsx
const opciones = useMemo(() => ({ pageSize, sortBy }), [pageSize, sortBy]);
useEffect(() => {
  fetchData(opciones);
}, [opciones]); // ahora la referencia es estable
```

Reglas de dependencias

Al igual que useEffect, las dependencias deben incluir todos los valores reactivos usados dentro.
Diferencia con React.memo

- React.memo evita re-render del componente si sus props no cambiaron (comparación superficial).

- useCallback y useMemo evitan que las props (funciones/objetos) cambien innecesariamente.

Buenas prácticas

- Medir primero (React DevTools Profiler) antes de optimizar.

- Preferir useCallback/useMemo solo en hot paths (listas grandes, animaciones).

- Para funciones que no dependen de estado/props, definirlas fuera del componente (mejor aún).
