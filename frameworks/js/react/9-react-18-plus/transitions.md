# ⚡ Transitions: Priorizando la Experiencia de Usuario

Las **Transitions** (Transiciones) en React 18+ permiten marcar ciertas actualizaciones de estado como "no urgentes". Esto asegura que las interacciones críticas (como escribir en un teclado o hacer clic) se procesen de inmediato, mientras que las tareas pesadas (como filtrar una lista gigante) ocurran en segundo plano sin bloquear la interfaz.

---

## 🏗️ El Hook `useTransition`

Este hook devuelve un estado de pendiente y una función para envolver las actualizaciones de estado lentas.

```jsx
const [isPending, startTransition] = useTransition();
```

*   **`isPending`**: Un booleano que indica si la transición está actualmente en progreso (útil para mostrar un spinner).
*   **`startTransition`**: Envuelve la función que actualiza el estado.

---

## 🚀 Ejemplo: Búsqueda con Filtrado Pesado

```jsx
function SearchApp() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleSearch = (e) => {
    const value = e.target.value;

    // 🔴 Prioridad ALTA: Actualizar el input inmediatamente
    setQuery(value);

    // 🟡 Prioridad BAJA: Filtrar la lista sin bloquear el input
    startTransition(() => {
      const filtered = heavyFilter(data, value);
      setResults(filtered);
    });
  };

  return (
    <div>
      <input type="text" value={query} onChange={handleSearch} />
      {isPending && <p>Buscando resultados...</p>}
      <List items={results} />
    </div>
  );
}
```

---

## ⏳ `useDeferredValue` (Alternativa)

A diferencia de `useTransition` que envuelve una acción, `useDeferredValue` envuelve un **valor**. Se usa cuando no tienes control directo sobre el `setState` (ej: el valor viene de una prop).

```jsx
const [query, setQuery] = useState('');
const deferredQuery = useDeferredValue(query);

// React priorizará el renderizado con 'query', 
// y luego intentará renderizar 'results' con 'deferredQuery' en segundo plano.
const results = useMemo(() => filter(data, deferredQuery), [deferredQuery]);
```

---

## ⚖️ Comparativa: Transition vs DeferredValue

| Característica | `useTransition` | `useDeferredValue` |
| :--- | :--- | :--- |
| **Control** | Sobre la **acción** (update) | Sobre el **valor** (data) |
| **Feedback** | Incluye `isPending` | No incluye estado de carga nativo |
| **Uso Ideal** | Al llamar a `setState` en un evento | Cuando el valor llega por `props` |

---

## 🛡️ Reglas y Consideraciones

1.  **Solo para Estado**: Las transiciones solo funcionan con cambios de estado de React. No se pueden usar con el contenido de variables normales.
2.  **Interrumpibles**: Si una transición está en curso y ocurre otra actualización urgente (ej: el usuario presiona otra tecla), React abandonará la transición actual y empezará la nueva.
3.  **No para Inputs**: Nunca envuelvas el `value` de un input directo en una transición, o el campo de texto se sentirá "laggeado".

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

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
