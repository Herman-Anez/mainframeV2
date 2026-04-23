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

Si alguna parte de la página necesita interactividad o personalización, se puede implementar con Client Components que obtengan datos adicionales en el cliente, mientras el esqueleto estático se entrega casi instantáneamente
