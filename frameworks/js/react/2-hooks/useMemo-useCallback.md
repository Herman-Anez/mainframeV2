# 🧠 useMemo & useCallback: Optimización de Rendimiento

Ambos hooks sirven para **memorizar** (cachear) valores o funciones, evitando cálculos innecesarios o recreaciones constantes de referencias entre renderizados.

---

## ⚡ useMemo: Memorizar Valores

Se usa para evitar cálculos costosos en cada render.

```jsx
const valorMemoizado = useMemo(() => computoCostoso(a, b), [a, b]);
```

### 🧪 Ejemplo Práctico

```jsx
function ListaFiltrada({ items, filtro }) {
  const itemsFiltrados = useMemo(() => {
    console.log("Filtrando...");
    return items.filter(item => item.includes(filtro));
  }, [items, filtro]); // Solo se recalcula si items o filtro cambian
  
  return <ul>{itemsFiltrados.map(i => <li key={i}>{i}</li>)}</ul>;
}
```

---

## 🖇️ useCallback: Memorizar Funciones

Devuelve la misma instancia de una función entre renders, a menos que sus dependencias cambien.

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

> [!TIP]
> Su uso principal es pasar callbacks a componentes hijos optimizados con `React.memo` para evitar que estos se re-rendericen innecesariamente.

*   **Estabilidad**: Evita que componentes hijos (optimizados con `React.memo`) se re-rendericen innecesariamente al recibir una "nueva" función en cada render.

---

## ⚖️ Diferencia Clave

| Hook | Qué memoriza | Uso típico |
| :--- | :--- | :--- |
| **`useMemo`** | El **resultado** de una función | Cálculos pesados, objetos/arrays derivados. |
| **`useCallback`**| La **función** misma | Pasar funciones estables a hijos memoizados. |

---

## 🚫 ¿Cuándo NO usarlos? (Trampas Comunes)

> [!WARNING]
> La optimización prematura puede ser contraproducente. Memorizar tiene un costo de memoria y tiempo de ejecución.

1.  **Operaciones baratas**: Sumas, concatenaciones o filtros en arrays pequeños no necesitan `useMemo`.
2.  **Hijos no memoizados**: No sirve de nada usar `useCallback` si el componente hijo no está envuelto en `React.memo`.
3.  **Componentes Nativos**: No uses `useCallback` para funciones que se pasan a un `div`, `button` u otros elementos nativos, ya que estos siempre se re-renderizan si el padre lo hace.

## 📏 Reglas y Buenas Prácticas

1.  **Mide primero**: Usa el Profiler de React DevTools para identificar cuellos de botella reales.
2.  **Dependencias completas**: Al igual que `useEffect`, debes incluir todos los valores reactivos usados dentros.
3.  **Estabilidad de referencias**: Úsalos cuando un objeto o función sea dependencia de otro hook (como `useEffect`).

---

Trampa común
```jsx
// ❌ Mal: useCallback para una función que se pasa a un div nativo
const handleClick = useCallback(() => {}, []);
<div onClick={handleClick} />

// ✅ Bien: solo cuando el hijo está envuelto en React.memo
const HijoMemo = React.memo(({ onClick }) => ...);
```

---

## 🚀 Casos de Uso Avanzados

### Objetos como dependencia
Usa `useMemo` para objetos que son dependencia de otros hooks como `useEffect` para evitar ejecuciones infinitas.

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

----

### Diferencia con React.memo
*   **`React.memo`**: Evita re-render del componente si sus props no cambiaron (comparación superficial).
*   **`useCallback` / `useMemo`**: Evitan que las props (funciones/objetos) cambien innecesariamente, permitiendo que `React.memo` funcione correctamente.

---

## 💡 Buenas Prácticas

*   **Mide primero**: Usa el Profiler de React DevTools antes de optimizar. Si la aplicación no tiene problemas de rendimiento, no añadas complejidad.
*   **Dependencias completas**: Incluye **todos** los valores reactivos usados dentro del hook en el array de dependencias.
*   **Definición externa**: Para funciones que no dependen de estado o props, defínelas **fuera** del componente para evitar recrearlas sin necesidad de hooks.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>

