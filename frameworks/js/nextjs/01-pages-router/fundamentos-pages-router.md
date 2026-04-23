## 📘 01-pages-router/fundamentos-pages-router.md

### Fundamentos del Pages Router

El Pages Router fue el sistema de enrutamiento original de Next.js. Se basa en la carpeta `pages/`: cada archivo `.js`, `.jsx`, `.ts` o `.tsx` dentro de ella se convierte automáticamente en una ruta accesible.

#### Rutas basadas en archivos

| Estructura de archivo | Ruta resultante |
| :--- | :--- |
| `pages/index.js` | `/` (raíz) |
| `pages/about.js` | `/about` |
| `pages/blog/index.js` | `/blog` |
| `pages/blog/first.js` | `/blog/first` |

Los archivos deben exportar por defecto un componente React. Next.js se encarga de envolverlo con el renderizado adecuado y el encabezado HTML base.

#### Componente `_app.js`

Permite personalizar la inicialización de las páginas. Es el componente que envuelve a todas las páginas. Se usa para:

- Mantener estados globales (contextos, providers).
- Agregar layouts comunes.
- Inyectar estilos globales.

**Ejemplo básico:**

```jsx
import '../styles/globals.css'

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}
```

#### Componente `_document.js`

Sirve para modificar la estructura del documento HTML (`<html>`, `<body>`). Solo se renderiza en el servidor. Útil para añadir fuentes, atributos `lang`, etc. No debe contener lógica de aplicación.

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

#### Páginas de error personalizadas

- `pages/404.js`: Se muestra automáticamente para rutas no encontradas.
- `pages/_error.js`: Error genérico (500, etc.). Puede recibir `statusCode`.

#### Enlaces y navegación

Usa el componente `Link` de `next/link` para navegación entre páginas sin recargar completamente el navegador (client-side routing). Se precargan automáticamente cuando el enlace entra al viewport.

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

#### Estilos

Next.js soporta:

- **CSS Modules:** Archivos `[nombre].module.css` importables en componentes.
- **SASS:** (instalando `sass`).
- **CSS-in-JS:** (`styled-components`, `emotion`) con configuración extra.
- **Tailwind CSS:** (recomendado en instalación).

> [!NOTE]
> Con el Pages Router tienes una base sólida para cualquier aplicación tradicional de React con renderizado híbrido.

---
