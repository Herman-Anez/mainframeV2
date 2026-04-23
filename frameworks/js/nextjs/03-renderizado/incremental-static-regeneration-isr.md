
## Archivo: `03-renderizado/incremental-static-regeneration-isr.md`

Incremental Static Regeneration (ISR)

ISR permite actualizar páginas estáticas después del build sin necesidad de reconstruir todo el sitio. Next.js regenera la página en segundo plano cuando ocurre una solicitud después de que el tiempo revalidate ha expirado.
ISR en Pages Router

Se configura mediante la propiedad revalidate en el objeto retornado por getStaticProps.

```jsx
export async function getStaticProps() {
  const res = await fetch('https://.../posts')
  const posts = await res.json()

  return {
    props: { posts },
    revalidate: 60, // regenerar como máximo cada 60 segundos
  }
}
```

    La primera solicitud después del build servirá la página estática generada.

    Tras 60 segundos, la siguiente solicitud todavía sirve la versión anterior (stale), pero dispara una regeneración en segundo plano.

    La solicitud que activó la regeneración podría ver la versión antigua (o nueva con una bandera de stale) dependiendo de la estrategia.

    Una vez completada la regeneración, Next.js actualiza la caché y las siguientes peticiones verán la nueva versión.

### ISR con fallback en rutas dinámicas

Para rutas dinámicas con getStaticPaths, puedes combinar fallback: true o 'blocking' con revalidate. Así, las páginas no pre-renderizadas se generan bajo demanda (como ISR inicial) y luego se regeneran según revalidate.
ISR en App Router

En el App Router, la ISR se configura a nivel de fetch o por segmento de ruta.

### Opción 1: fetch con next.revalidate

```jsx
// app/products/page.js
export default async function Products() {
  const res = await fetch('https://.../products', { next: { revalidate: 60 } })
  const products = await res.json()
  return <ProductList products={products} />
}
```

Next.js almacenará en caché la respuesta de fetch (Data Cache) por 60 segundos. La página se servirá estáticamente, pero se actualizará la data en background si hay una solicitud que lo requiere después del período.

### Opción 2: Segment config revalidate

Exporta una constante revalidate desde la página o layout:

```jsx
export const revalidate = 60
```

Esto establece el revalidate para toda la ruta. Si además usas fetch sin especificar revalidate, hereda este valor.

### Opción 3: Revalidación bajo demanda (On-demand revalidation)

Además de revalidación por tiempo, puedes regenerar páginas específicas mediante revalidación por etiqueta o ruta usando Server Actions o Route Handlers.

    revalidatePath('/products') – revalida una ruta completa.

    revalidateTag('products') – revalida todos los fetch que tengan ese tag.

Ejemplo con fetch etiquetado:

```jsx
const res = await fetch('https://...', { next: { tags: ['products'] } })
```

Luego, desde una Server Action después de una mutación:

```jsx
import { revalidateTag } from 'next/cache'

export async function updateProduct() {
  // ... actualizar
  revalidateTag('products')
}
```

Esto limpia la caché de datos asociada a esa etiqueta y la próxima visita regenerará la página con datos frescos.
Cómo funciona la caché de datos

Next.js mantiene un Data Cache persistente entre builds y deployments (en Vercel) o en memoria (en Node.js). Cuando usas fetch con las opciones next.revalidate o tags, los datos se almacenan en este caché. La página se renderiza con esos datos cacheados y se sirve. Al expirar el revalidate o al invalidar manualmente, la siguiente solicitud hace fetch nuevamente.
Stale-while-revalidate

El comportamiento por defecto es stale-while-revalidate: se sirve la página cacheada mientras se regenera en background. Esto garantiza que el usuario nunca espere por la regeneración.

Puedes cambiar este comportamiento con revalidate = 0: fuerza la regeneración en cada solicitud (como SSR) sin servir stale.
Configuración avanzada

    Revalidación a nivel de layout: También puedes colocar export const revalidate = N en un layout.js; afectará a todas las páginas anidadas.

    ISR en Edge: Soportado en Vercel y entornos compatibles.

    Caché de Imágenes: next/image tiene su propio mecanismo de revalidación; no afecta al Data Cache.

### Caso de uso típico

Un blog con miles de artículos. Generas las páginas más populares en build, el resto con fallback: 'blocking'. Todas las páginas se regeneran si son visitadas después de 3600 segundos (revalidate: 3600). Cuando el autor edita un artículo, se activa una revalidación bajo demanda vía webhook, actualizando solo esa página.

ISR te da lo mejor de SSG y SSR: velocidad estática con contenido casi en tiempo real
---
