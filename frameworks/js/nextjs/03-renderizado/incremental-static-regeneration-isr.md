# Incremental Static Regeneration (ISR)

**ISR** permite actualizar páginas estáticas después del build sin necesidad de reconstruir todo el sitio. Next.js regenera la página en segundo plano cuando ocurre una solicitud después de que el tiempo de revalidación (`revalidate`) ha expirado.

## ISR en Pages Router

Se configura mediante la propiedad `revalidate` en el objeto retornado por `getStaticProps`.

```jsx
export async function getStaticProps() {
  const res = await fetch('https://api.example.com/posts')
  const posts = await res.json()

  return {
    props: { posts },
    revalidate: 60, // regenerar como máximo cada 60 segundos
  }
}
```

### Funcionamiento:
1.  **Build:** La primera solicitud sirve la página estática generada en tiempo de compilación.
2.  **Período Stale:** Tras 60 segundos, la siguiente solicitud todavía sirve la versión anterior (**stale**), pero dispara una regeneración en segundo plano.
3.  **Actualización:** Una vez completada la regeneración, Next.js actualiza la caché y las siguientes peticiones verán la nueva versión.

> [!NOTE]
> Para rutas dinámicas con `getStaticPaths`, puedes combinar `fallback: true` o `'blocking'` con `revalidate`. Así, las páginas no pre-renderizadas se generan bajo demanda y luego se regeneran según el intervalo definido.

## ISR en App Router

En el App Router, la ISR se configura a nivel de `fetch` o por segmento de ruta.

### Opción 1: `fetch` con `next.revalidate`

```jsx
// app/products/page.js
export default async function Products() {
  const res = await fetch('https://api.example.com/products', { 
    next: { revalidate: 60 } 
  })
  const products = await res.json()
  return <ProductList products={products} />
}
```

Next.js almacenará en caché la respuesta de `fetch` (**Data Cache**) por 60 segundos. La página se servirá estáticamente, pero se actualizará la data en background si hay una solicitud después del período.

### Opción 2: Segment Config `revalidate`

Exporta una constante `revalidate` desde la página o layout:

```jsx
export const revalidate = 60
```

> [!TIP]
> Esto establece el `revalidate` para toda la ruta. Si además usas `fetch` sin especificar `revalidate`, heredará este valor automáticamente.

### Opción 3: Revalidación bajo demanda (On-demand revalidation)

Además de revalidación por tiempo, puedes regenerar páginas específicas mediante etiquetas o rutas usando **Server Actions** o **Route Handlers**.

*   `revalidatePath('/products')` – revalida una ruta completa.
*   `revalidateTag('products')` – revalida todos los `fetch` que tengan esa etiqueta.

**Ejemplo con fetch etiquetado:**
```jsx
const res = await fetch('https://api.example.com/data', { 
  next: { tags: ['products'] } 
})
```

**Ejemplo de Server Action para invalidar:**
```jsx
'use server'
import { revalidateTag } from 'next/cache'

export async function updateProduct() {
  // ... lógica de actualización en BD
  revalidateTag('products')
}
```

## Cómo funciona la caché de datos

Next.js mantiene un **Data Cache** persistente entre builds y deployments. Cuando usas `fetch` con `next.revalidate` o `tags`, los datos se almacenan en este caché. Al expirar el tiempo o al invalidar manualmente, la siguiente solicitud realiza el `fetch` nuevamente.

### Estrategia Stale-while-revalidate

El comportamiento por defecto es **stale-while-revalidate**: se sirve la página cacheada mientras se regenera en background. Esto garantiza que el usuario nunca espere por la regeneración de la interfaz.

> [!IMPORTANT]
> Si estableces `revalidate = 0`, fuerzas la regeneración en cada solicitud (similar a SSR) sin servir contenido stale.

## Configuración avanzada

*   **Revalidación en Layouts:** Colocar `export const revalidate = N` en un `layout.js` afectará a todas las páginas anidadas.
*   **ISR en el Edge:** Soportado en Vercel y entornos compatibles para una distribución global más rápida.
*   **Caché de Imágenes:** `next/image` tiene su propio mecanismo de revalidación independiente del Data Cache.

## Caso de uso típico

Un blog con miles de artículos: Generas las páginas más populares en el build y el resto con `fallback: 'blocking'`. Todas las páginas se regeneran si son visitadas después de 3600 segundos (`revalidate: 3600`). Cuando el autor edita un artículo, se activa una **revalidación bajo demanda** vía webhook, actualizando solo esa página específica de forma instantánea.

---

ISR ofrece el equilibrio perfecto entre SSG y SSR: la velocidad de archivos estáticos con la frescura de contenido dinámico.
