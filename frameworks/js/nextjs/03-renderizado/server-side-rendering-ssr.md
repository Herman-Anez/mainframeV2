# Server-Side Rendering (SSR) en Next.js

El **Server-Side Rendering (SSR)** es una técnica donde la página se genera en el servidor por cada solicitud que el cliente realiza. Next.js lo soporta de forma nativa tanto en **Pages Router** como en **App Router**, aunque con aproximaciones diferentes.

## SSR en Pages Router

Se logra mediante la función `getServerSideProps` exportada de la página. El servidor ejecuta esta función en cada petición, obtiene datos y los pasa como props al componente. El HTML resultante se envía al navegador.

```jsx
export async function getServerSideProps(context) {
  const res = await fetch(`https://api.example.com/data`)
  const data = await res.json()
  
  return { 
    props: { data } 
  }
}
```

> [!NOTE]
> El tiempo hasta el primer byte (**TTFB**) es mayor porque el servidor debe ejecutar la función antes de responder. Sin embargo, el cliente recibe HTML listo, lo que favorece el SEO y el **LCP** (Largest Contentful Paint).

## SSR en App Router

En el App Router no existe `getServerSideProps`. En su lugar, usas **Server Components** dinámicos configurando el comportamiento de `fetch` o las opciones de segmento.

### Forma 1: `fetch` con `cache: 'no-store'`

```jsx
// app/dashboard/page.js
export default async function Dashboard() {
  const res = await fetch('https://api.example.com/stats', { 
    cache: 'no-store' 
  })
  const data = await res.json()
  
  return <div>{data.content}</div>
}
```

Al marcar `cache: 'no-store'`, Next.js trata la página como dinámica: se renderiza en cada solicitud (tanto en Node.js como en Edge Runtime).

### Forma 2: Opciones de segmento (`force-dynamic`)

Exporta `export const dynamic = 'force-dynamic'` desde la página o layout para obligar a la ruta a ser completamente dinámica.

```jsx
export const dynamic = 'force-dynamic'
```

### Forma 3: Uso de funciones dinámicas

Si el componente utiliza `cookies()` o `headers()` de `next/headers`, la ruta automáticamente se vuelve dinámica, ya que estos datos dependen intrínsecamente de la solicitud entrante.

## Diferencia entre SSR y "dinámico" en App Router

En App Router, "dinámico" no es un interruptor global, sino que se determina por el comportamiento de la ruta. Si la ruta no usa fuentes dinámicas, seguirá siendo estática por defecto. Esto permite un **renderizado híbrido**: puedes tener partes estáticas y partes dinámicas en el mismo layout gracias al **streaming**.

---

## Ventajas y Desventajas del SSR

### Ventajas:
*   **Contenido en tiempo real:** Ideal para personalización, sesiones de usuario y noticias recientes.
*   **SEO Óptimo:** El contenido está disponible para los rastreadores sin necesidad de ejecutar JavaScript en el cliente.
*   **Datos cambiantes:** Adecuado para información que se actualiza con frecuencia.

### Desventajas:
*   **Carga del servidor:** Cada petición ejecuta lógica en el servidor, aumentando el consumo de recursos.
*   **Latencia:** El tiempo de respuesta es más alto comparado con el contenido estático servido desde una CDN.
*   **Escalabilidad:** Más complejo de escalar al no ser cacheable directamente en CDN sin configuración adicional.

---

## Estrategias de caché para SSR

Incluso con SSR, puedes añadir encabezados de caché desde el servidor para reducir la carga.

**En Pages Router:**
```javascript
export async function getServerSideProps({ res }) {
  res.setHeader(
    'Cache-Control',
    'public, s-maxage=60, stale-while-revalidate=300'
  )
  // ...
}
```

**En App Router:**
Utiliza la función `revalidate` o configura el **Data Cache** con `fetch` y `next.revalidate`. Para SSR puro sin caché, basta con `no-store`. Si buscas un punto intermedio, considera **ISR**.

## ¿Cuándo elegir SSR?

1.  **Páginas personalizadas:** Dashboards de usuario con datos en vivo y privados.
2.  **Contenido único por usuario:** Aplicaciones donde cada usuario ve contenido distinto que no se puede compartir en caché global.
3.  **Acceso a Headers/Cookies:** Funcionalidades que requieren lectura directa de las cabeceras de la petición.

---

En proyectos reales, rara vez todo es SSR; Next.js permite mezclar **SSG**, **ISR** y **SSR** de manera granular según las necesidades de cada página.
