# otros-hooks.md

## useId

Genera identificadores únicos estables para accesibilidad (atributos id). Evita problemas de hidratación en SSR.

```jsx
function Campo() {
  const id = useId();
  return (
    <>
      <label htmlFor={id}>Nombre:</label>
      <input id={id} type="text" />
    </>
  );
}
```

- No usar para keys en listas.

- Cada llamada produce un ID único entre componentes.

## useLayoutEffect

Similar a useEffect, pero se ejecuta síncronamente después de mutar el DOM y antes de que el navegador pinte. Útil para medir el DOM o hacer ajustes visuales inmediatos.

```jsx
useLayoutEffect(() => {
  const { height } = ref.current.getBoundingClientRect();
  setAltura(height);
}, []);
```

Precaución: Bloquea el paint, puede degradar rendimiento. Usa useEffect por defecto.
## useImperativeHandle

Personaliza el valor expuesto por una ref cuando se usa forwardRef. Permite controlar qué métodos o propiedades expones.

```jsx
const FancyInput = forwardRef((props, ref) => {
  const inputRef = useRef();
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    customClear: () => { inputRef.current.value = ''; }
  }));
  return <input ref={inputRef} {...props} />;
});
// Padre
const ref = useRef();
<FancyInput ref={ref} />
ref.current.focus(); // válido
ref.current.customClear();
```

## useDebugValue

Etiqueta un custom hook en React DevTools. Solo útil para depuración.

```jsx
function useFriendStatus(friendID) {
  const [isOnline, setIsOnline] = useState(null);
  useDebugValue(isOnline ? 'Online' : 'Offline');
  return isOnline;
}
```

Para valores costosos, acepta una función de formato:

```jsx
useDebugValue(date, date => date.toDateString());
```

## useTransition (React 18+)

Marca una actualización de estado como no urgente (transición), permitiendo que el UI siga respondiendo mientras se renderiza contenido pesado.

```jsx
```

const [isPending, startTransition] = useTransition();

const handleSearch = (input) => {
  startTransition(() => {
    setSearchQuery(input); // actualización "lenta"
  });
};

return (
  <div>
    <input onChange={e => handleSearch(e.target.value)} />
    {isPending && <Spinner />}
    <Resultados query={searchQuery} />
  </div>
);

## useSyncExternalStore

Hook avanzado para suscribirse a fuentes de datos externas (store de Redux, estado global no React). Recomendado para autores de librerías.

```jsx
const state = useSyncExternalStore(store.subscribe, store.getState);
```

## useDeferredValue (mencionar breve)

Similar a useTransition pero para valores: recibe un valor y devuelve una versión "desfasada" que se actualiza en segundo plano.
