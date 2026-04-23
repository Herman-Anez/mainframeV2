# Internacionalización (i18n) en App Router

En el **App Router**, Next.js no incluye el enrutamiento i18n nativo del Pages Router. En su lugar, se recomienda implementar i18n mediante **middleware** y un segmento dinámico `[locale]` en la estructura de archivos, apoyándose en librerías robustas como `next-intl`.

## Estrategia Principal

1.  **Carpeta Dinámica:** Estructurar el proyecto dentro de `app/[locale]/...`.
2.  **Detección:** Usar un middleware para identificar el idioma del usuario (vía URL, cookies o cabeceras) y redirigir si es necesario.
3.  **Traducciones:** Cargar los mensajes en **Server Components** y ofrecer un Provider para los **Client Components**.

### Configuración con `next-intl` (Recomendado)

```bash
npm install next-intl
```

**Estructura del Proyecto:**
```text
app/
├── [locale]/
│   ├── layout.tsx
│   └── page.tsx
├── layout.tsx        (Opcional, para redirección inicial)
├── middleware.ts
└── i18n.ts           (Configuración central)
messages/             (Traducciones JSON)
├── en.json
└── es.json
```

---

## Implementación Técnica

### 1. Configuración de Carga (`i18n.ts`)
```ts
import { getRequestConfig } from 'next-intl/server'

export default getRequestConfig(async ({ locale }) => ({
  messages: (await import(`./messages/${locale}.json`)).default,
}))
```

### 2. Middleware de Enrutamiento
```ts
import createMiddleware from 'next-intl/middleware'

export default createMiddleware({
  locales: ['es', 'en'],
  defaultLocale: 'es',
  localeDetection: true,
})

export const config = {
  // Ignorar rutas internas (api, static, etc.)
  matcher: ['/((?!api|_next|_vercel|.*\\..*).*)'],
}
```

### 3. Layout Localizado (`app/[locale]/layout.tsx`)
```tsx
import { NextIntlClientProvider } from 'next-intl'
import { getMessages } from 'next-intl/server'

export default async function LocaleLayout({ children, params: { locale } }) {
  const messages = await getMessages()

  return (
    <html lang={locale}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
```

---

## Uso de Traducciones

### En Server Components
```tsx
import { getTranslations } from 'next-intl/server'

export default async function HomePage() {
  const t = await getTranslations('Home')
  return <h1>{t('title')}</h1>
}
```

### En Client Components
```tsx
'use client'
import { useTranslations } from 'next-intl'

export function ClientComponent() {
  const t = useTranslations('Home')
  return <button>{t('cta')}</button>
}
```

---

## Generación de Metadatos y SSG

### Metadatos Dinámicos
```tsx
export async function generateMetadata({ params: { locale } }) {
  const t = await getTranslations({ locale, namespace: 'Metadata' })
  return {
    title: t('title'),
    description: t('description'),
  }
}
```

### Pre-renderizado Estático (SSG)
Usa `generateStaticParams` para generar todas las versiones de idioma en tiempo de compilación.
```tsx
export async function generateStaticParams() {
  return [{ locale: 'es' }, { locale: 'en' }]
}
```

---

## Consideraciones Importantes

*   **Exclusiones:** Asegúrate de que el matcher del middleware excluya `/api` y archivos estáticos para evitar errores de redirección innecesarios.
*   **Acceso Global:** En Server Actions o Route Handlers, puedes obtener el locale actual mediante cabeceras o la configuración de `next-intl`.
*   **SEO:** El uso de prefijos en la URL (`/es`, `/en`) es la mejor práctica para que los motores de búsqueda indexen correctamente cada versión de idioma.

> [!TIP]
> Aunque el App Router requiere una configuración manual inicial, este patrón ofrece un control total sobre el ciclo de vida de la localización y es compatible con el streaming de React.
