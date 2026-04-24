## 📘 00-introduccion/que-es-nextjs.md
¿Qué es Next.js?

Next.js es un framework de React creado por Vercel que permite construir aplicaciones web modernas aprovechando renderizado híbrido (estático y servidor), enrutamiento basado en el sistema de archivos, optimizaciones automáticas y una excelente experiencia de desarrollo. Es la capa sobre React que resuelve problemas comunes como el renderizado del lado del servidor (SSR), la generación de sitios estáticos (SSG), la división de código y la configuración de herramientas complejas.
Características principales

    Renderizado flexible: Puedes elegir por página si usar SSR, SSG, ISR (Incremental Static Regeneration) o incluso renderizado del lado del cliente.

    Enrutamiento basado en archivos: Sin necesidad de react-router, la estructura de carpetas define las rutas.

    Optimizaciones automáticas: Imágenes, fuentes, scripts y bundles se optimizan de forma nativa.

    Soporte TypeScript total: Tipos incluidos y configuración automática.

    API Routes: Permite construir endpoints de backend dentro del mismo proyecto.

    Internacionalización: Sistema de rutas con prefijo de idioma, detección automática.

    Ecosistema: Amplia comunidad y despliegue instantáneo en Vercel.

### Historia breve

Lanzado en 2016, revolucionó la forma de hacer sitios web con React al ofrecer SSR y SSG sencillos. Con la versión 13, introdujo el App Router, basado en React Server Components, marcando un nuevo paradigma. Actualmente, conviven el Pages Router (estable) y el App Router (recomendado para nuevos proyectos).
¿Por qué usar Next.js en lugar de React solo?

Un proyecto con React puro necesita configurar manualmente:

    Webpack o Vite para bundling.

    React Router para navegación.

    Herramientas para SSR (como Express con renderToString).

    Soluciones de SEO personalizadas.

    Caché y optimización de imágenes.

Next.js proporciona todo esto de serie, con convenciones claras y decisiones técnicas probadas.
📘 00-introduccion/comparacion-con-react.md
Next.js vs React (con Vite / CRA)

Aunque Next.js está construido con React, las diferencias van mucho más allá de ser un simple “React con esteroides”. Aquí tienes una comparación detallada.
1. Renderizado
Característica	React (SPA tradicional)	Next.js
Renderizado inicial	Cliente: El HTML está casi vacío, el JS monta toda la app.	Servidor/Estático: El HTML llega completamente renderizado, mejor LCP.
SEO	Depende de soluciones externas (react-helmet, prerender.io).	Nativo, con metadatos por página y renderizado del lado del servidor.
Carga en redes lentas	Puede ser lenta, pues el bundle JS debe descargarse y ejecutarse.	Más rápido porque el HTML ya contiene el contenido.
Opciones de renderizado	Solo cliente (SPA).	Por página: SSG, SSR, ISR, CSR.
2. Enrutamiento
React	Next.js
Requiere librerías (react-router-dom). Configuración manual de rutas.	Enrutamiento basado en archivos: una carpeta = una ruta. Soporte automático para layouts, rutas dinámicas, anidadas, paralelas.
Las rutas protegidas dependen de lógica en componentes.	Middleware nativo para interceptar peticiones basadas en cookies, headers, etc.
3. Obtención de datos
React	Next.js
useEffect + fetch, SWR, React Query. Los datos se cargan después del montaje (a menos que se use un SSR casero).	Funciones dedicadas como getServerSideProps, getStaticProps, fetch nativo extendido en servidor, React Server Components. Los datos pueden cargarse antes de que el HTML llegue al cliente.
4. Rendimiento

    División de código: En React hay que configurarla con React.lazy. Next.js la hace automática por ruta.

    Imágenes: Next.js tiene next/image con lazy loading, formatos modernos y redimensionamiento automático. En React necesitas librerías externas.

    Fuentes: next/font elimina peticiones a Google Fonts y optimiza la carga.

### 5. Configuración y tooling

    React: Necesitas crear un proyecto con Vite o CRA. Configurar ESLint, Prettier manualmente. El soporte SSR requiere Node.js y código extra.

    Next.js: create-next-app da un proyecto listo para producción. Configuración de TypeScript, ESLint y Tailwind incluida opcionalmente. Compilación y empaquetado con Turbopack (rápido en desarrollo).

### 6. Despliegue

    React: Se genera una carpeta dist con archivos estáticos. Para SSR necesitas un servidor Node.js.

    Next.js: Puede exportarse como sitio estático (output: 'export'), ejecutarse como servidor Node.js, o desplegar en Vercel, Netlify, etc., aprovechando Edge Functions e ISR.

Conclusión: Next.js es la opción recomendada por la documentación oficial de React para iniciar un proyecto, porque proporciona una solución completa con convenciones bien pensadas.
📘 00-introduccion/instalacion-y-setup.md
Instalación y configuración inicial
Requisitos previos

    Node.js 18.17 o superior (recomendado).

    Gestor de paquetes: npm, yarn, pnpm o bun.

### Crear un proyecto nuevo
```bash
npx create-next-app@latest mi-proyecto
```

El instalador interactivo te preguntará:

    TypeScript: Recomendado (Sí).

    ESLint: Recomendado (Sí).

    Tailwind CSS: Opcional, pero útil.

    Directorio src/: Si prefieres tener las carpetas app/ y pages/ dentro de src/.

    App Router: ¿Usar el nuevo App Router? (Sí/No). Puedes elegir Pages Router para seguir esta sección.

    Alias de importación: Por defecto @/*.

### Estructura básica (Pages Router)
```text
mi-proyecto/
├── pages/
│   ├── api/
│   │   └── hello.js       // API route
│   ├── _app.js             // Componente global (layouts, estados)
│   ├── _document.js        // Estructura HTML personalizada
│   └── index.js            // Página principal "/"
├── public/                 // Archivos estáticos
├── styles/                 // CSS global o módulos
├── next.config.js          // Configuración de Next.js
├── package.json
└── ...
```

### Ejecutar el proyecto
```bash
npm run dev        # Inicia servidor de desarrollo en http://localhost:3000
npm run build      # Crea la versión de producción
npm start          # Inicia el servidor en modo producción
```

### Personalizar el puerto
```bash
npm run dev -- -p 4000
```

### Tu primera página

Crea pages/index.js:
```jsx
export default function Home() {
  return <h1>¡Hola Next.js con Pages Router!</h1>;
}
```

Visita http://localhost:3000 y verás el resultado.
Instalación manual en un proyecto existente

Si ya tienes un proyecto, instala:
```bash
npm install next react react-dom
```

Luego configura los scripts en package.json:
```json
"scripts": {
  "dev": "next dev",
  "build": "next build",
  "start": "next start"
}
```

Crea la carpeta pages/ con un archivo index.js. Ya puedes empezar.
📘 01-pages-router/fundamentos-pages-router.md
Fundamentos del Pages Router

El Pages Router fue el sistema de enrutamiento original de Next.js. Se basa en la carpeta pages/: cada archivo .js, .jsx, .ts o .tsx dentro de ella se convierte automáticamente en una ruta accesible.
Rutas basadas en archivos
Estructura de archivo	Ruta resultante
pages/index.js	/ (raíz)
pages/about.js	/about
pages/blog/index.js	/blog
pages/blog/first.js	/blog/first

Los archivos deben exportar por defecto un componente React. Next.js se encarga de envolverlo con el renderizado adecuado y el encabezado HTML base.
Componente _app.js

Permite personalizar la inicialización de las páginas. Es el componente que envuelve a todas las páginas. Se usa para:

    Mantener estados globales (contextos, providers).

    Agregar layouts comunes.

    Inyectar estilos globales.

Ejemplo básico:
```jsx
import '../styles/globals.css'

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}
```

### Componente _document.js

Sirve para modificar la estructura del documento HTML (<html>, <body>). Solo se renderiza en el servidor. Útil para añadir fuentes, atributos lang, etc. No debe contener lógica de aplicación.
```jsx
import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="es">
      <Head />
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
```

### Páginas de error personalizadas

    pages/404.js: Se muestra automáticamente para rutas no encontradas.

    pages/_error.js: Error genérico (500, etc.). Puede recibir statusCode.

### Enlaces y navegación

Usa el componente Link de next/link para navegación entre páginas sin recargar completamente el navegador (cliente side routing). Se precargan automáticamente cuando el enlace entra al viewport.
```jsx
import Link from 'next/link'

export default function Nav() {
  return (
    <nav>
      <Link href="/">Inicio</Link>
      <Link href="/about">Acerca de</Link>
    </nav>
  )
}
```

Para redirecciones programáticas o acceso al objeto router:
```jsx
import { useRouter } from 'next/router'

export default function Component() {
  const router = useRouter()
  const handleClick = () => router.push('/about')
  // ...
}
```

### Estilos

Next.js soporta:

    CSS Modules: Archivos [nombre].module.css importables en componentes.

    SASS (instalando sass).

    CSS-in-JS (styled-components, emotion) con configuración extra.

    Tailwind CSS (recomendado en instalación).

Con el Pages Router tienes una base sólida para cualquier aplicación tradicional de React con renderizado híbrido. En los siguientes capítulos veremos rutas dinámicas, obtención de datos y más.
📘 01-pages-router/rutas-estaticas-y-dinamicas.md
Rutas estáticas y dinámicas en Pages Router

El sistema de archivos de pages/ soporta dos tipos de rutas: estáticas (archivos con nombre fijo) y dinámicas (archivos con corchetes).
Rutas estáticas

Cualquier archivo que no use corchetes se convierte en una ruta fija.

### pages/contacto.js → /contacto

### pages/productos/categoria.js → /productos/categoria

### Rutas dinámicas básicas

Las rutas dinámicas permiten capturar segmentos variables de la URL. Se definen encerrando el nombre del parámetro entre corchetes.

    pages/posts/[id].js → /posts/1, /posts/abc, etc.

Dentro del componente de página, se accede al parámetro mediante useRouter:
```jsx
import { useRouter } from 'next/router'

export default function Post() {
  const router = useRouter()
  const { id } = router.query

  return <h1>Artículo: {id}</h1>
}
```

router.query es un objeto que contiene los parámetros de la URL. En el primer renderizado puede estar vacío (pre-renderizado estático o en cliente), por eso debes manejar el estado de carga.
Rutas dinámicas anidadas

### pages/posts/[id]/comments.js → /posts/1/comments

El hook useRouter devolverá { id: '1' } en query.
Rutas catch-all (captura todas)

Permiten capturar múltiples segmentos de la ruta. Se utiliza [...nombre].

    pages/docs/[...slug].js → /docs, /docs/intro, /docs/guia/instalacion, etc.

El valor de slug será un array de strings.
```jsx
import { useRouter } from 'next/router'

export default function Docs() {
  const router = useRouter()
  const { slug = [] } = router.query // ¡siempre array!

  return <h1>Ruta completa: {slug.join('/')}</h1>
}
```

### Rutas catch-all opcionales

Para que la ruta también coincida sin el parámetro (es decir, la ruta base), se usa doble corchete: [[...slug]].

### pages/productos/[[...filtros]].js

        /productos → filtros será undefined o [].

        /productos/electronica/2024 → filtros = ['electronica', '2024'].

Permite tener una misma página que maneje tanto la lista general como los fitros.
Enlaces y prefetching

El componente Link funciona perfectamente con rutas dinámicas:
```jsx
<Link href={`/posts/${post.id}`}>{post.title}</Link>
```

Para prefetching automático, Next.js solo precarga la página si el enlace es visible (predeterminado) o si se usa prefetch={true}. Puedes deshabilitarlo con prefetch={false}.
Navegación superficial (Shallow Routing)

Permite cambiar la URL sin ejecutar métodos de obtención de datos (getServerSideProps, etc.). Útil para filtros que solo afectan el lado del cliente.
```jsx
router.push('/productos?color=rojo', undefined, { shallow: true })
```

Así puedes actualizar router.query y reaccionar a él sin recargar la página.
Consideraciones

    Siempre valida el tipo de query.params porque inicialmente pueden estar vacíos.

    Evita usar router.query directamente en el renderizado si tu página depende del dato; mejor usa un estado o maneja isReady.

```jsx
const router = useRouter()
if (!router.isReady) return <div>Cargando...</div>
```

Con estas herramientas, el Pages Router ofrece un control completo sobre el mapeo de URLs.
📘 01-pages-router/getServerSideProps.md
getServerSideProps: Renderizado en cada solicitud

getServerSideProps (SSR) es una función que se ejecuta en el servidor en cada petición. Permite generar la página con datos frescos antes de enviarla al cliente. Se define dentro del archivo de la página y debe ser exportada.
Sintaxis básica
```jsx
export async function getServerSideProps(context) {
  return {
    props: {
      // datos que recibirá el componente
    },
  }
}

export default function Page({ data }) {
  return <div>{data}</div>
}
```

### El objeto context

Contiene información sobre la solicitud actual:

    params: Parámetros de ruta dinámica (ej. { id: '5' }).

    req: El objeto http.IncomingMessage (solo en servidor).

    res: El objeto http.ServerResponse.

    query: El query string de la URL.

    resolvedUrl: La URL completa resuelta.

Ejemplo usando params:
```jsx
// pages/posts/[pid].js
export async function getServerSideProps({ params }) {
  const res = await fetch(`https://.../posts/${params.pid}`)
  const post = await res.json()

  return { props: { post } }
}
```

### Cuándo usar getServerSideProps

    Datos que cambian a menudo (precios de acciones, noticias en tiempo real).

    Contenido personalizado según el usuario (sesiones, cookies).

    Páginas que necesitan leer req (cabeceras de autenticación, geolocalización).

### Rendimiento

Como se ejecuta en cada solicitud, puede aumentar el tiempo de respuesta y la carga del servidor. Para reducir el trabajo, puedes agregar un encabezado de cache con res.setHeader('Cache-Control', ...).
```jsx
export async function getServerSideProps({ res }) {
  res.setHeader('Cache-Control', 'public, s-maxage=10, stale-while-revalidate=59')
  // ...
}
```

### Redirecciones y notFound

Puedes retornar un objeto para redirigir o retornar un 404.
```jsx
export async function getServerSideProps(context) {
  const data = await fetchData()

  if (!data) {
    return {
      notFound: true, // muestra la página 404
    }
  }

  if (shouldRedirect) {
    return {
      redirect: {
        destination: '/nueva-ruta',
        permanent: false, // 307 (temporal), o true para 308
      },
    }
  }

  return { props: { data } }
}
```

### Con TypeScript

Next.js proporciona el tipo GetServerSideProps:
```tsx
import type { GetServerSideProps } from 'next'

type Post = { id: number; title: string }

export const getServerSideProps: GetServerSideProps<{ post: Post }> = async (ctx) => {
  // ...
  return { props: { post } }
}
```

### Acceso a cookies

Para leer cookies, usa el objeto req de Node (o librerías como cookie o next-cookies).
```jsx
export async function getServerSideProps({ req }) {
  const token = req.cookies.token
  // validar...
}
```

### Consideraciones importantes

    Esta función solo se ejecuta en el servidor, nunca en el cliente. Puedes usar módulos de Node (fs, path, variables de entorno sin NEXT_PUBLIC_).

    No se puede usar dentro de componentes, solo en páginas.

    El código no se incluye en el bundle del cliente.

getServerSideProps te da el máximo dinamismo, pero a costa de rendimiento. En la práctica, combina SSG con ISR para la mayoría de las páginas y reserva SSR para las que realmente lo necesitan.
📘 01-pages-router/getStaticProps-y-getStaticPaths.md
getStaticProps y getStaticPaths: Generación de sitios estáticos (SSG)

Next.js permite generar páginas estáticas en tiempo de compilación. Para rutas dinámicas, necesitas también getStaticPaths.
getStaticProps

Se ejecuta durante la compilación (build) y genera HTML estático. Los datos se obtienen una vez y se reutilizan.
```jsx
export async function getStaticProps(context) {
  const res = await fetch('https://.../posts')
  const posts = await res.json()

  return {
    props: { posts },
    revalidate: 10, // ISR: regenera cada 10 segundos (opcional)
  }
}

export default function Blog({ posts }) {
  // ...
}
```

Ventajas:

    Máximo rendimiento (servido desde CDN, sin cálculos por petición).

    SEO perfecto.

context incluye:

    params (si es ruta dinámica y se combina con getStaticPaths).

    preview: booleano para modo preview.

    locale, locales, defaultLocale para i18n.

### getStaticPaths

Define qué rutas dinámicas deben pre-renderizarse de forma estática. Se usa solo en páginas con rutas dinámicas ([id].js).
```jsx
export async function getStaticPaths() {
  const res = await fetch('https://.../posts')
  const posts = await res.json()

  const paths = posts.map((post) => ({
    params: { id: post.id.toString() },
  }))

  return {
    paths,
    fallback: false, // o true / 'blocking'
  }
}

    paths: Array de objetos con params. También puede contener locale si usas i18n.

    fallback: Controla el comportamiento para rutas no generadas en el build.
```

### Opciones de fallback
Valor	Comportamiento
false	Cualquier ruta no pre-renderizada retorna 404.
true	La página se genera en el servidor en la primera solicitud. Mientras, muestra un estado de carga (el componente debe manejar router.isFallback).
'blocking'	Similar a true, pero sin estado de carga: la respuesta espera a que la página se genere (SSR temporal).

Ejemplo con fallback: true:
```jsx
import { useRouter } from 'next/router'

export default function Post({ post }) {
  const router = useRouter()

  if (router.isFallback) {
    return <div>Cargando...</div>
  }

  return <div>{post.title}</div>
}

export async function getStaticProps({ params }) {
  const post = await fetchPost(params.id)
  return { props: { post }, revalidate: 60 }
}

export async function getStaticPaths() {
  const posts = await fetchPosts()
  const paths = posts.map(p => ({ params: { id: p.id } }))
  return { paths, fallback: true }
}
```

### Generación incremental (ISR)

Al añadir revalidate en getStaticProps, permites que Next.js actualice la página estática en segundo plano sin rebuild completo. La primera solicitud después de expirar revalidate hace que se regenere la página; el usuario ve la versión anterior mientras se construye la nueva.
```jsx
return {
  props: { data },
  revalidate: 60, // segundos
}
```

Para invalidar manualmente, puedes usar res.revalidate() dentro de un API Route o el sistema de revalidación bajo demanda (revalidateTag, revalidatePath en App Router).
Consideraciones

    getStaticProps y getStaticPaths se ejecutan en tiempo de build (Node.js). Puedes acceder a bases de datos, sistema de archivos, etc.

    Si tienes demasiadas páginas (cientos de miles), generar todas en build puede ser lento. Usa fallback: 'blocking' o ISR para mejorar el tiempo de build.

    Las rutas estáticas sin getStaticPaths también pueden usar getStaticProps para datos en build.

Esta combinación es el pilar de sitios de contenido (blogs, documentación) y puede escalar a millones de páginas con la regeneración incremental.
📘 01-pages-router/api-routes-pages.md
API Routes en Pages Router

Las API Routes permiten construir tu backend dentro del mismo proyecto Next.js, bajo la carpeta pages/api/. Cualquier archivo dentro de esa carpeta se convierte en un endpoint.
Creando un endpoint básico

pages/api/hola.js:
```jsx
export default function handler(req, res) {
  res.status(200).json({ mensaje: 'Hola mundo' })
}
```

Accesible en /api/hola.
El objeto req (Request)

Es una instancia de http.IncomingMessage, extendida con helpers de Next.js:

    req.query: query string parseado como objeto.

    req.body: cuerpo parseado (si el método es POST y el Content-Type adecuado). Requiere export const config = { api: { bodyParser: true } } (por defecto true).

    req.cookies: objeto con cookies.

    req.method: método HTTP (GET, POST, etc.).

### El objeto res (Response)

Es http.ServerResponse con métodos helper:

    res.status(code) para establecer código HTTP.

    res.json(data) envía respuesta JSON.

    res.send(data) envía datos en bruto.

    res.redirect(url) redirige.

    res.setHeader(name, value).

### Manejo de diferentes métodos HTTP

Estructura recomendada usando switch:
```jsx
export default async function handler(req, res) {
  if (req.method === 'GET') {
    // obtener datos
    res.status(200).json({ data })
  } else if (req.method === 'POST') {
    // crear recurso
    const body = req.body
    res.status(201).json({ result })
  } else {
    res.setHeader('Allow', ['GET', 'POST'])
    res.status(405).end(`Método ${req.method} no permitido`)
  }
}
```

### Conectando a una base de datos
```jsx
import clientPromise from '../../lib/mongodb'

export default async function handler(req, res) {
  const client = await clientPromise
  const db = client.db('mi_db')
  const collection = db.collection('posts')

  if (req.method === 'GET') {
    const posts = await collection.find({}).toArray()
    res.json(posts)
  } else if (req.method === 'POST') {
    const result = await collection.insertOne(req.body)
    res.json(result)
  }
}
```

### Middleware personalizado

Puedes envolver handlers con funciones middleware:
```jsx
function withAuth(handler) {
  return async (req, res) => {
    const token = req.cookies.token
    if (!token) return res.status(401).json({ error: 'No autorizado' })
    // validar token...
    return handler(req, res)
  }
}

async function handler(req, res) { /* ... */ }

export default withAuth(handler)
```

### Variables de entorno

Accede a secretos con process.env.SECRET. Estas variables no se exponen al cliente si no llevan el prefijo NEXT_PUBLIC_.
Limitaciones

    Las API Routes se ejecutan como funciones serverless en Vercel (o en Node si despliegas en servidor propio). No mantienen estado entre peticiones (websockets no funcionan bien en serverless).

    Para archivos grandes, el bodyParser por defecto tiene límite de 1MB. Puedes desactivarlo export const config = { api: { bodyParser: false } } y usar streaming.

    Para lógica de borde, se recomienda usar Edge API Routes (App Router), pero en Pages Router tienes un modelo probado.

### Ejemplo completo: endpoint POST con validación
```jsx
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Método no permitido' })
  }

  const { email, password } = req.body
  if (!email || !password) {
    return res.status(400).json({ error: 'Faltan datos' })
  }

  // Lógica de registro...
  res.status(200).json({ ok: true })
}
```

Las API Routes son ideales para formularios, webhooks, proxy de servicios externos o prototipos rápidos.
📘 01-pages-router/componente-head-y-seo.md
<Head> y SEO en Pages Router

En el Pages Router, el componente <Head> de next/head te permite modificar el <head> del documento HTML. Es esencial para SEO, metaetiquetas sociales y scripts externos.
Uso básico

Importa Head y agrégalo dentro de tu componente de página:
```jsx
import Head from 'next/head'

export default function Home() {
  return (
    <>
      <Head>
        <title>Mi Sitio - Inicio</title>
        <meta name="description" content="Descripción de la página de inicio" />
        <meta property="og:title" content="Mi Sitio" />
        <meta property="og:description" content="Comparte esta página" />
      </Head>
      <main>Contenido...</main>
    </>
  )
}
```

### Anidamiento y fusión

Si tienes un <Head> en _app.js y otro en una página, Next.js fusiona ambos, pero los duplicados se sobrescriben en favor del último definido. Ejemplo típico:

En _app.js:
```jsx
<Head>
  <title>Sitio por defecto</title>
  <meta name="description" content="Descripción global" />
</Head>
```

En la página about.js:
```jsx
<Head>
  <title>Acerca de nosotros</title>
  {/* la descripción se mantiene de _app si no se redefine */}
</Head>
```

Así, cada página puede definir su propio título sin perder las metaetiquetas comunes.
Metaetiquetas importantes para SEO

    title: Clave para los resultados de búsqueda.

    description: Debe ser única y atractiva.

    canonical: Evita contenido duplicado.

    robots: Controla indexación.

    og:title, og:description, og:image: Open Graph (Facebook, WhatsApp).

    twitter:card, twitter:title, etc.: Twitter Cards.

```jsx
<Head>
  <link rel="canonical" href="https://misitio.com/pagina" />
  <meta name="robots" content="index, follow" />
</Head>
```

### Contenido dinámico en el head

Si obtienes datos con getServerSideProps o getStaticProps, puedes pasar valores al componente y usarlos en Head:
```jsx
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
```

### Scripts externos con next/script

Aunque no es Head, es relevante. Para cargar scripts externos de forma óptima, usa next/script:
```jsx
import Script from 'next/script'
```

### <Script src="https://analytics.example.com/script.js" strategy="lazyOnload" />

Esto permite cargar scripts sin bloquear la renderización.
Limitaciones de <Head>

    Solo afecta el <head> de la página actual (no funciona para layouts persistentes como en App Router).

    Si tienes que modificar html o body, debes usar _document.js.

    Para SEO avanzado, considera generar dinámicamente sitemap.xml y robots.txt en la carpeta public/ o mediante API Routes.

### Buenas prácticas

    Define una plantilla base en _app.js y sobreescribe el título en cada página.

    Siempre incluye al menos title y description.

    Verifica con herramientas como Lighthouse o la extensión de SEO.

Con <Head> puedes controlar por completo la información que los motores de búsqueda indexan de tu aplicación.
📘 01-pages-router/diferencias-con-app-router.md
Diferencias entre Pages Router y App Router

Next.js 13 introdujo el App Router, un nuevo paradigma construido sobre React Server Components, streaming y layouts anidados. Convive con el Pages Router, pero entender sus diferencias es vital para migrar o decidir cuál usar.
1. Directorio y convención
Pages Router	App Router
Carpeta pages/. Cada archivo es una ruta.	Carpeta app/. Las carpetas definen rutas y deben contener page.js (o page.tsx) para ser accesibles.
Archivos especiales: _app.js, _document.js.	Archivos especiales: layout.js, loading.js, error.js, template.js, not-found.js.
2. Componentes por defecto: Servidor vs Cliente

    Pages Router: Los componentes son de cliente por defecto (usan hooks, interactividad). No hay React Server Components. El JavaScript de la página se envía al navegador.

    App Router: Todos los componentes son React Server Components por defecto (se renderizan en el servidor). Esto reduce el JS en el cliente, pero no pueden usar estado ni efectos. Para añadir interactividad, se marca 'use client' al inicio del archivo, convirtiéndolo en un Client Component.

3. Layouts y persistencia

    Pages Router: No tiene concepto nativo de layouts que persistan entre navegaciones. Cada página se monta y desmonta completamente. Los layouts se implementan manualmente con componentes envolventes en _app.js o por página.

    App Router: Los layouts (layout.js) se anidan y persisten al navegar entre páginas que los comparten. Solo se recarga la parte de page.js. Esto permite mantener estado (ej. reproductor de música, barra lateral abierta) sin perderlo.

### 4. Obtención de datos

    Pages Router: Funciones exportadas (getServerSideProps, getStaticProps, getStaticPaths). Se ejecutan en el servidor y proporcionan props al componente.

    App Router: Los Server Components obtienen datos directamente en el cuerpo del componente, usando fetch con extensiones de caché. No se necesitan funciones especiales separadas. Ejemplo:
```jsx
    async function Page() {
      const res = await fetch('...', { next: { revalidate: 60 } })
      const data = await res.json()
      return <div>{data}</div>
    }
```

### 5. Manejo de errores y carga

    Pages Router: Necesitas implementar estados de carga y errores manualmente dentro de cada página (con router.isFallback para SSG, o estados locales para SSR).

    App Router: Archivos loading.js muestran una UI de carga automática gracias a React Suspense. error.js aísla errores en partes de la UI sin romper toda la página. También hay not-found.js para páginas 404.

### 6. Enrutamiento

    Pages Router: Rutas dinámicas con [id].js. Rutas opcionales con [[...slug]].js. Sin rutas paralelas ni interceptación de rutas.

    App Router: Soporta rutas dinámicas, catch-all y opcionales igual, pero además:

        Rutas paralelas: con slots (@analytics, @team) que pueden mostrarse en el mismo layout.

        Rutas interceptadas: muestran una versión diferente de la página según el contexto (útil para modales, feeds).

### 7. Medio de ejecución

    Pages Router: SSR se ejecuta únicamente en Node.js (serverless/Node). No hay soporte nativo para Edge Runtime en páginas (solo en API Routes si se configura explícitamente).

    App Router: Puedes elegir el runtime por segmento (Node.js o Edge Runtime) exportando runtime = 'edge'. Esto permite ejecutar partes de la aplicación en el borde, más cerca del usuario.

### 8. Metadata y SEO

    Pages Router: Se usa <Head> para metaetiquetas, por lo que es un componente de cliente (necesita hidratarse).

    App Router: API de Metadata estática o dinámica exportando metadata o generateMetadata desde layouts/pages. También hay soporte nativo para sitemap.ts, robots.ts, opengraph-image.tsx.

### 9. Server Actions

    Pages Router: No existen. Las mutaciones se manejan mediante API Routes.

    App Router: Las Server Actions permiten ejecutar funciones del servidor directamente desde formularios o manejadores de eventos en el cliente, sin crear endpoints manualmente.

### 10. Migración y convivencia

Puedes tener ambos routers en el mismo proyecto (carpeta pages/ y app/). Sin embargo, Next.js recomienda adoptar gradualmente el App Router para nuevos proyectos, ya que aprovecha las últimas innovaciones de React.
¿Cuándo seguir con Pages Router?

    Proyectos grandes y estables donde una migración completa no es prioritaria.

    Equipos acostumbrados al modelo clásico y que no necesitan Server Components.

    Ciertas librerías del ecosistema React aún podrían no ser totalmente compatibles con RSC.

El App Router es el futuro, pero el Pages Router seguirá siendo mantenido y es perfectamente válido para producción.

---

## Archivo: `02-app-router/fundamentos-app-router.md`

Fundamentos del App Router

El App Router es el sistema de enrutamiento introducido en Next.js 13 (estable desde 13.4) que reemplaza progresivamente al Pages Router. Está construido sobre React Server Components, Streaming y Suspense, y utiliza la carpeta app/ en lugar de pages/.
Convenciones del directorio app/

A diferencia del Pages Router, donde cada archivo dentro de pages/ se convierte automáticamente en una ruta, en el App Router necesitas carpetas que contengan archivos especiales con nombres reservados:
Archivo especial	Propósito
page.js / page.tsx	Define la interfaz de usuario única de una ruta.
layout.js	Envuelve a las páginas y persiste entre navegaciones dentro de la misma jerarquía.
loading.js	UI de carga que se muestra mientras la página o segmento espera datos (Suspense).
error.js	Aísla errores en una parte de la ruta sin colapsar la aplicación completa.
template.js	Similar a layout pero se vuelve a montar en cada navegación.
not-found.js	Se muestra cuando una ruta no existe. Reemplaza al 404.js del Pages Router.
route.js / route.ts	Define controladores HTTP (API endpoints) sin componente visual.
head.js (obsoleto)	Reemplazado por la API de Metadata exportando metadata o generateMetadata.
Rutas básicas

Una ruta se define por una carpeta dentro de app/ que contenga un archivo page.js.
Ejemplo: app/about/page.js → /about
app/blog/page.js → /blog

Las carpetas que no contienen page.js o route.js se vuelven privadas (no accesibles desde la URL), permitiendo organizar componentes, hooks y utilidades sin exponer rutas.
Jerarquía de archivos especiales

En una misma carpeta pueden coexistir: layout.js, page.js, loading.js, error.js, template.js. Todos estos se convierten en anidados automáticamente:
```text
app/
├── layout.js          (Layout raíz obligatorio)
├── page.js            (Página principal "/")
├── about/
│   ├── layout.js      (Layout opcional para /about/*)
│   └── page.js        (Página "/about")
├── blog/
│   ├── layout.js      (Layout del blog)
│   ├── loading.js     (Carga mientras se resuelve /blog)
│   ├── error.js       (Error para /blog y sus hijos)
│   ├── page.js        ("/blog")
│   └── [slug]/
│       └── page.js    ("/blog/123")
```

### El layout raíz

Todo proyecto con App Router debe tener un layout raíz en app/layout.js. Este componente envuelve toda la aplicación y es el lugar para definir la estructura HTML, fuentes, metadatos globales y proveedores.
```jsx
export const metadata = {
  title: 'Mi aplicación',
  description: 'Descripción global',
}

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        <nav>Barra de navegación global</nav>
        {children}
      </body>
    </html>
  )
}
```

Los layouts raíz son Server Components por defecto; no pueden usar hooks de cliente. Si necesitas proveedores de contexto (Redux, temas, etc.), debes crear un Client Component separado e importarlo.
Ventajas del App Router

    Renderizado híbrido y granular: puedes combinar Server Components estáticos, dinámicos y Client Components en un mismo árbol.

    Layouts persistentes: no se desmontan al navegar, lo que mejora la experiencia y reduce código.

    Streaming y Suspense integrados: carga progresiva sin configuración compleja.

    Server Actions: mutaciones desde el cliente sin API routes.

    Caché más fino: control por fetch, segmentos y rutas con revalidatePath, revalidateTag.

Entender estas bases es fundamental antes de profundizar en los siguientes conceptos.
---

## Archivo: `02-app-router/server-components-vs-client.md`

React Server Components vs Client Components

En el App Router, Next.js trata a todos los componentes como React Server Components (RSC) por defecto. Para usar interactividad, estado o efectos, necesitas un Client Component.
React Server Components (RSC)

¿Qué son? Componentes que se renderizan únicamente en el servidor (o en tiempo de build). Su resultado (HTML + formato especial de React) se envía al cliente sin JavaScript adicional.

Características:

    No pueden usar useState, useEffect, useContext, useReducer ni ningún hook que requiera el ciclo de vida del navegador.

    No pueden manejar eventos como onClick o onSubmit (a menos que sea una Server Action).

    Pueden usar async/await directamente en el cuerpo del componente.

    Tienen acceso directo a bases de datos, sistema de archivos, variables de entorno privadas.

    El código que contienen nunca se expone al cliente, mejorando la seguridad y el tamaño del bundle.

Ejemplo:
```jsx
// app/blog/page.js
export default async function BlogPage() {
  const posts = await fetch('https://api.../posts', { next: { revalidate: 60 } })
  const data = await posts.json()

  return (
    <ul>
      {data.map(post => <li key={post.id}>{post.title}</li>)}
    </ul>
  )
}
```

Aquí BlogPage es un Server Component: obtiene datos en el servidor y renderiza HTML sin hidratación.
Client Components

Se definen añadiendo la directiva 'use client' en la primera línea del archivo. Esto le indica a Next.js que el componente y sus dependencias deben enviarse al navegador y seguir las reglas tradicionales de React.

Cuándo usarlos:

### Manejo de estado (useState, useReducer)

### Efectos y ciclo de vida (useEffect, useLayoutEffect)

### Eventos del DOM (onClick, onChange)

### Contexto de cliente (useContext con un provider creado en un Client Component)

### Hooks personalizados que usan lo anterior

### Librerías que dependen del navegador (gráficos, carruseles)

Ejemplo:
```jsx
'use client'

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

Todo componente que importe un Client Component se convierte también en Client Component si no se separa cuidadosamente.
Composición: la clave para optimizar

Es posible intercalar Server y Client Components. La regla: puedes renderizar un Client Component dentro de un Server Component, y pasar Server Components como children (o props) de un Client Component. Así mantienes el renderizado del servidor para la mayor parte del árbol.
```jsx
// app/layout.js (Server Component raíz)
import ThemeProvider from './ThemeProvider' // Client Component (provee contexto)
import Navigation from './Navigation' // Server Component

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ThemeProvider>
          <Navigation /> {/* Server Component pasado como children */}
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

ThemeProvider es un Client Component porque usa useState para el tema, pero los hijos que recibe pueden ser Server Components; no se hidratan como cliente, manteniendo cero JS.
Límites de cliente y rendimiento

Next.js genera un límite de cliente (client boundary) al importar un Client Component desde un Server Component. El bundle JS del Client Component incluirá todo el subárbol a partir de ese punto. Por eso es recomendable empujar los Client Components lo más abajo posible en el árbol.

Buenas prácticas:

    Usa Server Components para la estructura y fetching.

    Extrae la interactividad en pequeños Client Components (p. ej., un botón de "Me gusta" es Client Component, pero el post completo sigue siendo Server Component).

    Pasa datos desde Server Components a Client Components vía props (serializables).

    No conviertas innecesariamente componentes grandes en cliente solo por un pequeño hook.

### Casos típicos de mezcla

    Navegación interactiva: El componente Nav es Server, pero el botón hamburguesa (estado abierto/cerrado) es Client.

    Formularios con Server Actions: El formulario es Client (necesita onSubmit con JavaScript), pero la acción que invoca es del servidor.

    Tema oscuro: Un provider Client a nivel raíz, pero las páginas son completamente Server.

Entender esta separación te permite maximizar el rendimiento y la experiencia de desarrollo.
---

## Archivo: `02-app-router/rutas-estaticas-dinamicas-paralelas.md`

Rutas estáticas, dinámicas y paralelas en App Router

El App Router ofrece un modelo de enrutamiento mucho más potente que el Pages Router. Además de las rutas estáticas y dinámicas, introduce rutas paralelas e interceptación de rutas.
Rutas estáticas

Simplemente crea una carpeta con un archivo page.js. Ejemplos:

### app/contacto/page.js → /contacto

### app/acerca/nosotros/page.js → /acerca/nosotros

El archivo page.js exporta por defecto un componente (Server o Client). Next.js asigna la URL automáticamente.
Rutas dinámicas (segmentos variables)

Se indican con carpetas entre corchetes: [id], [slug].

    app/productos/[id]/page.js → /productos/1, /productos/abc, etc.

Dentro de page.js, los parámetros se reciben mediante la prop params (en Server Components) o con useParams (en Client Components).

En Server Component:
```jsx
export default function Producto({ params }) {
  const { id } = params
  return <h1>Producto: {id}</h1>
}
```

En TypeScript:
```tsx
type Props = { params: { id: string } }

export default function Producto({ params }: Props) { /* ... */ }
```

En Client Component:
```jsx
'use client'
import { useParams } from 'next/navigation'

export default function Producto() {
  const params = useParams() // { id: '...' }
  return <h1>{params.id}</h1>
}
```

### Rutas catch-all (captura todas)

Se definen con [...slug] y capturan cualquier cantidad de segmentos.

### app/docs/[...slug]/page.js → /docs, /docs/intro, /docs/guia/instalacion

params.slug será un array de strings (['intro'], ['guia', 'instalacion']).

Para que la ruta base también coincida (sin segmentos extras), usa [[...slug]] (opcional):

    app/docs/[[...slug]]/page.js → /docs (slug = undefined/[]), /docs/uno (slug = ['uno']).

### Rutas paralelas

Las rutas paralelas permiten renderizar múltiples árboles de páginas en la misma vista, cada uno con su propio enrutamiento. Se implementan mediante slots: carpetas con el prefijo @.

Ejemplo típico en un dashboard:
```text
app/
├── layout.js
├── page.js              (página principal)
├── @analytics/
│   └── page.js          (slot analytics)
├── @team/
│   └── page.js          (slot team)
└── dashboard/
    ├── layout.js        (layout que define los slots en la misma vista)
    ├── @analytics/
    │   ├── page.js      (analytics en /dashboard)
    │   └── reports/
    │       └── page.js  (analytics en /dashboard/reports)
    └── @team/
        ├── page.js
        └── settings/
            └── page.js
```

En app/dashboard/layout.js, los slots se reciben como props:
```jsx
export default function DashboardLayout({ children, analytics, team }) {
  return (
    <div className="dashboard">
      <aside>{children}</aside>   {/* contenido principal opcional */}
      <main>
        <section>{team}</section>
        <section>{analytics}</section>
      </main>
    </div>
  )
}

    Cada slot (carpeta @...) funciona como una ruta paralela independiente.
```

    La navegación entre páginas dentro de un slot mantiene el estado de los demás.

    Si un slot no tiene una ruta activa, puedes mostrar un default.js para ese slot (archivo que define el contenido por defecto cuando no hay página coincidente).

Default views:
Crea un archivo default.js en el slot para que siempre haya contenido renderizado (por ejemplo, cuando navegas a una ruta que no tiene ese slot definido).
Beneficios de rutas paralelas

    Construcción de interfaces complejas tipo dashboard sin necesidad de estado global para manejar subrutas.

    Carga independiente y streaming por slot.

    Mejor organización del código (cada slot es autónomo).

### Rutas de interceptación (ver capítulo siguiente)

Las rutas paralelas suelen usarse junto con rutas de interceptación para crear modales, feeds, etc.

Dominar rutas estáticas, dinámicas y paralelas te da un control total sobre la estructura de URLs y la composición de la UI en el App Router.
---

## Archivo: `02-app-router/interceptacion-de-rutas.md`

Interceptación de rutas en App Router

La interceptación de rutas permite interceptar una navegación y mostrar una versión alternativa de la página de destino, manteniendo el contexto actual. Esto es ideal para modales, galerías, o feeds de detalle que no quieres que reemplacen la página completa.
Cómo funciona

Se utilizan convenciones de nomenclatura especiales en las carpetas para indicar que una ruta debe interceptar a otra. Se basan en la notación de segmentos relativos:

### (.) → intercepta el mismo nivel

### (..) → intercepta un nivel superior

### (..)(..) → dos niveles superiores

### (...) → intercepta desde la raíz

La carpeta de interceptación se coloca al mismo nivel que la ruta interceptada, usando la notación.
Ejemplo: Modal de foto

Supongamos la ruta /feed (feed de fotos) y /photo/[id] (página de detalle completa). Queremos que al hacer clic en una foto desde el feed, se abra un modal en lugar de navegar a la página completa.

Estructura:
```text
app/
├── feed/
│   ├── page.js           # lista de fotos
│   └── (.)photo/         # intercepta /photo desde /feed
│       └── [id]/
│           └── page.js   # modal de la foto
├── photo/
│   └── [id]/
│       └── page.js       # página de detalle completa
└── layout.js
```

Cuando el usuario está en /feed y hace clic en una foto, Next.js busca coincidencias en el mismo nivel con (.), encuentra (.)photo/[id]/page.js y la renderiza en lugar de la página real. Si el usuario recarga la página o accede directamente a /photo/123, se carga la ruta real photo/[id]/page.js.
Implementación común con paralelas

Para que el modal se renderice sobre el feed sin perder el contenido de fondo, usarás rutas paralelas. Por ejemplo, un slot @modal que contenga la interceptación:
```text
app/
├── layout.js            (define children y modal slots)
├── @modal/
│   ├── default.js       (null, no muestra nada por defecto)
│   └── (.)photo/
│       └── [id]/
│           └── page.js  (contenido del modal)
├── feed/
│   ├── layout.js        (si es necesario)
│   └── page.js
└── photo/
    └── [id]/
        └── page.js
```

En app/layout.js:
```jsx
export default function RootLayout({ children, modal }) {
  return (
    <html>
      <body>
        {children}
        {modal}
      </body>
    </html>
  )
}
```

modal será renderizado en paralelo. default.js en @modal puede retornar null para no mostrar nada cuando no hay modal activo.
Navegación entre interceptación y ruta real

    Desde el feed, el Link a /photo/123 activa la interceptación.

    Si se comparte la URL /photo/123, se carga la página completa sin modal.

    Puedes cerrar el modal con router.back() o redirigiendo a /feed.

### Estados de carga y error

Puedes añadir loading.js y error.js dentro de la ruta interceptada para manejar la carga del modal y errores, igual que cualquier otra ruta.
Combinación con rutas paralelas

Las rutas paralelas permiten mantener la página original (feed) mientras la interceptación se superpone (modal). Es la forma recomendada para modales, diálogos, bandejas de notificaciones, etc.
Notación adicional

    (..) intercepta un nivel superior. Útil cuando desde /dashboard/settings quieres interceptar /dashboard/help.

    (...) intercepta desde la raíz de app/, ideal para interceptar rutas profundas desde cualquier nivel sin preocuparte por la profundidad.

Ejemplo con (...):
Carpeta app/(...)photo/[id]/page.js intercepta photo/[id] desde cualquier ruta.
Diferencias con redirecciones o modales hechos a mano

La interceptación de rutas se basa en la navegación del lado del cliente. Es más performante porque la página de fondo no se desmonta ni pierde su estado. Además, la URL se actualiza normalmente (por defecto, usando push).
Resumen práctico

    Usa (.)nombreRuta para interceptar en el mismo nivel.

    Combínalo con slots (@modal, @sidebar) para separar responsabilidades.

    Define default.js para que los slots no muestren nada por defecto.

    Aprovecha que la ruta real sigue existiendo para permitir acceso directo y compartir enlaces.

Con esta técnica puedes crear experiencias de usuario fluidas manteniendo URLs normales y navegación natural.
---

## Archivo: `02-app-router/layouts-y-templates.md`

Layouts y Templates en App Router

Next.js proporciona dos mecanismos para definir la estructura que envuelve las páginas: layouts y templates. Ambos se basan en archivos layout.js y template.js dentro de la carpeta app/.
Layout (layout.js)

Un layout es un componente que envuelve las páginas de un segmento y persiste su estado entre navegaciones. El layout raíz (app/layout.js) es obligatorio y define la estructura HTML principal.

Características clave:

    Solo se renderiza una vez cuando se monta, y no se vuelve a renderizar al navegar entre páginas hijas (a menos que cambie searchParams o params del layout anidado).

    Ideal para barras de navegación, pies de página, menús laterales.

    Recibe children (la página o segmento interior) y opcionalmente params.

    Puede ser asíncrono (Server Component) para obtener datos para el layout (p. ej., datos del usuario).

### Ejemplo: layout con fetching
```jsx
// app/dashboard/layout.js
export default async function DashboardLayout({ children, params }) {
  const user = await fetchUser(params.userId)

  return (
    <div className="dashboard">
      <aside>
        <UserMenu user={user} />
      </aside>
      <main>{children}</main>
    </div>
  )
}
```

Porque el layout persiste, el menú lateral no pierde su estado (por ejemplo, scroll, selección de elemento) al cambiar de página dentro del dashboard.
Anidamiento de layouts

Los layouts se anidan según la jerarquía de carpetas. Por ejemplo:
```text
app/
├── layout.js          (RootLayout)
├── products/
│   ├── layout.js      (ProductsLayout)
│   └── [category]/
│       ├── layout.js  (CategoryLayout)
│       └── page.js
```

Cada layout envuelve al siguiente. El flujo: RootLayout → ProductsLayout → CategoryLayout → page.

Al navegar de /products/ropa a /products/electronica, ProductsLayout y RootLayout se mantienen, mientras que CategoryLayout y la página cambian. Sin embargo, si CategoryLayout tiene datos propios dependientes de params.category, se ejecutará el renderizado del servidor para ese layout (porque params cambió).
Template (template.js)

Un template es similar a un layout, pero se crea una nueva instancia del componente cada vez que el usuario navega a una página dentro de ese segmento. No persiste el estado.

Cuándo usarlo:

    Para animaciones de entrada/salida usando motion o framer-motion, donde necesitas que el componente se monte/desmonte.

    Para reinicializar ciertos estados locales (por ejemplo, un formulario que debe vaciarse al cambiar de página).

    Cuando dependes de useEffect para cierta lógica que debe ejecutarse al entrar a la página.

Ejemplo:
```jsx
// app/dashboard/template.js
'use client'

import { motion } from 'framer-motion'

export default function DashboardTemplate({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      {children}
    </motion.div>
  )
}
```

Como no persiste, al navegar entre páginas del dashboard se reproduce la animación.
Uso conjunto

Puedes tener layout.js y template.js en la misma carpeta; ambos envolverán la página. El orden es: layout → template → page.
```jsx
// Layout (persistente)
export default function Layout({ children }) {
  return <div><Nav />{children}</div>
}

// Template (se re-monta)
export default function Template({ children }) {
  return <div className="fade">{children}</div>
}

// Page
export default function Page() {
  return <h1>Contenido</h1>
}
```

### Estructura resultante: <Layout><Template><Page/></Template></Layout>
Pasar información entre layouts y páginas

No hay un mecanismo directo para pasar props de layout a page. Utiliza React Context (Client Component) o cookies/headers accesibles en Server Components. También puedes usar Server Actions para modificar datos del layout desde la página.
Layouts y Server Actions

Puedes colocar Server Actions en el layout (ejemplo: cerrar sesión) y pasarlas a componentes cliente.
Layouts dinámicos y revalidación

Si un layout obtiene datos con fetch, puedes configurar revalidate para ISR, igual que en páginas.

Los layouts constituyen el núcleo del App Router, facilitando la creación de interfaces complejas con mínimo esfuerzo y código repetitivo.
---

## Archivo: `02-app-router/loading-y-error.md`

loading.js y error.js: Manejo de estados en App Router

El App Router simplifica drásticamente el manejo de estados de carga y errores mediante dos archivos especiales: loading.js y error.js. Ambos aprovechan React Suspense y los Error Boundaries de React para encapsular cada segmento de ruta.
loading.js – UI de carga instantánea

Cuando una página (o un layout) tiene un componente asíncrono (Server Component que usa await), Next.js necesita mostrar algo mientras se resuelve la promesa. loading.js define el fallback de Suspense para esa ruta.

Cómo funciona:

    Coloca loading.js en la misma carpeta que page.js (o en cualquier segmento).

    Mientras la página se genera (en el servidor o con streaming), se muestra el contenido de loading.js.

    Cuando la página está lista, se reemplaza automáticamente.

Ejemplo básico:
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

El archivo loading.js se convierte en un límite de Suspense para el segmento. Next.js lo envuelve automáticamente con <Suspense fallback={<Loading/>}>.

Anidamiento:

Si tienes loading.js en app/ y otro en app/blog/, cada uno actúa solo para su segmento. Navegar a /blog mostrará el loading del blog, mientras el resto de la interfaz (layout) ya está disponible (streaming).

Streaming y carga parcial:

Cuando usas loading.js, no necesitas esperar que toda la página se genere. Next.js puede enviar el layout raíz y el shell de inmediato, luego el loading del segmento, y finalmente el contenido de la página. Esto mejora el LCP y la interactividad.
error.js – Aislamiento de errores

error.js define un Error Boundary para una ruta. Captura errores ocurridos en los Server Components o Client Components hijos, sin afectar el resto de la interfaz.

Requisitos:

    Debe ser un Client Component (porque maneja el ciclo de vida de error).

    Exporta una función que recibe { error, reset }.

```jsx
'use client' // Error boundaries must be Client Components

export default function DashboardError({ error, reset }) {
  return (
    <div>
      <h2>Ocurrió un error en el dashboard</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Intentar de nuevo</button>
    </div>
  )
}

    reset() es una función que intenta re-renderizar el segmento. Si el error fue transitorio (p. ej., fetch fallido), el segmento se recupera sin recargar toda la página.
```

    El error no se propaga a los layouts superiores ni a la página raíz.

Ubicación:

Coloca error.js en la carpeta del segmento a proteger. Puedes tener múltiples niveles (por ejemplo, app/error.js global y uno específico en app/dashboard/error.js). El más cercano captura primero.
not-found.js

Aunque no es exactamente de error, es relevante. not-found.js se muestra cuando se invoca notFound() desde un Server Component o se visita una ruta inexistente. Debe ser un Client Component (opcional) y se renderiza dentro del layout sin 404 HTTP (puede mostrarse con layout conservado).
```jsx
import { notFound } from 'next/navigation'

export default async function Page({ params }) {
  const post = await getPost(params.slug)
  if (!post) notFound()
  // ...
}
```

not-found.js puede estar en cualquier nivel; el más cercano se muestra.
Combinación de loading y error

Puedes tener ambos en el mismo directorio. Por ejemplo:
```text
app/
├── dashboard/
│   ├── loading.js
│   ├── error.js
│   └── page.js
```

    Primero se muestra loading.js mientras page.js espera.

    Si ocurre un error, error.js lo captura y muestra la UI de error.

### Manejo de errores en Server Actions

Los errores lanzados en Server Actions se pueden capturar en el error boundary correspondiente a la ruta donde se usó, o bien manejarlos localmente con try/catch en el Client Component.
Caché de errores

El error boundary mantiene la UI de error mientras no se llame reset(). Si se recarga la página, se reintenta el renderizado original. No hay almacenamiento en caché del error.
Migración desde Pages Router

En Pages Router tenías que implementar estados de carga manualmente (router.isFallback, estados locales para SSR). En App Router, la experiencia es declarativa, mucho más limpia y robusta.

loading.js y error.js representan uno de los mayores avances del App Router: encapsulan el comportamiento esperado de cualquier aplicación moderna con mínimo código.
---

## Archivo: `02-app-router/route-handlers-app.md`

Route Handlers en App Router

Los Route Handlers reemplazan a las API Routes del Pages Router dentro del App Router. Se definen en archivos route.js (o route.ts) y te permiten crear endpoints HTTP personalizados sin renderizar una página.
Configuración básica

En cualquier carpeta de app/ que no contenga page.js, puedes crear un archivo route.js. La carpeta define la ruta base y el archivo exporta funciones nombradas según el método HTTP.
```js
// app/api/hello/route.js
export async function GET(request) {
  return new Response(JSON.stringify({ message: 'Hola mundo' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  })
}
```

Al igual que las API Routes, las rutas son servidas por Next.js y pueden coexistir con páginas, pero una carpeta no puede tener page.js y route.js simultáneamente.
Métodos HTTP soportados

Exporta funciones con los nombres de los métodos HTTP que deseas manejar: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS. Si un método no está definido, Next.js retorna 405 Method Not Allowed automáticamente.
```js
export async function POST(request) {
  const body = await request.json()
  // procesar...
  return new Response(JSON.stringify({ success: true }), { status: 201 })
}
```

### El objeto Request y Response

Los Route Handlers reciben un objeto Web Request estándar (no el req de Node.js). Esto los hace compatibles con entornos Edge y Node.

    request.url: URL completa.

    request.method: método HTTP.

    request.headers: cabeceras (tipo Headers).

    request.json(), request.formData(), etc.

    request.cookies: representación de cookies (Next.js extiende la API Web).

Puedes usar NextRequest (de next/server) que extiende Request con propiedades adicionales como nextUrl, cookies, geo (en Edge). Es útil para middleware y lógica de rutas más compleja.
```js
import { NextResponse } from 'next/server'

export async function GET(request) {
  // Acceso a query params de manera fácil
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')
  // ...
  return NextResponse.json({ id })
}
```

### NextResponse

NextResponse es la contraparte de Response de las API Web, con helpers como:

    NextResponse.json(data, options) → Response con JSON.

    NextResponse.redirect(url, status?) → Redirección.

    NextResponse.next() → Continúa con el siguiente manejador (útil en middleware).

    NextResponse.rewrite(destination) → Reescribe la URL internamente.

### Segmentos dinámicos

Al igual que las páginas, las rutas pueden ser dinámicas. La carpeta [id] contendrá un route.js que recibe params en un segundo argumento.
```js
// app/api/items/[id]/route.js
export async function GET(request, { params }) {
  const id = params.id
  const item = await getItem(id)
  return NextResponse.json(item)
}
```

Los parámetros son accesibles de forma síncrona en la firma de la función.
Middleware de ruta

Los Route Handlers permiten configurar el runtime y opciones de caché mediante el objeto config exportado (opcional):
```js
export const runtime = 'edge' // 'nodejs' (por defecto)
export const dynamic = 'force-dynamic' // para que no se cachee
export const revalidate = 60 // ISR para endpoint GET (no oficial pero puede usarse)
```

Para un control más fino, usa la API de fetch con next.revalidate o cache: 'no-store'.
Streams y procesamiento de archivos

Puedes devolver streams directamente. Por ejemplo, para leer un archivo grande:
```js
import { NextResponse } from 'next/server'

export async function GET() {
  const readableStream = new ReadableStream({...})
  return new Response(readableStream, {
    headers: { 'Content-Type': 'application/octet-stream' },
  })
}
```

Esto es útil para descargas, streaming de video, etc.
CORS y cabeceras personalizadas

Configura las cabeceras CORS dentro del handler o en next.config.js. Dentro del handler puedes añadir:
```js
export async function GET() {
  return new Response(JSON.stringify(data), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST',
    },
  })
}
```

Para preflight OPTIONS, define también el manejador.
Comparación con API Routes (Pages)
API Routes (Pages)	Route Handlers (App)
req es http.IncomingMessage	request es Web Request
res es http.ServerResponse	Devuelves Response directamente
Solo Node.js	Node.js o Edge Runtime
req.query, req.body	request.nextUrl.searchParams, request.json()
Rutas anidadas en pages/api/	Se integran en la estructura app/

La estandarización en la API Web hace que los Route Handlers sean más portables y consistentes.
Buenas prácticas

    Mantén los Route Handlers delgados: delegar lógica a servicios.

    Usa Server Actions para mutaciones asociadas a interfaz de usuario; los Route Handlers son para endpoints públicos/API.

    Combínalos con Middleware (middleware.js) para proteger rutas.

    Aprovecha los segmentos dinámicos para mantener RESTful.

Los Route Handlers te dan un backend ligero y completamente integrado con el resto de tu aplicación Next.js.
---

## Archivo: `02-app-router/server-actions.md`

Server Actions en App Router

Las Server Actions son funciones asíncronas ejecutadas en el servidor, pero que pueden ser invocadas desde Client Components o incluso desde formularios HTML sin necesidad de crear un API endpoint. Fueron introducidas como característica experimental y ahora son estables (Next.js 14+).
Definición

Una Server Action se define con la directiva 'use server' al inicio de un archivo o dentro de una función asíncrona. Pueden residir en Server Components, en archivos separados o incluso en Client Components (con restricciones).

### Forma 1: Directiva en archivo independiente
```js
// app/actions.js
'use server'

export async function createPost(formData) {
  const title = formData.get('title')
  // Validar y guardar en BD
  await db.post.create({ data: { title } })
  // Revalidar la página de lista
  revalidatePath('/posts')
}
```

### Forma 2: Dentro de un Server Component
```js
// app/new-post/page.js
import { revalidatePath } from 'next/cache'

export default function NewPost() {
  async function handleSubmit(formData) {
    'use server'
    // ... lógica
  }

  return (
    <form action={handleSubmit}>
      <input name="title" />
      <button>Crear</button>
    </form>
  )
}
```

### Invocación desde formularios

La forma más natural es usar el atributo action de un <form>. El navegador enviará automáticamente un POST a la Server Action si está en un Client Component y se usa con JavaScript habilitado (progressive enhancement). Sin JS, el formulario funciona igual (se ejecuta la acción en el servidor).
```jsx
// Client Component
'use client'

import { createPost } from '@/app/actions'

export default function Form() {
  return (
    <form action={createPost}>
      <input type="text" name="title" required />
      <button type="submit">Enviar</button>
    </form>
  )
}
```

Puedes usar useFormStatus y useFormState (hooks de React DOM) para estados de carga y manejo de errores.

Ejemplo con useFormStatus:
```jsx
'use client'
import { useFormStatus } from 'react-dom'

function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? 'Guardando...' : 'Guardar'}</button>
}
```

### Acceso al request y cookies

Dentro de una Server Action puedes leer cookies y headers con las funciones de next/headers (que son dinámicas), por ejemplo:
```js
import { cookies } from 'next/headers'

export async function updatePreferences(formData) {
  const cookieStore = cookies()
  const token = cookieStore.get('token')
  // ...
}
```

### Redirecciones y manejo de errores

Puedes redirigir después de ejecutar una acción usando redirect de next/navigation:
```js
import { redirect } from 'next/navigation'

export async function login(formData) {
  // verificar credenciales...
  redirect('/dashboard')
}
```

Para manejar errores y mostrarlos en el cliente, puedes retornar un objeto serializable desde la acción y usar useFormState (experimental) o simplemente lanzar una excepción que capture el error boundary.
Revalidación de datos

Uno de los usos principales es mutar datos y luego revalidar la caché asociada:
```js
import { revalidatePath, revalidateTag } from 'next/cache'

export async function addComment(commentData) {
  await db.comment.create(...)
  revalidatePath('/posts/[slug]')  // revalida la página de ese post
  // o revalidateTag('comments')
}
```

Con esto, la interfaz se actualiza automáticamente sin recargar.
Invocación desde manejadores de eventos

Aunque lo común es mediante action, también puedes invocar Server Actions desde un onClick o useEffect usando la función exportada como cualquier función asíncrona normal (gracias a la integración con hooks como useTransition). Se envuelve en startTransition para manejar la navegación optimista.
```jsx
'use client'
import { createPost } from '@/app/actions'
import { useTransition } from 'react'

export default function CreateButton() {
  const [isPending, startTransition] = useTransition()

  const handleClick = () => {
    startTransition(async () => {
      await createPost(new FormData()) // construyes FormData
    })
  }

  return <button onClick={handleClick} disabled={isPending}>Crear</button>
}
```

Esto permite usar Server Actions sin formularios.
Seguridad

    Las Server Actions son endpoints POST automáticos con identificadores generados. Next.js las protege con CSRF (envía un token en un header al hacer llamadas desde el cliente). No es necesario configurarlo manualmente.

    Para acciones públicas, puedes usar headers() para verificar el origen.

    No expongas secretos en el código que se envía al cliente (todo lo exportado de un archivo con 'use server' no se filtra, solo el identificador).

### Limitaciones

    Las Server Actions solo pueden ser llamadas desde el mismo proyecto (mismo origen) por defecto.

    No pueden ser usadas en componentes puros del servidor (fuera de forms/eventos), su invocación debe originarse en un Client Component o a través de action.

    El tamaño máximo del payload es 1 MB (configurable en next.config.js con serverActions.bodySizeLimit).

### Cuándo usar Server Actions vs Route Handlers

    Server Actions: mutaciones estrechamente ligadas a una interfaz de usuario (formularios, likes, carritos). Ofrecen experiencia progresiva y revalidación automática.

    Route Handlers: APIs públicas, webhooks, integraciones de terceros, o cuando necesitas control total sobre códigos de estado, CORS, streaming.

Las Server Actions simplifican el patrón tradicional de crear endpoints API para cada formulario, reuniendo la lógica del servidor con la interfaz de usuario.
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


---

## Archivo: `04-data-fetching/patrones-pages-router.md`

Patrones de obtención de datos en Pages Router

En el Pages Router de Next.js, la obtención de datos puede ocurrir en el servidor (SSR, SSG) o en el cliente. La elección del patrón adecuado determina el rendimiento, el SEO y la experiencia de usuario.
Obtención de datos en el servidor
1. getServerSideProps (SSR)

Se ejecuta en cada solicitud. Perfecto para datos que cambian frecuentemente o son personalizados.
```jsx
export async function getServerSideProps(context) {
  const res = await fetch(`https://api.ejemplo.com/productos`)
  const productos = await res.json()
  return { props: { productos } }
}
```

Patrones:

    Cacheo con cabeceras HTTP: puedes agregar encabezados de caché para que las respuestas del servidor sean almacenadas por CDN o proxy.

```js
export async function getServerSideProps({ res }) {
  res.setHeader('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=300')
  // ...
}
```

    Obtención condicional según el usuario: lee cookies o headers para personalizar la respuesta.

    Redirecciones y notFound: usa redirect o notFound para manejar accesos no autorizados o contenido inexistente.

2. getStaticProps (SSG)

Se ejecuta en tiempo de compilación. Genera páginas estáticas que pueden ser servidas desde un CDN.
```jsx
export async function getStaticProps() {
  const res = await fetch('https://api.ejemplo.com/posts')
  const posts = await res.json()
  return { props: { posts }, revalidate: 3600 } // ISR opcional
}
```

Patrones:

    Obtención de múltiples fuentes: realiza varias llamadas en paralelo con Promise.all.

    Revalidación incremental (ISR): define revalidate para que la página se regenere periódicamente.

    Pre-renderizado de rutas dinámicas: combina con getStaticPaths. Puedes usar fallback: true o 'blocking' para páginas no pre-renderizadas.

3. getStaticPaths (para rutas dinámicas estáticas)

Controla qué rutas se generan en el build.
```jsx
export async function getStaticPaths() {
  const res = await fetch('https://api.ejemplo.com/posts')
  const posts = await res.json()
  const paths = posts.map(post => ({ params: { id: post.id.toString() } }))
  return { paths, fallback: 'blocking' }
}

    fallback: false: solo las rutas listadas funcionan; cualquier otra devuelve 404.

    fallback: true: genera rutas no listadas bajo demanda (cliente verá un estado de carga mientras se genera).

    fallback: 'blocking': la solicitud espera la generación en el servidor (sin estado de carga, mejor para SEO).
```

### Obtención de datos en el cliente

Para datos que no necesitan SEO o que dependen de interacciones del usuario, puedes obtenerlos desde el navegador.
Uso básico con useEffect y fetch
```jsx
import { useState, useEffect } from 'react'

export default function Perfil() {
  const [usuario, setUsuario] = useState(null)

  useEffect(() => {
    fetch('/api/usuario')
      .then(res => res.json())
      .then(data => setUsuario(data))
  }, [])

  if (!usuario) return <div>Cargando...</div>
  return <div>{usuario.nombre}</div>
}
```

Desventajas:

    Sin SEO para el contenido cargado en cliente.

    Posible cascada de carga si no se maneja correctamente.

    Puede penalizar Core Web Vitals (LCP).

### SWR y React Query (librerías de cliente recomendadas)

Estas librerías resuelven caché, revalidación, sincronización y estados de carga de forma más eficiente. Se tratan en detalle en el capítulo correspondiente.
```jsx
import useSWR from 'swr'

export default function Perfil() {
  const { data, error } = useSWR('/api/usuario', fetcher)
  if (error) return <div>Error</div>
  if (!data) return <div>Cargando...</div>
  return <div>{data.nombre}</div>
}
```

### Patrones híbridos

Puedes combinar datos del servidor con datos del cliente en la misma página.

    Carga la estructura y datos iniciales con getStaticProps/getServerSideProps.

    Hidrata la página con esos datos y luego usa SWR para actualizarlos continuamente.

```jsx
export default function Productos({ productosIniciales }) {
  const { data: productos } = useSWR('/api/productos', fetcher, { fallbackData: productosIniciales })

  return <ul>{productos.map(p => <li key={p.id}>{p.nombre}</li>)}</ul>
}

export async function getStaticProps() {
  const productos = await getProductos()
  return { props: { productosIniciales: productos } }
}
```

### Prefetching y precarga

    Link prefetching: <Link> precarga automáticamente la página de destino (si es estática o tiene getStaticProps).

    Prefetch manual: router.prefetch(url) para calentar la caché del cliente.

    Precarga de datos con SWR: puedes precargar la caché global de SWR con datos de las páginas que probablemente se visitarán.

```js
// En alguna interacción
router.prefetch('/productos/123')
```

### Resumen de criterios de elección
Método	Cuándo usarlo
getStaticProps	Datos que no cambian por usuario, actualizables con ISR.
getServerSideProps	Datos personalizados o que cambian cada solicitud.
Cliente (fetch / SWR)	Datos que dependen de interacción, o no necesitan SEO inmediato.
Híbrido	Muestra inicial instantánea con SSG/SSR y actualizaciones en cliente.

Dominar estos patrones te permitirá construir aplicaciones rápidas, escalables y con excelente SEO en Pages Router.
---

## Archivo: `04-data-fetching/patrones-app-router.md`

Patrones de obtención de datos en App Router

El App Router introduce React Server Components, que permiten obtener datos directamente en el servidor, dentro del componente, sin necesidad de funciones externas. Además, extiende la API fetch con potentes opciones de caching.
Obtención en Server Components (por defecto)

En un Server Component puedes usar async/await y fetch directamente. Next.js optimiza las solicitudes automáticamente.
```tsx
// app/productos/page.tsx
export default async function Productos() {
  const res = await fetch('https://api.ejemplo.com/productos')
  const productos = await res.json()
  return <ul>{productos.map(p => <li key={p.id}>{p.nombre}</li>)}</ul>
}
```

Al no especificar opciones de caché, fetch usa por defecto cache: 'force-cache', lo que vuelve la página estática (SSG). Los datos se almacenan en el Data Cache y se sirven desde ahí hasta que los revalides.
Control de caché por fetch

Puedes controlar el comportamiento con opciones en el segundo argumento:

    cache: 'force-cache' (por defecto): los datos se cachean. La página es estática.

    cache: 'no-store': cada solicitud vuelve a obtener los datos → página dinámica (SSR).

    next: { revalidate: N }: ISR. Se cachea por N segundos, luego se revalida en segundo plano.

    next: { tags: ['nombre-tag'] }: permite revalidar bajo demanda con revalidateTag.

```tsx
const res = await fetch('https://api...', { next: { revalidate: 60 } })
```

### Fetching paralelo y secuencial

    Paralelo: Si varios fetch no dependen entre sí, se ejecutan en paralelo de forma automática. Puedes usar Promise.all para iniciarlos al mismo tiempo.

```tsx
const [productos, categorias] = await Promise.all([
  fetch('.../productos'),
  fetch('.../categorias')
])
```

O simplemente lanzarlos en orden sin await intermedio; Next.js los agrupa.

    Secuencial: Cuando un fetch depende de otro, debes usar await:

```tsx
const user = await fetch(`.../user/${id}`).then(r => r.json())
const posts = await fetch(`.../posts?userId=${user.id}`).then(r => r.json())
```

### Precarga de datos con generateStaticParams

Para rutas dinámicas estáticas, define generateStaticParams para pre-renderizar ciertas rutas en el build.
```tsx
export async function generateStaticParams() {
  const posts = await fetch('.../posts').then(r => r.json())
  return posts.map(post => ({ slug: post.slug }))
}
```

### Obtención de datos en Client Components

En Client Components, se recomienda usar bibliotecas como SWR o TanStack Query, o useEffect + fetch. Evita usar fetch directamente en Client Components para datos que se podrían obtener en el servidor; en su lugar, obtén los datos en un Server Component padre y pásalos como props.

Ejemplo con SWR en un Client Component:
```tsx
'use client'
import useSWR from 'swr'

export default function ContadorVisitas() {
  const { data } = useSWR('/api/visitas', fetcher)
  return <span>{data || 0}</span>
}
```

### Patrón híbrido: Server + Client

Obtén los datos en un Server Component y pásalos a un Client Component que los muestre o los actualice.
```tsx
// app/productos/page.tsx
import ListaProductos from './ListaProductos' // Client Component

export default async function Pagina() {
  const productos = await fetch('...').then(r => r.json())
  return <ListaProductos productosIniciales={productos} />
}
```

### tsx

### 'use client'
export default function ListaProductos({ productosIniciales }) {
  const { data } = useSWR('...', fetcher, { fallbackData: productosIniciales })
  // ...
}

### Streaming y Suspense para carga progresiva

Puedes envolver componentes con datos lentos en <Suspense> para que el resto de la página se muestre inmediatamente.
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

### Fetching en Server Actions

Para mutaciones, las Server Actions son la opción recomendada. Después de mutar, puedes revalidar datos con revalidatePath o revalidateTag.
Estrategia de revalidación bajo demanda

Etiqueta tus fetch con tags y crea una Server Action que los invalide cuando sea necesario (por ejemplo, al editar un producto).
```tsx
// al crear producto
await fetch('.../productos', { method: 'POST', ... })
revalidateTag('productos')
```

### Recomendaciones generales

    Prefiere Server Components para datos que pueden ser públicos y no requieren interactividad.

    Utiliza Suspense para descomponer la carga y mejorar LCP.

    Aprovecha la caché de Next.js al máximo; solo desactívala (no-store) cuando realmente necesites datos en tiempo real.

    Para dependencias de cliente, utiliza SWR o TanStack Query con hidratación.

El App Router ofrece un modelo declarativo y flexible para la obtención de datos, alineado con las últimas capacidades de React y el streaming.
---

## Archivo: `04-data-fetching/cache-y-revalidate.md`

Caché y revalidación en Next.js

Next.js posee varios niveles de caché que trabajan juntos para ofrecer un rendimiento óptimo. Comprender cómo operan y cómo controlarlos es fundamental para equilibrar frescura y velocidad.
Las capas de caché

### Router Cache (Cliente)

        Almacena en memoria las páginas visitadas (RSC payload) para navegación instantánea.

        Se limpia al recargar la página o por tiempo (30s por defecto en producción; experimentalmente configurable).

### Full Route Cache (Servidor)

        Caché del HTML y RSC payload pre-renderizados.

        Se guarda en el servidor (o CDN).

        Se invalida con revalidaciones (tiempo o bajo demanda).

### Data Cache (Servidor)

        Caché de los resultados de fetch. Persiste entre builds y despliegues (en plataformas como Vercel, usa una capa distribuida).

        Controlado por revalidate, tags o invalidación manual.

### Image Cache

        Imágenes optimizadas por next/image tienen su propia caché (independiente).

### Revalidación basada en tiempo (ISR)

Para páginas que usan datos con fetch, puedes especificar next.revalidate:
```tsx
export default async function Pagina() {
  const res = await fetch('https://...', { next: { revalidate: 60 } })
  // ...
}
```

Esto almacena en el Data Cache por 60 segundos. Durante ese tiempo, las solicitudes sirven la versión cacheada. Pasado el tiempo, la próxima solicitud dispara una regeneración en segundo plano (stale-while-revalidate).

También puedes exportar revalidate en la página o layout:
```tsx
export const revalidate = 120
```

Este valor se aplica a todos los fetch que no tengan su propio revalidate. Si hay varios, Next.js toma el menor como referencia.
Revalidación bajo demanda (On-demand)

Ideal para casos donde el contenido solo debe actualizarse después de una mutación (ej., al publicar un artículo).

Mecanismo de etiquetas (tags):

Etiquetas tus fetch con uno o varios tags:
```tsx
const res = await fetch('https://...', { next: { tags: ['posts'] } })
```

Luego, en una Server Action, Route Handler o incluso un webhook, invalidas ese tag:
```tsx
import { revalidateTag } from 'next/cache'
```

### revalidateTag('posts') // todos los fetch con ese tag se invalidan

Revalidación por ruta:
```tsx
import { revalidatePath } from 'next/cache'
```

### revalidatePath('/blog')        // revalida esa ruta específica
revalidatePath('/blog/[slug]') // revalida todas las rutas dinámicas que coincidan

La revalidación bajo demanda puede combinarse con ISR basado en tiempo para una estrategia híbrida.
Caché del cliente (Router Cache)

El Router Cache guarda las páginas completas (payload RSC) en memoria durante la sesión. No afecta al servidor.

    Invalidación: se refresca al hacer una navegación completa (window.location, redirección en acción) o al pasar el tiempo de stale (30s predeterminado).

    Configuración experimental: puedes ajustar staleTimes en next.config.js para extender su duración.

### Forzar comportamiento dinámico

Si necesitas que una ruta nunca se cachee (comportamiento 100% SSR), puedes:

    Usar cache: 'no-store' en todos los fetch.

    Exportar export const dynamic = 'force-dynamic'.

    Usar funciones dinámicas como cookies(), headers() o searchParams.

### Caché y Edge Runtime

Cuando ejecutas en Edge, el Data Cache puede no estar disponible (depende del proveedor). En Vercel, Edge también tiene acceso a la caché distribuida global, por lo que funciona idéntico.
Invalidación de toda la caché

Puedes forzar una regeneración completa de un segmento con revalidatePath sobre la ruta raíz ('/'), pero es costoso.
Ejemplo práctico: blog con ISR + revalidación bajo demanda

### Página de posts: fetch con next: { tags: ['posts'], revalidate: 3600 }

    Al crear o modificar un post, una Server Action ejecuta revalidateTag('posts').

    Además, la ruta del post individual se revalida con revalidatePath('/blog/' + slug).

### Headers de caché

Aunque el Data Cache funciona a nivel de fetch, para la Full Route Cache puedes influir con encabezados HTTP si despliegas en un servidor Node personalizado, aunque en Vercel esto se maneja automáticamente según la configuración de Next.js.
Resumen de comandos
Acción	Código
Revalidar por tag	revalidateTag('tag')
Revalidar ruta exacta	revalidatePath('/ruta')
Revalidar ruta dinámica	revalidatePath('/ruta/[param]')
Forzar dinámico	export const dynamic = 'force-dynamic'
Fijar revalidate por ruta	export const revalidate = 3600
No cachear fetch	fetch(url, { cache: 'no-store' })

Entender estos mecanismos te permitirá afinar la frescura de los datos sin sacrificar rendimiento.
---

## Archivo: `04-data-fetching/librerias-cliente-swr-query.md`

Librerías de cliente: SWR y TanStack Query (React Query) en Next.js

Para la obtención de datos en el cliente, Next.js recomienda dos bibliotecas principales: SWR (creada por Vercel) y TanStack Query (antes React Query). Ambas resuelven la gestión del estado del servidor, ofreciendo caché, revalidación automática, paginación, mutaciones y mucho más.
SWR (stale-while-revalidate)

SWR es una librería ligera que sigue el principio HTTP stale-while-revalidate: primero devuelve los datos en caché (stale), luego envía la solicitud al servidor y finalmente actualiza la UI con los nuevos datos.

Instalación:
```bash
npm install swr
```

Uso básico:
```tsx
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function Perfil() {
  const { data, error, isLoading } = useSWR('/api/usuario', fetcher)

  if (isLoading) return <div>Cargando...</div>
  if (error) return <div>Error</div>
  return <div>Hola {data.nombre}</div>
}
```

Características principales:

    Revalidación automática en foco de ventana, reconexión de red o intervalo configurable.

    Dependencias claves: la URL y el fetcher identifican la query.

    Soporte de mutaciones (mutate) y optimismo.

    Paginación con useSWRInfinite.

### TanStack Query (React Query)

Es más completa, con herramientas para manejo de caché avanzado, mutaciones con cache invalidation, devtools, etc.

Instalación:
```bash
npm i @tanstack/react-query
```

Uso básico con el provider:
```tsx
// app/providers.tsx
'use client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()
export default function Providers({ children }: { children: React.ReactNode }) {
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
}
```

Luego lo usas en cualquier componente cliente:
```tsx
'use client'
import { useQuery } from '@tanstack/react-query'

export default function Usuarios() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['usuarios'],
    queryFn: () => fetch('/api/usuarios').then(r => r.json()),
  })
  // ...
}
```

Ventajas:

    Caché persistente en memoria.

    Mutaciones con actualización optimista y revalidación automática.

    Devtools para inspeccionar el caché.

    Soporte para SSR/SSG con hidratación (Hydrate).

### Integración con Next.js
Hidratación desde el servidor (SSR/SSG)

Puedes precargar datos en el servidor y pasarlos como estado inicial para que el cliente los tenga al instante.

Con SWR:

En Pages Router:
```tsx
export async function getServerSideProps() {
  const data = await fetchData()
  return { props: { fallback: { '/api/usuario': data } } }
}

export default function Page({ fallback }) {
  const { data } = useSWR('/api/usuario', fetcher, { fallback })
}
```

En App Router: crea un provider que inicialice SWR con los datos obtenidos en un Server Component.

Con TanStack Query:

Usa HydrationBoundary (nuevo en v5) o Hydrate (versión anterior) para hidratar el query client.
```tsx
// app/posts/page.tsx
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query'
import Posts from './Posts' // Client Component

export default async function PostsPage() {
  const queryClient = new QueryClient()
  await queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: () => fetch('.../posts').then(r => r.json()),
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Posts />
    </HydrationBoundary>
  )
}
```

Así el cliente comienza con el caché ya lleno.
Revalidación y mutaciones

Después de una mutación (POST, PUT), es común querer actualizar la UI:

SWR:
```tsx
const { mutate } = useSWRConfig()
await fetch('/api/crear', { method: 'POST', body })
mutate('/api/tareas') // revalida esa clave
```

TanStack Query:
```tsx
const mutation = useMutation({
  mutationFn: (nuevaTarea) => fetch('/api/tareas', { method: 'POST', body: JSON.stringify(nuevaTarea) }),
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['tareas'] }),
})
```

### Cuándo usar cada una

    SWR: proyectos más simples, con necesidades estándar de caching y revalidación. Muy ligera y fácil de usar.

    TanStack Query: aplicaciones con lógica de caché compleja, muchos orígenes de datos, mutaciones optimistas, paginación infinita, etc.

Ambas funcionan perfectamente con Next.js y pueden coexistir. A menudo, la decisión se reduce a preferencias del equipo y complejidad del proyecto.
---

## Archivo: `05-optimizacion/next-image.md`

Optimización de imágenes con next/image

El componente <Image> de next/image sustituye a la etiqueta <img> nativa y proporciona optimizaciones automáticas que mejoran notablemente el rendimiento.
Principales beneficios

    Tamaño y formato automático: sirve la imagen en el tamaño exacto requerido según el dispositivo y en formatos modernos (WebP, AVIF) si el navegador lo soporta.

    Lazy loading nativo: las imágenes se cargan solo cuando están cerca del viewport.

    Prevención de CLS (Cumulative Layout Shift): reserva el espacio automáticamente usando las dimensiones.

    Caché y compresión: las imágenes se optimizan bajo demanda y se cachean en el servidor/cdn.

    Qualidad ajustable: sin perder nitidez.

### Uso básico
```jsx
import Image from 'next/image'
import logo from '../public/logo.png'

export default function Componente() {
  return (
    <Image
      src={logo}                // imagen importada localmente
      alt="Logo de la empresa"
      width={200}
      height={100}
      priority
    />
  )
}
```

### Imágenes locales vs remotas

    Locales: almacenadas en la carpeta public/. Puedes importarlas directamente y Next.js conoce sus dimensiones.

    Remotas: provenientes de una URL externa. Debes configurar los dominios permitidos en next.config.js:

```js
module.exports = {
  images: {
    domains: ['cdn.ejemplo.com'],
    // o remotePatterns (recomendado)
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.ejemplo.com',
        port: '',
        pathname: '/imagenes/**',
      },
    ],
  },
}
```

### Props esenciales

    src: ruta de la imagen (string o importación estática).

    width y height: dimensiones para reservar espacio (obligatorio excepto en fill o imágenes locales donde se infieren).

    alt: texto alternativo para accesibilidad (obligatorio).

    priority: cuando es true, la imagen se considera LCP y se carga con prioridad, eliminando el lazy loading. Debe usarse en la imagen más grande del fold.

    fill: hace que la imagen llene el contenedor padre (el padre debe tener position: relative). Útil cuando el tamaño es desconocido.

    sizes: información sobre el ancho de la imagen en distintos breakpoints, clave para que el navegador descargue el tamaño justo.

    quality: calidad de la imagen optimizada (1-100, por defecto 75).

    placeholder: 'empty' (default) o 'blur' (muestra un placeholder difuminado mientras carga).

    loader: función personalizada para generar la URL de la imagen (por defecto, el loader de Next.js).

### Estrategia de tamaño y sizes

El atributo sizes le dice al navegador qué ancho ocupará la imagen en diferentes tamaños de pantalla, para que descargue la resolución adecuada.
```jsx
<Image
  src="/hero.jpg"
  width={1200}
  height={600}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  alt="Hero"
/>
```

En este ejemplo, en móvil la imagen ocupa el 100% del viewport, en tablet el 50%, en desktop el 33%. Con sizes y srcset automático, se evita descargar una imagen de 1200px en un móvil pequeño.
Placeholder blur

Para imágenes locales, Next.js genera automáticamente un placeholder difuminado en el build.
```jsx
import hero from '../public/hero.jpg'
```

### <Image src={hero} placeholder="blur" alt="..." />

Para imágenes remotas, debes proveer la propiedad blurDataURL con una versión minúscula en base64.
Imágenes en contenedores flexibles o con fill

Cuando no puedes especificar un ancho fijo (p.ej., un banner al 100% del ancho), usa fill:
```jsx
<div style={{ position: 'relative', width: '100%', height: '300px' }}>
  <Image
    src="/banner.jpg"
    alt="Banner"
    fill
    style={{ objectFit: 'cover' }}
    sizes="100vw"
  />
</div>
```

### Optimización bajo demanda

Next.js crea un endpoint interno /_next/image que sirve las imágenes optimizadas. En producción (Vercel u otros) esto escala automáticamente. Para exportación estática (next export) no se soporta next/image; en ese caso se recomienda usar un proveedor de imágenes externo y un loader personalizado.
Configuración avanzada

    minimumCacheTTL: tiempo mínimo de caché de las imágenes en el servidor (por defecto 60s, en Vercel se ignora).

    deviceSizes y imageSizes: controlan qué tamaños se generan para el srcset.

    formats: ['image/avif', 'image/webp'] (por defecto) para formatos modernos.

    dangerouslyAllowSVG: permite optimizar SVG (puede tener implicaciones de seguridad si el SVG proviene de fuentes no confiables).

### Buenas prácticas

    Siempre define width/height o usa fill con contenedor proporcionado.

    Marca con priority las imágenes que estén en la parte visible inicial (especialmente LCP).

    Proporciona sizes siempre que la imagen no sea de ancho fijo.

    Utiliza importación estática para imágenes locales.

    Para imágenes generadas por usuario, habilita remotePatterns con rutas específicas.

next/image elimina la complejidad de la optimización de imágenes, una de las principales causas de mal rendimiento web.
---

## Archivo: `05-optimizacion/next-font.md`

Optimización de fuentes con next/font

next/font es el sistema de carga de fuentes incorporado en Next.js. Permite importar fuentes de Google Fonts o locales, y las auto-hospeda, eliminando peticiones externas y mejorando el rendimiento y la privacidad.
¿Por qué auto-hospedar?

    Rendimiento: las fuentes se sirven desde tu mismo dominio, evitando búsquedas DNS extra y conexiones a servidores de terceros.

    Privacidad: no se envían solicitudes a Google.

    Control total: puedes decidir exactamente el formato y la estrategia de carga.

### Google Fonts con next/font/google
```jsx
import { Montserrat } from 'next/font/google'

const montserrat = Montserrat({
  subsets: ['latin'],
  display: 'swap',
  weight: ['400', '700'],
})

export default function Layout({ children }) {
  return <html className={montserrat.className}>{children}</html>
}

    subsets: qué subconjuntos de caracteres incluir (p.ej., latin, cyrillic). Especifica al menos uno para reducir el tamaño.

    weight: pesos que necesitas. Si usas variable fonts, no necesitas pesos separados; solo incluye axes si son personalizables.

    display: controla cómo se comporta mientras la fuente se carga. 'swap' muestra texto con la fuente de sistema de inmediato y la cambia cuando la web font está lista (recomendado para evitar FOIT).
```

Para fuentes variables, puedes usarlas sin especificar weight:
```jsx
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })
```

### Fuentes locales con next/font/local

Carga fuentes que tengas en tu proyecto (por ejemplo, en public/fonts o dentro de src).
```jsx
import localFont from 'next/font/local'

const miFuente = localFont({
  src: [
    {
      path: '../public/fonts/MiFuente-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../public/fonts/MiFuente-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  display: 'swap',
})
```

Next.js automáticamente generará una variable CSS con la declaración @font-face y optimizará la entrega.
Uso con Tailwind CSS

Puedes integrar fácilmente tu fuente con Tailwind asignando una variable CSS.
```jsx
import { Roboto } from 'next/font/google'

const roboto = Roboto({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-roboto',
})

export default function Layout({ children }) {
  return <html className={`${roboto.variable} font-sans`}>{children}</html>
}
```

Luego en tailwind.config.js:
```js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-roboto)'],
      },
    },
  },
}
```

### Estrategias de carga y display

    auto: el navegador decide (puede causar FOIT).

    block: bloquea la visualización del texto un corto periodo.

    swap: muestra texto con fuente de sistema inmediatamente y lo intercambia cuando la web font está lista (mejor para LCP y UX).

    fallback: oculta el texto muy poco tiempo antes de intercambiarlo.

    optional: puede no aplicar la web font si tarda mucho (el usuario verá la de sistema).

swap es generalmente la mejor opción para Core Web Vitals.
Preload y subsetting automático

Next.js genera automáticamente un enlace <link rel="preload"> para los archivos de fuente necesarios, de modo que el navegador los descargue cuanto antes. Además, ajusta los subsets y caracteres para que incluyan solo los necesarios.
Optimizaciones para fuentes variables

Las fuentes variables contienen múltiples estilos en un solo archivo, reduciendo el número de descargas. next/font las maneja de forma nativa.
```jsx
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'] })
```

### Fuentes en Edge Runtime

next/font funciona sin problemas en Edge Runtime. Las definiciones de fuente se incrustan en el HTML base o se sirven desde el servidor.
Consideraciones

    El tamaño de las fuentes puede impactar en el LCP si no se manejan correctamente. Prefiere subset adecuado y solo los pesos necesarios.

    Si usas muchas fuentes, prioriza las que se usan en la parte visible.

    Las fuentes locales son ideales para un control absoluto sobre el rendimiento.

Con next/font, la tipografía web deja de ser un dolor de cabeza para convertirse en una parte optimizada y fácil de mantener.
---

## Archivo: `05-optimizacion/caching-estrategias.md`

Estrategias de caché en Next.js

Más allá de los mecanismos básicos de revalidación, Next.js ofrece varias capas de caché que pueden combinarse para obtener el mejor equilibrio entre rendimiento y frescura de datos. Este capítulo profundiza en cómo diseñar una estrategia de caché efectiva.
1. Capas de caché (repaso ampliado)
Router Cache (cliente)

    Almacena en memoria el payload de React Server Components durante la navegación.

    Duración: 30 segundos en producción (configurable experimentalmente), o hasta que se recargue la página.

    Propósito: navegación instantánea entre páginas ya visitadas.

    Invalidación: al hacer un hard refresh, al pasar el tiempo stale, o cuando se ejecutan mutaciones (revalidaciones bajo demanda pueden limpiarlo).

### Full Route Cache (servidor)

    Almacena en el servidor (disco, memoria o CDN) el HTML y RSC payload de rutas estáticas.

    Se genera en build o en ISR. Persiste hasta que se revalida o se redespiga.

    Controlado por dynamic (si es force-static o force-dynamic) y revalidaciones.

### Data Cache (fetch)

    Caché persistente (incluso entre despliegues) para respuestas de fetch.

    Clave compuesta por URL + opciones. Tamaño ilimitado pero con límites de plataforma (en Vercel hasta 2 MB por entrada).

### Image Cache

    Caché de imágenes optimizadas por next/image.

2. Estrategias según el tipo de datos
Contenido público raramente cambiante (ej. páginas de "Acerca de")

    Estrategia: SSG completo (estático en build) + opcional ISR con revalidate: 86400 (1 día) para actualizaciones programadas.

    Cache: Full Route Cache almacenado en CDN; nunca se recalcula en petición.

    Invalidación: solo al redeploy o al recibir un webhook que llame revalidatePath.

### Contenido público con cambios cada pocos minutos (ej. listado de noticias)

    Estrategia: ISR con revalidate bajo (60-300 segundos).

    Cache: Data Cache guarda respuestas de fetch por ese periodo; Full Route Cache se revalida en background.

    Invalidación: automática por tiempo. Opcionalmente, revalidación bajo demanda cuando se publica una noticia urgente.

### Contenido personalizado por usuario (ej. dashboard)

    Estrategia: SSR (páginas dinámicas) sin caché de HTML, pero puedes cachear llamadas a APIs comunes con fetch + cache: 'force-cache' y tags, revalidándolas cuando cambien los datos del usuario.

    Cache: Data Cache para datos comunes entre usuarios; la página se renderiza en cada solicitud pero con algunos datos cacheados.

### Datos específicos del usuario, alta frecuencia de cambio (ej. precios en vivo)

    Estrategia: Cliente-side fetching (SWR/React Query) con polling o websockets. La página se entrega estática (shell) y los datos dinámicos se cargan en cliente.

3. Técnicas avanzadas de invalidación
Invalidación granular con tags

Etiqueta cada fetch con un tag único o compartido.
```tsx
// Página de lista
const posts = await fetch('.../posts', { next: { tags: ['posts'] } })

// Página de un post
const post = await fetch(`.../posts/${id}`, { next: { tags: [`post-${id}`, 'posts'] } })
```

Luego:

    revalidateTag('posts') actualiza todas las consultas etiquetadas como 'posts'.

    revalidatePath('/blog') actualiza además la ruta completa en el Full Route Cache.

### Revalidación bajo demanda con Server Actions
```tsx
// actions.ts
'use server'
import { revalidateTag } from 'next/cache'

export async function actualizarPost(data) {
  await saveToDB(data)
  revalidateTag('posts')
  revalidateTag(`post-${data.id}`)
}
```

### Invalidación del Router Cache del cliente

Cuando realizas una mutación, puedes forzar que el cliente refresque su caché de navegación llamando a router.refresh() en un Client Component. Esto recupera nuevos datos del servidor para la ruta actual sin recargar la página.
```tsx
import { useRouter } from 'next/navigation'
const router = useRouter()
router.refresh()
```

### 4. Configuración de tiempos de stale

    Data Cache: controlado por revalidate en fetch o por segmento.

    Full Route Cache: se limpia cuando expira el revalidate o se llama a revalidatePath/revalidateTag.

    Router Cache: en Next.js 15 se permite ajustar el tiempo de stale mediante staleTimes en next.config.js.

```js
module.exports = {
  experimental: {
    staleTimes: {
      dynamic: 30,  // segundos para rutas dinámicas
      static: 300,  // segundos para rutas estáticas
    },
  },
}
```

### 5. Entendiendo el flujo de una solicitud con ISR

    El cliente pide /productos.

    Next.js busca en la Full Route Cache. Si existe y no ha expirado, la sirve.

    Si ha expirado, sirve la versión stale mientras regenera en background.

    Durante la regeneración, ejecuta los fetch del componente. Si el Data Cache de esos fetch aún es válido, los usa; si no, hace solicitudes reales y actualiza Data Cache.

    El nuevo HTML se almacena en la Full Route Cache y las siguientes solicitudes reciben la versión fresca.

### 6. Caché en desarrollo vs producción

En desarrollo, las cachés están desactivadas para facilitar la iteración. Por eso ves siempre datos frescos. En producción, las cachés están activas según tu configuración.
7. Herramientas de depuración

    La respuesta de Next.js incluye el encabezado X-Nextjs-Cache que puede decir HIT, STALE, MISS, BYPASS. Útil para ver qué cache se usó.

    Puedes inspeccionar el build output para ver qué rutas son estáticas ○ o dinámicas λ.

    En Vercel, tienes logs de revalidación.

Una estrategia de caché bien pensada permite que tu aplicación escale sin perder frescura de datos.
---

## Archivo: `05-optimizacion/turbopack.md`

Turbopack: el empaquetador de nueva generación para Next.js

Turbopack es el nuevo empaquetador de desarrollo para Next.js, escrito en Rust por el equipo de Vercel. Sustituye de forma incremental a Webpack, ofreciendo un rendimiento de recarga en caliente (HMR) hasta 10 veces más rápido en proyectos grandes.
¿Por qué Turbopack?

Webpack, aunque potente, tiene un cuello de botella inherente al estar escrito en JavaScript y realizar mucho trabajo de serialización de módulos. Turbopack se diseñó desde cero en Rust, aprovechando el paralelismo y la compilación nativa.

Beneficios principales:

    Arranque casi instantáneo: compila solo los módulos necesarios bajo demanda.

    HMR ultrarrápido: los cambios se reflejan en milisegundos, incluso en proyectos con miles de componentes.

    Arquitectura de caché granular: comparte caché entre builds y sesiones, evitando recompilar código que no ha cambiado.

    Integración nativa con React Server Components y streaming.

### Estado actual

Desde Next.js 14, Turbopack es la opción por defecto para desarrollo si se usa create-next-app con App Router. Aún no está disponible para producción (next build) de forma estable (aunque hay avances en esa dirección). Se espera que reemplace completamente a Webpack en el futuro.
Habilitar Turbopack

En un proyecto existente, lanza el servidor de desarrollo con el flag --turbo:
```bash
next dev --turbo
```

Para configurarlo permanentemente, en next.config.js:
```js
module.exports = {
  experimental: {
    turbo: {
      // Configuración avanzada (opcional)
    },
  },
}
```

La mayoría de los proyectos no necesitan ninguna configuración adicional.
Migración desde Webpack

La gran mayoría de las configuraciones de Webpack no se aplican en Turbopack. Si tu proyecto usa plugins personalizados de Webpack, puede que no funcione con --turbo. La buena noticia es que, para la mayoría de los casos, Turbopack ya incluye soporte nativo para CSS, SASS, imágenes, etc.

Limitaciones conocidas (a principios de 2025):

    No todos los loaders de Webpack tienen equivalente en Turbopack (aunque los más comunes están soportados).

    Algunas configuraciones avanzadas de next.config.js como webpack personalizado no tienen efecto.

    El proceso de build (next build) aún usa Webpack por defecto, pero puedes forzar Turbopack en builds experimentales (con next build --turbo a partir de Next.js 15, sujeto a cambios).

### Arquitectura interna

Turbopack funciona con una gráfica de dependencias computada de forma perezosa. Cuando editas un archivo, solo se recompila ese nodo y sus dependencias directas, manteniendo el resto cacheado. Utiliza la misma resolución de módulos que Node.js, asegurando compatibilidad.
Rendimiento en la práctica

Pruebas con aplicaciones grandes muestran que Turbopack reduce el tiempo de HMR de varios segundos a menos de 100 ms. Esto transforma la experiencia de desarrollo, eliminando la espera.
Integración con Turborepo

Turbopack se complementa con Turborepo, el sistema de monorepo, pero son herramientas distintas. Turbopack es el empaquetador; Turborepo orquesta tareas en múltiples paquetes. Juntos ofrecen un ecosistema de alto rendimiento.
¿Deberías usarlo hoy?

Si estás comenzando un proyecto nuevo con Next.js 14+ y no tienes configuraciones avanzadas de Webpack, Turbopack es altamente recomendado para desarrollo. Si tu proyecto tiene modificaciones complejas de Webpack, prueba --turbo y evalúa si todo funciona; en caso contrario, sigue con Webpack hasta que Turbopack madure en producción.
El futuro

Vercel apuesta fuerte por Turbopack como el empaquetador oficial para Next.js tanto en desarrollo como en producción. Se prevé que alcance paridad total con Webpack en las próximas versiones.

Resumen: Turbopack es la mayor innovación en la experiencia de desarrollo de Next.js, eliminando los tiempos de espera y permitiendo un flujo de trabajo casi instantáneo.

---

## Archivo: `06-seo-y-metadata/seo-en-pages-head.md`

SEO con <Head> en Pages Router

En el Pages Router, la gestión de metaetiquetas, títulos y otros elementos del <head> se realiza mediante el componente <Head> proporcionado por next/head. Aunque es sencillo, requiere ciertas prácticas para obtener un SEO sólido.
Uso básico de <Head>

Importa Head desde next/head y añádelo a tu componente de página. Puedes usarlo en cualquier parte del árbol, pero cada página lo define de forma independiente.
```jsx
import Head from 'next/head'

export default function Inicio() {
  return (
    <>
      <Head>
        <title>Mi Sitio - Inicio</title>
        <meta name="description" content="Bienvenido a mi sitio web" />
        <link rel="canonical" href="https://misitio.com" />
        <meta property="og:title" content="Mi Sitio" />
        <meta property="og:description" content="Bienvenido a mi sitio web" />
        <meta property="og:image" content="https://misitio.com/og-image.jpg" />
        <meta name="twitter:card" content="summary_large_image" />
      </Head>
      <main>Contenido...</main>
    </>
  )
}
```

### Fusión de múltiples Head

Si tienes un Head en _app.js y otro en una página, Next.js fusiona el contenido. Las claves duplicadas (por ejemplo, title) serán sobrescritas por la última definición encontrada durante el renderizado (normalmente la de la página). Esto te permite tener valores por defecto en _app.js y sobreescribirlos en páginas específicas.

_app.js:
```jsx
import Head from 'next/head'

export default function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>Mi Proyecto</title>
        <meta name="description" content="Descripción global" />
        <meta name="robots" content="index, follow" />
      </Head>
      <Component {...pageProps} />
    </>
  )
}
```

Luego, en pages/productos.js:
```jsx
import Head from 'next/head'

export default function Productos() {
  return (
    <>
      <Head>
        <title>Productos - Mi Proyecto</title>
        <meta name="description" content="Lista de todos nuestros productos" />
      </Head>
      <h1>Productos</h1>
    </>
  )
}
```

El resultado será: title "Productos - Mi Proyecto", description "Lista de todos nuestros productos", y robots "index, follow" (heredado de _app).
Etiquetas esenciales para SEO

Además del title, las metaetiquetas más importantes son:

    description: texto que aparece en los resultados de búsqueda.

    robots: controla la indexación (index, follow o noindex, nofollow).

    canonical: evita contenido duplicado indicando la URL preferida.

    Open Graph (og:*): para compartir en redes sociales (Facebook, WhatsApp).

    Twitter Cards (twitter:*): para una buena presentación en Twitter/X.

    viewport: aunque Next.js lo incluye automáticamente, puedes ajustarlo.

    charset: se incluye por defecto, no necesitas definirlo.

### Contenido dinámico

Cuando los datos de la página vienen de getServerSideProps o getStaticProps, puedes usar esos datos para llenar las metaetiquetas.
```jsx
export default function Articulo({ articulo }) {
  return (
    <>
      <Head>
        <title>{articulo.titulo} - Blog</title>
        <meta name="description" content={articulo.extracto} />
        <meta property="og:title" content={articulo.titulo} />
        <meta property="og:image" content={articulo.imagen} />
        <link rel="canonical" href={`https://blog.com/articulo/${articulo.slug}`} />
      </Head>
      <article>...</article>
    </>
  )
}

export async function getServerSideProps({ params }) {
  const articulo = await obtenerArticulo(params.slug)
  return { props: { articulo } }
}
```

### Idioma del documento (lang)

El atributo lang del <html> solo puede definirse en _document.js, no en <Head>. Crea o modifica pages/_document.js:
```jsx
import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="es">
      <Head />
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
```

Esto es fundamental para la accesibilidad y para que los motores de búsqueda entiendan el idioma de la página.
Datos estructurados (JSON-LD)

Puedes incluir datos estructurados directamente en el <head> usando la etiqueta <script>:
```jsx
import Head from 'next/head'

export default function Producto({ producto }) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: producto.nombre,
    description: producto.descripcion,
    image: producto.imagen,
    // ...
  }

  return (
    <>
      <Head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </Head>
      <div>...</div>
    </>
  )
}
```

Recuerda usar dangerouslySetInnerHTML porque estás insertando JavaScript crudo.
Limitaciones de <Head>

    No puedes usarlo en _document.js para metaetiquetas dinámicas (solo define la estructura base).

    Si tienes layouts manuales, no hay un equivalente a los layouts persistentes del App Router, por lo que debes repetir metaetiquetas comunes en cada página o usar un componente envolvente que las incluya.

    No hay una API declarativa; mezcla lógica de UI con SEO.

### Buenas prácticas

    Establece un title y description único en cada página.

    Siempre define og:image con dimensiones 1200x630 píxeles para una buena previsualización social.

    Usa canonical para evitar contenido duplicado, sobre todo si usas parámetros de seguimiento.

    Mantén robots adecuado (por ejemplo, noindex en páginas de administración).

    Genera un sitemap.xml y robots.txt (puedes colocarlos en la carpeta public/ o generarlos dinámicamente con una API route).

Con estas técnicas, el Pages Router proporciona una base de SEO sólida, aunque requiere mayor atención manual que el App Router.
---

## Archivo: `06-seo-y-metadata/metadata-api-app.md`

API de Metadata en App Router

El App Router revoluciona la gestión de SEO y metaetiquetas mediante una API de Metadata declarativa. En lugar de un componente <Head>, exportas un objeto metadata o una función generateMetadata desde layout.js o page.js. Next.js se encarga de inyectarlo automáticamente en el <head> del HTML.
Metadata estática

Para datos fijos, exporta un objeto llamado metadata:
```tsx
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Mi Aplicación',
  description: 'Descripción global del sitio',
  keywords: ['next.js', 'react', 'seo'],
  robots: {
    index: true,
    follow: true,
  },
  openGraph: {
    title: 'Mi Aplicación',
    description: 'Descripción para redes sociales',
    url: 'https://misitio.com',
    siteName: 'Mi Sitio',
    images: [
      {
        url: 'https://misitio.com/og-image.jpg',
        width: 1200,
        height: 630,
      },
    ],
    locale: 'es_ES',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Mi Aplicación',
    description: 'Descripción para Twitter',
    images: ['https://misitio.com/twitter-image.jpg'],
  },
}

export default function RootLayout({ children }) {
  return <html lang="es">{children}</html>
}
```

No necesitas importar nada; solo exportar metadata. Next.js lo serializa en el <head> automáticamente.
Metadata dinámica con generateMetadata

Cuando los valores dependen de datos de la ruta (por ejemplo, un artículo de blog), exportas una función asíncrona generateMetadata en lugar del objeto estático. Esta función recibe los mismos parámetros que la página: params, searchParams.
```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'
import { obtenerArticulo } from '@/lib/blog'

type Props = {
  params: { slug: string }
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const articulo = await obtenerArticulo(params.slug)

  return {
    title: articulo.titulo,
    description: articulo.extracto,
    openGraph: {
      title: articulo.titulo,
      description: articulo.extracto,
      images: [articulo.imagen],
    },
  }
}

export default async function ArticuloPage({ params }: Props) {
  const articulo = await obtenerArticulo(params.slug)
  return <article>...</article>
}
```

generateMetadata se ejecuta en el servidor, por lo que puedes hacer fetch, leer archivos o consultar bases de datos. Además, Next.js deduplica los fetch realizados tanto en generateMetadata como en el componente de página, si son idénticos.
Herencia y fusión de metadatos

Los metadatos se heredan desde los layouts superiores hacia las páginas. Next.js los fusiona siguiendo estas reglas:

    Los campos simples (title, description) en una página sobrescriben completamente los del layout.

    Los campos anidados (openGraph, twitter) se fusionan profundamente, combinando las propiedades.

    El title en layouts puede usar la plantilla %s para que las páginas añadan un sufijo automáticamente.

Ejemplo con plantilla de título:

En app/layout.tsx:
```tsx
export const metadata: Metadata = {
  title: {
    template: '%s - Mi Blog',
    default: 'Mi Blog',   // usado si la página no define title
  },
}
```

En app/blog/[slug]/page.tsx:
```tsx
export async function generateMetadata({ params }) {
  const articulo = await obtenerArticulo(params.slug)
  return {
    title: articulo.titulo, // se reemplaza en la plantilla -> "Título - Mi Blog"
  }
}
```

Si una página no exporta title, se usará 'Mi Blog' (el default).
Metadatos basados en archivos

Además de exportar objetos, puedes añadir archivos especiales en las carpetas de app/ que Next.js convierte en recursos del <head>:

    favicon.ico – icono del sitio.

    icon.png, icon.jpg – íconos en formatos alternativos.

    apple-icon.png – icono para iOs.

    opengraph-image.png, opengraph-image.jpg – imagen Open Graph por defecto para esa ruta.

    twitter-image.png – imagen para Twitter Card.

    sitemap.xml – sitemap generado automáticamente (si no existe, Next.js puede generarlo dinámicamente con una función sitemap.ts).

    robots.txt – reglas de robots (también puede generarse con robots.ts).

### Ejemplo: opengraph-image.tsx dinámico
```tsx
// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og'

export const runtime = 'edge'
export const alt = 'Mi artículo'
export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default async function Image({ params }: { params: { slug: string } }) {
  const articulo = await obtenerArticulo(params.slug)
  return new ImageResponse(
    (
      <div style={{ background: 'white', ... }}>{articulo.titulo}</div>
    ),
    { width: 1200, height: 630 }
  )
}
```

Así generas imágenes OG dinámicas sin depender de un CDN de imágenes.
generateViewport y otros metadatos especiales

Además de metadata, puedes exportar generateViewport para controlar las etiquetas de viewport, theme-color, etc. Es similar a metadatos pero separado para no mezclar propiedades.
```tsx
export const viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: '#ffffff',
}
```

### Datos estructurados (JSON-LD) dinámicos

Puedes incluirlos dentro del head usando la misma API de Metadata o insertándolos manualmente en el layout como <script>. Por ejemplo, en un Server Component:
```tsx
export default async function ProductPage({ params }: { params: { id: string } }) {
  const producto = await getProduct(params.id)
  const jsonLd = { ... }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div>...</div>
    </>
  )
}
```

### Comparación con <Head> del Pages Router
Característica	Pages Router	App Router
Definición	Componente <Head>	Exportación metadata / generateMetadata
Herencia	Manual (fusor de etiquetas)	Automática, jerárquica
Datos dinámicos	Tienes que pasar props al Head	generateMetadata asíncrono
Imágenes OG	Manual (URL)	Archivos dedicados, generación dinámica con ImageResponse
Rendimiento	El componente <Head> se envía en el bundle del cliente (hidratación)	Los metadatos se inyectan en el servidor, sin JS extra
Archivos especiales (favicon, etc.)	Carpeta public/	Pueden vivir en cualquier ruta de app/

La API de Metadata del App Router es más potente, segura y fácil de mantener en aplicaciones con muchas páginas.
---

## Archivo: `07-autenticacion/patrones-pages-router.md`

Patrones de autenticación en Pages Router

En el Pages Router, la autenticación suele implementarse combinando obtención de datos del lado del servidor (getServerSideProps) con API Routes para manejar el inicio/cierre de sesión, y cookies httpOnly para almacenar tokens de sesión de forma segura. A continuación, los patrones más comunes.
Autenticación basada en sesión con cookies httpOnly

Este enfoque usa cookies para almacenar un token de sesión o un JWT de forma que no sea accesible desde JavaScript (previene XSS). El flujo:

    El usuario envía credenciales a una API route (/api/login).

    El servidor valida, crea una sesión y establece una cookie httpOnly con un token.

    Las páginas protegidas verifican la cookie en getServerSideProps y redirigen si no es válida.

    Para cerrar sesión, otra API route elimina la cookie.

### API de login: pages/api/login.js
```js
import { serialize } from 'cookie'
import { signToken } from '../../../lib/jwt'

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end()

  const { email, password } = req.body
  const user = await validateUser(email, password)
  if (!user) return res.status(401).json({ error: 'Credenciales inválidas' })

  const token = await signToken(user)
  res.setHeader('Set-Cookie', serialize('token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    maxAge: 60 * 60 * 24, // 1 día
  }))

  res.status(200).json({ ok: true })
}
```

Protección de páginas:
```jsx
// pages/dashboard.js
import { verifyToken } from '../lib/jwt'

export default function Dashboard({ usuario }) {
  return <div>Bienvenido {usuario.nombre}</div>
}

export async function getServerSideProps({ req }) {
  const token = req.cookies.token
  if (!token) {
    return { redirect: { destination: '/login', permanent: false } }
  }

  try {
    const usuario = await verifyToken(token)
    return { props: { usuario } }
  } catch {
    return { redirect: { destination: '/login', permanent: false } }
  }
}
```

Puedes envolver esta lógica en un helper reutilizable (withAuth) para no repetirla en cada página.

### API de logout: pages/api/logout.js
```js
import { serialize } from 'cookie'

export default function handler(req, res) {
  res.setHeader('Set-Cookie', serialize('token', '', {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    expires: new Date(0),
  }))
  res.redirect('/')
}
```

### Autenticación con NextAuth.js (v4) en Pages Router

NextAuth.js (o Auth.js) simplifica la autenticación con proveedores OAuth, credenciales y más. En Pages Router, se configura un archivo [...nextauth].js dentro de pages/api/auth/.

Instalación y configuración:
```bash
npm install next-auth
```

pages/api/auth/[...nextauth].js:
```js
import NextAuth from 'next-auth'
import GithubProvider from 'next-auth/providers/github'
import CredentialsProvider from 'next-auth/providers/credentials'

export default NextAuth({
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_CLIENT_ID,
      clientSecret: process.env.GITHUB_CLIENT_SECRET,
    }),
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        // lógica contra BD
        const user = await findUser(credentials.email, credentials.password)
        if (user) return user
        return null
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) token.role = user.role
      return token
    },
    async session({ session, token }) {
      session.user.role = token.role
      return session
    }
  },
  pages: {
    signIn: '/auth/login',   // página personalizada
  },
  secret: process.env.NEXTAUTH_SECRET,
})
```

Proteger páginas:

Usa getServerSession en getServerSideProps:
```jsx
import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'

export default function Dashboard({ session }) { ... }

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  if (!session) {
    return { redirect: { destination: '/api/auth/signin', permanent: false } }
  }
  return { props: { session } }
}
```

Cliente: el SessionProvider envuelve la aplicación en _app.js para usar el hook useSession en componentes cliente.
```jsx
// pages/_app.js
import { SessionProvider } from 'next-auth/react'

export default function App({ Component, pageProps: { session, ...pageProps } }) {
  return (
    <SessionProvider session={session}>
      <Component {...pageProps} />
    </SessionProvider>
  )
}
```

### Roles y protección por roles

Extiende la lógica de redirección según roles. Puedes crear un HOC que envuelva páginas y verifique el rol.
```js
export function withRole(Component, role) {
  return function Authenticated(props) {
    const { data: session } = useSession()
    if (session?.user?.role !== role) return <p>Acceso denegado</p>
    return <Component {...props} />
  }
}
```

En getServerSideProps también puedes redirigir si el token decodificado no tiene el rol esperado.
Consideraciones

    Las cookies httpOnly requieren HTTPS en producción (secure: true).

    Para APIs externas desde el servidor, pasa el token como cabecera Authorization usando req dentro de getServerSideProps.

    No guardes información sensible en props que se serializan al cliente; mejor envía solo lo necesario.

    Con NextAuth, la sesión se almacena en una cookie JWT por defecto, lo que la hace stateless; si necesitas almacenar en BD, configura un adaptador.

El Pages Router te obliga a implementar la protección “a mano” en cada página, pero con helpers y NextAuth es un proceso limpio y flexible.
---

## Archivo: `07-autenticacion/nextauth-app-router.md`

Autenticación con NextAuth.js (Auth.js) en App Router

En el App Router, NextAuth.js (actualmente en su versión 5, llamada Auth.js) se integra de forma nativa mediante Server Components, Server Actions y middleware. Su configuración es más modular y se beneficia de la nueva arquitectura.
Instalación y configuración
```bash
npm install next-auth@beta
```

Crea un archivo auth.ts (o .js) en la raíz de src o en una carpeta lib/. Allí defines tu configuración y exportas las funciones auth, signIn, signOut, y los handlers.
```ts
// auth.ts
import NextAuth from 'next-auth'
import GitHub from 'next-auth/providers/github'
import Credentials from 'next-auth/providers/credentials'

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID,
      clientSecret: process.env.GITHUB_CLIENT_SECRET,
    }),
    Credentials({
      credentials: {
        email: {},
        password: {},
      },
      authorize: async (credentials) => {
        const user = await validarCredenciales(credentials)
        return user ?? null
      },
    }),
  ],
  callbacks: {
    jwt({ token, user }) {
      if (user) token.role = user.role
      return token
    },
    session({ session, token }) {
      session.user.role = token.role
      return session
    },
  },
  pages: {
    signIn: '/login',
  },
})
```

Los handlers son las funciones que manejan las rutas de API de NextAuth. Ahora debemos exponerlos mediante un Route Handler en app/api/auth/[...nextauth]/route.ts:
```ts
import { handlers } from '@/auth'

export const { GET, POST } = handlers
```

Listo. Ya tienes la autenticación lista para usar en el App Router.
Obtener la sesión en Server Components

Usa la función auth exportada para obtener la sesión en cualquier Server Component:
```tsx
// app/dashboard/page.tsx
import { auth } from '@/auth'
import { redirect } from 'next/navigation'

export default async function Dashboard() {
  const session = await auth()
  if (!session) redirect('/api/auth/signin')

  return <div>Bienvenido {session.user?.name}</div>
}
```

La sesión se obtiene de las cookies automáticamente, sin necesidad de pasar el request manualmente.
Proteger rutas con middleware

El middleware es la forma más eficiente de proteger múltiples rutas sin repetir código. Crea middleware.ts en la raíz del proyecto:
```ts
// middleware.ts
import { auth } from '@/auth'
import { NextResponse } from 'next/server'

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isOnDashboard = req.nextUrl.pathname.startsWith('/dashboard')

  if (isOnDashboard && !isLoggedIn) {
    return NextResponse.redirect(new URL('/login', req.url))
  }
  return NextResponse.next()
})

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*'],
}
```

Al exportar auth como middleware, NextAuth maneja automáticamente la verificación de sesión y la añade a req.auth. Puedes también usar la función auth simple y envolver lógica personalizada.
Uso en Client Components

Para componentes interactivos, necesitas el contexto de sesión en el cliente. Proporciona un SessionProvider (aún de next-auth/react) en un layout o provider:
```tsx
// app/layout.tsx
import { SessionProvider } from 'next-auth/react'
import { auth } from '@/auth'

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const session = await auth()

  return (
    <html lang="es">
      <body>
        <SessionProvider session={session}>
          {children}
        </SessionProvider>
      </body>
    </html>
  )
}
```

Luego, en cualquier Client Component:
```tsx
'use client'
import { useSession } from 'next-auth/react'

export default function UserStatus() {
  const { data: session } = useSession()
  if (session) return <p>Conectado como {session.user?.email}</p>
  return <p>No has iniciado sesión</p>
}
```

### Inicio y cierre de sesión desde el cliente

Usa las funciones signIn y signOut desde next-auth/react:
```tsx
import { signIn, signOut } from 'next-auth/react'
```

### <button onClick={() => signIn()}>Iniciar sesión</button>
<button onClick={() => signOut()}>Cerrar sesión</button>

### Credenciales personalizadas y validación avanzada

Con el proveedor Credentials, puedes manejar completamente la lógica de login. El callback authorize debe retornar un objeto usuario o null. Puedes almacenar el token en una base de datos si usas un adaptador, o confiar en JWT (por defecto).
Adaptadores y base de datos

Si necesitas guardar usuarios, cuentas y sesiones en BD, instala un adaptador (ej. @auth/prisma-adapter). Configúralo en auth.ts:
```ts
import { PrismaAdapter } from '@auth/prisma-adapter'
import prisma from '@/lib/prisma'

export const { handlers, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [...],
})
```

Con adaptador, las sesiones se almacenan en BD y el JWT solo se usa para el token de sesión; el tamaño de la cookie se reduce.
Compatibilidad con Edge Runtime

Las funciones auth y los handlers funcionan completamente en el Edge Runtime si se configuran adecuadamente (sin dependencias pesadas de Node). Puedes forzar el runtime edge en los Route Handlers:
```ts
// route.ts
export const runtime = 'edge'
export const { GET, POST } = handlers
```

Sin embargo, si tu adaptador o base de datos requiere Node, deberás mantenerlos en Node.js.
Consideraciones de seguridad

    Las cookies de sesión son httpOnly y secure en producción automáticamente.

    Utiliza NEXTAUTH_SECRET en variables de entorno.

    Para rutas API que necesitan sesión, usa auth() en Route Handlers:

```ts
import { auth } from '@/auth'
import { NextResponse } from 'next/server'

export async function GET() {
  const session = await auth()
  if (!session) return NextResponse.json({ error: 'No autorizado' }, { status: 401 })
  // ...
}
```

NextAuth v5 (Auth.js) está optimizado para App Router, reduciendo el boilerplate y aprovechando al máximo los Server Components.
---

## Archivo: `07-autenticacion/middleware.md`

Middleware en Next.js para autenticación

El middleware de Next.js se ejecuta antes de que una solicitud se complete, permitiendo interceptar peticiones, modificar cabeceras, redirigir o verificar autenticación. Corre en el Edge Runtime, por lo que debe ser ligero y no puede usar APIs específicas de Node.js.
Conceptos básicos

    Archivo middleware.ts (o .js) en la raíz del proyecto (al mismo nivel que app/ o pages/).

    Exporta una función middleware que recibe un objeto NextRequest y retorna una NextResponse.

    Se aplica a todas las rutas, pero puedes restringir con un config.matcher.

### Ejemplo mínimo: redirección por autenticación
```ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(req: NextRequest) {
  const token = req.cookies.get('token')
  const isAuthPage = req.nextUrl.pathname.startsWith('/login')

  if (!token && !isAuthPage) {
    return NextResponse.redirect(new URL('/login', req.url))
  }
  if (token && isAuthPage) {
    return NextResponse.redirect(new URL('/dashboard', req.url))
  }
  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login'],
}
```

    Si no hay cookie token y la ruta es protegida, redirige a /login.

    Si ya hay token y está en /login, redirige al dashboard.

    matcher evita que el middleware se ejecute en rutas innecesarias.

### Middleware con NextAuth v5

NextAuth proporciona un helper para integrar su lógica de sesión en el middleware. Puedes envolver tu propio middleware con auth() o usar auth como middleware directamente.

### Opción 1: middleware de NextAuth simple
```ts
// middleware.ts
import { auth } from '@/auth'

export default auth((req) => {
  // req.auth contiene la sesión (null si no autenticado)
  if (!req.auth && req.nextUrl.pathname.startsWith('/dashboard')) {
    return Response.redirect(new URL('/login', req.url))
  }
})

export const config = { matcher: ['/dashboard/:path*'] }
```

Al exportar auth, NextAuth automáticamente maneja la verificación de sesión y la añade al request.

### Opción 2: lógica personalizada combinada
```ts
import { auth } from '@/auth'
import { NextResponse } from 'next/server'

export default auth((req) => {
  const logged = !!req.auth
  const isAdmin = req.auth?.user?.role === 'admin'
  const path = req.nextUrl.pathname

  if (path.startsWith('/admin') && !isAdmin) {
    return NextResponse.redirect(new URL('/403', req.url))
  }
  if (path.startsWith('/dashboard') && !logged) {
    return NextResponse.redirect(new URL('/login', req.url))
  }
  return NextResponse.next()
})

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*'],
}
```

### Acceso a cookies, headers y geolocalización

El middleware tiene acceso a:

    req.cookies: cookies como objeto iterable.

    req.headers: cabeceras de la solicitud.

    req.geo (solo en Vercel, Edge): información geográfica (país, ciudad, etc.).

    req.nextUrl: objeto URL con información de la ruta.

Ejemplo de bloqueo por país:
```ts
export function middleware(req: NextRequest) {
  const country = req.geo?.country || 'US'
  if (country === 'XX') {
    return new Response('No disponible en tu región', { status: 403 })
  }
}
```

### Limitaciones del Edge Runtime

    No puedes usar módulos nativos de Node.js (fs, path, etc.) ni muchas librerías que dependan de Node.

    Solo puedes importar módulos que funcionen en Edge (o que estén marcados como edge compatibles). Por suerte, las funciones auth de NextAuth y las de next/server sí lo están.

    El middleware se ejecuta en cada solicitud, por lo que debe ser rápido; evita hacer fetch pesados.

    No tienes acceso al req.body porque el cuerpo puede no estar disponible antes de la ejecución (el middleware ocurre antes del parseo del body). Para validar cuerpos debes usar Route Handlers o Server Actions.

### Redirecciones y reescrituras

Puedes usar NextResponse.redirect(url, status) o NextResponse.rewrite(destination). La reescritura es interna, el cliente no ve el cambio de URL.
```ts
// Reescribe todas las solicitudes de /pro a /promociones
if (req.nextUrl.pathname.startsWith('/pro')) {
  return NextResponse.rewrite(new URL('/promociones', req.url))
}
```

### Evitar bucles de redirección

Al redirigir, asegúrate de no crear un bucle. Por ejemplo, no redirijas a /login si ya estás en /login. Siempre verifica la URL actual.
Combinación con internacionalización

Si usas next-intl u otra solución de i18n, el middleware debe combinarse con la lógica de idiomas. Puedes encadenar middlewares o integrar la verificación de sesión dentro del middleware de i18n.
Rendimiento y buenas prácticas

    Define un matcher lo más restrictivo posible para que el middleware solo se ejecute en las rutas necesarias.

    Evita usar * que abarque todo; prefiere patrones como ['/app/:path*', '/api/auth/:path*'].

    El middleware no debe bloquear la respuesta; siempre devuelve una NextResponse sin demora.

### Middleware para APIs (Route Handlers)

El middleware también se ejecuta en las API routes del App Router. Puedes protegerlas de la misma manera:
```ts
if (req.nextUrl.pathname.startsWith('/api/admin') && !req.auth?.user?.isAdmin) {
  return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
}
```

El middleware de autenticación es una herramienta central en el App Router para garantizar la seguridad sin tocar cada página o endpoint individualmente.

---

## Archivo: `08-internacionalizacion/i18n-pages-router.md`

Internacionalización (i18n) en Pages Router

El Pages Router ofrece soporte de internacionalización nativo desde Next.js 10. No requiere librerías externas para el enrutamiento, aunque las traducciones siguen dependiendo de soluciones como next-i18next, next-translate o react-intl.
Configuración en next.config.js

La clave es la propiedad i18n. Define los idiomas soportados y el idioma por defecto:
```js
// next.config.js
module.exports = {
  i18n: {
    locales: ['es', 'en', 'fr'],
    defaultLocale: 'es',
    // localeDetection: true, // por defecto true
  },
}
```

Con esto Next.js automáticamente:

    Crea rutas con prefijo de idioma (/es, /en, /fr).

    La raíz / redirige al idioma por defecto (/es).

    Detecta el idioma del navegador mediante la cabecera Accept-Language (si localeDetection: true) y redirige en la primera visita.

### Tipos de enrutamiento

Sub-ruta (predeterminado):
https://misitio.com/es/sobre-nosotros
https://misitio.com/en/about

Dominio: puedes asignar un dominio distinto a cada idioma:
```js
i18n: {
  locales: ['es', 'en'],
  defaultLocale: 'es',
  domains: [
    { domain: 'misitio.es', defaultLocale: 'es' },
    { domain: 'misitio.com', defaultLocale: 'en' },
  ],
}
```

Requiere que ambos dominios apunten al mismo servidor y certificados SSL configurados.
Acceso al idioma en la página

El objeto context de getStaticProps, getServerSideProps y getStaticPaths incluye las propiedades locale, locales y defaultLocale.

En getStaticProps:
```js
export async function getStaticProps({ locale }) {
  // Cargar contenido según locale
  const contenido = await cargarContenido(locale)
  return { props: { contenido } }
}
```

En el componente: usa el hook useRouter para acceder al idioma actual.
```jsx
import { useRouter } from 'next/router'

export default function Pagina() {
  const router = useRouter()
  const { locale, locales, defaultLocale } = router

  return <p>Idioma actual: {locale}</p>
}
```

### Navegación con Link y router

El componente Link y el router manejan automáticamente el prefijo de idioma basado en el locale actual.
```jsx
<Link href="/about">
  <a>Acerca de</a>
</Link>
// Renderiza <a href="/es/about"> (si locale es 'es')

// Cambiar de idioma explícitamente:
<Link href="/about" locale="en">
  <a>English</a>
</Link>
```

Con useRouter:
```js
router.push('/about', undefined, { locale: 'en' })
```

### Rutas dinámicas e i18n

Las rutas dinámicas también obtienen el locale en getStaticPaths. Puedes generar rutas para cada idioma:
```js
export async function getStaticPaths({ locales }) {
  let paths = []
  for (const locale of locales) {
    const posts = await obtenerPosts(locale)
    paths = paths.concat(posts.map(post => ({
      params: { slug: post.slug },
      locale,           // importante
    })))
  }
  return { paths, fallback: false }
}
```

Para cada post obtienes su slug en el idioma correspondiente.
Traducciones con librerías externas

El enrutamiento i18n de Next.js no incluye traducciones. Necesitas una librería. Las más populares:

    next-i18next: basada en i18next, carga archivos JSON por idioma.

    next-translate: minimalista, usa archivos JSON en locales/[lang]/....

    react-intl / Format.js: más completo para aplicaciones complejas.

Ejemplo con next-translate:

Configura i18n.js (o en next.config.js) y estructura de archivos:
```text
locales/
  es/
    common.json
  en/
    common.json
```

Usa el hook useTranslate:
```jsx
import useTranslation from 'next-translate/useTranslation'

export default function Home() {
  const { t, lang } = useTranslation('common')
  return <h1>{t('title')}</h1>
}
```

### Cambio de idioma sin navegación

Si solo necesitas cambiar las traducciones sin cambiar la URL, puedes usar el hook y un estado local, pero para SEO es mejor cambiar la ruta.
Consideraciones

    Con SSR (getServerSideProps) y locales, la URL siempre tiene prefijo. El lenguaje lo obtienes del contexto.

    Si necesitas evitar el prefijo para el idioma por defecto (que / sirva es), Next.js no lo permite para el Pages Router; siempre hay prefijo. Muchos optan por redirecciones personalizadas.

    Los archivos _document.js y _app.js también pueden acceder al locale.

El soporte nativo de i18n en Pages Router simplifica drásticamente el enrutamiento multilingüe, pero ha sido relegado en el App Router a soluciones externas.
---

## Archivo: `08-internacionalizacion/i18n-app-router.md`

Internacionalización (i18n) en App Router

En el App Router, Next.js no incluye el enrutamiento i18n incorporado que existía en el Pages Router. En su lugar, se recomienda implementar i18n con middleware y una carpeta dinámica [locale] en el sistema de archivos, junto con librerías como next-intl o next-i18next (en su versión para App Router).
Estrategia principal

    Crear una estructura de carpetas con un segmento dinámico para el idioma: app/[locale]/....

    Utilizar un middleware para detectar el idioma del usuario y redirigir a la ruta localizada si es necesario.

    Con la ayuda de next-intl (recomendado), cargar traducciones y ofrecerlas a todo el árbol de componentes mediante Server Components y un Provider para Client Components.

### Configuración con next-intl

Instalación:
```bash
npm install next-intl
```

Estructura de carpetas:
```text
app/
  [locale]/
    layout.tsx
    page.tsx
    ...
  layout.tsx          (opcional, redirige a [locale])
middleware.ts
messages/
  en.json
  es.json
i18n.ts
```

Archivo i18n.ts: configura los locales y las traducciones:
```ts
import { getRequestConfig } from 'next-intl/server'

export default getRequestConfig(async ({ locale }) => ({
  messages: (await import(`./messages/${locale}.json`)).default,
}))
```

La función getRequestConfig devuelve los mensajes según el locale. El locale proviene del segmento dinámico, que es leído por next-intl a través del middleware.

Middleware (middleware.ts):
```ts
import createMiddleware from 'next-intl/middleware'

export default createMiddleware({
  locales: ['es', 'en'],
  defaultLocale: 'es',
  localeDetection: true,
})

export const config = {
  matcher: ['/((?!api|_next|_vercel|.*\\..*).*)'],
}
```

Este middleware:

    Detecta el idioma del navegador (Accept-Language) si no hay un segmento [locale] en la URL.

    Redirige las rutas sin prefijo a la versión localizada (ej. / → /es).

    Inyecta el locale en las peticiones para que next-intl funcione correctamente.

Layout principal app/[locale]/layout.tsx:
```tsx
import { NextIntlClientProvider } from 'next-intl'
import { getMessages } from 'next-intl/server'

export default async function LocaleLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode
  params: { locale: string }
}) {
  const messages = await getMessages()

  return (
    <html lang={locale}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
```

NextIntlClientProvider permite usar traducciones en Client Components.

Página de ejemplo app/[locale]/page.tsx:
```tsx
import { useTranslations } from 'next-intl'
import { getTranslations } from 'next-intl/server'

// Para Server Components:
export default async function HomePage() {
  const t = await getTranslations('Home')
  return <h1>{t('title')}</h1>
}

// O para Client Components:
'use client'
export function ClientComponent() {
  const t = useTranslations('Home')
  return <button>{t('cta')}</button>
}
```

Archivos de traducción JSON:

messages/es.json:
```json
{
  "Home": {
    "title": "Bienvenido",
    "cta": "Haz clic aquí"
  }
}
```

### Generación de metadatos por idioma
```tsx
// app/[locale]/page.tsx
import { getTranslations } from 'next-intl/server'

export async function generateMetadata({ params: { locale } }) {
  const t = await getTranslations({ locale, namespace: 'Metadata' })
  return {
    title: t('title'),
    description: t('description'),
  }
}
```

### Ruta sin prefijo (raíz del sitio)

Puedes crear un app/layout.tsx mínimo que redirija al locale por defecto usando redirect de next/navigation dentro de un Server Component, o simplemente dejar que el middleware lo gestione.
Rutas estáticas con i18n

Si deseas pre-renderizar todas las versiones localizadas para SSG, utiliza generateStaticParams en las páginas dentro de [locale]:
```tsx
// app/[locale]/page.tsx
export async function generateStaticParams() {
  return [{ locale: 'es' }, { locale: 'en' }]
}
```

Para rutas anidadas, como [locale]/blog/[slug], generas los slugs para cada locale.
Alternativas a next-intl

    next-i18next (con adaptador para App Router) funciona de manera similar pero con configuración basada en i18next.

    Implementación manual con accept-language y carga de JSON propia. El middleware puede leer accept-language, establecer una cookie y redirigir a la ruta con prefijo.

### Consideraciones importantes

    Las rutas de API (api/) no deben ser interceptadas por el middleware de i18n; por eso el matcher excluye api.

    Las imágenes, archivos estáticos y recursos deben seguir funcionando sin el prefijo de idioma.

    Si usas next-intl, las Server Actions y los Route Handlers pueden obtener el locale desde las cabeceras o desde cookies().

La internacionalización en App Router requiere más configuración manual que en Pages Router, pero next-intl ofrece una experiencia casi idéntica al soporte nativo, con pleno control sobre el enrutamiento y la carga de traducciones.
---

## Archivo: `09-deploy-y-configuracion/next-config-js.md`

Configuración de next.config.js

next.config.js es el archivo central de configuración de Next.js. Permite personalizar desde el empaquetado hasta el enrutamiento, pasando por optimizaciones avanzadas. Se trata de un módulo Node.js que exporta un objeto o una función.
Estructura básica
```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,       // Modo estricto de React
  swcMinify: true,             // Minificación con SWC (por defecto true)
  // Más opciones...
}
```

### module.exports = nextConfig

### Opciones esenciales
reactStrictMode

Activa el modo estricto de React en desarrollo, ayudando a detectar efectos secundarios inesperados.
images

Configura el componente next/image. Fundamental para imágenes remotas.
```js
images: {
  domains: ['cdn.ejemplo.com'],   // deprecado, mejor usar remotePatterns
  remotePatterns: [
    {
      protocol: 'https',
      hostname: '**.ejemplo.com',
      pathname: '/imagenes/**',
    },
  ],
  formats: ['image/avif', 'image/webp'],
  deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048],
  minimumCacheTTL: 60,
}
```

### i18n (solo Pages Router)

Configura internacionalización. Ver capítulo anterior.
Redirecciones, reescrituras y cabeceras

Redirecciones (redirects): cambian la ruta y el código de estado.
```js
async redirects() {
  return [
    {
      source: '/antigua',
      destination: '/nueva',
      permanent: true,         // 308
    },
  ]
}
```

Reescrituras (rewrites): internamente mapean una URL a otra, el cliente no lo ve.
```js
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: 'https://api.externa.com/:path*',
    },
  ]
}
```

Cabeceras (headers): añaden cabeceras HTTP a rutas concretas.
```js
async headers() {
  return [
    {
      source: '/(.*)',
      headers: [
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'Content-Security-Policy', value: "default-src 'self'" },
      ],
    },
  ]
}
```

Pueden ser funciones asíncronas y pueden consultar una base de datos para generar rutas dinámicamente.
Configuración del compilador
```js
compiler: {
  removeConsole: process.env.NODE_ENV === 'production',
  styledComponents: true,   // soporte nativo para styled-components
  // swcMinify está en la raíz, no aquí
}
```

### Configuración de webpack

Aunque Turbopack es el futuro, todavía puedes extender Webpack:
```js
webpack: (config, { isServer }) => {
  if (!isServer) {
    config.resolve.fallback = { fs: false }
  }
  return config
}
```

### Opciones experimentales

Muchas funcionalidades de Next.js pasan primero por experimental. Algunas relevantes:
```js
experimental: {
  serverActions: true,      // en Next.js 14 ya es estable, no necesario
  turbo: {},                // config para Turbopack
  staleTimes: {
    dynamic: 30,
    static: 300,
  },
  mdxRs: true,              // MDX con Rust
}
```

### Salida y tipo de build

    output: 'standalone': genera una carpeta .next/standalone con todo lo necesario para desplegar en Node.js sin node_modules.

    output: 'export': genera sitio estático puro.

### Configuración como función

Puedes exportar una función para acceso a phase (build, dev) y argumentos por defecto:
```js
module.exports = (phase, { defaultConfig }) => {
  return { ...defaultConfig, /* tus cambios */ }
}
```

### Variables de entorno en next.config.js

next.config.js se ejecuta en tiempo de build y puede acceder a process.env. Para exponer variables al navegador, debes usar la propiedad env o el prefijo NEXT_PUBLIC_ en archivos .env.
```js
module.exports = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.API_URL,
  },
}
```

### Buenas prácticas

    Mantén el archivo limpio; si la configuración crece, separa en módulos.

    Usa comentarios JSDoc @type para intellisense.

    Documenta las redirecciones complejas.

next.config.js es el único punto donde puedes modificar el comportamiento interno del framework, así que vale la pena conocerlo a fondo.
---

## Archivo: `09-deploy-y-configuracion/variables-de-entorno.md`

Variables de entorno en Next.js

Next.js facilita el manejo de variables de entorno mediante archivos .env y una convención de prefijos que define qué se expone al navegador. Un mal manejo puede exponer datos sensibles al cliente, por lo que es crucial entender las reglas.
Archivos .env

Next.js carga automáticamente los siguientes archivos, por orden de prioridad:

### .env (todos los entornos)

### .env.local (local, nunca se sube a git)

### .env.development (solo en next dev)

### .env.production (solo en next build / next start)

### .env.test (solo cuando NODE_ENV === 'test')

Prioridad: las variables definidas en archivos más específicos sobrescriben a las más generales (.env.local gana a .env).
Prefijo NEXT_PUBLIC_

Para que una variable de entorno esté disponible en el navegador (Client Components), debes prefijarla con NEXT_PUBLIC_. En caso contrario, solo estará disponible en el entorno Node.js (Server Components, API Routes, next.config.js).
```text
NEXT_PUBLIC_ANALYTICS_ID=UA-123456    # accesible en cliente
DATABASE_URL=postgres://...           # solo servidor
```

Acceso en cualquier lugar:
```js
console.log(process.env.NEXT_PUBLIC_ANALYTICS_ID)
```

### Uso en Server Components y API Routes

En Server Components, getServerSideProps, getStaticProps, Route Handlers y middleware, puedes acceder a todas las variables sin restricción, siempre que el código se ejecute en el servidor.

En next.config.js, process.env está disponible como en cualquier módulo Node.
Variables en el middleware (Edge Runtime)

El middleware se ejecuta en Edge Runtime. Las variables de entorno se deben definir en el momento del build (o mediante Vercel/plataforma), no se pueden leer dinámicamente de archivos .env. En desarrollo local, las variables del archivo .env sí están disponibles. En producción, asegúrate de configurarlas en el panel de la plataforma.
Exposición al cliente con env en next.config.js

La propiedad env de next.config.js expone variables al cliente en tiempo de build. Es una alternativa al prefijo NEXT_PUBLIC_, pero menos recomendada porque las inyecta directamente en el JavaScript.
```js
module.exports = {
  env: {
    API_URL: process.env.API_URL,  // cuidado: expone al cliente si no filtras
  },
}
```

Si API_URL no tiene NEXT_PUBLIC_, no estará disponible en cliente a menos que uses esta opción (lo que puede ser inseguro). Mejor usa NEXT_PUBLIC_ explícitamente.
Variables en tiempo de ejecución vs build

Las variables de entorno se congelan en el momento del build para el cliente. Si necesitas valores que cambien en runtime (ej. en un contenedor Docker), debes:

    Para Server Components/API: usar getServerSideProps o Route Handlers que lean process.env en cada petición (en producción con next start, las variables de entorno del sistema están disponibles).

    Para el cliente: no hay forma directa. Puedes pasar valores desde el servidor al cliente como props o a través de una API.

Técnica común: exponer un endpoint /api/config que devuelva variables públicas que puedan cambiar en runtime.
Secretos y seguridad

    Jamás expongas claves de API o secretos en variables NEXT_PUBLIC_.

    En Server Components, las variables no prefijadas nunca se envían al cliente.

    Si necesitas usar una clave en Server Side pero también referenciarla en un Client Component (por ejemplo, para iniciar un SDK), el SDK debe inicializarse con una clave pública, no un secreto. La clave pública sí puede ser NEXT_PUBLIC_.

### Ejemplo de configuración completa

.env.local:
```text
DATABASE_URL=postgres://...
NEXT_PUBLIC_SITE_URL=https://misitio.com
```

En app/server-page.js:
```tsx
export default async function ServerPage() {
  const dbUrl = process.env.DATABASE_URL   // OK, solo servidor
  // ...
}
```

En un Client Component:
```tsx
'use client'
export default function Component() {
  const url = process.env.NEXT_PUBLIC_SITE_URL   // OK
}
```

El manejo cuidadoso de las variables de entorno es esencial para la seguridad y la flexibilidad en el despliegue.
---

## Archivo: `09-deploy-y-configuracion/despliegue-vercel.md`

Despliegue en Vercel

Vercel es la plataforma creada por los desarrolladores de Next.js y ofrece la integración más profunda y sencilla posible. Permite desplegar con un solo comando desde Git y proporciona características como ISR, Edge Functions y análisis.
Conexión con repositorio Git (recomendado)

    Crea un proyecto en vercel.com e importa tu repositorio (GitHub, GitLab, Bitbucket).

    Vercel detecta automáticamente que es un proyecto Next.js y configura los comandos de build y salida.

    Define las variables de entorno en el panel del proyecto.

    Cada push a la rama principal dispara un despliegue de producción. Las ramas de pull request generan un preview deployment automático.

### Despliegue manual con Vercel CLI

Instala Vercel CLI:
```bash
npm i -g vercel
```

Desde la raíz del proyecto:
```bash
vercel
```

La primera vez te guiará para iniciar sesión y vincular el proyecto. Luego, vercel --prod para producción.
Variables de entorno

Configúralas en el dashboard del proyecto (Settings → Environment Variables) para producción, preview y development. Vercel las inyecta en tiempo de build y en las funciones serverless.

También puedes definirlas en vercel.json (aunque no es común para variables).
Configuración de vercel.json

Aunque no es necesario, puedes personalizar comportamientos:
```json
{
  "functions": {
    "api/**/*.js": {
      "memory": 512,
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Custom", "value": "my-value" }
      ]
    }
  ],
  "rewrites": [
    { "source": "/blog", "destination": "/news" }
  ]
}
```

### Edge Functions

Next.js en Vercel puede ejecutar middleware y Route Handlers en el borde global. Solo necesitas exportar export const runtime = 'edge'. Vercel despliega automáticamente en su red Edge.
ISR y Cache

El ISR se almacena en la capa de Edge Cache de Vercel, lo que asegura regeneraciones atómicas y baja latencia. No requiere configuración extra. Las revalidaciones por revalidateTag y revalidatePath funcionan instantáneamente.
Dominios personalizados y SSL

Desde el dashboard puedes añadir cualquier dominio; Vercel provee SSL automático con Let's Encrypt. También puedes proteger con autenticación o IP whitelist.
Análisis y logs

Vercel Analytics (Web Vitals) y Runtime Logs están integrados. Puedes ver errores, tiempo de respuesta, y métricas de experiencia de usuario.
Escalado automático

El plan Pro escala automáticamente según la demanda. No necesitas administrar servidores.
Consideraciones

    Si usas next export en Vercel, la exportación estática se sirve como sitio estático, sin serverless.

    Las Server Actions funcionan de forma nativa.

    El límite de tamaño de función serverless es 50 MB (comprimido), ten cuidado con dependencias muy pesadas.

    Puedes configurar funciones de fondo con maxDuration hasta 800 segundos (plan Enterprise).

Vercel es la opción más rápida y directa para desplegar Next.js, aprovechando al máximo sus características.
---

## Archivo: `09-deploy-y-configuracion/despliegue-node.md`

Despliegue en servidor Node.js

Cuando no usas un proveedor especializado como Vercel, puedes ejecutar Next.js en tu propio servidor Node.js. Esto te da control total pero requiere una configuración adicional para producción.
Construcción y arranque

Ejecuta:
```bash
npm run build
npm start
```

next start inicia el servidor en modo producción en el puerto 3000. Para cambiar el puerto:
```bash
PORT=8000 npm start
```

### Uso de un gestor de procesos (PM2)

Para mantener la aplicación viva y balancear carga, usa PM2:
```bash
npm install -g pm2
pm2 start npm --name "mi-app" -- start
pm2 save
pm2 startup
```

Configuración más fina con un archivo ecosystem.config.js:
```js
module.exports = {
  apps: [{
    name: 'next-app',
    script: 'node_modules/.bin/next',
    args: 'start',
    instances: 'max',        // número de núcleos
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000,
    },
  }],
}
```

Inicia con:
```bash
pm2 start ecosystem.config.js
```

### Configuración de proxy inverso (Nginx)

Es recomendable colocar Nginx delante de Next.js para terminar SSL, comprimir respuestas y servir estáticos.
nginx

### server {
    listen 80;
    server_name misitio.com;
    return 301 https://$host$request_uri;
}

### server {
    listen 443 ssl http2;
    server_name misitio.com;

### ssl_certificate /ruta/cert.pem;
    ssl_certificate_key /ruta/key.pem;

### location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

### # Static assets cache
    location /_next/static {
        alias /ruta/app/.next/static;
        expires 1y;
        access_log off;
    }

### location /static {
        alias /ruta/app/public/static;
        expires 1y;
        access_log off;
    }
}

### Variables de entorno

En producción, las variables de entorno se toman del sistema donde se ejecuta next start. Puedes definirlas en el archivo de servicio (systemd) o en el script de inicio. Para PM2, se definen en el ecosystem.config.js o directamente en la línea de comandos.
Servicio systemd (Linux)

Crea un archivo /etc/systemd/system/nextjs.service:
```text
[Unit]
Description=Next.js App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/ruta/a/la/app
ExecStart=/usr/bin/npm start
Restart=on-failure
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

Actívalo:
```bash
systemctl enable nextjs
systemctl start nextjs
```

### Servidor personalizado con Express

Si necesitas lógica adicional (manejo de sesiones, websockets, subprocesos), puedes crear un servidor Express que importe el request handler de Next.js. Esto desactiva algunas optimizaciones, pero es posible.
```ts
// server.ts
import express from 'express'
import next from 'next'

const dev = process.env.NODE_ENV !== 'production'
const app = next({ dev })
const handle = app.getRequestHandler()
```

### app.prepare().then(() => {
  const server = express()
  server.all('*', (req, res) => handle(req, res))
  server.listen(3000)
})

Luego compilas server.ts con tsc y lo ejecutas con Node.
Consideraciones de rendimiento

    Usa el cluster mode de PM2 para aprovechar multi-core.

    Configura Nginx para compresión gzip/br.

    Ajusta las cabeceras de caché de estáticos.

    Monitorea con herramientas como pm2 monit o Prometheus.

Desplegar en Node.js propio te da total flexibilidad, ideal para entornos corporativos o de hosting tradicional.
---

## Archivo: `09-deploy-y-configuracion/dockerizar.md`

Dockerizar una aplicación Next.js

Dockerizar permite empaquetar la aplicación con todas sus dependencias y desplegarla en cualquier entorno compatible con contenedores. La opción standalone de Next.js optimiza la imagen eliminando la necesidad de node_modules completos.
Configurar next.config.js para standalone
```js
module.exports = {
  output: 'standalone',
}
```

Esta opción genera una carpeta .next/standalone después del build que contiene solo el código necesario (el servidor Next.js compilado, tus archivos públicos y una copia mínima de node_modules).
Dockerfile multi-stage
dockerfile

### # Etapa 1: dependencias
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --only=production

### # Etapa 2: build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

### # Etapa 3: runner
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

### COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

### EXPOSE 3000
CMD ["node", "server.js"]

Explicación:

    La etapa deps instala solo dependencias de producción (útil para la etapa final si no usas standalone, aunque standalone incluye las suyas).

    builder copia node_modules completas y ejecuta next build.

    runner copia el standalone y los estáticos desde .next/static (necesario porque standalone no los incluye directamente). Lanza node server.js.

### Construir y ejecutar
```bash
docker build -t mi-next-app .
docker run -p 3000:3000 -e DATABASE_URL=... mi-next-app
```

Las variables de entorno se pasan en tiempo de ejecución con -e.
Mejores prácticas

    Usa un .dockerignore para excluir node_modules local, .git, etc.

    Para imágenes más pequeñas, usa node:20-slim o alpine, pero Alpine puede tener problemas con algunas librerías nativas. Prueba que funcione.

    Si usas next/image con imágenes remotas, asegúrate de que los patrones estén configurados.

    Para ISR con almacenamiento persistente, monta un volumen en la ubicación del archivo de caché (por defecto en .next/cache). Con standalone, la caché de fetch se guarda en la carpeta de trabajo; si necesitas persistencia entre reinicios, monta un volumen.

### Uso con Docker Compose

```yaml
### version: '3'
services:
  next:
    build: .
    ports:
      - '3000:3000'
    environment:
      - DATABASE_URL=postgres://...
    volumes:
      - next-cache:/app/.next/cache

volumes:
  next-cache:

### Consideraciones con ISR y múltiples instancias

En entornos con múltiples contenedores (Kubernetes, Swarm), el ISR basado en revalidate puede tener problemas porque la caché está en cada instancia. Soluciones:

    Usar un almacenamiento compartido (NFS, S3) para el directorio .next/cache.

    Utilizar revalidación bajo demanda con un webhook que notifique a todas las instancias.

    Deshabilitar ISR entiempo y usar solo SSR o SSG puro si la consistencia inmediata es crítica.

### Publicación en registros

Después de construir, publica en un registro como Docker Hub o GitHub Container Registry:
```bash
docker tag mi-next-app usuario/mi-next-app:1.0
docker push usuario/mi-next-app:1.0
```

Dockerizar con standalone genera imágenes ligeras y eficientes, listas para correr en cualquier plataforma de contenedores.
---

## Archivo: `09-deploy-y-configuracion/export-estatico.md`

Exportación estática (Static HTML Export)

La exportación estática genera un sitio compuesto únicamente por HTML, CSS, JavaScript y archivos estáticos, sin necesidad de servidor Node.js. Es ideal para alojar en GitHub Pages, S3, Netlify (como sitio estático), o cualquier CDN.
Configuración

En next.config.js, habilita el modo exportación:
```js
module.exports = {
  output: 'export',
}
```

Opcionalmente, define la ruta base si el sitio no se sirve desde la raíz:
```js
basePath: '/mi-proyecto',
```

### Comando de construcción

Ejecuta:
```bash
npm run build
```

Next.js generará una carpeta out/ con el sitio estático listo para desplegar. La carpeta contiene:

    out/index.html para la ruta /.

    out/about.html para /about.

    out/posts/[id].html para rutas dinámicas pre-renderizadas.

    out/_next/static/ con los bundles JS y CSS.

    out/images/... para archivos de la carpeta public/.

### Limitaciones de la exportación estática

Al no haber servidor, no funcionan:

    Rutas de API (pages/api/ o Route Handlers).

    getServerSideProps (debes usar solo getStaticProps).

    ISR con revalidate (puedes usar revalidate: false o directamente omitirlo; la página será estática al momento del build).

    Middleware (no hay tiempo de ejecución).

    next/image con el loader por defecto (requiere servidor para optimización). Debes configurar un loader externo como Cloudinary, imgix o un loader personalizado que use imágenes sin optimizar (unoptimized).

    Server Actions y streaming.

    Redirecciones y reescrituras server-side; puedes configurar redirecciones a nivel de plataforma (por ejemplo, con _redirects en Netlify).

    Cookies en getStaticProps (no hay req).

### Rutas dinámicas con getStaticPaths

Debes pre-renderizar todas las rutas posibles. Generalmente usas fallback: false para que solo existan las generadas; cualquier otra devolverá 404.
```js
export async function getStaticPaths() {
  const posts = await fetchPosts()
  const paths = posts.map(post => ({ params: { id: post.id } }))
  return { paths, fallback: false }
}
```

En App Router, usas generateStaticParams y la página se vuelve estática.
Manejo de imágenes

El componente next/image con el loader por defecto no funciona en exportación estática porque intenta usar /_next/image. Opciones:

    Usar unoptimized en cada imagen: <Image ... unoptimized /> — y sirves las imágenes originales.

    Configurar un loader externo y añadir dominio en images.loaderFile o images.loader:

```js
images: {
  loader: 'custom',
  loaderFile: './loader.js',
},
```

loader.js personalizado:
```js
export default function customLoader({ src, width, quality }) {
  return `https://mi-cdn.com/${src}?w=${width}&q=${quality || 75}`
}

    Utilizar un servicio de imagen (Cloudinary, Imgix) y configurar el loader correspondiente.
```

### Variables de entorno en cliente

Las variables NEXT_PUBLIC_ se hornean en el build y funcionan perfectamente en exportación estática. No puedes usar variables privadas en lógica de servidor porque no hay servidor.
Despliegue de la carpeta out

Puedes servirla con cualquier servidor HTTP. Ejemplos:

    Netlify: arrastra la carpeta out o configura el comando de build next build && next export y la carpeta de publicación out. Para redirecciones SPA, usa un archivo _redirects en public/.

    Vercel: también soporta sitios estáticos; configura output: 'export' y Vercel lo despliega automáticamente como estático.

    AWS S3 + CloudFront: sube el contenido de out a un bucket y sirve con CloudFront. Configura páginas de error y redirecciones.

    GitHub Pages: usa la acción JamesIves/github-pages-deploy-action o sube manualmente a la rama gh-pages. Recuerda configurar basePath si el repositorio es de proyecto.

¿Cuándo elegir exportación estática?

    Sitios completamente sin lógica de servidor: blogs, portafolios, landing pages.

    Cuando quieres alojar en infraestructura de bajo costo (CDN, almacenamiento de objetos).

    Proyectos donde el contenido no cambia entre despliegues (o cambia con poca frecuencia y se reconstruye).

Es la opción más simple y escalable, pero sacrifica todas las capacidades dinámicas y bajo demanda de Next.js.

---

## Archivo: `10-testing/testing-pages-router.md`

Testing en Pages Router

Probar una aplicación Next.js con Pages Router implica combinar tests unitarios, de integración y end‑to‑end (E2E). La naturaleza híbrida (SSR/SSG) exige verificar tanto la lógica del servidor como la del cliente.
Herramientas recomendadas

    Jest como framework de testing unitario y de integración.

    React Testing Library (RTL) para probar componentes en un entorno simulado de navegador.

    Cypress o Playwright para E2E.

    MSW (Mock Service Worker) para interceptar peticiones en tests de cliente/integración.

### Configuración de Jest

Instala dependencias:
```bash
npm i -D jest @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom
```

En package.json añade los scripts y la configuración de Jest:
```json
"scripts": {
  "test": "jest --watch",
  "test:ci": "jest --ci"
},
"jest": {
  "testEnvironment": "jsdom",
  "setupFilesAfterSetup": ["<rootDir>/jest.setup.js"],
  "moduleNameMapper": {
    "^@/(.*)$": "<rootDir>/src/$1"
  }
}
```

Crea jest.setup.js:
```js
import '@testing-library/jest-dom'
```

Opcionalmente instala @types/jest para TypeScript.
Test unitario de una función de utilidad
```js
// utils/sum.js
export const sum = (a, b) => a + b
```

js

### // __tests__/sum.test.js
import { sum } from '../utils/sum'

### test('suma correctamente dos números', () => {
  expect(sum(2, 3)).toBe(5)
})

### Test de un componente básico (sin datos del servidor)
```jsx
// components/Saludo.js
export default function Saludo({ nombre }) {
  return <h1>Hola {nombre}</h1>
}
```

### jsx

### // __tests__/Saludo.test.jsx
import { render, screen } from '@testing-library/react'
import Saludo from '../components/Saludo'

### test('muestra el saludo con el nombre', () => {
  render(<Saludo nombre="Mario" />)
  expect(screen.getByText('Hola Mario')).toBeInTheDocument()
})

### Test de una página con getStaticProps

Podemos probar la función getStaticProps de forma aislada (es una función que retorna props).
```js
// pages/blog.js
export async function getStaticProps() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json())
  return { props: { posts } }
}
```

js

### // __tests__/blog.test.js
import { getStaticProps } from '../pages/blog'

### jest.mock('node-fetch')  // o fetch global con jest.fn()

### test('obtiene posts y los retorna como props', async () => {
  const mockPosts = [{ id: 1, title: 'A' }]
  global.fetch = jest.fn(() =>
    Promise.resolve({ json: () => Promise.resolve(mockPosts) })
  )

### const result = await getStaticProps({})
  expect(result.props.posts).toEqual(mockPosts)
})

Nota: En Next.js el fetch está disponible globalmente en el entorno de test si usas Node 18+, así que puedes mockearlo directamente.
Test de una página renderizada (SSG/SSR) con datos de servidor

Cuando la página recibe props desde el servidor, podemos renderizarla sin necesidad de ejecutar getStaticProps. Pasamos las props manualmente.
```jsx
// pages/blog.js
export default function Blog({ posts }) {
  return (
    <ul>
      {posts.map(p => <li key={p.id}>{p.title}</li>)}
    </ul>
  )
}
```

### jsx

### // __tests__/Blog.test.jsx
import { render, screen } from '@testing-library/react'
import Blog from '../pages/blog'

### test('renderiza lista de posts', () => {
  const posts = [{ id: 1, title: 'Un post' }]
  render(<Blog posts={posts} />)
  expect(screen.getByText('Un post')).toBeInTheDocument()
})

### Simular el router

Para componentes que usan useRouter o <Link>, podemos mockear next/router.
```js
// __tests__/helpers.js
jest.mock('next/router', () => ({
  useRouter: () => ({
    route: '/',
    pathname: '',
    query: {},
    asPath: '',
    push: jest.fn(),
    replace: jest.fn(),
  }),
}))
```

Para next/link, RTL lo reconoce porque renderiza un <a>, así que podemos comprobar el atributo href.
Test de API Routes

Las API Routes son funciones que reciben req y res. Podemos probarlas con httpMocks o creando objetos mock.
```js
// pages/api/hola.js
export default function handler(req, res) {
  res.status(200).json({ mensaje: 'Hola' })
}
```

js

### import handler from '../pages/api/hola'
import { createMocks } from 'node-mocks-http'

### test('devuelve mensaje de hola', async () => {
  const { req, res } = createMocks({ method: 'GET' })
  await handler(req, res)

### expect(res._getStatusCode()).toBe(200)
  expect(JSON.parse(res._getData())).toEqual({ mensaje: 'Hola' })
})

### Integración con Cypress

Cypress se ejecuta contra la aplicación corriendo. Para Pages Router, es similar a cualquier React app. Un ejemplo de test E2E:
```js
// cypress/e2e/home.cy.js
describe('Página principal', () => {
  it('muestra el título', () => {
    cy.visit('/')
    cy.contains('Bienvenido').should('be.visible')
  })
})
```

Cypress maneja la navegación igual que un navegador real. Para SSR/SSG no hay diferencia porque el HTML ya viene renderizado.
Mock de fetch en el frontend con MSW

Para testear componentes que llaman a APIs en el cliente, MSW permite interceptar y simular respuestas.
```js
// __tests__/setupMSW.js
import { rest } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  rest.get('/api/perfil', (req, res, ctx) =>
    res(ctx.json({ nombre: 'Test' }))
  )
)
beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

Con esto, los componentes que usan fetch('/api/perfil') reciben el mock.

El testing en Pages Router es directo: separas la lógica de servidor de los componentes y aplicas técnicas estándar de React testing con algunos mocks específicos de Next.js.
---

## Archivo: `10-testing/testing-app-router.md`

Testing en App Router

El App Router trae un modelo de React Server Components que cambia la forma de testear. No puedes renderizar Server Components en un entorno puramente cliente (jsdom), pero tenemos estrategias para probar tanto el comportamiento del servidor como la UI interactiva.
Enfoques de testing según el tipo de componente

    Funciones, lógica de negocio, auth.ts, utils: se prueban como funciones Node.js normales.

    Server Components (asíncronos): se prueban renderizándolos con @testing-library/react en un entorno que soporte async. Next.js recomienda usar render de @testing-library/react junto con jsdom y jest (con algunas adaptaciones). Para RSC puros (no clientes) podemos importar y renderizar directamente el componente, pasando las props que normalmente obtendría del servidor.

    Client Components: igual que en Pages Router, pero necesitan la directiva 'use client'; si se importan desde un test, debes mockear lo mínimo (por ejemplo, next/navigation).

    Route Handlers: se testean invocando las funciones exportadas con objetos Request simulados.

    Server Actions: se prueban como funciones asíncronas con argumentos simulados y luego verificamos efectos secundarios o revalidaciones.

    Middlewares: se prueban creando un NextRequest falso y llamando al middleware.

### Configuración de Jest para App Router

Instala las mismas dependencias que para Pages, además de next-router-mock o mocks manuales de next/navigation. A partir de Next.js 14, muchos proyectos utilizan Vitest por su mejor soporte ESM, pero Jest sigue siendo popular. Usaremos Jest con las transformaciones necesarias.

Para soportar next/dynamic, next/image, next/link, etc., necesitas mocks. La guía de testing de Next.js sugiere lo siguiente en jest.config.js:
```js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterSetup: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^next/navigation$': '<rootDir>/__mocks__/next-navigation.js',
    '^next/image$': '<rootDir>/__mocks__/next-image.js',
    '^next/link$': '<rootDir>/__mocks__/next-link.js',
  },
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', { presets: ['next/babel'] }],
  },
}
```

Crea los mocks:

__mocks__/next-navigation.js:
```js
export const useRouter = jest.fn(() => ({
  push: jest.fn(),
  replace: jest.fn(),
  back: jest.fn(),
  prefetch: jest.fn(),
}))

export const usePathname = jest.fn(() => '/')
export const useSearchParams = jest.fn(() => new URLSearchParams())
export const notFound = jest.fn()
export const redirect = jest.fn()
```

__mocks__/next-image.js:
```js
const MockImage = (props) => <img {...props} />
export default MockImage
```

__mocks__/next-link.js:
```js
import React from 'react'
const MockLink = ({ children, href, ...rest }) => (
  <a href={href} {...rest}>{children}</a>
)
export default MockLink
```

### Test de un Server Component

Los Server Components asíncronos pueden ser renderizados con render de RTL si los envolvemos en un Suspense y los tratamos como un componente normal. Como no son 'use client', podemos importarlos y renderizarlos. Ejemplo:
```tsx
// app/productos/page.tsx
export default async function ProductosPage() {
  const res = await fetch('https://api.example.com/productos')
  const productos = await res.json()
  return <ul>{productos.map(p => <li key={p.id}>{p.nombre}</li>)}</ul>
}
```

Para testearlo, mockeamos fetch:
```tsx
// __tests__/ProductosPage.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import ProductosPage from '@/app/productos/page'
```

### beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve([{ id: 1, nombre: 'Pelota' }]),
    })
  ) as jest.Mock
})

### test('renderiza lista de productos', async () => {
  // El componente es async, se resuelve en el render
  render(await ProductosPage())
  expect(screen.getByText('Pelota')).toBeInTheDocument()
})

También podemos usar waitFor si el componente tiene Suspense.
Test de un Client Component

Funciona igual que en Pages Router, solo que debemos tener cuidado con las importaciones de next/navigation. Al mockearlas, el componente usará los mocks y podremos verificar llamadas a push.
```tsx
'use client'
import { useRouter } from 'next/navigation'

export default function BotonNavegar() {
  const router = useRouter()
  return <button onClick={() => router.push('/about')}>Ir</button>
}
```

### tsx

### import { render, screen, fireEvent } from '@testing-library/react'
import BotonNavegar from '@/components/BotonNavegar'
import { useRouter } from 'next/navigation'

### jest.mock('next/navigation')

### test('navega a /about al hacer clic', () => {
  const pushMock = jest.fn()
  ;(useRouter as jest.Mock).mockReturnValue({ push: pushMock })

### render(<BotonNavegar />)
  fireEvent.click(screen.getByText('Ir'))
  expect(pushMock).toHaveBeenCalledWith('/about')
})

### Test de Route Handlers

Exportas funciones GET, POST, etc. Simula un Request y llama a la función.
```ts
// app/api/hello/route.ts
export async function GET() {
  return Response.json({ message: 'Hola' })
}
```

ts

### import { GET } from '@/app/api/hello/route'

### test('retorna mensaje', async () => {
  const response = await GET()
  const data = await response.json()
  expect(response.status).toBe(200)
  expect(data).toEqual({ message: 'Hola' })
})

### Test de Server Actions

Son funciones normales, las importamos y las ejecutamos.
```ts
'use server'
export async function crearPost(formData: FormData) {
  // lógica...
}
```

ts

### import { crearPost } from '@/actions'
import { revalidatePath } from 'next/cache'

### jest.mock('next/cache', () => ({
  revalidatePath: jest.fn(),
}))

### test('crea un post y revalida', async () => {
  const formData = new FormData()
  formData.append('title', 'Nuevo')
  await crearPost(formData)
  expect(revalidatePath).toHaveBeenCalledWith('/posts')
})

### Test de Middleware

Crea un NextRequest simulado con la URL y cookies deseadas.
```ts
import { middleware, config } from '@/middleware'
import { NextResponse } from 'next/server'
```

### test('redirige a login si no hay token', async () => {
  const req = new Request('http://localhost/dashboard', { headers: {} })
  // Middleware espera NextRequest; podemos usar NextRequest o simular
  const res = await middleware(req as any)
  expect(res?.status).toBe(307) // redirección
})

### E2E con Cypress / Playwright

El testing E2E en App Router es similar a Pages, pero aprovecha que el streaming puede causar que el contenido aparezca de forma asíncrona. Playwright tiene mejor soporte para esperar por el contenido estático/dinámico. Ejemplo con Playwright:
```ts
import { test, expect } from '@playwright/test'
```

### test('página de productos muestra lista', async ({ page }) => {
  await page.goto('/productos')
  await expect(page.locator('li')).toHaveCount(10)
})

Playwright maneja el streaming: espera a que el HTML completo esté presente.

El testing en App Router requiere mockear las nuevas APIs (next/navigation, next/headers, etc.) pero mantiene la misma filosofía: aislar y probar cada capa (funciones, componentes cliente, endpoints). Con los mocks adecuados, la experiencia es fluida.
---

## Archivo: `11-typescript/configuracion.md`

Configuración de TypeScript en Next.js

Next.js tiene soporte nativo para TypeScript, por lo que no necesitas configurar compiladores adicionales. Basta con usar la extensión .ts o .tsx y Next se encarga del resto.
Crear proyecto con TypeScript

Al ejecutar create-next-app, la opción “TypeScript” viene activada por defecto, generando tsconfig.json.
```bash
npx create-next-app@latest mi-app
```

Si migras un proyecto existente, crea un tsconfig.json vacío y ejecuta npm run dev. Next.js lo rellenará automáticamente con la configuración recomendada.
tsconfig.json por defecto
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

Los puntos más relevantes:

    strict: true habilita todas las verificaciones estrictas (recomendado).

    paths: permite importar con alias @/ (ajusta según tu carpeta src o raíz).

    plugins: [{ name: 'next' }]: habilita el plugin del lenguaje Next en editores como VS Code, mejorando el autocompletado.

    .next/types contiene tipos generados por Next (ej. para rutas).

### Tipos adicionales

Instala @types/react y @types/node si no están.
```bash
npm i -D @types/react @types/node
```

### TypeScript en next.config.js

Puedes renombrar next.config.js a next.config.ts para usar TypeScript. Next.js lo transpilará antes de usarlo.
```ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  reactStrictMode: true,
}
export default config
```

### Tipos para Pages Router

Next exporta tipos específicos que puedes usar para tipar páginas:

    NextPage para componentes de página.

    GetServerSideProps, GetStaticProps, GetStaticPaths para las funciones de obtención de datos.

```tsx
import { GetServerSideProps, NextPage } from 'next'

type Post = { id: number; title: string }

interface Props {
  posts: Post[]
}

export const getServerSideProps: GetServerSideProps<Props> = async () => {
  const posts: Post[] = await fetch('...').then(r => r.json())
  return { props: { posts } }
}

const Blog: NextPage<Props> = ({ posts }) => (
  <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
)

export default Blog
```

Para getStaticPaths:
```ts
export const getStaticPaths: GetStaticPaths = async () => {
  // ...
}
```

### Tipos para App Router

El App Router usa sus propios tipos, a menudo inferidos automáticamente. Por ejemplo, los parámetros de ruta (params) y searchParams tienen tipado automático en muchos casos con el plugin de Next. Pero es bueno especificarlos:
```tsx
// app/blog/[slug]/page.tsx
type Props = {
  params: { slug: string }
  searchParams?: { [key: string]: string | string[] | undefined }
}

export default function Page({ params }: Props) {
  return <h1>{params.slug}</h1>
}
```

Para generateMetadata:
```ts
import { Metadata } from 'next'

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  return { title: params.slug }
}
```

### Tipos para Server Actions

Puedes definir Server Actions con FormData o tipos personalizados:
```ts
'use server'

export async function actualizar(formData: FormData): Promise<void> {
  const nombre = formData.get('nombre') as string
  // ...
}
```

### Strict mode y any

Es tentador usar any cuando los tipos de Next se vuelven complejos. Intenta evitarlo, especialmente en funciones de obtención de datos y páginas. Las herramientas de Next y TypeScript evolucionan constantemente, y cada vez es más fácil tener tipos precisos.
Módulos externos sin tipos

Si una librería no tiene tipos, puedes declarar un módulo en *.d.ts. Por ejemplo, js-cookie:
```ts
// types/global.d.ts
declare module 'js-cookie' {
  export function get(name: string): string | undefined
  export function set(name: string, value: string, options?: any): void
}
```

La configuración de TypeScript en Next.js está diseñada para funcionar de inmediato, pero conocer los detalles te permitirá aprovechar al máximo el autocompletado y la seguridad de tipos.
---

## Archivo: `11-typescript/tipos-utiles.md`

Tipos útiles de Next.js y TypeScript

Next.js proporciona una gran cantidad de tipos para mejorar la productividad y evitar errores. A continuación, un compendio de los más utilizados.
Tipos para Pages Router
Tipo	Uso
NextPage	Componente de página opcionalmente tipado por props.
NextPageWithLayout	Permite definir un método getLayout en la página.
GetServerSideProps	Tipa la función getServerSideProps.
GetStaticProps	Tipa la función getStaticProps.
GetStaticPaths	Tipa la función getStaticPaths.
InferGetServerSidePropsType	Infiere el tipo de las props a partir de getServerSideProps.
InferGetStaticPropsType	Similar para getStaticProps.

Ejemplo de InferGetStaticPropsType (evita redundancia):
```tsx
import { InferGetStaticPropsType } from 'next'

export async function getStaticProps() {
  const data = await fetchData()
  return { props: { data } }
}

export default function Page({ data }: InferGetStaticPropsType<typeof getStaticProps>) {
  // data está tipado correctamente
}
```

### Tipos para App Router

Los tipos principales provienen de next y next/navigation.

PageProps (informal): aunque no existe un tipo exportado llamado PageProps, puedes definir uno basado en los parámetros esperados.
```tsx
type Props = {
  params: { id: string }
  searchParams: { [key: string]: string | string[] | undefined }
}
```

Metadata y ResolvingMetadata: para generar metadatos.
```ts
import type { Metadata, ResolvingMetadata } from 'next'

export async function generateMetadata(
  { params }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const previousOpenGraph = (await parent).openGraph ?? {}
  return {
    title: 'Nuevo',
    openGraph: { ...previousOpenGraph, title: 'Nuevo' },
  }
}
```

Web Request y NextRequest / NextResponse: en Route Handlers y middleware.
```ts
import { NextRequest, NextResponse } from 'next/server'

export function middleware(req: NextRequest) {
  // ...
}
```

React.ReactNode en layouts y children.
```tsx
export default function Layout({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}
```

### Tipos de next/navigation
Hook / Función	Tipo / Retorno
useRouter	NextRouter
usePathname	string
useSearchParams	ReadonlyURLSearchParams
useParams	{ [key: string]: string | string[] }
redirect	never (no retorna)
notFound	never

Al mockear en tests, es útil conocer estos tipos.
Tipos para next/headers

Las funciones cookies() y headers() devuelven objetos con métodos tipados.
```ts
import { cookies } from 'next/headers'

export function getToken() {
  const cookieStore = cookies()
  const token = cookieStore.get('token') // { name: string, value: string } | undefined
}
```

### Tipos para Server Actions

Puedes tipar el parámetro formData o usar tipos convencionales cuando se invocan desde eventos.
```ts
'use server'
export async function submit(data: { name: string; email: string }) {
  // ...
}
```

Si se usa desde un formulario con action={submit}, se debe usar FormData. Pero puedes crear una función intermedia:
```ts
export async function handleSubmit(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string
  await submit({ name, email })
}
```

### Tipos para next.config.ts
```ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  env: {
    miVariable: process.env.MI_VARIABLE, // error si no existe en el entorno
  },
}
```

### Tipos para next/image

El componente Image acepta ImageProps (exportado) que extiende los atributos de imagen HTML con propiedades específicas.
```tsx
import Image, { ImageProps } from 'next/image'
type Props = Omit<ImageProps, 'src' | 'alt'> & {
  imagen: string
  descripcion: string
}
```

### Tipos en getStaticPaths con i18n

Cuando usas locales, GetStaticPathsContext incluye locales y defaultLocale.
```ts
export const getStaticPaths: GetStaticPaths = async (context) => {
  const { locales } = context
  // ...
}
```

### NextApiRequest y NextApiResponse (Pages Router API)
```ts
import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse<Data>) {
  // ...
}
```

### Tipos para contexto en layouts anidados

No hay un tipo integrado para params en layouts, porque pueden variar. Pero puedes crear una interfaz:
```tsx
interface DashboardLayoutProps {
  children: React.ReactNode
  params: { userId: string }
}
```

### Utiliza satisfies para seguridad extra

Con TypeScript 4.9+ puedes emplear satisfies para verificar que un objeto cumple un tipo sin cambiar su inferencia. Muy útil en configuraciones.
```ts
const metadata = {
  title: 'Mi app',
} satisfies Metadata
```

Estos tipos reducen los errores en tiempo de compilación y mejoran la experiencia de desarrollo.
---

## Archivo: `12-cli-y-scripts/comandos-next.md`

CLI de Next.js y scripts personalizados

Next.js incluye una interfaz de línea de comandos (CLI) con múltiples comandos para desarrollo, construcción y análisis. También ofrece un conjunto de scripts que se integran en package.json.
Comandos principales de la CLI
Comando	Descripción
next dev	Inicia el servidor de desarrollo con Hot Module Replacement en localhost:3000.
next build	Compila la aplicación para producción (optimizada).
next start	Inicia el servidor en modo producción (requiere next build previo).
next lint	Ejecuta ESLint en los archivos del proyecto.
next telemetry	Habilita/deshabilita la telemetría (datos anónimos de uso a Vercel).
next info	Muestra información del entorno (útil para reportar bugs).
next dev
```bash
next dev [opciones]
```

Opciones comunes:

    -p, --port <puerto>: cambiar el puerto (por defecto 3000).

    -H, --hostname <host>: por defecto localhost. Usa 0.0.0.0 para exponer en red local.

    --turbo: usa Turbopack para compilaciones más rápidas (si está disponible).

Ejemplos:
```bash
next dev -p 4000
next dev --turbo
```

### next build
```bash
next build
```

Genera una carpeta .next con el bundle optimizado. Analiza las páginas y muestra si son estáticas ○, dinámicas λ, o requieren ISR. Es compatible con perfiles: next build --profile habilita el perfilador de Webpack/Turbopack.
next start
```bash
next start [opciones]
```

Similar a next dev en opciones de puerto y host. Inicia la aplicación en modo producción (después de next build). Ideal para pruebas locales de la build final.
next lint
```bash
next lint [opciones]
```

Ejecuta ESLint con la configuración base de Next.js. Opciones:

    --fix: corrige automáticamente errores.

    --dir <directorio>: limita el escaneo a un directorio.

    --file <archivo>: analiza un solo archivo.

Por defecto, el comando se configura en package.json como "lint": "next lint".
next telemetry
```bash
next telemetry [status/enable/disable]
```

Muestra el estado o modifica la telemetría. Los datos recopilados son anónimos y se limitan a características usadas, rendimiento de build, etc.
next info
```bash
next info
```

Imprime información relevante del entorno: versión de Next, Node, sistema operativo, configuraciones. Muy útil al abrir una issue en GitHub.
Scripts recomendados en package.json
```json
"scripts": {
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "next lint",
  "lint:fix": "next lint --fix",
  "type-check": "tsc --noEmit",
  "format": "prettier --write .",
  "test": "jest --watch",
  "test:ci": "jest --ci",
  "prepare": "husky install"
}
```

### create-next-app

Aunque no es parte de la CLI en sí, create-next-app es el generador oficial:
```bash
npx create-next-app@latest [nombre] [opciones]
```

Opciones interactivas: TypeScript, ESLint, Tailwind, src directory, App Router, import alias. También acepta flags:
```bash
npx create-next-app@latest --ts --tailwind --app mi-app
```

### Personalización avanzada

Puedes crear scripts personalizados que invoquen la Next.js CLI desde Node.js. Por ejemplo, un script que genere sitemaps después del build:
```js
// scripts/generate-sitemap.js
const { execSync } = require('child_process')
execSync('next build', { stdio: 'inherit' })
// luego generas el sitemap...
```

### Uso de next export (legado)

Hasta Next.js 13, next export era el comando para salida estática. Ahora se configura con output: 'export' y next build crea directamente la carpeta out.
Modo de depuración

Para depurar el servidor Next.js (con Node inspector), ejecuta:
```bash
NODE_OPTIONS='--inspect' next dev
```

Luego conecta el inspector de Chrome o VS Code.

La CLI de Next.js es concisa pero potente, y al combinarla con scripts personalizados puedes automatizar tareas de desarrollo y despliegue con facilidad.

