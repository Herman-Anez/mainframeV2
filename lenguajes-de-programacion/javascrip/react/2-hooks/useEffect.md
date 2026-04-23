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
>
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
2. **No mientas sobre las dependencias**: Si usas una variable dentro del efecto, **debe** estar en el array de dependencias (o usa la forma funcional de los setters de estado).
3. **Evita bucles infinitos**: Si modificas una variable de estado que también está en las dependencias, entrarás en un bucle infinito a menos que uses lógica condicional o setters funcionales.

---

## Reglas importantes

- No llames a useEffect dentro de condicionales o bucles.

- No hagas async directamente en el callback (debe devolver función de cleanup o undefined). Usa función interna.

- Si la dependencia es un objeto o función definida dentro del componente, puede causar bucles infinitos. Usa useCallback o useMemo.

Efectos que se ejecutan antes del paint: useLayoutEffect

Si necesitas medir el DOM o mutar elementos antes de que el navegador pinte, usa useLayoutEffect. Más adelante se detalla.
Advertencia de dependencias faltantes (eslint-plugin-react-hooks)

```jsx
useEffect(() => {
  setCount(count + 1); // count debería estar en dependencias
}, []); // ❌ warning
```

Solución: incluye count o usa la forma funcional setCount(prev => prev + 1).
Ciclo de vida completo

- Montaje: se ejecuta el efecto.

- Actualización: si cambian dependencias, se ejecuta cleanup anterior y luego el nuevo efecto.

- Desmontaje: se ejecuta cleanup.

Buenas prácticas

- Cada efecto debe tener una responsabilidad única (separar varios useEffect).

- Usar dependencias correctas para evitar renders innecesarios.

- Para fetching, considera librerías como React Query que abstraen efectos.

[⬅️ Volver al Índice](../README.md)
