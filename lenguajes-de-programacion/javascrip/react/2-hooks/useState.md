# ⚓ useState Avanzado: Más allá de lo básico

Aunque ya conoces los fundamentos de `useState`, existen patrones y comportamientos internos que son cruciales para construir aplicaciones robustas y eficientes.

---

## ⚡ Inicialización Diferida (Lazy Initialization)

Si el estado inicial requiere un cálculo costoso (por ejemplo, leer de `localStorage` o procesar una lista grande), puedes pasar una **función** a `useState`. Esta función solo se ejecutará **una vez**, en el primer montaje.

```jsx
const [state, setState] = useState(() => {
  const initialState = performExpensiveComputation();
  return initialState;
});
```

---

## 🖇️ Actualizaciones basadas en el estado anterior

> [!REDUNDANT]
> Este concepto también se menciona en [useState Básico](../1-basics/estado-useState.md), pero es fundamental recordarlo aquí.

Siempre que la nueva dependa del valor previo, usa la forma funcional para evitar bugs por closures obsoletos:

```jsx
setCount(prevCount => prevCount + 1);
```

---

## 🧊 Inmutabilidad (Objetos y Arrays)

> [!REDUNDANT]
> Información duplicada con el módulo de [Fundamentos](../1-basics/estado-useState.md).

React compara el estado anterior con el nuevo por referencia (Object.is). Si mutas el objeto, la referencia no cambia y React no re-renderiza.

### 📦 Con Objetos

```jsx
const [user, setUser] = useState({ name: 'Juan', age: 30 });
setUser({ ...user, age: 31 });        // spread
setUser(prev => ({ ...prev, age: 31 }));
```

### 📋 Con Arrays

```jsx
const [list, setList] = useState([]);
// Agregar
setList([...list, nuevoElemento]);
setList(prev => [...prev, nuevoElemento]);

// Eliminar por id
setList(prev => prev.filter(item => item.id !== id));
```

---

## 🏎️ Agrupamiento de Actualizaciones (Batching)

React agrupa múltiples actualizaciones de estado en una sola renderización por motivos de rendimiento. Esto significa que el estado no cambia inmediatamente después de llamar a la función setter.

```jsx
const handleClick = () => {
  setCount(c => c + 1);
  setCount(c => c + 1);
  setCount(c => c + 1);
  // React solo re-renderizará UNA vez, no tres.
};
```

---

## 🧐 ¿useState o useReducer?

A medida que el estado se vuelve más complejo, elegir entre `useState` y `useReducer` es vital:

* **Usa `useState` cuando**: Tienes estados simples (booleanos, strings, números) o objetos pequeños con propiedades independientes.
* **Usa `useReducer` cuando**: El siguiente estado depende del anterior de forma compleja, o cuando varias partes del estado deben cambiar juntas en respuesta a una acción.

---

## 🛡️ Patrones de Diseño: Estado Elevado

Cuando dos o más componentes necesitan acceder al mismo estado, la solución estándar es **elevar el estado** al ancestro común más cercano.

```jsx
// El componente Padre gestiona el estado y lo pasa vía props
function Parent() {
  const [value, setValue] = useState("");
  return (
    <>
      <Input value={value} onChange={setValue} />
      <Display value={value} />
    </>
  );
}
```

---

## Múltiples estados vs un solo objeto

* Varios useState: más legible para estados no relacionados.

* Un objeto con useState: útil para estados que siempre cambian juntos (ej. formulario). Pero cuidado: al actualizar debes esparcir todo el objeto.

---

## 🧪 Estado derivado

> [!TIP]
> No guardes en el estado valores que puedan ser calculados a partir de otros estados o props.

```jsx
// Mal
const [precio, setPrecio] = useState(100);
const [conIva, setConIva] = useState(121); // derivado ❌

// Bien
const conIva = precio * 1.21; // ✅
```

---

## 📏 Reglas Internas y Buenas Prácticas

React se basa en el **orden de las llamadas** a los Hooks. Por eso:

> [!CAUTION]
> **NUNCA** llames a un Hook dentro de un `if`, `for` o función anidada. Si el orden de las llamadas cambia entre renders, React se confundirá.

1. **Nomenclatura**: Usa siempre `[state, setState]`.
2. **Atomicidad**: Mantén el estado lo más pequeño posible.
3. **Persistencia**: Si necesitas que el estado sobreviva a una recarga de página, combínalo con `localStorage` en un efecto o usa librerías como Zustand.

---
Buenas prácticas

* Nombra el estado y su setter con [algo, setAlgo].

* Mantén el estado lo más atómico posible.

* Extrae lógica de actualización compleja a funciones aparte o custom hooks.

[⬅️ Volver al Índice](../README.md)