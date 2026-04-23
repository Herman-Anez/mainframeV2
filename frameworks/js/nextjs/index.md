


---




---


---


---


---

## Archivo: `03-renderizado/server-side-rendering-ssr.md`

Server-Side Rendering (SSR) en Next.js

El Server-Side Rendering es una técnica donde la página se genera en el servidor por cada solicitud que el cliente realiza. Next.js lo soporta de forma nativa tanto en Pages Router como en App Router, aunque con aproximaciones diferentes.
SSR en Pages Router

Se logra mediante la función getServerSideProps exportada de la página. El servidor ejecuta esta función en cada petición, obtiene datos y los pasa como props al componente. El HTML resultante se envía al navegador.
```jsx
export async function getServerSideProps(context) {
  const res = await fetch(`https://...`)
  const data = await res.json()
  return { props: { data } }
}
```

El tiempo hasta el primer byte (TTFB) es mayor porque el servidor debe ejecutar la función antes de responder. Sin embargo, el cliente recibe HTML listo, lo que favorece el SEO y el LCP.
SSR en App Router

En el App Router no existe getServerSideProps. En su lugar, usas Server Components dinámicos con fetch sin caché o utilizando las opciones dynamic = 'force-dynamic'.

### Forma 1: fetch con cache: 'no-store'
```jsx
// app/dashboard/page.js
export default async function Dashboard() {
  const res = await fetch('https://...', { cache: 'no-store' })
  const data = await res.json()
  return <div>{data.content}</div>
}
```

Al marcar cache: 'no-store', Next.js trata la página como dinámica: se renderiza en cada solicitud (tanto en Node.js como en Edge Runtime).

### Forma 2: Opciones de segmento

Exporta export const dynamic = 'force-dynamic' desde la página o layout. Esto obliga a la ruta a ser completamente dinámica.
```jsx
export const dynamic = 'force-dynamic'
```

### Forma 3: Uso de cookies o headers

Si el componente utiliza cookies() o headers() de next/headers, la ruta automáticamente se vuelve dinámica, porque estos datos dependen de la solicitud.
Diferencia entre SSR y "dinámico" en App Router

En App Router, "dinámico" no es un switch global, sino que se determina por el comportamiento de la ruta. Si la ruta no usa fuentes dinámicas, seguirá siendo estática por defecto. Esto permite un renderizado híbrido: puedes tener partes estáticas y partes dinámicas en el mismo layout gracias al streaming.
Ventajas y desventajas del SSR

Ventajas:

    Contenido actualizado en tiempo real (personalización, sesiones, noticias recientes).

    Buen SEO sin configuración adicional.

    Adecuado para datos que cambian frecuentemente.

Desventajas:

    Mayor carga del servidor (cada petición ejecuta lógica).

    Tiempo de respuesta más alto que contenido estático en CDN.

    Escalado más complejo (no cacheable directamente en CDN sin configuración adicional).

### Estrategias de caché para SSR

Incluso con SSR, puedes añadir encabezados de caché desde el servidor (Node.js) para reducir la carga.

En Pages Router:
```js
export async function getServerSideProps({ res }) {
  res.setHeader('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=300')
  // ...
}
```

En App Router: Puedes usar el objeto response de NextResponse en Route Handlers, pero para páginas no tienes acceso directo a res. En su lugar, utiliza la función revalidate o configura el Data Cache con fetch y next.revalidate. Para SSR puro sin caché, basta con no-store. Si quieres algo intermedio, considera ISR.
¿Cuándo elegir SSR?

    Páginas muy personalizadas (dashboard de usuario con datos en vivo).

    Aplicaciones donde cada usuario ve contenido distinto y esos datos no se pueden compartir.

    Funcionalidades que requieren lectura de cookies/headers de manera directa.

En proyectos reales, rara vez todo es SSR; Next.js te permite mezclar SSG, ISR y SSR según la página.
---

## Archivo: `03-renderizado/static-generation-ssg.md`

Static Site Generation (SSG) en Next.js

La generación de sitios estáticos implica pre-renderizar las páginas en tiempo de compilación (next build). El resultado son archivos HTML (y JSON para transiciones del lado del cliente) que pueden servirse directamente desde un CDN.
SSG en Pages Router

Se logra con la función getStaticProps (y getStaticPaths para rutas dinámicas). La página se construye una vez y se sirve estáticamente, lo que garantiza el mejor rendimiento posible y excelente SEO.
```jsx
// pages/posts/[slug].js
export async function getStaticProps({ params }) {
  const post = await getPost(params.slug)
  return { props: { post } }
}

export async function getStaticPaths() {
  const posts = await getAllPosts()
  const paths = posts.map(p => ({ params: { slug: p.slug } }))
  return { paths, fallback: false }
}

export default function Post({ post }) {
  return <article>{post.title}</article>
}
```

### SSG en App Router

En el App Router, los Server Components son estáticos por defecto cuando no utilizan fuentes de datos dinámicas (es decir, si no contienen cookies(), headers(), o fetch con cache: 'no-store'). Durante el build, Next.js renderiza esas rutas y las guarda como archivos estáticos.

No necesitas exportar funciones especiales; solo escribe un Server Component normal que obtenga datos sin forzar dinamismo:
```jsx
// app/about/page.js
export default function About() {
  return <h1>Acerca de Nosotros</h1>
}
```

Para contenido que proviene de una API externa:
```jsx
export default async function Blog() {
  const posts = await fetch('https://api.../posts') // sin cache: 'no-store'
  const data = await posts.json()
  return <>{data.map(...)}</>
}
```

Al no indicar cache: 'no-store', fetch usa el comportamiento predeterminado de caché (force-cache). Entonces Next.js hará la solicitud en build, cacheará el resultado (Data Cache) y generará HTML estático. Si necesitas regenerar ese contenido más adelante, configura ISR con next.revalidate.
Rutas dinámicas estáticas

En App Router, si necesitas pre-renderizar rutas dinámicas, debes generar los parámetros estáticos usando generateStaticParams.
```jsx
// app/blog/[slug]/page.js
export default function BlogPost({ params }) { ... }

export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then(res => res.json())
  return posts.map(post => ({ slug: post.slug }))
}
```

generateStaticParams reemplaza a getStaticPaths. Solo los slugs devueltos serán pre-renderizados en build. Por defecto, dynamicParams = true, lo que significa que cualquier ruta no generada en build se renderizará bajo demanda (como SSR) y luego se cacheará. Puedes cambiar a dynamicParams = false para que las rutas no pre-renderizadas devuelvan 404.
Ventajas del SSG

    Velocidad: El HTML es servido desde CDN (tiempo de respuesta casi instantáneo).

    Escalabilidad: Sin carga en el servidor por petición.

    SEO óptimo: Los motores de búsqueda reciben todo el contenido.

### Desventajas

    Tiempo de build más largo para muchos miles de páginas (aunque generateStaticParams y el renderizado de build pueden demorar).

    Contenido desactualizado si no implementas ISR.

### Combinación con ISR

Para obtener lo mejor de ambos mundos, puedes agregar revalidate a tus fetch o configurarlo en el segmento. Así la página se vuelve estática pero se regenera en segundo plano a intervalos definidos. (Esto se trata en profundidad en el siguiente capítulo).
¿Cuándo usar SSG?

    Blogs, portafolios, documentación.

    Páginas de producto donde el contenido no cambia con cada visita.

    Cualquier página que no dependa de datos personalizados en cada solicitud.

Si alguna parte de la página necesita interactividad o personalización, se puede implementar con Client Components que obtengan datos adicionales en el cliente, mientras el esqueleto estático se entrega casi instantáneamente.
---

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

ISR te da lo mejor de SSG y SSR: velocidad estática con contenido casi en tiempo real.
---

## Archivo: `03-renderizado/streaming-y-suspense.md`

Streaming y Suspense en Next.js

El streaming es una técnica que permite al servidor enviar partes del HTML al cliente a medida que se generan, en lugar de esperar a que toda la página esté lista. Next.js lo implementa usando React Suspense y los Server Components, permitiendo una carga progresiva y mejores métricas.
Cómo funciona en Next.js

Cuando un Server Component se suspende (porque está esperando una promesa), Next.js no bloquea toda la respuesta. En su lugar, envía el shell de la aplicación (los layouts y componentes que ya están listos) y luego, a medida que los datos se resuelven, envía el HTML restante en el mismo stream HTTP.

El navegador puede empezar a pintar el HTML parcial inmediatamente, reduciendo el Time to First Byte (TTFB) y el First Contentful Paint (FCP).
Implementación con loading.js

La forma más simple de habilitar streaming es crear un archivo loading.js en el segmento que tarda. loading.js se convierte en el fallback de Suspense para esa ruta.

Estructura básica:
```text
app/
├── layout.js
└── posts/
    ├── page.js        (obtiene datos lentos)
    └── loading.js     (UI de carga)
```

Cuando se visita /posts, Next.js envía inmediatamente el layout (que ya está listo) y muestra loading.js dentro del área de posts. Una vez que page.js termina de obtener los datos, el HTML del componente se envía y reemplaza el loading.

Internamente: Next.js envuelve la página en un <Suspense fallback={<Loading />}>. Por eso el streaming funciona incluso fuera de loading.js si usas Suspense manualmente.
Suspense manual para mayor granularidad

Puedes envolver partes específicas de una página en <Suspense> para controlar exactamente qué se streamea primero.
```jsx
// app/productos/page.js
import { Suspense } from 'react'
import ListaProductos from './ListaProductos' // Server Component pesado
import Filtros from './Filtros'               // Server Component ligero

export default function Page() {
  return (
    <div>
      <h1>Productos</h1>
      <Filtros />
      <Suspense fallback={<div>Cargando productos...</div>}>
        <ListaProductos />
      </Suspense>
    </div>
  )
}
```

En este caso, el servidor enviará el título y los filtros inmediatamente, y luego, cuando ListaProductos termine de cargar, enviará ese bloque. El HTML se construye de forma incremental.
Suspense y fetching paralelo

Si tienes múltiples componentes asíncronos, Next.js ejecuta los fetch en paralelo (si son independientes). Sin Suspense, esperaría a que todos terminen antes de enviar nada. Con Suspense, cada bloque se puede enviar apenas está listo.
Configuración del streaming

El streaming está habilitado por defecto en App Router. No necesitas ninguna configuración. En entornos que no soporten streaming (p. ej., algunos proxies), Next.js automáticamente espera la página completa (pero esto degrada el rendimiento).
Impacto en Edge Runtime

El streaming es especialmente efectivo en Edge, donde la latencia de red es baja pero la ejecución de código puede ser más limitada. Al enviar el HTML estático temprano, se solapa la descarga con la espera de datos dinámicos.
Diferencia con SSR tradicional

En SSR sin streaming, toda la página debe generarse antes de que el servidor envíe el primer byte. Con streaming, se envía inmediatamente el shell estático, mejorando la percepción de velocidad. También se aprovecha el soporte HTTP/1.1 chunked transfer y HTTP/2.
Errores durante streaming

Si un componente dentro de <Suspense> falla, el error se puede capturar con el error.js del segmento o con un Error Boundary dentro del mismo Suspense. El resto de la página sigue intacta.
Uso con Client Components

Los Client Components que se suspenden también participan del streaming si se envuelven en <Suspense>. Sin embargo, su JavaScript aún debe cargarse e hidratarse, pero la parte visual (HTML) puede mostrarse tan pronto llegue.
Desactivar streaming en un segmento

Si decides que no quieres streaming (por ejemplo, para depuración), puedes forzar el renderizado dinámico completo con export const dynamic = 'force-dynamic' y no usar <Suspense>. Next.js esperará a que todo el árbol se resuelva antes de responder.
Cuándo usar streaming

    Páginas con datos lentos (consultas a BD, APIs de terceros).

    Cualquier página donde quieras mejorar LCP mostrando la estructura antes.

    Dashboards con múltiples widgets independientes.

El streaming con Suspense transforma la experiencia del usuario al proporcionar retroalimentación visual casi inmediata mientras los contenidos se cargan por detrás. Es una de las características más potentes del App Router.

Con esto tienes los 12 archivos desarrollados a fondo. Si necesitas profundizar más en alguno o continuar con la siguiente tanda (optimización, middleware, i18n, etc.), no dudes en pedírmelo.
