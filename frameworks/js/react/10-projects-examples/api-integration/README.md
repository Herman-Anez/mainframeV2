# 📡 Ejemplo: Integración con API (Data Fetching)

Este proyecto práctico enseña cómo interactuar con servicios externos, manejar estados de carga y errores, y optimizar el rendimiento mediante caché dinámica.

---

## 🏗️ Arquitectura del Ejemplo

Comparamos dos enfoques populares para obtener datos en React: **useEffect (Básico)** y **TanStack Query (Profesional)**.

| Componente | Responsabilidad |
| :--- | :--- |
| **`UserDashboard`** | Componente contenedor que orquesta la carga de datos. |
| **`SkeletonLoader`** | Interfaz visual de carga (Fallback) para mejorar el UX. |
| **`ErrorMessage`** | Gestión visual de fallos en la petición. |
| **`Pagination`** | Lógica de navegación entre conjuntos de datos. |

---

## 🧠 Conceptos Aplicados

1.  **React Query**: Manejo automático de caché, reintentos (retries) y re-fetching al enfocar la ventana.
2.  **AbortController**: Cómo cancelar peticiones asíncronas si el componente se desmonta antes de terminar.
3.  **Debouncing**: Optimización de peticiones de búsqueda para no colapsar el servidor en cada pulsación de tecla.

---

## 🚀 Desafíos Sugeridos

*   **Offline Mode**: Usa `useQuery` con `networkMode: 'offlineFirst'` para mostrar datos cacheados sin conexión.
*   **Infinite Scroll**: Implementa `useInfiniteQuery` en lugar de paginación tradicional.
*   **Mutation**: Crea un componente para añadir nuevos items ejecutando un `POST` y actualizando la caché local (`invalidateQueries`).

---

<div align="center">

[⬅️ Volver al Índice](../../README.md)

</div>
