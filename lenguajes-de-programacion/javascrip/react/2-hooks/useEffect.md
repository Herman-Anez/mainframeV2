useEffect.md

Concepto

useEffect permite realizar efectos secundarios en componentes funcionale### Sustituye a los métodos de ciclo de vida de clases (componentDidMount, componentDidUpdate, componentWillUnmount).
Sintaxis básica

```jsx
```

useEffect(() => {
  // efecto aquí
  return () => {
    // cleanup (opcional)
  };
}, [dependencias]);

## Formas según el array de dependencias

### Sin dependencias (ejecuta en cada render)

```jsx
useEffect(() => {
  console.log('Se ejecuta después de cada render');
});
```

Evitar a menos que sea estrictamente necesario (problemas de rendimiento).

### Array vacío [] (solo montaje y desmontaje)

```jsx
useEffect(() => {
  console.log('Solo al montar');
  return () => console.log('Al desmontar');
}, []);
```

Útil para suscripciones, event listeners, fetch inicial.

### Con dependencias (se ejecuta cuando cambian)

```jsx
useEffect(() => {
  document.title = `Has clickeado ${count} veces`;
}, [count]);
```

## Efecto con cleanup (limpieza)

Previene memory leaks. Se ejecuta antes de desmontar y antes de la próxima ejecución del efecto.

```jsx
useEffect(() => {
  const id = setInterval(() => setTime(Date.now()), 1000);
  return () => clearInterval(id);
}, []);
```


## Casos comunes
### Fetch de datos

```jsx
useEffect(() => {
  let ignore = false;
  async function fetchData() {
    const response = await fetch(url);
    const data = await response.json();
    if (!ignore) setData(data);
  }
  fetchData();
  return () => { ignore = true; }; // evita actualizar estado si componente desmontó
}, [url]);

```

### Suscripción a eventos

```jsx
useEffect(() => {
  const handleResize = () => setWidth(window.innerWidth);
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```


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
