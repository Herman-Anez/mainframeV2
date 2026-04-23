# Patrones de obtención de datos en App Router

El **App Router** introduce **React Server Components (RSC)**, que permiten obtener datos directamente en el servidor, dentro del componente, sin necesidad de funciones externas como `getStaticProps`. Además, extiende la API `fetch` nativa con potentes opciones de caching y revalidación.

## Obtención en Server Components

En un Server Component puedes usar `async/await` y `fetch` directamente. Next.js optimiza las solicitudes automáticamente para evitar redundancias.

```tsx
// app/productos/page.tsx
export default async function Productos() {
  const res = await fetch('https://api.ejemplo.com/productos')
  const productos = await res.json()
  
  return (
    <ul>
      {productos.map(p => (
        <li key={p.id}>{p.nombre}</li>
      ))}
    </ul>
  )
}
```

> [!NOTE]
> Por defecto, `fetch` usa `cache: 'force-cache'`, lo que vuelve la página estática (**SSG**). Los datos se almacenan en el **Data Cache** hasta que sean invalidados o revalidados.

## Control de caché por `fetch`

Puedes ajustar el comportamiento de cada petición mediante el segundo argumento de `fetch`:

*   **`cache: 'force-cache'`** (Por defecto): Datos cacheados. Página estática.
*   **`cache: 'no-store'`**: Datos frescos en cada solicitud. Página dinámica (**SSR**).
*   **`next: { revalidate: N }`**: **ISR**. Cachea por N segundos y luego revalida en background.
*   **`next: { tags: ['mi-tag'] }`**: Permite revalidación bajo demanda mediante `revalidateTag`.

```tsx
const res = await fetch('https://api...', { next: { revalidate: 60 } })
```

---

## Fetching Paralelo vs Secuencial

### 1. Paralelo (Recomendado)
Si los datos no dependen entre sí, ejecútalos simultáneamente para reducir el tiempo total de carga.

```tsx
const [productos, categorias] = await Promise.all([
  fetch('.../productos').then(r => r.json()),
  fetch('.../categorias').then(r => r.json())
])
```

### 2. Secuencial
Úsalo solo cuando una petición dependa del resultado de la anterior.
```tsx
const user = await fetch(`.../user/${id}`).then(r => r.json())
const posts = await fetch(`.../posts?userId=${user.id}`).then(r => r.json())
```

---

## Precarga con `generateStaticParams`

Para rutas dinámicas que deben ser estáticas, usa `generateStaticParams` para pre-renderizarlas durante el build.

```tsx
export async function generateStaticParams() {
  const posts = await fetch('.../posts').then(r => r.json())
  return posts.map(post => ({ slug: post.slug }))
}
```

---

## Patrón Híbrido: Server + Client

Obtén los datos iniciales en el servidor y pásalos a un Client Component que maneje la interactividad o actualizaciones en vivo.

```tsx
// app/productos/page.tsx (Server Component)
import ListaProductos from './ListaProductos'

export default async function Pagina() {
  const productos = await fetch('...').then(r => r.json())
  return <ListaProductos productosIniciales={productos} />
}
```

```tsx
// ListaProductos.tsx (Client Component)
'use client'
import useSWR from 'swr'

export default function ListaProductos({ productosIniciales }) {
  const { data } = useSWR('...', fetcher, { fallbackData: productosIniciales })
  // ... lógica de cliente
}
```

---

## Streaming y Suspense

Envuelve componentes con fetching lento en `<Suspense>` para evitar bloquear el renderizado de toda la página.

```tsx
import { Suspense } from 'react'
import ProductosRecomendados from './ProductosRecomendados' // Server Component lento

export default function Tienda() {
  return (
    <div>
      <h1>Tienda</h1>
      <Suspense fallback={<div>Cargando recomendados...</div>}>
        <ProductosRecomendados />
      </Suspense>
    </div>
  )
}
```

---

## Recomendaciones generales

*   **Prioriza Server Components** para datos públicos o estructurales.
*   **Usa `Suspense`** para descomponer la carga y mejorar el LCP.
*   **Aprovecha el Data Cache** de Next.js; desactívalo (`no-store`) solo cuando los datos en tiempo real sean estrictamente necesarios.
*   **Revalidación bajo demanda:** Etiqueta tus fetch con `tags` e invalídalos tras mutaciones en **Server Actions**.

---

El App Router ofrece un modelo declarativo y flexible alineado con el streaming de React, facilitando aplicaciones más rápidas y fáciles de mantener.
