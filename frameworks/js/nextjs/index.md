02-app-router/fundamentos-app-router.md
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
text

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

El layout raíz

Todo proyecto con App Router debe tener un layout raíz en app/layout.js. Este componente envuelve toda la aplicación y es el lugar para definir la estructura HTML, fuentes, metadatos globales y proveedores.
jsx

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

Los layouts raíz son Server Components por defecto; no pueden usar hooks de cliente. Si necesitas proveedores de contexto (Redux, temas, etc.), debes crear un Client Component separado e importarlo.
Ventajas del App Router

    Renderizado híbrido y granular: puedes combinar Server Components estáticos, dinámicos y Client Components en un mismo árbol.

    Layouts persistentes: no se desmontan al navegar, lo que mejora la experiencia y reduce código.

    Streaming y Suspense integrados: carga progresiva sin configuración compleja.

    Server Actions: mutaciones desde el cliente sin API routes.

    Caché más fino: control por fetch, segmentos y rutas con revalidatePath, revalidateTag.

Entender estas bases es fundamental antes de profundizar en los siguientes conceptos.
02-app-router/server-components-vs-client.md
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
jsx

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

Aquí BlogPage es un Server Component: obtiene datos en el servidor y renderiza HTML sin hidratación.
Client Components

Se definen añadiendo la directiva 'use client' en la primera línea del archivo. Esto le indica a Next.js que el componente y sus dependencias deben enviarse al navegador y seguir las reglas tradicionales de React.

Cuándo usarlos:

    Manejo de estado (useState, useReducer)

    Efectos y ciclo de vida (useEffect, useLayoutEffect)

    Eventos del DOM (onClick, onChange)

    Contexto de cliente (useContext con un provider creado en un Client Component)

    Hooks personalizados que usan lo anterior

    Librerías que dependen del navegador (gráficos, carruseles)

Ejemplo:
jsx

'use client'

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

Todo componente que importe un Client Component se convierte también en Client Component si no se separa cuidadosamente.
Composición: la clave para optimizar

Es posible intercalar Server y Client Components. La regla: puedes renderizar un Client Component dentro de un Server Component, y pasar Server Components como children (o props) de un Client Component. Así mantienes el renderizado del servidor para la mayor parte del árbol.
jsx

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

ThemeProvider es un Client Component porque usa useState para el tema, pero los hijos que recibe pueden ser Server Components; no se hidratan como cliente, manteniendo cero JS.
Límites de cliente y rendimiento

Next.js genera un límite de cliente (client boundary) al importar un Client Component desde un Server Component. El bundle JS del Client Component incluirá todo el subárbol a partir de ese punto. Por eso es recomendable empujar los Client Components lo más abajo posible en el árbol.

Buenas prácticas:

    Usa Server Components para la estructura y fetching.

    Extrae la interactividad en pequeños Client Components (p. ej., un botón de "Me gusta" es Client Component, pero el post completo sigue siendo Server Component).

    Pasa datos desde Server Components a Client Components vía props (serializables).

    No conviertas innecesariamente componentes grandes en cliente solo por un pequeño hook.

Casos típicos de mezcla

    Navegación interactiva: El componente Nav es Server, pero el botón hamburguesa (estado abierto/cerrado) es Client.

    Formularios con Server Actions: El formulario es Client (necesita onSubmit con JavaScript), pero la acción que invoca es del servidor.

    Tema oscuro: Un provider Client a nivel raíz, pero las páginas son completamente Server.

Entender esta separación te permite maximizar el rendimiento y la experiencia de desarrollo.
02-app-router/rutas-estaticas-dinamicas-paralelas.md
Rutas estáticas, dinámicas y paralelas en App Router

El App Router ofrece un modelo de enrutamiento mucho más potente que el Pages Router. Además de las rutas estáticas y dinámicas, introduce rutas paralelas e interceptación de rutas.
Rutas estáticas

Simplemente crea una carpeta con un archivo page.js. Ejemplos:

    app/contacto/page.js → /contacto

    app/acerca/nosotros/page.js → /acerca/nosotros

El archivo page.js exporta por defecto un componente (Server o Client). Next.js asigna la URL automáticamente.
Rutas dinámicas (segmentos variables)

Se indican con carpetas entre corchetes: [id], [slug].

    app/productos/[id]/page.js → /productos/1, /productos/abc, etc.

Dentro de page.js, los parámetros se reciben mediante la prop params (en Server Components) o con useParams (en Client Components).

En Server Component:
jsx

export default function Producto({ params }) {
  const { id } = params
  return <h1>Producto: {id}</h1>
}

En TypeScript:
tsx

type Props = { params: { id: string } }

export default function Producto({ params }: Props) { /* ... */ }

En Client Component:
jsx

'use client'
import { useParams } from 'next/navigation'

export default function Producto() {
  const params = useParams() // { id: '...' }
  return <h1>{params.id}</h1>
}

Rutas catch-all (captura todas)

Se definen con [...slug] y capturan cualquier cantidad de segmentos.

    app/docs/[...slug]/page.js → /docs, /docs/intro, /docs/guia/instalacion

params.slug será un array de strings (['intro'], ['guia', 'instalacion']).

Para que la ruta base también coincida (sin segmentos extras), usa [[...slug]] (opcional):

    app/docs/[[...slug]]/page.js → /docs (slug = undefined/[]), /docs/uno (slug = ['uno']).

Rutas paralelas

Las rutas paralelas permiten renderizar múltiples árboles de páginas en la misma vista, cada uno con su propio enrutamiento. Se implementan mediante slots: carpetas con el prefijo @.

Ejemplo típico en un dashboard:
text

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

En app/dashboard/layout.js, los slots se reciben como props:
jsx

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

    La navegación entre páginas dentro de un slot mantiene el estado de los demás.

    Si un slot no tiene una ruta activa, puedes mostrar un default.js para ese slot (archivo que define el contenido por defecto cuando no hay página coincidente).

Default views:
Crea un archivo default.js en el slot para que siempre haya contenido renderizado (por ejemplo, cuando navegas a una ruta que no tiene ese slot definido).
Beneficios de rutas paralelas

    Construcción de interfaces complejas tipo dashboard sin necesidad de estado global para manejar subrutas.

    Carga independiente y streaming por slot.

    Mejor organización del código (cada slot es autónomo).

Rutas de interceptación (ver capítulo siguiente)

Las rutas paralelas suelen usarse junto con rutas de interceptación para crear modales, feeds, etc.

Dominar rutas estáticas, dinámicas y paralelas te da un control total sobre la estructura de URLs y la composición de la UI en el App Router.
02-app-router/interceptacion-de-rutas.md
Interceptación de rutas en App Router

La interceptación de rutas permite interceptar una navegación y mostrar una versión alternativa de la página de destino, manteniendo el contexto actual. Esto es ideal para modales, galerías, o feeds de detalle que no quieres que reemplacen la página completa.
Cómo funciona

Se utilizan convenciones de nomenclatura especiales en las carpetas para indicar que una ruta debe interceptar a otra. Se basan en la notación de segmentos relativos:

    (.) → intercepta el mismo nivel

    (..) → intercepta un nivel superior

    (..)(..) → dos niveles superiores

    (...) → intercepta desde la raíz

La carpeta de interceptación se coloca al mismo nivel que la ruta interceptada, usando la notación.
Ejemplo: Modal de foto

Supongamos la ruta /feed (feed de fotos) y /photo/[id] (página de detalle completa). Queremos que al hacer clic en una foto desde el feed, se abra un modal en lugar de navegar a la página completa.

Estructura:
text

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

Cuando el usuario está en /feed y hace clic en una foto, Next.js busca coincidencias en el mismo nivel con (.), encuentra (.)photo/[id]/page.js y la renderiza en lugar de la página real. Si el usuario recarga la página o accede directamente a /photo/123, se carga la ruta real photo/[id]/page.js.
Implementación común con paralelas

Para que el modal se renderice sobre el feed sin perder el contenido de fondo, usarás rutas paralelas. Por ejemplo, un slot @modal que contenga la interceptación:
text

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

En app/layout.js:
jsx

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

modal será renderizado en paralelo. default.js en @modal puede retornar null para no mostrar nada cuando no hay modal activo.
Navegación entre interceptación y ruta real

    Desde el feed, el Link a /photo/123 activa la interceptación.

    Si se comparte la URL /photo/123, se carga la página completa sin modal.

    Puedes cerrar el modal con router.back() o redirigiendo a /feed.

Estados de carga y error

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
02-app-router/layouts-y-templates.md
Layouts y Templates en App Router

Next.js proporciona dos mecanismos para definir la estructura que envuelve las páginas: layouts y templates. Ambos se basan en archivos layout.js y template.js dentro de la carpeta app/.
Layout (layout.js)

Un layout es un componente que envuelve las páginas de un segmento y persiste su estado entre navegaciones. El layout raíz (app/layout.js) es obligatorio y define la estructura HTML principal.

Características clave:

    Solo se renderiza una vez cuando se monta, y no se vuelve a renderizar al navegar entre páginas hijas (a menos que cambie searchParams o params del layout anidado).

    Ideal para barras de navegación, pies de página, menús laterales.

    Recibe children (la página o segmento interior) y opcionalmente params.

    Puede ser asíncrono (Server Component) para obtener datos para el layout (p. ej., datos del usuario).

Ejemplo: layout con fetching
jsx

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

Porque el layout persiste, el menú lateral no pierde su estado (por ejemplo, scroll, selección de elemento) al cambiar de página dentro del dashboard.
Anidamiento de layouts

Los layouts se anidan según la jerarquía de carpetas. Por ejemplo:
text

app/
├── layout.js          (RootLayout)
├── products/
│   ├── layout.js      (ProductsLayout)
│   └── [category]/
│       ├── layout.js  (CategoryLayout)
│       └── page.js

Cada layout envuelve al siguiente. El flujo: RootLayout → ProductsLayout → CategoryLayout → page.

Al navegar de /products/ropa a /products/electronica, ProductsLayout y RootLayout se mantienen, mientras que CategoryLayout y la página cambian. Sin embargo, si CategoryLayout tiene datos propios dependientes de params.category, se ejecutará el renderizado del servidor para ese layout (porque params cambió).
Template (template.js)

Un template es similar a un layout, pero se crea una nueva instancia del componente cada vez que el usuario navega a una página dentro de ese segmento. No persiste el estado.

Cuándo usarlo:

    Para animaciones de entrada/salida usando motion o framer-motion, donde necesitas que el componente se monte/desmonte.

    Para reinicializar ciertos estados locales (por ejemplo, un formulario que debe vaciarse al cambiar de página).

    Cuando dependes de useEffect para cierta lógica que debe ejecutarse al entrar a la página.

Ejemplo:
jsx

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

Como no persiste, al navegar entre páginas del dashboard se reproduce la animación.
Uso conjunto

Puedes tener layout.js y template.js en la misma carpeta; ambos envolverán la página. El orden es: layout → template → page.
jsx

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

Estructura resultante: <Layout><Template><Page/></Template></Layout>
Pasar información entre layouts y páginas

No hay un mecanismo directo para pasar props de layout a page. Utiliza React Context (Client Component) o cookies/headers accesibles en Server Components. También puedes usar Server Actions para modificar datos del layout desde la página.
Layouts y Server Actions

Puedes colocar Server Actions en el layout (ejemplo: cerrar sesión) y pasarlas a componentes cliente.
Layouts dinámicos y revalidación

Si un layout obtiene datos con fetch, puedes configurar revalidate para ISR, igual que en páginas.

Los layouts constituyen el núcleo del App Router, facilitando la creación de interfaces complejas con mínimo esfuerzo y código repetitivo.
02-app-router/loading-y-error.md
loading.js y error.js: Manejo de estados en App Router

El App Router simplifica drásticamente el manejo de estados de carga y errores mediante dos archivos especiales: loading.js y error.js. Ambos aprovechan React Suspense y los Error Boundaries de React para encapsular cada segmento de ruta.
loading.js – UI de carga instantánea

Cuando una página (o un layout) tiene un componente asíncrono (Server Component que usa await), Next.js necesita mostrar algo mientras se resuelve la promesa. loading.js define el fallback de Suspense para esa ruta.

Cómo funciona:

    Coloca loading.js en la misma carpeta que page.js (o en cualquier segmento).

    Mientras la página se genera (en el servidor o con streaming), se muestra el contenido de loading.js.

    Cuando la página está lista, se reemplaza automáticamente.

Ejemplo básico:
jsx

// app/dashboard/loading.js
export default function DashboardLoading() {
  return (
    <div className="skeleton">
      <Spinner /> Cargando dashboard...
    </div>
  )
}

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

jsx

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

    El error no se propaga a los layouts superiores ni a la página raíz.

Ubicación:

Coloca error.js en la carpeta del segmento a proteger. Puedes tener múltiples niveles (por ejemplo, app/error.js global y uno específico en app/dashboard/error.js). El más cercano captura primero.
not-found.js

Aunque no es exactamente de error, es relevante. not-found.js se muestra cuando se invoca notFound() desde un Server Component o se visita una ruta inexistente. Debe ser un Client Component (opcional) y se renderiza dentro del layout sin 404 HTTP (puede mostrarse con layout conservado).
jsx

import { notFound } from 'next/navigation'

export default async function Page({ params }) {
  const post = await getPost(params.slug)
  if (!post) notFound()
  // ...
}

not-found.js puede estar en cualquier nivel; el más cercano se muestra.
Combinación de loading y error

Puedes tener ambos en el mismo directorio. Por ejemplo:
text

app/
├── dashboard/
│   ├── loading.js
│   ├── error.js
│   └── page.js

    Primero se muestra loading.js mientras page.js espera.

    Si ocurre un error, error.js lo captura y muestra la UI de error.

Manejo de errores en Server Actions

Los errores lanzados en Server Actions se pueden capturar en el error boundary correspondiente a la ruta donde se usó, o bien manejarlos localmente con try/catch en el Client Component.
Caché de errores

El error boundary mantiene la UI de error mientras no se llame reset(). Si se recarga la página, se reintenta el renderizado original. No hay almacenamiento en caché del error.
Migración desde Pages Router

En Pages Router tenías que implementar estados de carga manualmente (router.isFallback, estados locales para SSR). En App Router, la experiencia es declarativa, mucho más limpia y robusta.

loading.js y error.js representan uno de los mayores avances del App Router: encapsulan el comportamiento esperado de cualquier aplicación moderna con mínimo código.
02-app-router/route-handlers-app.md
Route Handlers en App Router

Los Route Handlers reemplazan a las API Routes del Pages Router dentro del App Router. Se definen en archivos route.js (o route.ts) y te permiten crear endpoints HTTP personalizados sin renderizar una página.
Configuración básica

En cualquier carpeta de app/ que no contenga page.js, puedes crear un archivo route.js. La carpeta define la ruta base y el archivo exporta funciones nombradas según el método HTTP.
js

// app/api/hello/route.js
export async function GET(request) {
  return new Response(JSON.stringify({ message: 'Hola mundo' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  })
}

Al igual que las API Routes, las rutas son servidas por Next.js y pueden coexistir con páginas, pero una carpeta no puede tener page.js y route.js simultáneamente.
Métodos HTTP soportados

Exporta funciones con los nombres de los métodos HTTP que deseas manejar: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS. Si un método no está definido, Next.js retorna 405 Method Not Allowed automáticamente.
js

export async function POST(request) {
  const body = await request.json()
  // procesar...
  return new Response(JSON.stringify({ success: true }), { status: 201 })
}

El objeto Request y Response

Los Route Handlers reciben un objeto Web Request estándar (no el req de Node.js). Esto los hace compatibles con entornos Edge y Node.

    request.url: URL completa.

    request.method: método HTTP.

    request.headers: cabeceras (tipo Headers).

    request.json(), request.formData(), etc.

    request.cookies: representación de cookies (Next.js extiende la API Web).

Puedes usar NextRequest (de next/server) que extiende Request con propiedades adicionales como nextUrl, cookies, geo (en Edge). Es útil para middleware y lógica de rutas más compleja.
js

import { NextResponse } from 'next/server'

export async function GET(request) {
  // Acceso a query params de manera fácil
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')
  // ...
  return NextResponse.json({ id })
}

NextResponse

NextResponse es la contraparte de Response de las API Web, con helpers como:

    NextResponse.json(data, options) → Response con JSON.

    NextResponse.redirect(url, status?) → Redirección.

    NextResponse.next() → Continúa con el siguiente manejador (útil en middleware).

    NextResponse.rewrite(destination) → Reescribe la URL internamente.

Segmentos dinámicos

Al igual que las páginas, las rutas pueden ser dinámicas. La carpeta [id] contendrá un route.js que recibe params en un segundo argumento.
js

// app/api/items/[id]/route.js
export async function GET(request, { params }) {
  const id = params.id
  const item = await getItem(id)
  return NextResponse.json(item)
}

Los parámetros son accesibles de forma síncrona en la firma de la función.
Middleware de ruta

Los Route Handlers permiten configurar el runtime y opciones de caché mediante el objeto config exportado (opcional):
js

export const runtime = 'edge' // 'nodejs' (por defecto)
export const dynamic = 'force-dynamic' // para que no se cachee
export const revalidate = 60 // ISR para endpoint GET (no oficial pero puede usarse)

Para un control más fino, usa la API de fetch con next.revalidate o cache: 'no-store'.
Streams y procesamiento de archivos

Puedes devolver streams directamente. Por ejemplo, para leer un archivo grande:
js

import { NextResponse } from 'next/server'

export async function GET() {
  const readableStream = new ReadableStream({...})
  return new Response(readableStream, {
    headers: { 'Content-Type': 'application/octet-stream' },
  })
}

Esto es útil para descargas, streaming de video, etc.
CORS y cabeceras personalizadas

Configura las cabeceras CORS dentro del handler o en next.config.js. Dentro del handler puedes añadir:
js

export async function GET() {
  return new Response(JSON.stringify(data), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST',
    },
  })
}

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
02-app-router/server-actions.md
Server Actions en App Router

Las Server Actions son funciones asíncronas ejecutadas en el servidor, pero que pueden ser invocadas desde Client Components o incluso desde formularios HTML sin necesidad de crear un API endpoint. Fueron introducidas como característica experimental y ahora son estables (Next.js 14+).
Definición

Una Server Action se define con la directiva 'use server' al inicio de un archivo o dentro de una función asíncrona. Pueden residir en Server Components, en archivos separados o incluso en Client Components (con restricciones).

Forma 1: Directiva en archivo independiente
js

// app/actions.js
'use server'

export async function createPost(formData) {
  const title = formData.get('title')
  // Validar y guardar en BD
  await db.post.create({ data: { title } })
  // Revalidar la página de lista
  revalidatePath('/posts')
}

Forma 2: Dentro de un Server Component
js

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

Invocación desde formularios

La forma más natural es usar el atributo action de un <form>. El navegador enviará automáticamente un POST a la Server Action si está en un Client Component y se usa con JavaScript habilitado (progressive enhancement). Sin JS, el formulario funciona igual (se ejecuta la acción en el servidor).
jsx

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

Puedes usar useFormStatus y useFormState (hooks de React DOM) para estados de carga y manejo de errores.

Ejemplo con useFormStatus:
jsx

'use client'
import { useFormStatus } from 'react-dom'

function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? 'Guardando...' : 'Guardar'}</button>
}

Acceso al request y cookies

Dentro de una Server Action puedes leer cookies y headers con las funciones de next/headers (que son dinámicas), por ejemplo:
js

import { cookies } from 'next/headers'

export async function updatePreferences(formData) {
  const cookieStore = cookies()
  const token = cookieStore.get('token')
  // ...
}

Redirecciones y manejo de errores

Puedes redirigir después de ejecutar una acción usando redirect de next/navigation:
js

import { redirect } from 'next/navigation'

export async function login(formData) {
  // verificar credenciales...
  redirect('/dashboard')
}

Para manejar errores y mostrarlos en el cliente, puedes retornar un objeto serializable desde la acción y usar useFormState (experimental) o simplemente lanzar una excepción que capture el error boundary.
Revalidación de datos

Uno de los usos principales es mutar datos y luego revalidar la caché asociada:
js

import { revalidatePath, revalidateTag } from 'next/cache'

export async function addComment(commentData) {
  await db.comment.create(...)
  revalidatePath('/posts/[slug]')  // revalida la página de ese post
  // o revalidateTag('comments')
}

Con esto, la interfaz se actualiza automáticamente sin recargar.
Invocación desde manejadores de eventos

Aunque lo común es mediante action, también puedes invocar Server Actions desde un onClick o useEffect usando la función exportada como cualquier función asíncrona normal (gracias a la integración con hooks como useTransition). Se envuelve en startTransition para manejar la navegación optimista.
jsx

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

Esto permite usar Server Actions sin formularios.
Seguridad

    Las Server Actions son endpoints POST automáticos con identificadores generados. Next.js las protege con CSRF (envía un token en un header al hacer llamadas desde el cliente). No es necesario configurarlo manualmente.

    Para acciones públicas, puedes usar headers() para verificar el origen.

    No expongas secretos en el código que se envía al cliente (todo lo exportado de un archivo con 'use server' no se filtra, solo el identificador).

Limitaciones

    Las Server Actions solo pueden ser llamadas desde el mismo proyecto (mismo origen) por defecto.

    No pueden ser usadas en componentes puros del servidor (fuera de forms/eventos), su invocación debe originarse en un Client Component o a través de action.

    El tamaño máximo del payload es 1 MB (configurable en next.config.js con serverActions.bodySizeLimit).

Cuándo usar Server Actions vs Route Handlers

    Server Actions: mutaciones estrechamente ligadas a una interfaz de usuario (formularios, likes, carritos). Ofrecen experiencia progresiva y revalidación automática.

    Route Handlers: APIs públicas, webhooks, integraciones de terceros, o cuando necesitas control total sobre códigos de estado, CORS, streaming.

Las Server Actions simplifican el patrón tradicional de crear endpoints API para cada formulario, reuniendo la lógica del servidor con la interfaz de usuario.
03-renderizado/server-side-rendering-ssr.md
Server-Side Rendering (SSR) en Next.js

El Server-Side Rendering es una técnica donde la página se genera en el servidor por cada solicitud que el cliente realiza. Next.js lo soporta de forma nativa tanto en Pages Router como en App Router, aunque con aproximaciones diferentes.
SSR en Pages Router

Se logra mediante la función getServerSideProps exportada de la página. El servidor ejecuta esta función en cada petición, obtiene datos y los pasa como props al componente. El HTML resultante se envía al navegador.
jsx

export async function getServerSideProps(context) {
  const res = await fetch(`https://...`)
  const data = await res.json()
  return { props: { data } }
}

El tiempo hasta el primer byte (TTFB) es mayor porque el servidor debe ejecutar la función antes de responder. Sin embargo, el cliente recibe HTML listo, lo que favorece el SEO y el LCP.
SSR en App Router

En el App Router no existe getServerSideProps. En su lugar, usas Server Components dinámicos con fetch sin caché o utilizando las opciones dynamic = 'force-dynamic'.

Forma 1: fetch con cache: 'no-store'
jsx

// app/dashboard/page.js
export default async function Dashboard() {
  const res = await fetch('https://...', { cache: 'no-store' })
  const data = await res.json()
  return <div>{data.content}</div>
}

Al marcar cache: 'no-store', Next.js trata la página como dinámica: se renderiza en cada solicitud (tanto en Node.js como en Edge Runtime).

Forma 2: Opciones de segmento

Exporta export const dynamic = 'force-dynamic' desde la página o layout. Esto obliga a la ruta a ser completamente dinámica.
jsx

export const dynamic = 'force-dynamic'

Forma 3: Uso de cookies o headers

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

Estrategias de caché para SSR

Incluso con SSR, puedes añadir encabezados de caché desde el servidor (Node.js) para reducir la carga.

En Pages Router:
js

export async function getServerSideProps({ res }) {
  res.setHeader('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=300')
  // ...
}

En App Router: Puedes usar el objeto response de NextResponse en Route Handlers, pero para páginas no tienes acceso directo a res. En su lugar, utiliza la función revalidate o configura el Data Cache con fetch y next.revalidate. Para SSR puro sin caché, basta con no-store. Si quieres algo intermedio, considera ISR.
¿Cuándo elegir SSR?

    Páginas muy personalizadas (dashboard de usuario con datos en vivo).

    Aplicaciones donde cada usuario ve contenido distinto y esos datos no se pueden compartir.

    Funcionalidades que requieren lectura de cookies/headers de manera directa.

En proyectos reales, rara vez todo es SSR; Next.js te permite mezclar SSG, ISR y SSR según la página.
03-renderizado/static-generation-ssg.md
Static Site Generation (SSG) en Next.js

La generación de sitios estáticos implica pre-renderizar las páginas en tiempo de compilación (next build). El resultado son archivos HTML (y JSON para transiciones del lado del cliente) que pueden servirse directamente desde un CDN.
SSG en Pages Router

Se logra con la función getStaticProps (y getStaticPaths para rutas dinámicas). La página se construye una vez y se sirve estáticamente, lo que garantiza el mejor rendimiento posible y excelente SEO.
jsx

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

SSG en App Router

En el App Router, los Server Components son estáticos por defecto cuando no utilizan fuentes de datos dinámicas (es decir, si no contienen cookies(), headers(), o fetch con cache: 'no-store'). Durante el build, Next.js renderiza esas rutas y las guarda como archivos estáticos.

No necesitas exportar funciones especiales; solo escribe un Server Component normal que obtenga datos sin forzar dinamismo:
jsx

// app/about/page.js
export default function About() {
  return <h1>Acerca de Nosotros</h1>
}

Para contenido que proviene de una API externa:
jsx

export default async function Blog() {
  const posts = await fetch('https://api.../posts') // sin cache: 'no-store'
  const data = await posts.json()
  return <>{data.map(...)}</>
}

Al no indicar cache: 'no-store', fetch usa el comportamiento predeterminado de caché (force-cache). Entonces Next.js hará la solicitud en build, cacheará el resultado (Data Cache) y generará HTML estático. Si necesitas regenerar ese contenido más adelante, configura ISR con next.revalidate.
Rutas dinámicas estáticas

En App Router, si necesitas pre-renderizar rutas dinámicas, debes generar los parámetros estáticos usando generateStaticParams.
jsx

// app/blog/[slug]/page.js
export default function BlogPost({ params }) { ... }

export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then(res => res.json())
  return posts.map(post => ({ slug: post.slug }))
}

generateStaticParams reemplaza a getStaticPaths. Solo los slugs devueltos serán pre-renderizados en build. Por defecto, dynamicParams = true, lo que significa que cualquier ruta no generada en build se renderizará bajo demanda (como SSR) y luego se cacheará. Puedes cambiar a dynamicParams = false para que las rutas no pre-renderizadas devuelvan 404.
Ventajas del SSG

    Velocidad: El HTML es servido desde CDN (tiempo de respuesta casi instantáneo).

    Escalabilidad: Sin carga en el servidor por petición.

    SEO óptimo: Los motores de búsqueda reciben todo el contenido.

Desventajas

    Tiempo de build más largo para muchos miles de páginas (aunque generateStaticParams y el renderizado de build pueden demorar).

    Contenido desactualizado si no implementas ISR.

Combinación con ISR

Para obtener lo mejor de ambos mundos, puedes agregar revalidate a tus fetch o configurarlo en el segmento. Así la página se vuelve estática pero se regenera en segundo plano a intervalos definidos. (Esto se trata en profundidad en el siguiente capítulo).
¿Cuándo usar SSG?

    Blogs, portafolios, documentación.

    Páginas de producto donde el contenido no cambia con cada visita.

    Cualquier página que no dependa de datos personalizados en cada solicitud.

Si alguna parte de la página necesita interactividad o personalización, se puede implementar con Client Components que obtengan datos adicionales en el cliente, mientras el esqueleto estático se entrega casi instantáneamente.
03-renderizado/incremental-static-regeneration-isr.md
Incremental Static Regeneration (ISR)

ISR permite actualizar páginas estáticas después del build sin necesidad de reconstruir todo el sitio. Next.js regenera la página en segundo plano cuando ocurre una solicitud después de que el tiempo revalidate ha expirado.
ISR en Pages Router

Se configura mediante la propiedad revalidate en el objeto retornado por getStaticProps.
jsx

export async function getStaticProps() {
  const res = await fetch('https://.../posts')
  const posts = await res.json()

  return {
    props: { posts },
    revalidate: 60, // regenerar como máximo cada 60 segundos
  }
}

    La primera solicitud después del build servirá la página estática generada.

    Tras 60 segundos, la siguiente solicitud todavía sirve la versión anterior (stale), pero dispara una regeneración en segundo plano.

    La solicitud que activó la regeneración podría ver la versión antigua (o nueva con una bandera de stale) dependiendo de la estrategia.

    Una vez completada la regeneración, Next.js actualiza la caché y las siguientes peticiones verán la nueva versión.

ISR con fallback en rutas dinámicas

Para rutas dinámicas con getStaticPaths, puedes combinar fallback: true o 'blocking' con revalidate. Así, las páginas no pre-renderizadas se generan bajo demanda (como ISR inicial) y luego se regeneran según revalidate.
ISR en App Router

En el App Router, la ISR se configura a nivel de fetch o por segmento de ruta.

Opción 1: fetch con next.revalidate
jsx

// app/products/page.js
export default async function Products() {
  const res = await fetch('https://.../products', { next: { revalidate: 60 } })
  const products = await res.json()
  return <ProductList products={products} />
}

Next.js almacenará en caché la respuesta de fetch (Data Cache) por 60 segundos. La página se servirá estáticamente, pero se actualizará la data en background si hay una solicitud que lo requiere después del período.

Opción 2: Segment config revalidate

Exporta una constante revalidate desde la página o layout:
jsx

export const revalidate = 60

Esto establece el revalidate para toda la ruta. Si además usas fetch sin especificar revalidate, hereda este valor.

Opción 3: Revalidación bajo demanda (On-demand revalidation)

Además de revalidación por tiempo, puedes regenerar páginas específicas mediante revalidación por etiqueta o ruta usando Server Actions o Route Handlers.

    revalidatePath('/products') – revalida una ruta completa.

    revalidateTag('products') – revalida todos los fetch que tengan ese tag.

Ejemplo con fetch etiquetado:
jsx

const res = await fetch('https://...', { next: { tags: ['products'] } })

Luego, desde una Server Action después de una mutación:
jsx

import { revalidateTag } from 'next/cache'

export async function updateProduct() {
  // ... actualizar
  revalidateTag('products')
}

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

Caso de uso típico

Un blog con miles de artículos. Generas las páginas más populares en build, el resto con fallback: 'blocking'. Todas las páginas se regeneran si son visitadas después de 3600 segundos (revalidate: 3600). Cuando el autor edita un artículo, se activa una revalidación bajo demanda vía webhook, actualizando solo esa página.

ISR te da lo mejor de SSG y SSR: velocidad estática con contenido casi en tiempo real.
03-renderizado/streaming-y-suspense.md
Streaming y Suspense en Next.js

El streaming es una técnica que permite al servidor enviar partes del HTML al cliente a medida que se generan, en lugar de esperar a que toda la página esté lista. Next.js lo implementa usando React Suspense y los Server Components, permitiendo una carga progresiva y mejores métricas.
Cómo funciona en Next.js

Cuando un Server Component se suspende (porque está esperando una promesa), Next.js no bloquea toda la respuesta. En su lugar, envía el shell de la aplicación (los layouts y componentes que ya están listos) y luego, a medida que los datos se resuelven, envía el HTML restante en el mismo stream HTTP.

El navegador puede empezar a pintar el HTML parcial inmediatamente, reduciendo el Time to First Byte (TTFB) y el First Contentful Paint (FCP).
Implementación con loading.js

La forma más simple de habilitar streaming es crear un archivo loading.js en el segmento que tarda. loading.js se convierte en el fallback de Suspense para esa ruta.

Estructura básica:
text

app/
├── layout.js
└── posts/
    ├── page.js        (obtiene datos lentos)
    └── loading.js     (UI de carga)

Cuando se visita /posts, Next.js envía inmediatamente el layout (que ya está listo) y muestra loading.js dentro del área de posts. Una vez que page.js termina de obtener los datos, el HTML del componente se envía y reemplaza el loading.

Internamente: Next.js envuelve la página en un <Suspense fallback={<Loading />}>. Por eso el streaming funciona incluso fuera de loading.js si usas Suspense manualmente.
Suspense manual para mayor granularidad

Puedes envolver partes específicas de una página en <Suspense> para controlar exactamente qué se streamea primero.
jsx

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
