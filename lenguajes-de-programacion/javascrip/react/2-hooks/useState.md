# useState.md

- Nota: Aunque useState ya se introdujo en 1-basics/estado-useState.md, aquí se profundiza en aspectos más avanzados y patrones.

Concepto avanzado

useState es el hook fundamental para manejar estado local en componentes funcionales. React garantiza que el valor del estado se mantenga entre renders y que al actualizarlo se programe un nuevo render.
Formas de inicialización
Inicialización directa

```jsx
const [count, setCount] = useState(0);
```

Inicialización diferida (lazy initialization)

Cuando el estado inicial requiere un cálculo costoso, pasa una función:

```jsx
const [state, setState] = useState(() => {
  const valorInicial = calcularValorCostoso();
  return valorInicial;
});
```

Esta función solo se ejecutará en el primer render.
Actualizaciones basadas en el estado anterior

Siempre que la nueva dependa del valor previo, usa la forma funcional para evitar bugs por closures obsoletos:

```jsx
setCount(prevCount => prevCount + 1);
```

Actualizaciones de objetos y arrays (inmutabilidad)

React compara el estado anterior con el nuevo por referencia (Object.is). Si mutas el objeto, la referencia no cambia y React no re-renderiza.

Forma correcta con objetos:

```jsx
const [user, setUser] = useState({ name: 'Juan', age: 30 });
setUser({ ...user, age: 31 });        // spread
setUser(prev => ({ ...prev, age: 31 }));
```

Con arrays:

```jsx
const [list, setList] = useState([]);
// Agregar
setList([...list, nuevoElemento]);
setList(prev => [...prev, nuevoElemento]);

// Eliminar por id
setList(prev => prev.filter(item => item.id !== id));

// Actualizar un elemento
setList(prev => prev.map(item => item.id === id ? { ...item, done: true } : item));
```

¿El setter es asíncrono?

setState es asíncrono. React agrupa múltiples actualizaciones para mejorar rendimiento. No confíes en que el estado cambie inmediatamente después de llamar al setter.

```jsx
setCount(count + 1);
console.log(count); // todavía el valor anterior
```

Si necesitas leer el valor justo después de actualizar, usa useEffect con dependencia en ese estado.
Múltiples estados vs un solo objeto

- Varios useState: más legible para estados no relacionados.

- Un objeto con useState: útil para estados que siempre cambian juntos (ej. formulario). Pero cuidado: al actualizar debes esparcir todo el objeto.

Estado derivado (no lo guardes en el estado)

```jsx
// Mal
const [precio, setPrecio] = useState(100);
const [conIva, setConIva] = useState(121); // derivado

// Bien
const conIva = precio * 1.21;
```

useState vs useReducer

- useState: para estado simple (boolean, número, string, objeto pequeño).

- useReducer: para estado complejo con múltiples sub-valores o transiciones interdependientes.

Buenas prácticas

- Nombra el estado y su setter con [algo, setAlgo].

- Mantén el estado lo más atómico posible.

- Extrae lógica de actualización compleja a funciones aparte o custom hooks.
