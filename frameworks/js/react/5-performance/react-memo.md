# 🧠 React.memo: Memorización de Componentes

`React.memo` es un **Componente de Alto Orden (HOC)** que permite optimizar el rendimiento al evitar que un componente funcional se re-renderice si sus props no han cambiado.

---

## 🏗️ Sintaxis Básica

Por defecto, `React.memo` realiza una **comparación superficial (shallow comparison)** de todos los objetos en las props.

```jsx
const ComponenteMemoizado = React.memo(MyComponent);
```

### 🚀 Ejemplo de Uso

Si el componente `Padre` cambia su estado pero las props de `Hijo` permanecen iguales, `Hijo` no se volverá a renderizar.

```jsx
const Hijo = React.memo(({ nombre }) => {
  console.log('Rendering Hijo...');
  return <p>Hola, {nombre}</p>;
});

function Padre() {
  const [contador, setContador] = useState(0);

  return (
    <>
      <button onClick={() => setContador(c => c + 1)}>Incrementar</button>
      <Hijo nombre="Elena" />
    </>
  );
}
```

---

## 🖇️ Personalización de la Comparación

Puedes pasar un segundo argumento opcional para definir manualmente cuándo se deben considerar "iguales" las props.

```jsx
const MyComponent = React.memo(
  (props) => { /* componente */ },
  (prevProps, nextProps) => {
    // Retorna true si quieres EVITAR el renderizado
    // Retorna false si quieres FORZAR el renderizado
    return prevProps.id === nextProps.id;
  }
);
```

---

## 🚫 Trampas Comunes y Soluciones

El error más frecuente al usar `React.memo` es pasar tipos de datos no primitivos (objetos, arrays o funciones) sin estabilizarlos, lo que rompe la memorización.

### 1. Funciones como Props

Las funciones flecha definidas en el cuerpo del padre se recrean en cada render.

* **Solución**: Envuelve la función en `useCallback`.

```jsx
// ✅ Forma Correcta
const handleClick = useCallback(() => { ... }, []);
<HijoMemoizado onClick={handleClick} />
```

### 2. Objetos y Arrays

Si pasas un objeto literal `style={{ ... }}`, la referencia cambia siempre.

* **Solución**: Estabilizar con `useMemo` o definir el objeto fuera del componente.

```jsx
// ✅ Forma Correcta
const opciones = useMemo(() => ({ theme: 'dark' }), []);
<HijoMemoizado config={opciones} />
```

---

## ⚖️ ¿Cuándo usar React.memo?

> [!TIP]
> Úsalo cuando un componente renderiza el mismo resultado dado el mismo conjunto de props y se renderiza con mucha frecuencia.

* **Listas Largas**: Elementos individuales de listas que no cambian a menudo.
* **Componentes Pesados**: Componentes que realizan cálculos costosos o tienen un árbol de nodos grande.
* **Páginas con Dashboard**: Secciones que no dependen de la actualización global del estado.

---

## ⚠️ ¿Cuándo NO usarlo? (Optimización Prematura)

1. **Componentes Ligeros**: Si el componente es muy simple, el costo de ejecutar la comparación de props puede ser mayor que el costo del re-renderizado mismo.
2. **Props Dinámicas**: Si el componente casi siempre recibe props diferentes (ej: un input controlado), `React.memo` añadirá trabajo innecesario al procesador.

---

## React.memo solo mira las props, no el estado interno ni el contexto

Si el componente usa useContext y el contexto cambia, se re-renderizará igualmente.
¿Cuándo NO usar React.memo?

* Componentes que casi siempre reciben props diferentes (ej. inputs controlados).

* Componentes muy ligeros (el costo de la comparación supera el beneficio).

* En toda la aplicación sin medir (optimización prematura).

Medir antes de optimizar

Usa React DevTools → Profiler para identificar componentes que se re-renderizan innecesariamente. Solo entonces aplica React.memo.
React.memo vs PureComponent

* React.memo para componentes funcionales.

* PureComponent para componentes de clase (implementa shouldComponentUpdate con shallow compare).

Buenas prácticas

* Envuelve solo los componentes que realmente lo necesitan.

* Combínalo con useCallback y useMemo para props estables.

* Prefiere la composición para evitar pasar props innecesarias.

----
<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
