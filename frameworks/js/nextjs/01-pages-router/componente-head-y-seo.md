## 📘 01-pages-router/componente-head-y-seo.md

### `<Head>` y SEO en Pages Router

En el Pages Router, el componente `<Head>` de `next/head` te permite modificar el `<head>` del documento HTML.

#### Uso básico

```jsx
import Head from 'next/head'

export default function Home() {
  return (
    <>
      <Head>
        <title>Mi Sitio - Inicio</title>
        <meta name="description" content="Descripción de la página de inicio" />
        <meta property="og:title" content="Mi Sitio" />
      </Head>
      <main>Contenido...</main>
    </>
  )
}
```

#### Anidamiento y fusión

Si tienes un `<Head>` en `_app.js` y otro en una página, Next.js fusiona ambos, pero los duplicados se sobrescriben en favor del último definido.
i tienes un <Head> en _app.js y otro en una página, Next.js fusiona ambos, pero los duplicados se sobrescriben en favor del último definido. Ejemplo típico:

En _app.js:
jsx

<Head>
  <title>Sitio por defecto</title>
  <meta name="description" content="Descripción global" />
</Head>

En la página about.js:
jsx

<Head>
  <title>Acerca de nosotros</title>
  {/* la descripción se mantiene de _app si no se redefine */}
</Head>

Así, cada página puede definir su propio título sin perder las metaetiquetas comunes.
Metaetiquetas importantes para SEO

    title: Clave para los resultados de búsqueda.

    description: Debe ser única y atractiva.

    canonical: Evita contenido duplicado.

    robots: Controla indexación.

    og:title, og:description, og:image: Open Graph (Facebook, WhatsApp).

    twitter:card, twitter:title, etc.: Twitter Cards.

jsx

<Head>
  <link rel="canonical" href="https://misitio.com/pagina" />
  <meta name="robots" content="index, follow" />
</Head>
Contenido dinámico en el head

Si obtienes datos con getServerSideProps o getStaticProps, puedes pasar valores al componente y usarlos en Head:
jsx

export default function Post({ post }) {
  return (
    <>
      <Head>
        <title>{post.title} - Mi Blog</title>
        <meta name="description" content={post.excerpt} />
      </Head>
      <article>...</article>
    </>
  )
}

#### Scripts externos con `next/script`

```jsx
import Script from 'next/script'

<Script src="https://analytics.example.com/script.js" strategy="lazyOnload" />
```

#### Limitaciones de `<Head>`

- Solo afecta el `<head>` de la página actual.
- Si tienes que modificar `html` o `body`, debes usar `_document.js`.

---

📘 01-pages-router/diferencias-con-app-router.md
Diferencias entre Pages Router y App Router

Next.js 13 introdujo el App Router, un nuevo paradigma construido sobre React Server Components, streaming y layouts anidados. Convive con el Pages Router, pero entender sus diferencias es vital para migrar o decidir cuál usar.

1. Directorio y convención
Pages Router App Router
Carpeta pages/. Cada archivo es una ruta. Carpeta app/. Las carpetas definen rutas y deben contener page.js (o page.tsx) para ser accesibles.
Archivos especiales: _app.js,_document.js. Archivos especiales: layout.js, loading.js, error.js, template.js, not-found.js.
2. Componentes por defecto: Servidor vs Cliente

    Pages Router: Los componentes son de cliente por defecto (usan hooks, interactividad). No hay React Server Components. El JavaScript de la página se envía al navegador.

    App Router: Todos los componentes son React Server Components por defecto (se renderizan en el servidor). Esto reduce el JS en el cliente, pero no pueden usar estado ni efectos. Para añadir interactividad, se marca 'use client' al inicio del archivo, convirtiéndolo en un Client Component.

3. Layouts y persistencia

    Pages Router: No tiene concepto nativo de layouts que persistan entre navegaciones. Cada página se monta y desmonta completamente. Los layouts se implementan manualmente con componentes envolventes en _app.js o por página.

    App Router: Los layouts (layout.js) se anidan y persisten al navegar entre páginas que los comparten. Solo se recarga la parte de page.js. Esto permite mantener estado (ej. reproductor de música, barra lateral abierta) sin perderlo.

4. Obtención de datos

    Pages Router: Funciones exportadas (getServerSideProps, getStaticProps, getStaticPaths). Se ejecutan en el servidor y proporcionan props al componente.

    App Router: Los Server Components obtienen datos directamente en el cuerpo del componente, usando fetch con extensiones de caché. No se necesitan funciones especiales separadas. Ejemplo:
    jsx

    async function Page() {
      const res = await fetch('...', { next: { revalidate: 60 } })
      const data = await res.json()
      return <div>{data}</div>
    }

5. Manejo de errores y carga

    Pages Router: Necesitas implementar estados de carga y errores manualmente dentro de cada página (con router.isFallback para SSG, o estados locales para SSR).

    App Router: Archivos loading.js muestran una UI de carga automática gracias a React Suspense. error.js aísla errores en partes de la UI sin romper toda la página. También hay not-found.js para páginas 404.

6. Enrutamiento

    Pages Router: Rutas dinámicas con [id].js. Rutas opcionales con [[...slug]].js. Sin rutas paralelas ni interceptación de rutas.

    App Router: Soporta rutas dinámicas, catch-all y opcionales igual, pero además:

        Rutas paralelas: con slots (@analytics, @team) que pueden mostrarse en el mismo layout.

        Rutas interceptadas: muestran una versión diferente de la página según el contexto (útil para modales, feeds).

7. Medio de ejecución

    Pages Router: SSR se ejecuta únicamente en Node.js (serverless/Node). No hay soporte nativo para Edge Runtime en páginas (solo en API Routes si se configura explícitamente).

    App Router: Puedes elegir el runtime por segmento (Node.js o Edge Runtime) exportando runtime = 'edge'. Esto permite ejecutar partes de la aplicación en el borde, más cerca del usuario.

8. Metadata y SEO

    Pages Router: Se usa <Head> para metaetiquetas, por lo que es un componente de cliente (necesita hidratarse).

    App Router: API de Metadata estática o dinámica exportando metadata o generateMetadata desde layouts/pages. También hay soporte nativo para sitemap.ts, robots.ts, opengraph-image.tsx.

9. Server Actions

    Pages Router: No existen. Las mutaciones se manejan mediante API Routes.

    App Router: Las Server Actions permiten ejecutar funciones del servidor directamente desde formularios o manejadores de eventos en el cliente, sin crear endpoints manualmente.

10. Migración y convivencia

Puedes tener ambos routers en el mismo proyecto (carpeta pages/ y app/). Sin embargo, Next.js recomienda adoptar gradualmente el App Router para nuevos proyectos, ya que aprovecha las últimas innovaciones de React.
¿Cuándo seguir con Pages Router?

    Proyectos grandes y estables donde una migración completa no es prioritaria.

    Equipos acostumbrados al modelo clásico y que no necesitan Server Components.

    Ciertas librerías del ecosistema React aún podrían no ser totalmente compatibles con RSC.
 