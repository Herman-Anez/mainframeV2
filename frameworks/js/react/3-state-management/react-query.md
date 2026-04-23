# 📡 TanStack Query (React Query)

React Query (ahora TanStack Query) es la librería definitiva para gestionar el **Estado del Servidor** en React. A diferencia de Redux o Zustand, no se enfoca en el estado global del cliente, sino en sincronizar los datos de tu API con la UI de forma eficiente.

---

## ⚖️ Auditoría de Contenido

> [!NOTE]
> Este archivo se enfoca exclusivamente en **Server State**. Es el complemento perfecto para [Redux](./redux.md) o [Zustand](./zustand.md), ya que elimina la necesidad de guardar datos de API en el estado global del cliente.

---

## 🏗️ Diferencia con Estado Global

*   **Estado global (Redux/Zustand)**: guarda datos del cliente (UI, preferencias, estados de formularios locales).
*   **React Query**: guarda datos del servidor (API, base de datos) con estrategias inteligentes de caché y revalidación.

---

## 🚀 Conceptos Clave

*   **Caching**: Guarda los datos en memoria para evitar peticiones duplicadas.
*   **Stale-while-revalidate**: Muestra datos "viejos" (stale) mientras descarga los nuevos en segundo plano.
*   **Auto-Refetch**: Sincroniza los datos automáticamente cuando el usuario vuelve a enfocar la ventana.
*   **Deduplicación**: Si dos componentes piden lo mismo al mismo tiempo, solo se hace una única petición real.

---

## 🛠️ Configuración Inicial

### Instalación

```bash
npm install @tanstack/react-query
```

### Setup del Provider

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

---

## 🏗️ Características Avanzadas

> [!REDUNDANT]
> Esta sección complementa a "Conceptos Clave" con detalles técnicos de implementación.

*   **Caché persistente**: tiempo de vida configurable.
*   **Revalidación en segundo plano**: (stale-while-revalidate).
*   **Paginación y carga infinita**: mediante `useInfiniteQuery`.
*   **Prefetching**: carga de datos anticipada para mejorar la UX.

### Configuración global del QueryClient

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

> [!REDUNDANT]
> La siguiente tabla repite la comparativa anterior con un enfoque más directo en el manejo manual vs automático.

| Con useEffect | Con React Query |
| :--- | :--- |
| Manual handling de loading/error | Automático |
| Sin caché | Caché automático |
| Solicitude duplicadas | Deduplicación |
| Dependencia manual de efectos | Declarativo con `queryKey` |

---

## 💡 Buenas Prácticas

*   **queryKey Estructuradas**: Usa arrays con parámetros (ej. `['user', id]`).
*   **Separación de API**: Define las funciones `queryFn` en archivos independientes.
*   **Uso de `enabled`**: Para consultas condicionales (ej. solo disparar si hay un token válido).
*   **Combinación**: Úsalo con Zustand/Redux solo para estado local que **no** provenga de una API.

---

## ⚔️ React Query vs Redux (para datos de API)

No compiten: **se complementan**. React Query maneja el *Server State* y Redux maneja el *Client State*. Puedes (y suele ser recomendable) usar ambos en proyectos grandes.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>

