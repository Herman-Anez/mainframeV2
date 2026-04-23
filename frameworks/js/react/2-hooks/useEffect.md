# ⚓ useEffect: Gestión de Efectos Secundarios

El Hook `useEffect` te permite realizar operaciones que afectan a otros componentes o al sistema fuera de React (side effects) desde un componente funcional.

> [!NOTE]
> Equivale a la combinación de `componentDidMount`, `componentDidUpdate` y `componentWillUnmount` en los componentes de clase.

---

## 🛠️ Sintaxis y Variaciones

La ejecución de `useEffect` depende enteramente de su segundo argumento: el **array de dependencias**.

### 1. Sin array de dependencias

Se ejecuta en **cada renderizado** de la aplicación.

```jsx
useEffect(() => {
  console.log("Me ejecuto siempre");
});
```

### 2. Array vacío `[]`

Se ejecuta **solo una vez**, justo después del primer montaje. Ideal para inicializaciones.

```jsx
useEffect(() => {
  console.log("Solo al montar");
}, []);
```

### 3. Con dependencias `[dep1, dep2]`

Se ejecuta al montar y cada vez que **cualquiera** de las dependencias cambie su valor.

```jsx
useEffect(() => {
  console.log("Cambió el contador:", count);
}, [count]);
```

---

## 🧹 La Función de Limpieza (Cleanup)

Para evitar fugas de memoria (memory leaks), algunos efectos requieren ser "limpiados" cuando el componente se desmonta o antes de volver a ejecutar el efecto.

```jsx
useEffect(() => {
  const timer = setInterval(() => {
    console.log("Tick");
  }, 1000);

  // Función de limpieza
  return () => clearInterval(timer);
}, []);
```

---

## 💡 Casos de Uso Comunes

### Fetch de Datos (Forma Segura)

> [!WARNING]
> No marques el callback de `useEffect` como `async`. En su lugar, define la función dentro.

```jsx
useEffect(() => {
  let isMounted = true;

  const fetchData = async () => {
    const res = await fetch('https://api.example.com/data');
    const json = await res.json();
    if (isMounted) setData(json);
  };

  fetchData();
  return () => { isMounted = false; }; 
}, [userId]);
```

### Suscripción a eventos

```jsx
useEffect(() => {
  const handleResize = () => setWidth(window.innerWidth);
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

---

## 📏 Reglas y Buenas Prácticas

1. **Responsabilidad Única**: Es mejor tener varios `useEffect` pequeños que uno gigante que haga de todo.
2. **No mientas sobre las dependencias**: Si usas una variable dentro del efecto, **debe** estar en el array de dependencias.
3. **Evita bucles infinitos**: Si modificas una variable de estado que también está en las dependencias, entrarás en un bucle infinito. Usa setters funcionales: `setCount(c => c + 1)`.
4. **No condiciones el Hook**: Al igual que todos los hooks, debe llamarse en el nivel superior. No lo metas dentro de un `if`.

---

## 🧪 useLayoutEffect

Si necesitas medir el DOM o mutar elementos **antes** de que el navegador pinte la pantalla, usa `useLayoutEffect`. Se ejecuta de forma síncrona después de todas las mutaciones del DOM.

---

[⬅️ Volver al Índice](../README.md)
