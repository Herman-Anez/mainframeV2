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
