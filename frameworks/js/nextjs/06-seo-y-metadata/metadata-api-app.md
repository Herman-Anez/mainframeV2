# API de Metadata en App Router

El **App Router** revoluciona la gestión de SEO y metaetiquetas mediante una **API de Metadata declarativa**. En lugar de usar un componente `<Head>`, exportas un objeto `metadata` o una función `generateMetadata` desde `layout.js` o `page.js`. Next.js se encarga de inyectar automáticamente estas etiquetas en el `<head>` del HTML.

## Metadata Estática

Para datos fijos, exporta un objeto llamado `metadata` en cualquier archivo `page.js` o `layout.js`.

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
  return <html lang="es"><body>{children}</body></html>
}
```

> [!NOTE]
> No necesitas importar componentes adicionales; la exportación de `metadata` es suficiente para que Next.js la procese e inyecte en el servidor.

## Metadata Dinámica con `generateMetadata`

Cuando los metadatos dependen de datos dinámicos (ej. un post de blog), exporta la función asíncrona `generateMetadata`. Esta función recibe los mismos parámetros que la página: `params` y `searchParams`.

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
```

> [!TIP]
> Next.js **deduplica** automáticamente las solicitudes `fetch` realizadas tanto en `generateMetadata` como en el componente de la página, por lo que no hay penalización de rendimiento al realizar la misma consulta en ambos lugares.

## Herencia y Plantillas de Título

Los metadatos se heredan jerárquicamente. Puedes definir una plantilla de título en el layout raíz para que todas las subpáginas sigan un formato consistente.

**En `app/layout.tsx`:**
```tsx
export const metadata: Metadata = {
  title: {
    template: '%s - Mi Blog',
    default: 'Mi Blog', // Usado si la página no define un título
  },
}
```

**En `app/blog/[slug]/page.tsx`:**
```tsx
export async function generateMetadata({ params }) {
  const articulo = await obtenerArticulo(params.slug)
  return {
    title: articulo.titulo, // Resulta en: "Título del Artículo - Mi Blog"
  }
}
```

---

## Metadatos basados en archivos

Puedes añadir archivos especiales en las carpetas de `app/` que Next.js detectará y servirá automáticamente:

*   **`favicon.ico`**: Icono del sitio.
*   **`icon.png`**, **`icon.jpg`**: Iconos en formatos alternativos.
*   **`apple-icon.png`**: Icono específico para dispositivos iOS.
*   **`opengraph-image.png`**: Imagen por defecto para Open Graph.
*   **`twitter-image.png`**: Imagen para Twitter Cards.
*   **`sitemap.xml`**: Mapa del sitio (puede generarse dinámicamente con `sitemap.ts`).
*   **`robots.txt`**: Reglas para rastreadores (puede generarse con `robots.ts`).

---

## Comparación con `<Head>` del Pages Router

| Característica | Pages Router | App Router |
| :--- | :--- | :--- |
| **Definición** | Componente `<Head>` | Exportación de objeto o función |
| **Herencia** | Manual | Automática y jerárquica |
| **Datos Dinámicos** | Props pasadas al componente | `generateMetadata` asíncrono |
| **Imágenes OG** | URL manual en etiqueta | Archivos dedicados o generación dinámica |
| **Rendimiento** | Se envía en el bundle de cliente | Inyectado en servidor, **cero JS extra** |

---

La API de Metadata del App Router es más potente, segura y fácil de mantener, eliminando la necesidad de gestionar etiquetas `head` manualmente en aplicaciones complejas.
