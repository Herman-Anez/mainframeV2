# 📌 useRef: Referencias y Valores Persistentes

`useRef` crea un objeto mutable con una propiedad `.current` que persiste durante todo el ciclo de vida del componente. A diferencia de `useState`, cambiar su valor **no provoca un re-render**.

---

## 🏗️ Usos Principales

### 1. Acceso directo al DOM

Ideal para enfocar elementos, medir dimensiones o integrar librerías externas que no son de React.

```jsx
function InputFocus() {
  const inputRef = useRef(null);
  
  const focusInput = () => {
    inputRef.current.focus();
  };
  
  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Enfocar Input</button>
    </>
  );
}
```

### 2. Guardar valores mutables (Variables de instancia)

Útil para timers, IDs de suscripción o cualquier dato que necesites recordar entre renders sin disparar la actualización de la UI.

```jsx
function Timer() {
  const intervalRef = useRef();
  
  useEffect(() => {
    intervalRef.current = setInterval(() => {
      console.log('Tick');
    }, 1000);
    
    return () => clearInterval(intervalRef.current);
  }, []);
}
```

---

## ⚖️ useState vs useRef

| Característica | `useState` | `useRef` |
| :--- | :---: | :---: |
| **¿Provoca re-render?** | ✅ Sí | ❌ No |
| **¿Persiste entre renders?** | ✅ Sí | ✅ Sí |
| **Actualización** | Asíncrona (Batch) | Síncrona (Directa) |
| **Uso típico** | Datos que se ven en UI | Datos "detrás de escena" |

---

## 🔗 ForwardRef: Pasar Refs a Hijos

Para pasar una referencia a un componente funcional hijo, debes envolver al hijo en `forwardRef`.

```jsx
const MyInput = forwardRef((props, ref) => (
  <input ref={ref} {...props} className="custom-input" />
));

// En el padre
const inputRef = useRef();
<MyInput ref={inputRef} />;
```

---

## 📏 Reglas y Advertencias

*   **No para renderizado**: Si usas un valor para mostrar algo en el JSX, **usa `useState`**. Si mutas `.current` en el cuerpo del render, podrías causar bugs visuales.
*   **Mutación síncrona**: El valor de `.current` cambia inmediatamente, lo que es útil para lógica imperativa.
*   **Persistencia**: Al igual que el estado, el valor se mantiene aunque el componente se re-renderice por otras causas.

---

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


-----
[⬅️ Volver al Índice](../README.md)
