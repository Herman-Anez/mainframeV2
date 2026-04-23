# ⚓ Custom Hooks: Reutilización de Lógica con Estado

Un **Custom Hook** es una función de JavaScript cuyo nombre comienza con `use` y que puede llamar a otros hooks. Permite extraer y reutilizar lógica compleja con estado entre diferentes componentes sin duplicar código.

---

## ⚖️ Reglas de los Hooks

Para que React pueda verificar que los hooks se comportan correctamente, los Custom Hooks deben seguir estas reglas:

*   **Nomenclatura**: Debe empezar obligatoriamente con el prefijo `use` (ej: `useFetch`, `useAuth`).
*   **Llamadas**: Solo pueden llamar a otros hooks en el nivel superior del Custom Hook (nunca dentro de condicionales o bucles).
*   **Flexibilidad**: Pueden recibir cualquier tipo de argumentos y devolver cualquier tipo de valor (arrays, objetos, variables, etc.).

---

## 🚀 Ejemplos Prácticos

### 1. `useLocalStorage` (Persistencia)
Ideal para sincronizar el estado de React con el almacenamiento local del navegador.

```jsx
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });
  
  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.log(error);
    }
  };
  
  return [storedValue, setValue];
}
```

### 2. `useFetch` (Consumo de APIs)
Maneja la carga, los datos y los errores de una petición HTTP de forma centralizada.

```jsx
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    let ignore = false;
    const fetchData = async () => {
      try {
        setLoading(true);
        const res = await fetch(url);
        const json = await res.json();
        if (!ignore) {
          setData(json);
          setError(null);
        }
      } catch (err) {
        if (!ignore) setError(err);
      } finally {
        if (!ignore) setLoading(false);
      }
    };
    fetchData();
    return () => { ignore = true; };
  }, [url]);
  
  return { data, loading, error };
}
```

### 3. `useOnClickOutside` (Interacción DOM)
Detecta clics fuera de un elemento específico (ej: cerrar un modal).

```jsx
function useOnClickOutside(ref, handler) {
  useEffect(() => {
    const listener = (event) => {
      if (!ref.current || ref.current.contains(event.target)) return;
      handler(event);
    };
    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);
    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [ref, handler]);
}
```

---

## 🏗️ Composición de Custom Hooks

Puedes combinar varios hooks existentes (nativos o personalizados) para crear lógica aún más potente:

```jsx
function useUser(userId) {
  const { data: user, loading, error } = useFetch(`/users/${userId}`);
  const [preferences, setPrefs] = useLocalStorage(`prefs_${userId}`, {});
  
  return { user, loading, error, preferences, setPrefs };
}
```

---

## 💡 Buenas Prácticas

*   **Propósito Único**: Cada hook debe tener una sola responsabilidad clara (Principio de Responsabilidad Única).
*   **Retorno de Valores**: 
    *   Usa **arrays** (ej: `[value, setValue]`) si el hook devuelve exactamente dos valores (estilo `useState`).
    *   Usa **objetos** (ej: `{ data, loading, error }`) si devuelve más de dos valores para facilitar la destructuración y extensión futura.
*   **Pruebas**: Utiliza `renderHook` de React Testing Library para probar la lógica sin necesidad de montar componentes visuales.
*   **Desacoplamiento**: Los custom hooks no deben devolver JSX; deben ser "puros" en lógica para que cualquier componente pueda decidir cómo renderizar esa información.

---

## ⚖️ Custom Hooks vs Componentes

*   **Custom Hooks**: Reutilizan **lógica de negocio** y estado. No devuelven elementos visuales.
*   **Componentes**: Reutilizan **UI** y, opcionalmente, lógica. Si necesitas reutilizar tanto el diseño como el comportamiento, crea un componente.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
