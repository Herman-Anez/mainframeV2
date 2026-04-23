# Static Site Generation (SSG) en Next.js

La **generación de sitios estáticos (SSG)** implica pre-renderizar las páginas en tiempo de compilación (`next build`). El resultado son archivos HTML (y JSON para transiciones del lado del cliente) que pueden servirse directamente desde una **CDN**, garantizando un rendimiento excepcional.

## SSG en Pages Router

Se logra con la función `getStaticProps` (y `getStaticPaths` para rutas dinámicas). La página se construye una vez y se sirve estáticamente, lo que garantiza el mejor rendimiento posible y un SEO excelente.

```jsx
// pages/posts/[slug].js
export async function getStaticProps({ params }) {
  const post = await getPost(params.slug)
  return { 
    props: { post } 
  }
}

export async function getStaticPaths() {
  const posts = await getAllPosts()
  const paths = posts.map(p => ({ params: { slug: p.slug } }))
  return { 
    paths, 
    fallback: false 
  }
}

export default function Post({ post }) {
  return <article>{post.title}</article>
}
```

---

## SSG en App Router

En el **App Router**, los Server Components son **estáticos por defecto** cuando no utilizan fuentes de datos dinámicas (es decir, si no contienen `cookies()`, `headers()`, o `fetch` con `cache: 'no-store'`). Durante el build, Next.js renderiza esas rutas y las guarda como archivos estáticos.

No necesitas exportar funciones especiales; solo escribe un Server Component normal que obtenga datos sin forzar dinamismo:

```jsx
// app/about/page.js
export default function About() {
  return <h1>Acerca de Nosotros</h1>
}
```

### Contenido desde API externa

```jsx
export default async function Blog() {
  const posts = await fetch('https://api.example.com/posts') // usa force-cache por defecto
  const data = await posts.json()
  
  return (
    <>
      {data.map(post => (
        <div key={post.id}>{post.title}</div>
      ))}
    </>
  )
}
```

> [!TIP]
> Al no indicar `cache: 'no-store'`, `fetch` usa el comportamiento predeterminado de caché (`force-cache`). Next.js realizará la solicitud durante el build, cacheará el resultado (**Data Cache**) y generará HTML estático.

---

## Rutas dinámicas estáticas

En App Router, si necesitas pre-renderizar rutas dinámicas, debes generar los parámetros estáticos usando `generateStaticParams`.

```jsx
// app/blog/[slug]/page.js
export default function BlogPost({ params }) {
  const { slug } = params
  // ... lógica del post
}

export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts').then(res => res.json())
  return posts.map(post => ({ slug: post.slug }))
}
```

> [!NOTE]
> `generateStaticParams` reemplaza a `getStaticPaths`. Por defecto, `dynamicParams = true`, lo que significa que cualquier ruta no generada en build se renderizará bajo demanda (como SSR) y luego se cacheará.

---

## Ventajas y Desventajas del SSG

### Ventajas:
*   **Velocidad Extrema:** El HTML es servido desde una CDN (tiempo de respuesta casi instantáneo).
*   **Escalabilidad:** Sin carga en el servidor por petición, permitiendo manejar picos masivos de tráfico.
*   **SEO Óptimo:** Los motores de búsqueda reciben el contenido completo de inmediato.

### Desventajas:
*   **Tiempo de Build:** Puede ser largo para sitios con miles de páginas.
*   **Contenido Estático:** Los datos pueden quedar desactualizados si no se implementa una estrategia de revalidación.

---

## ¿Cuándo usar SSG?

*   **Blogs, portafolios y documentación.**
*   **Páginas de producto:** Donde la información no cambia con cada visita.
*   **Contenido independiente:** Cualquier página que no dependa de datos personalizados por solicitud.

> [!IMPORTANT]
> Si una parte de la página necesita interactividad o personalización, puedes implementarla con **Client Components** que obtengan datos adicionales en el cliente, mientras el esqueleto estático se entrega instantáneamente. Para mantener los datos frescos, combínalo con **ISR**.
