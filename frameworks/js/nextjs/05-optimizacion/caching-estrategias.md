# Estrategias de Caché en Next.js

Next.js ofrece varias capas de caché que pueden combinarse para obtener el mejor equilibrio entre rendimiento y frescura de datos. Este capítulo profundiza en cómo diseñar una estrategia de caché efectiva.

## Capas de Caché (Repaso Ampliado)

| Capa | Ubicación | Duración / Propósito |
| :--- | :--- | :--- |
| **Router Cache** | Cliente (Navegador) | ~30s. Navegación instantánea entre rutas ya visitadas. |
| **Full Route Cache** | Servidor | Persiste hasta revalidación o redeploy. Almacena HTML y RSC payload. |
| **Data Cache** | Servidor | Persistente entre despliegues. Almacena respuestas de `fetch`. |
| **Image Cache** | Servidor | Caché específica para imágenes optimizadas. |

---

## Estrategias según el tipo de datos

### 1. Contenido estático rara vez cambiante
*   **Ejemplo:** Páginas "Acerca de", Términos y Condiciones.
*   **Estrategia:** SSG completo (en build) + ISR con revalidación larga (ej. 24h).
*   **Implementación:** `export const revalidate = 86400`.

### 2. Contenido público con cambios frecuentes
*   **Ejemplo:** Listado de noticias, blog con comentarios.
*   **Estrategia:** ISR con tiempos cortos (60-300 segundos) combinada con revalidación bajo demanda.
*   **Implementación:** `fetch(url, { next: { revalidate: 60 } })`.

### 3. Contenido personalizado (Dashboard)
*   **Ejemplo:** Perfil de usuario, configuraciones privadas.
*   **Estrategia:** SSR (Dinámico) para la página, pero con caché granular para datos comunes usando `tags`.
*   **Implementación:** `fetch(url, { next: { tags: ['user-data'] } })`.

### 4. Datos en tiempo real de alta frecuencia
*   **Ejemplo:** Precios de acciones, chats, marcadores deportivos.
*   **Estrategia:** Cliente-side fetching (SWR o TanStack Query) con polling o WebSockets. El servidor solo entrega el "shell" estático.

---

## Técnicas avanzadas de invalidación

### Invalidación granular con `tags`
Etiqueta tus peticiones para invalidar grupos de datos de forma precisa.

```tsx
// app/blog/page.tsx
const posts = await fetch('.../posts', { next: { tags: ['posts'] } })

// app/blog/[id]/page.tsx
const post = await fetch(`.../posts/${id}`, { next: { tags: [`post-${id}`, 'posts'] } })
```

> [!TIP]
> Al ejecutar `revalidateTag('posts')`, invalidas tanto la lista como los detalles de los posts individuales, asegurando coherencia total en la caché.

### Revalidación en Server Actions
```tsx
'use server'
import { revalidateTag, revalidatePath } from 'next/cache'

export async function updateAction(data) {
  await db.update(data)
  revalidateTag('posts')
  revalidatePath('/blog') // Refresca la caché de la ruta completa
}
```

### Refresco del Router Cache
En Client Components, usa `router.refresh()` para invalidar la caché de navegación y recuperar datos frescos del servidor para la ruta actual sin recargar la página.

```tsx
import { useRouter } from 'next/navigation'

const router = useRouter()
router.refresh()
```

---

## Configuración de tiempos de stale (Next.js 15)

En versiones recientes, puedes ajustar experimentalmente el tiempo que las rutas se mantienen en el cliente:

```javascript
// next.config.js
module.exports = {
  experimental: {
    staleTimes: {
      dynamic: 30,  // Segundos para rutas dinámicas
      static: 300,  // Segundos para rutas estáticas
    },
  },
}
```

---

## Depuración y Herramientas

*   **Encabezado `X-Nextjs-Cache`:** Inspecciona las respuestas para ver estados como `HIT`, `STALE`, `MISS` o `BYPASS`.
*   **Build Output:** Identifica qué rutas son estáticas (`○`) o dinámicas (`λ`).
*   **Vercel Logs:** Monitorea eventos de revalidación en tiempo real.

> [!IMPORTANT]
> En entorno de **Desarrollo**, la mayoría de las cachés están desactivadas para facilitar la iteración. Asegúrate de probar tus estrategias en un entorno de **Staging** o **Producción**.

---

Una estrategia de caché bien diseñada permite que tu aplicación escale masivamente sin sacrificar la frescura de los datos críticos.

---
[<- Anterior: Cache y Revalidate](../04-data-fetching/cache-y-revalidate.md) | [Siguiente: Next Image ->](next-image.md)
