
## Archivo: `09-deploy-y-configuracion/export-estatico.md`

Exportación estática (Static HTML Export)

La exportación estática genera un sitio compuesto únicamente por HTML, CSS, JavaScript y archivos estáticos, sin necesidad de servidor Node.js. Es ideal para alojar en GitHub Pages, S3, Netlify (como sitio estático), o cualquier CDN.
Configuración

En next.config.js, habilita el modo exportación:
```js
```
module.exports = {
  output: 'export',
}

Opcionalmente, define la ruta base si el sitio no se sirve desde la raíz:
```js
```
basePath: '/mi-proyecto',

### Comando de construcción

Ejecuta:
```bash
```
npm run build

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
```
images: {
  loader: 'custom',
  loaderFile: './loader.js',
},

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
