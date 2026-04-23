# Internacionalización (i18n) en Pages Router

El **Pages Router** ofrece soporte de internacionalización nativo desde la versión 10 de Next.js. A diferencia del App Router, no requiere configuraciones manuales de middleware para el enrutamiento básico, aunque las traducciones siguen dependiendo de librerías externas.

## Configuración en `next.config.js`

La clave es la propiedad `i18n`, donde defines los idiomas soportados y el idioma predeterminado.

```js
// next.config.js
module.exports = {
  i18n: {
    locales: ['es', 'en', 'fr'],
    defaultLocale: 'es',
    localeDetection: true, // Habilitado por defecto
  },
}
```

### Funcionalidades automáticas:
*   **Enrutamiento por prefijo:** Genera rutas automáticamente como `/es`, `/en`, `/fr`.
*   **Detección de idioma:** Identifica el idioma del navegador mediante la cabecera `Accept-Language` y redirige al usuario en su primera visita.
*   **Redirección raíz:** La ruta raíz `/` redirige automáticamente al `defaultLocale`.

---

## Estrategias de Enrutamiento

### 1. Sub-rutas (Por defecto)
Las URLs se ven así:
*   `https://misitio.com/es/sobre-nosotros`
*   `https://misitio.com/en/about-us`

### 2. Dominios específicos
Puedes asignar un dominio único a cada idioma:

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

> [!IMPORTANT]
> El enrutamiento por dominios requiere que todos los dominios apunten al mismo servidor y tengan certificados SSL configurados correctamente.

---

## Acceso al Idioma en la Aplicación

### En el Servidor (`getServerSideProps` / `getStaticProps`)
El objeto `context` incluye las propiedades `locale`, `locales` y `defaultLocale`.

```js
export async function getStaticProps({ locale }) {
  const contenido = await obtenerDatosSegunIdioma(locale)
  return { 
    props: { contenido } 
  }
}
```

### En el Cliente (`useRouter`)
Usa el hook `useRouter` para acceder al estado de internacionalización.

```jsx
import { useRouter } from 'next/router'

export default function MiPagina() {
  const { locale, locales } = useRouter()
  return <p>Idioma actual: {locale}</p>
}
```

---

## Navegación y Cambio de Idioma

El componente `<Link>` y la función `router.push` manejan el idioma actual de forma automática.

**Navegación normal:**
```jsx
<Link href="/contacto">
  <a>Contacto</a>
</Link>
// Renderiza <a href="/es/contacto"> si el idioma actual es 'es'
```
### Navegación con Link y router

El componente Link y el router manejan automáticamente el prefijo de idioma basado en el locale actual.
```jsx
```
<Link href="/about">
  <a>Acerca de</a>
</Link>
// Renderiza <a href="/es/about"> (si locale es 'es')

// Cambiar de idioma explícitamente:
<Link href="/about" locale="en">
  <a>English</a>
</Link>

Con useRouter:
```js
```
router.push('/about', undefined, { locale: 'en' })

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

- next-i18next: basada en i18next, carga archivos JSON por idioma.

- next-translate: minimalista, usa archivos JSON en locales/[lang]/....
- react-intl / Format.js: más completo para aplicaciones complejas.

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

- Con SSR (getServerSideProps) y locales, la URL siempre tiene prefijo. El lenguaje lo obtienes del contexto.

- Si necesitas evitar el prefijo para el idioma por defecto (que / sirva es), Next.js no lo permite para el Pages Router; siempre hay prefijo. Muchos optan por redirecciones personalizadas.

- Los archivos _document.js y _app.js también pueden acceder al locale.

**Cambio de idioma explícito:**
```jsx
<Link href="/contacto" locale="en">
  <a>Switch to English</a>
</Link>
```

---

## Traducciones con Librerías Externas

Como Next.js solo maneja el enrutamiento, necesitarás una librería para los textos. Las más comunes son:

*   **`next-i18next`**: La más robusta, basada en el popular framework `i18next`.
*   **`next-translate`**: Opción minimalista y ligera.
*   **`react-intl`**: Parte del ecosistema FormatJS, ideal para aplicaciones empresariales.

> [!TIP]
> Para la mayoría de proyectos en Pages Router, **`next-i18next`** es la opción estándar debido a su madurez y facilidad de integración con las funciones de Next.js.

---

El soporte nativo de i18n en el Pages Router simplifica drásticamente el enrutamiento multilingüe, permitiendo que te concentres en la lógica de las traducciones sin preocuparte por la gestión manual de las URLs.
