# Patrones de obtención de datos en Pages Router

En el **Pages Router** de Next.js, la obtención de datos puede ocurrir en el servidor (SSR, SSG) o en el cliente. La elección del patrón adecuado determina el rendimiento, el SEO y la experiencia de usuario final.

---

## Obtención de datos en el servidor

### 1. `getServerSideProps` (SSR)
Se ejecuta en cada solicitud. Es ideal para datos que cambian frecuentemente o que son personalizados para el usuario actual.

```jsx
export async function getServerSideProps(context) {
  const res = await fetch(`https://api.ejemplo.com/productos`)
  const productos = await res.json()
  
  return { 
    props: { productos } 
  }
}
```

**Patrones comunes:**
*   **Cacheo con cabeceras HTTP:** Agrega encabezados de caché para que las respuestas sean almacenadas por CDNs o proxies.
    ```js
    res.setHeader('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=300')
    ```
*   **Personalización:** Lee cookies o cabeceras para adaptar la respuesta al usuario.
*   **Manejo de errores:** Usa `redirect` o `notFound` para gestionar accesos no autorizados o contenido faltante.

### 2. `getStaticProps` (SSG)
Se ejecuta en tiempo de compilación. Genera páginas estáticas altamente optimizadas.

```jsx
export async function getStaticProps() {
  const res = await fetch('https://api.ejemplo.com/posts')
  const posts = await res.json()
  
  return { 
    props: { posts }, 
    revalidate: 3600 // ISR (opcional)
  }
}
```

**Patrones comunes:**
*   **Fetching Paralelo:** Realiza múltiples llamadas simultáneas con `Promise.all`.
*   **ISR (Incremental Static Regeneration):** Regenera la página periódicamente sin necesidad de un nuevo build.

### 3. `getStaticPaths` (Rutas dinámicas)
Controla qué rutas se generan estáticamente durante el build.

```jsx
export async function getStaticPaths() {
  return {
    paths: [{ params: { id: '1' } }],
    fallback: 'blocking'
  }
}
```

*   **`fallback: false`**: Solo las rutas listadas funcionan; otras dan 404.
*   **`fallback: true`**: Genera rutas faltantes bajo demanda mostrando un estado de carga.
*   **`fallback: 'blocking'`**: Espera la generación en el servidor (mejor para SEO).

---

## Obtención de datos en el cliente

Para datos que no necesitan SEO o dependen de la interacción del usuario, se obtienen directamente desde el navegador.

### Uso básico con `useEffect`
```jsx
useEffect(() => {
  fetch('/api/usuario')
    .then(res => res.json())
    .then(data => setUsuario(data))
}, [])
```

> [!CAUTION]
> El fetching en cliente no tiene SEO para el contenido cargado y puede penalizar el **LCP** (Largest Contentful Paint) si no se maneja con cuidado.

### SWR y React Query (Recomendado)
Estas librerías gestionan de forma eficiente la caché, revalidación y estados de carga.

```jsx
import useSWR from 'swr'

const { data, error } = useSWR('/api/usuario', fetcher)
```

---

## Patrones Híbridos

Combina la velocidad del servidor con la interactividad del cliente.

1.  Carga la estructura inicial con `getStaticProps` o `getServerSideProps`.
2.  Hidrata la página y usa **SWR** para mantener los datos actualizados.

```jsx
export default function Productos({ productosIniciales }) {
  const { data: productos } = useSWR('/api/productos', fetcher, { 
    fallbackData: productosIniciales 
  })
  return <ul>{/* ... renderizar productos */}</ul>
}
```

---

## Prefetching y Precarga

*   **Link Prefetching:** El componente `<Link>` precarga automáticamente las páginas vinculadas.
*   **Prefetch Manual:** `router.prefetch(url)` permite preparar la caché del cliente ante una acción inminente.

---

## Resumen de criterios de elección

| Método | Cuándo usarlo |
| :--- | :--- |
| **`getStaticProps`** | Datos compartidos que no cambian por usuario. |
| **`getServerSideProps`** | Datos personalizados o que cambian en cada solicitud. |
| **Cliente (SWR/Query)** | Datos post-interacción o que no requieren SEO. |
| **Híbrido** | Carga inicial rápida con actualizaciones dinámicas posteriores. |

---

Dominar estos patrones te permitirá construir aplicaciones rápidas, escalables y optimizadas para buscadores en el Pages Router.
