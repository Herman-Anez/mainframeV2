# 📡 TanStack Query (React Query)

React Query (ahora TanStack Query) es la librería definitiva para gestionar el **Estado del Servidor** en React. A diferencia de Redux o Zustand, no se enfoca en el estado global del cliente, sino en sincronizar los datos de tu API con la UI de forma eficiente.

Diferencia con estado global

- Estado global (Redux/Zustand): guarda datos del cliente (UI, preferencias, etc.).

- React Query: guarda datos del servidor (API, base de datos) con estrategias de caché y revalidación.

---

## 🚀 Conceptos Clave

- **Caching**: Guarda los datos en memoria para evitar peticiones duplicadas.
- **Stale-while-revalidate**: Muestra datos "viejos" (stale) mientras descarga los nuevos en segundo plano.
- **Auto-Refetch**: Sincroniza los datos automáticamente cuando el usuario vuelve a enfocar la ventana.
- **Deduplicación**: Si dos componentes piden lo mismo al mismo tiempo, solo se hace una petición.

---

## 🛠️ Configuración Inicial

Instalación

```bash
npm install @tanstack/react-query
```

```jsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Dashboard />
    </QueryClientProvider>
  );
}
```

---

## ⚓ Hooks Principales

### 1. `useQuery` (Lectura)

Se usa para obtener datos. Requiere una `queryKey` única y una función que devuelva una promesa.

```jsx
const { data, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers
});
```

### 2. `useMutation` (Escritura)

Se usa para crear, actualizar o borrar datos.

```jsx
const mutation = useMutation({
  mutationFn: (newUser) => axios.post('/users', newUser),
  onSuccess: () => {
    // Invalida la caché para forzar un refetch de los usuarios
    queryClient.invalidateQueries({ queryKey: ['users'] });
  }
});
```

Características avanzadas

- Caché persistente (tiempo de vida configurable).

- Revalidación en segundo plano (stale-while-revalidate).

- Paginación y carga infinita (useInfiniteQuery).

- Deduplicación de peticiones (mismas query key simultáneas).

- Prefetching para mejorar UX.

Configuración global del QueryClient

```jsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutos
      cacheTime: 1000 * 60 * 10,
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});
```

---

## 💡 ¿Por qué usarlo?

| Sin React Query | Con React Query |
| :--- | :--- |
| `useEffect` manual + `useState` | Declarativo y automático |
| Lógica compleja de `loading/error` | Variables `isLoading`, `isError` integradas |
| Se pierden datos al navegar | Caché persistente entre rutas |
| Múltiples peticiones idénticas | Deduplicación inteligente |

---
Comparación con useEffect + useState
|Con useEffect|Con React Query|
|-|-|
|Manual handling de loading/error|Automático|
|Sin caché|Caché automático|
|Solicitudes duplicadas|Deduplicación|
|Dependencia manual de efectos|Declarativo con queryKey|

---

## Buenas prácticas

- Usa queryKey bien definidas (array con parámetros).

- Separa las funciones de queryFn en archivos de API.

- Usa enabled para consultas condicionales (ej. solo si hay un id).

- Combínalo con Zustand/Redux solo para estado local del cliente.

React Query vs Redux (para datos de API)

No compiten; se complementan. React Query maneja el servidor-estado; Redux maneja el cliente-estado. Puedes usar ambos.

[⬅️ Volver al Índice](../README.md)
