# Caché y revalidación en Next.js

Next.js posee varios niveles de caché que trabajan juntos para ofrecer un rendimiento óptimo. Comprender cómo operan y cómo controlarlos es fundamental para equilibrar la frescura de los datos y la velocidad de respuesta.

## Las capas de caché

| Nivel de Caché | Ubicación | Propósito |
| :--- | :--- | :--- |
| **Router Cache** | Cliente (Navegador) | Almacena en memoria las páginas visitadas (RSC payload) para navegación instantánea. |
| **Full Route Cache** | Servidor | Caché del HTML y RSC payload pre-renderizados. Se guarda en el servidor o CDN. |
| **Data Cache** | Servidor | Caché persistente de resultados de `fetch`. Se mantiene entre builds y despliegues. |
| **Image Cache** | Servidor | Caché independiente para imágenes optimizadas por `next/image`. |

### Detalles clave:
*   **Router Cache:** Se limpia al recargar la página o tras un tiempo de inactividad (30s por defecto).
*   **Full Route Cache:** Se invalida mediante revalidaciones (por tiempo o bajo demanda).
*   **Data Cache:** Controlado por `revalidate`, `tags` o invalidación manual.

## Revalidación basada en tiempo (ISR)

Para páginas que obtienen datos con `fetch`, puedes especificar `next.revalidate`:

```tsx
export default async function Pagina() {
  const res = await fetch('https://api.example.com/data', { 
    next: { revalidate: 60 } 
  })
  // ...
}
```

> [!NOTE]
> Esto almacena los datos en el **Data Cache** por 60 segundos. Durante ese intervalo, se sirve la versión cacheada. Pasado el tiempo, la próxima solicitud dispara una regeneración en segundo plano (**stale-while-revalidate**).

También puedes configurar el tiempo de revalidación a nivel de segmento:
```tsx
export const revalidate = 120 // Segundos
```

> [!TIP]
> Si hay múltiples `fetch` con diferentes tiempos de revalidación, Next.js tomará el valor **menor** como referencia para el segmento completo.

## Revalidación bajo demanda (On-demand)

Ideal para casos donde el contenido debe actualizarse inmediatamente tras una mutación (ej. publicar un artículo).

### 1. Mecanismo de etiquetas (`tags`)
Etiqueta tus peticiones `fetch` para una invalidación precisa:
```tsx
const res = await fetch('https://...', { next: { tags: ['posts'] } })
```

Para invalidar desde una Server Action o Route Handler:
```tsx
import { revalidateTag } from 'next/cache'

export async function action() {
  revalidateTag('posts') // Todos los fetch con ese tag se invalidan
}
```

### 2. Revalidación por ruta
```tsx
import { revalidatePath } from 'next/cache'

revalidatePath('/blog')           // Revalida esa ruta específica
revalidatePath('/blog/[slug]')    // Revalida todas las rutas dinámicas coincidentes
```

## Forzar comportamiento dinámico

Si necesitas que una ruta nunca se cachee (comportamiento 100% SSR), puedes:

1.  Usar `cache: 'no-store'` en todos los `fetch`.
2.  Exportar `export const dynamic = 'force-dynamic'`.
3.  Utilizar funciones dinámicas como `cookies()`, `headers()` o `searchParams`.

> [!IMPORTANT]
> Cuando ejecutas en **Edge Runtime**, el Data Cache puede no estar disponible dependiendo del proveedor. En Vercel, Edge tiene acceso a la caché distribuida global de forma idéntica al Node.js runtime.

## Resumen de comandos y opciones

| Acción | Implementación |
| :--- | :--- |
| **Revalidar por tag** | `revalidateTag('tag')` |
| **Revalidar ruta exacta** | `revalidatePath('/ruta')` |
| **Revalidar ruta dinámica** | `revalidatePath('/ruta/[param]')` |
| **Forzar dinámico** | `export const dynamic = 'force-dynamic'` |
| **Fijar revalidate por ruta** | `export const revalidate = 3600` |
| **No cachear fetch** | `fetch(url, { cache: 'no-store' })` |

---

Entender estos mecanismos te permitirá afinar la frescura de los datos sin sacrificar el rendimiento de tu aplicación.