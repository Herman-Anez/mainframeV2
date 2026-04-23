# custom-hooks.md

Un custom hook es una función JavaScript cuyo nombre comienza con use y que puede llamar a otros hooks. Permite reutilizar lógica con estado entre componentes.
Reglas

- Debe empezar con use (convención para que React pueda verificar reglas de hooks).

- Solo puede llamar hooks en el nivel superior.

- Puede recibir argumentos y devolver cualquier valor.

Ejemplo simple: useLocalStorage

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

Ejemplo: useFetch

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


Ejemplo: useOnClickOutside (detectar clic fuera de un elemento)

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


Composición de custom hooks

Puedes combinar varios hooks dentro de uno:

```jsx
function useUser(userId) {
  const { data: user, loading, error } = useFetch(`/users/${userId}`);
  const [preferences, setPrefs] = useLocalStorage(`prefs_${userId}`, {});
  return { user, loading, error, preferences, setPrefs };
}
```


Buenas prácticas

- Un solo propósito por custom hook.

- Devolver un objeto con valores nombrados (en lugar de array) cuando hay más de dos valores.

- Escribir pruebas para custom hooks con renderHook (React Testing Library).

- Documentar los parámetros y el retorno.

Custom hooks vs componentes

- Los custom hooks no devuelven JSX, solo lógica con estado.

- Si necesitas reutilizar UI + lógica, crea un componente. Si solo lógica, custom hook.
