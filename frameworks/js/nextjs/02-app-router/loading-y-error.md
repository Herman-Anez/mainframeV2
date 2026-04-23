# `loading.js` y `error.js`: Manejo de estados en App Router

El **App Router** simplifica drásticamente el manejo de estados de carga y errores mediante dos archivos especiales: `loading.js` y `error.js`. Ambos aprovechan **React Suspense** y los **Error Boundaries** de React para encapsular cada segmento de ruta.

## `loading.js` – UI de carga instantánea

Cuando una página (o un layout) tiene un componente asíncrono (Server Component que usa `await`), Next.js necesita mostrar algo mientras se resuelve la promesa. `loading.js` define el fallback de Suspense para esa ruta.

### Cómo funciona:

1.  Coloca `loading.js` en la misma carpeta que `page.js` (o en cualquier segmento).
2.  Mientras la página se genera (en el servidor o con streaming), se muestra el contenido de `loading.js`.
3.  Cuando la página está lista, se reemplaza automáticamente.

**Ejemplo básico:**

```jsx
// app/dashboard/loading.js
export default function DashboardLoading() {
  return (
    <div className="skeleton">
      <Spinner /> Cargando dashboard...
    </div>
  )
}
```

> [!NOTE]
> El archivo `loading.js` se convierte en un límite de Suspense para el segmento. Next.js lo envuelve automáticamente con `<Suspense fallback={<Loading/>}>`.

### Anidamiento

Si tienes `loading.js` en `app/` y otro en `app/blog/`, cada uno actúa solo para su segmento. Navegar a `/blog` mostrará el loading del blog, mientras el resto de la interfaz (layout) ya está disponible (**streaming**).

### Streaming y carga parcial

Cuando usas `loading.js`, no necesitas esperar que toda la página se genere. Next.js puede enviar el layout raíz y el shell de inmediato, luego el loading del segmento, y finalmente el contenido de la página. Esto mejora el **LCP** (Largest Contentful Paint) y la interactividad.

## `error.js` – Aislamiento de errores

`error.js` define un **Error Boundary** para una ruta. Captura errores ocurridos en los Server Components o Client Components hijos, sin afectar el resto de la interfaz.

### Requisitos:

*   **Debe ser un Client Component** (porque maneja el ciclo de vida de error).
*   Exporta una función que recibe `{ error, reset }`.

```jsx
'use client' // Error boundaries must be Client Components

import { useEffect } from 'react'

export default function DashboardError({ error, reset }) {
  useEffect(() => {
    // Loguear el error a un servicio externo
    console.error(error)
  }, [error])

  return (
    <div>
      <h2>Ocurrió un error en el dashboard</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Intentar de nuevo</button>
    </div>
  )
}
```

> [!IMPORTANT]
> *   `reset()` es una función que intenta re-renderizar el segmento. Si el error fue transitorio (p. ej., fetch fallido), el segmento se recupera sin recargar toda la página.
> *   El error no se propaga a los layouts superiores ni a la página raíz (a menos que no haya un boundary intermedio).

### Ubicación:

Coloca `error.js` en la carpeta del segmento a proteger. Puedes tener múltiples niveles (por ejemplo, `app/error.js` global y uno específico en `app/dashboard/error.js`). El más cercano captura primero.

## `not-found.js`

Aunque no es exactamente de error, es relevante. `not-found.js` se muestra cuando se invoca `notFound()` desde un Server Component o se visita una ruta inexistente. Reemplaza al antiguo `404.js`.

```jsx
import { notFound } from 'next/navigation'

export default async function Page({ params }) {
  const post = await getPost(params.slug)
  if (!post) notFound()
  // ...
}
```

> [!TIP]
> `not-found.js` puede estar en cualquier nivel; el más cercano se muestra. Se renderiza dentro del layout, conservando la interfaz global.

## Combinación de `loading` y `error`

Puedes tener ambos en el mismo directorio. Por ejemplo:

```text
app/
├── dashboard/
│   ├── loading.js
│   ├── error.js
│   └── page.js
```

1.  Primero se muestra `loading.js` mientras `page.js` espera.
2.  Si ocurre un error, `error.js` lo captura y muestra la UI de error.

### Manejo de errores en Server Actions

Los errores lanzados en **Server Actions** se pueden capturar en el error boundary correspondiente a la ruta donde se usó, o bien manejarlos localmente con `try/catch` en el Client Component.

### Caché de errores

El error boundary mantiene la UI de error mientras no se llame `reset()`. Si se recarga la página, se reintenta el renderizado original. No hay almacenamiento en caché del error.

## Migración desde Pages Router

En **Pages Router** tenías que implementar estados de carga manualmente (`router.isFallback`, estados locales para SSR). En **App Router**, la experiencia es declarativa, mucho más limpia y robusta.

---

`loading.js` y `error.js` representan uno de los mayores avances del App Router: encapsulan el comportamiento esperado de cualquier aplicación moderna con mínimo código.