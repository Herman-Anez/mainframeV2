# SEO con `<Head>` en Pages Router

En el **Pages Router**, la gestión de metaetiquetas, títulos y otros elementos del `<head>` se realiza mediante el componente `<Head>` proporcionado por `next/head`. Aunque es sencillo, requiere ciertas prácticas para asegurar un SEO sólido y consistente.

## Uso básico de `<Head>`

Importa `Head` desde `next/head` y añádelo a tu componente de página. Puedes usarlo en cualquier parte del árbol de componentes, pero se recomienda definirlo en el nivel superior de cada página.

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
      <main>Contenido de la página...</main>
    </>
  )
}
```

## Fusión de múltiples componentes `<Head>`

Si tienes un `<Head>` en `_app.js` (global) y otro en una página específica, Next.js fusiona el contenido. Las claves duplicadas (como `title`) serán sobrescritas por la última definición encontrada.

**`_app.js` (Metadatos por defecto):**
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

> [!NOTE]
> Al navegar a una página que define su propio `<title>`, este sobrescribirá el valor de `_app.js`, permitiendo personalización granular manteniendo valores globales por defecto.

---

## Etiquetas esenciales para SEO

| Etiqueta | Propósito |
| :--- | :--- |
| **`title`** | El título que aparece en la pestaña y resultados de búsqueda. |
| **`description`** | Resumen que influye en el CTR de los resultados. |
| **`robots`** | Controla la indexación (`index, follow` o `noindex, nofollow`). |
| **`canonical`** | Indica la URL original para evitar penalizaciones por contenido duplicado. |
| **Open Graph** | Etiquetas `og:*` para optimizar la apariencia en redes sociales. |
| **Twitter Cards** | Etiquetas `twitter:*` para la visualización en X/Twitter. |

---

## Contenido Dinámico

Cuando los datos de la página provienen de `getServerSideProps` o `getStaticProps`, úsalos para inyectar metadatos dinámicos.

```jsx
export default function Articulo({ articulo }) {
  return (
    <>
      <Head>
        <title>{articulo.titulo} - Mi Blog</title>
        <meta name="description" content={articulo.extracto} />
        <meta property="og:image" content={articulo.imagen} />
        <link rel="canonical" href={`https://misitio.com/blog/${articulo.slug}`} />
      </Head>
      <article>{/* ... */}</article>
    </>
  )
}
```

---

## Idioma y Estructura Global

El atributo `lang` de la etiqueta `<html>` solo puede definirse en `pages/_document.js`.

```jsx
// pages/_document.js
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

> [!IMPORTANT]
> Definir el idioma correctamente es vital para la accesibilidad y para que los motores de búsqueda clasifiquen el contenido geográficamente de forma adecuada.

---

## Datos Estructurados (JSON-LD)

Mejora la apariencia de tus resultados (Rich Snippets) insertando scripts de datos estructurados.

```jsx
<Head>
  <script
    type="application/ld+json"
    dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdData) }}
  />
</Head>
```

> [!TIP]
> Usa siempre `dangerouslySetInnerHTML` para asegurar que el JSON se renderice correctamente como un bloque de script en el servidor.

---

## Buenas prácticas

1.  **Unicidad:** Cada página debe tener un título y una descripción únicos.
2.  **Imágenes OG:** Utiliza siempre imágenes de **1200x630px** para asegurar compatibilidad con todas las plataformas sociales.
3.  **Canonical:** Implementa enlaces canónicos especialmente si utilizas parámetros de búsqueda o seguimiento en tus URLs.
4.  **Robots:** Asegúrate de usar `noindex` en entornos de desarrollo o páginas de administración privadas.

---

Con estas técnicas, el Pages Router proporciona una base sólida para el SEO, permitiendo un control total sobre el comportamiento de búsqueda de tu aplicación.