# Exportación Estática (Static HTML Export)

La exportación estática genera un sitio compuesto únicamente por HTML, CSS, JavaScript y archivos estáticos, sin necesidad de un servidor Node.js. Es ideal para alojar en GitHub Pages, S3, Netlify (como sitio estático), o cualquier CDN.

## Configuración

En `next.config.js`, habilita el modo exportación:

```javascript
// next.config.js
module.exports = {
  output: 'export',
  // Opcional: define la ruta base si el sitio no se sirve desde la raíz
  // basePath: '/mi-proyecto',
}
```

### Comando de Construcción

Al ejecutar el build, Next.js generará automáticamente la salida estática:

```bash
npm run build
```

Next.js creará una carpeta `out/` con el sitio estático listo para desplegar. La estructura resultante incluye:

*   **`out/index.html`**: Para la ruta `/`.
*   **`out/about.html`**: Para la ruta `/about`.
*   **`out/posts/[id].html`**: Para rutas dinámicas pre-renderizadas.
*   **`out/_next/static/`**: Contiene los bundles JS y CSS.
*   **`out/images/...`**: Archivos provenientes de la carpeta `public/`.

---

## Limitaciones de la Exportación Estática

Al no contar con un servidor Node.js en tiempo de ejecución, las siguientes funcionalidades **no están disponibles**:

*   **Rutas de API**: (`pages/api/` o Route Handlers).
*   **getServerSideProps**: Se debe utilizar exclusivamente `getStaticProps`.
*   **ISR con revalidate**: La página será estática al momento del build.
*   **Middleware**: No hay entorno de ejecución para interceptar peticiones.
*   **Server Actions y Streaming**: Requieren un servidor activo.
*   **Cookies**: No se pueden leer en `getStaticProps` ya que no hay un objeto `req`.

> [!WARNING]
> **Optimización de Imágenes**: El componente `next/image` con el loader por defecto requiere un servidor. En exportación estática, debes usar un loader externo o la propiedad `unoptimized`.

---

## Rutas Dinámicas

Debes pre-renderizar todas las rutas posibles en tiempo de construcción.

### En Pages Router (`getStaticPaths`)
```javascript
export async function getStaticPaths() {
  const posts = await fetchPosts()
  const paths = posts.map(post => ({ params: { id: post.id } }))
  return { paths, fallback: false } // false asegura que rutas no generadas den 404
}
```

### En App Router (`generateStaticParams`)
Al definir `generateStaticParams`, Next.js exportará cada ruta como un archivo HTML independiente durante el build.

---

## Manejo de Imágenes

Para usar `next/image` en sitios estáticos, tienes estas opciones:

1.  **Imágenes sin optimizar**: Añade `unoptimized` al componente: `<Image ... unoptimized />`.
2.  **Loader Personalizado**: Configura un archivo para gestionar las URLs de las imágenes.

```javascript
// next.config.js
images: {
  loader: 'custom',
  loaderFile: './loader.js',
}

// loader.js
export default function myLoader({ src, width, quality }) {
  return `https://mi-cdn.com/${src}?w=${width}&q=${quality || 75}`
}
```

---

## Despliegue de la carpeta `out`

Puedes servir el contenido de la carpeta `out/` con cualquier servidor HTTP o plataforma de hosting estático:

*   **GitHub Pages**: Ideal para documentación o demos. Requiere configurar el `basePath` si el repo no es de usuario.
*   **Netlify / Vercel**: Soporte nativo para exportaciones estáticas.
*   **AWS S3 + CloudFront**: Escalabilidad masiva para sitios estáticos con baja latencia global.

---

## ¿Cuándo elegir Exportación Estática?

*   **Sitios de contenido puro**: Blogs, portafolios, landing pages.
*   **Costo Mínimo**: Alojamiento en CDNs o almacenamiento de objetos extremadamente barato.
*   **Seguridad**: No hay servidor Node.js que atacar, reduciendo la superficie de vulnerabilidad.

> [!IMPORTANT]
> Es la opción más simple y escalable, pero sacrifica todas las capacidades dinámicas y bajo demanda de Next.js.

---
[<- Anterior: Dockerizar Next.js](dockerizar.md) | [Siguiente: Testing ->](../10-testing/testing-pages-router.md)
