
react-query.md


React Query (ahora TanStack Query) no es una librería de estado global, sino un gestor de estado asíncrono del servidor. Maneja fetching, caching, sincronización, actualizaciones en segundo plano, etc.
Diferencia con estado global

- Estado global (Redux/Zustand): guarda datos del cliente (UI, preferencias, etc.).

- React Query: guarda datos del servidor (API, base de datos) con estrategias de caché y revalidación.

Instalación

```bash
npm install @tanstack/react-query
```


Configuración básica
```jsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <MiApp />
    </QueryClientProvider>
  );
}
```


Uso de useQuery (fetch y caché)
```jsx
import { useQuery } from '@tanstack/react-query';

function ListaUsuarios() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['usuarios'],
    queryFn: () => fetch('/api/usuarios').then(res => res.json()),
  });

  if (isLoading) return <Spinner />;
  if (error) return <Error mensaje={error.message} />;
  return <ul>{data.map(user => <li key={user.id}>{user.name}</li>)}</ul>;

}
```

useMutation (para crear, actualizar, eliminar)

```jsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

function AgregarUsuario() {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: (nuevoUsuario) => fetch('/api/usuarios', {
      method: 'POST',
      body: JSON.stringify(nuevoUsuario),
      headers: { 'Content-Type': 'application/json' },
    }).then(res => res.json()),
    onSuccess: () => {

      // Invalida la caché de usuarios para refetch
      queryClient.invalidateQueries({ queryKey: ['usuarios'] });
    },
  });

  return (
    <button onClick={() => mutation.mutate({ name: 'Nuevo' })}>
      Agregar
    </button>
  );
}
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


Comparación con useEffect + useState
|Con useEffect|Con React Query|
|-|-|
|Manual handling de loading/error|Automático|
|Sin caché|Caché automático|
|Solicitudes duplicadas|Deduplicación|
|Dependencia manual de efectos|Declarativo con queryKey|

## Buenas prácticas

- Usa queryKey bien definidas (array con parámetros).

- Separa las funciones de queryFn en archivos de API.

- Usa enabled para consultas condicionales (ej. solo si hay un id).

- Combínalo con Zustand/Redux solo para estado local del cliente.

React Query vs Redux (para datos de API)

No compiten; se complementan. React Query maneja el servidor-estado; Redux maneja el cliente-estado. Puedes usar ambos.

