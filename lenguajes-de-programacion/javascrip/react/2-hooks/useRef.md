
#useRef.md

Concepto

useRef crea un objeto mutable .current que persiste durante todo el ciclo de vida del componente. Cambiar .current no causa re-render.
Usos principales
## Acceso directo a elementos del DOM
```jsx
function InputFocus() {
  const inputRef = useRef(null);
  
  const focusInput = () => {
    inputRef.current.focus();
  };
  
  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Enfocar</button>
    </>
  );
}
```


## Guardar valores mutables que no deben causar re-render
```jsx
function Timer() {
  const intervalRef = useRef();
  
  useEffect(() => {
    intervalRef.current = setInterval(() => {
      console.log('tick');
    }, 1000);
    return () => clearInterval(intervalRef.current);
  }, []);
}
```


## Referencia a valores previos (como "prevProps" o "prevState")
```jsx
function usePrevious(value) {
  const ref = useRef();
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref.current;
}
```


Diferencias con useState

|Característica|useState|useRef|
|-|-|-|
|Cambio provoca re-render|Sí|No|
|Valor persiste entre renders|Sí|Sí|
|Síncrono o asíncrono|Asíncrono (batch)|Síncrono (mutación directa)|


## `ref` como prop: forwardRef

Para pasar una ref a un componente hijo, usa forwardRef:
```jsx
const InputConRef = forwardRef((props, ref) => {
  return <input ref={ref} {...props} />;
});

// Padre
const inputRef = useRef();
<InputConRef ref={inputRef} />
```


## Callback ref (más control)
```jsx
const [medidas, setMedidas] = useState(null);
const refCallback = (node) => {
  if (node !== null) {
    setMedidas(node.getBoundingClientRect());
  }
};
<div ref={refCallback}>...</div>
```


Casos avanzados

- Medir elementos DOM: combínalo con useLayoutEffect para leer dimensiones antes del paint.

- Evitar recreación de callbacks: si usas callback ref, memoízala con useCallback.

Advertencias

- No abuses de ref para "solución rápida" cuando deberías usar estado.

- Mutar .current no es reactivo; si necesitas que algo cambie en la UI, usa estado.
