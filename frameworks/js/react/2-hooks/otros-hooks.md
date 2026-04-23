# ⚓ Otros Hooks: Identidad, Imperatividad y Concurrencia

Este documento recopila Hooks de React menos comunes pero esenciales para casos de uso específicos como accesibilidad, optimización concurrente e integración con librerías externas.

---

## 🆔 useId

Genera identificadores únicos estables para accesibilidad (atributos `id`). Es crucial para evitar problemas de hidratación en aplicaciones con SSR (Server Side Rendering).

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

*   **No usar para keys**: No lo uses para generar la propiedad `key` en listas.
*   **Identidad**: Cada llamada produce un ID único, garantizando que los elementos del DOM no colisionen.

---

## 🏗️ useImperativeHandle

Personaliza el valor que se expone a un componente padre a través de una `ref` cuando se usa `forwardRef`. Permite mantener la encapsulación al exponer solo los métodos necesarios.

```jsx
const FancyInput = forwardRef((props, ref) => {
  const inputRef = useRef();
  
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    customClear: () => { inputRef.current.value = ''; }
  }));
  
  return <input ref={inputRef} {...props} />;
});

// Uso en el Padre
const ref = useRef();
<FancyInput ref={ref} />
ref.current.focus(); // válido
ref.current.customClear(); // método personalizado
```

---

## 🧪 useDebugValue

Permite etiquetar un Custom Hook en las **React DevTools**. Es puramente para mejorar la experiencia de desarrollo (DX).

```jsx
function useFriendStatus(friendID) {
  const [isOnline, setIsOnline] = useState(null);
  useDebugValue(isOnline ? 'Online' : 'Offline');
  return isOnline;
}
```

> [!TIP]
> Para formatear valores costosos, acepta una función como segundo argumento que solo se ejecuta cuando se inspeccionan las DevTools:
> `useDebugValue(date, date => date.toDateString());`

---

## ⚡ useTransition (React 18+)

Permite marcar actualizaciones de estado como "no urgentes" (transiciones). Esto permite que la interfaz siga respondiendo a interacciones del usuario (como clics o escritura) mientras se procesa una actualización pesada en segundo plano.

```jsx
const [isPending, startTransition] = useTransition();

const handleSearch = (input) => {
  startTransition(() => {
    setSearchQuery(input); // Esta actualización se procesará con menor prioridad
  });
};

return (
  <div>
    <input onChange={e => handleSearch(e.target.value)} />
    {isPending && <Spinner />}
    <Resultados query={searchQuery} />
  </div>
);
```

---

## 🌐 useSyncExternalStore

Hook avanzado diseñado para que las librerías de gestión de estado se suscriban a fuentes de datos externas de forma segura para la renderización concurrente.

```jsx
const state = useSyncExternalStore(store.subscribe, store.getState);
```

---

## ⏳ useDeferredValue

Similar a `useTransition`, pero se aplica a un **valor** directamente. Recibe un valor y devuelve una versión "desfasada" del mismo que se actualiza con menor prioridad, permitiendo que la UI renderice primero el contenido urgente.

---

## useLayoutEffect

Similar a useEffect, pero se ejecuta síncronamente después de mutar el DOM y antes de que el navegador pinte. Útil para medir el DOM o hacer ajustes visuales inmediatos.

```jsx
useLayoutEffect(() => {
  const { height } = ref.current.getBoundingClientRect();
  setAltura(height);
}, []);
```

Precaución: Bloquea el paint, puede degradar rendimiento. Usa useEffect por defecto.
---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
