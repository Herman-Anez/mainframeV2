# Librerías de cliente: SWR y TanStack Query

Para la obtención de datos en el cliente, Next.js recomienda dos bibliotecas principales: **SWR** (creada por Vercel) y **TanStack Query** (antes React Query). Ambas resuelven la gestión del estado del servidor, ofreciendo caché, revalidación automática, paginación y mutaciones optimistas.

## SWR (stale-while-revalidate)

SWR es una librería ligera que sigue el principio HTTP `stale-while-revalidate`: primero devuelve los datos en caché (**stale**), luego envía la solicitud al servidor y finalmente actualiza la interfaz con los nuevos datos.

### Instalación y Uso Básico

```bash
npm install swr
```

```tsx
'use client'
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function Perfil() {
  const { data, error, isLoading } = useSWR('/api/usuario', fetcher)

  if (isLoading) return <div>Cargando perfil...</div>
  if (error) return <div>Error al cargar datos</div>
  
  return <div>Hola, {data.nombre}</div>
}
```

### Características principales:
*   **Revalidación automática:** Se activa al enfocar la ventana, reconexión de red o intervalos configurables.
*   **Identificación por Key:** La URL (o key) y el `fetcher` identifican de forma única a la consulta.
*   **Mutaciones:** Soporte para `mutate` y actualizaciones optimistas.
*   **Paginación:** Manejo avanzado con `useSWRInfinite`.

---

## TanStack Query (React Query)

Es una solución más robusta y completa, con herramientas avanzadas para el manejo de caché, mutaciones con invalidación granular y herramientas de desarrollo.

### Instalación y Configuración

```bash
npm install @tanstack/react-query
```

**Configuración del Provider:**
```tsx
// app/providers.tsx
'use client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}
```

**Uso en un componente:**
```tsx
'use client'
import { useQuery } from '@tanstack/react-query'

export default function Usuarios() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['usuarios'],
    queryFn: () => fetch('/api/usuarios').then(r => r.json()),
  })
  // ...
}
```

---

## Integración con Next.js y Hidratación

Puedes precargar datos en el servidor y pasarlos como estado inicial para que el cliente los tenga al instante.

### Con TanStack Query (v5+)
Usa `HydrationBoundary` para hidratar el `queryClient` desde el servidor:

```tsx
// app/posts/page.tsx
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query'
import Posts from './Posts' // Client Component

export default async function PostsPage() {
  const queryClient = new QueryClient()
  
  await queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: () => fetch('https://api.example.com/posts').then(r => r.json()),
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Posts />
    </HydrationBoundary>
  )
}
```

---

## Revalidación y Mutaciones

### SWR (Mutación simple)
```tsx
const { mutate } = useSWRConfig()
await fetch('/api/crear', { method: 'POST', body })
mutate('/api/tareas') // Revalida esa clave específica
```

### TanStack Query (Mutación con invalidación)
```tsx
const mutation = useMutation({
  mutationFn: (nuevaTarea) => fetch('/api/tareas', { 
    method: 'POST', 
    body: JSON.stringify(nuevaTarea) 
  }),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['tareas'] })
  },
})
```

---

## ¿Cuándo usar cada una?

| Característica | SWR | TanStack Query |
| :--- | :--- | :--- |
| **Complejidad** | Baja / Media | Media / Alta |
| **Peso** | Muy ligero (~4kb) | Más pesado (~13kb) |
| **Herramientas** | Básicas | Devtools dedicadas |
| **Casos de uso** | Proyectos estándar, caching simple | Aplicaciones complejas, mutaciones optimistas |

> [!TIP]
> Ambas librerías funcionan perfectamente con Next.js. Si buscas simplicidad y ligereza, elige **SWR**. Si necesitas control total sobre el ciclo de vida de los datos y herramientas de depuración, **TanStack Query** es la mejor opción.
