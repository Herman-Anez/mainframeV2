# Optimización de fuentes con `next/font`

`next/font` es el sistema de carga de fuentes incorporado en Next.js. Permite importar fuentes de Google Fonts o locales y las **auto-hospeda** automáticamente, eliminando peticiones externas y mejorando significativamente el rendimiento y la privacidad.

## ¿Por qué auto-hospedar?

*   **Rendimiento:** Las fuentes se sirven desde tu propio dominio, evitando búsquedas DNS adicionales y conexiones a servidores de terceros.
*   **Privacidad:** No se envían solicitudes ni datos a Google.
*   **Control total:** Decides exactamente los formatos y la estrategia de carga.

## Google Fonts con `next/font/google`

```jsx
import { Montserrat } from 'next/font/google'

const montserrat = Montserrat({
  subsets: ['latin'],
  display: 'swap',
  weight: ['400', '700'],
})

export default function Layout({ children }) {
  return (
    <html lang="es" className={montserrat.className}>
      <body>{children}</body>
    </html>
  )
}
```

### Opciones principales:
*   **`subsets`:** Define qué subconjuntos de caracteres incluir (ej. `latin`, `cyrillic`). Especificar solo los necesarios reduce drásticamente el tamaño del archivo.
*   **`weight`:** Los pesos requeridos. Si usas **Variable Fonts**, no necesitas pesos separados.
*   **`display`:** Controla el comportamiento de carga. `'swap'` es el recomendado para evitar el texto invisible (**FOIT**).

> [!TIP]
> Para fuentes variables, puedes usarlas sin especificar el peso (`weight`):
> ```jsx
> import { Inter } from 'next/font/google'
> const inter = Inter({ subsets: ['latin'] })
> ```

## Fuentes locales con `next/font/local`

Carga fuentes personalizadas almacenadas en tu proyecto (ej. en `public/fonts`).

```jsx
import localFont from 'next/font/local'

const myFont = localFont({
  src: [
    {
      path: '../public/fonts/MyFont-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../public/fonts/MyFont-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  display: 'swap',
})
```

## Uso con Tailwind CSS

Puedes integrar fuentes fácilmente con Tailwind mediante variables CSS.

```jsx
const roboto = Roboto({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-roboto',
})

export default function Layout({ children }) {
  return (
    <html className={`${roboto.variable} font-sans`}>
      <body>{children}</body>
    </html>
  )
}
```

**En `tailwind.config.js`:**
```javascript
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-roboto)'],
      },
    },
  },
}
```

---

## Estrategias de carga (`display`)

| Valor | Comportamiento | Impacto UX |
| :--- | :--- | :--- |
| **`swap`** | Muestra fuente de sistema e intercambia cuando la web font está lista. | **Recomendado** para LCP. |
| **`block`** | Bloquea la visualización del texto hasta que la fuente carga. | Causa FOIT (Flash of Invisible Text). |
| **`fallback`** | Oculta el texto por un tiempo mínimo antes de intercambiar. | Balanceado. |
| **`optional`** | Si la fuente tarda mucho, no la aplica (usa sistema). | Ideal para conexiones lentas. |

## Optimizaciones Automáticas

*   **Preload:** Next.js genera automáticamente `<link rel="preload">` para que el navegador descargue las fuentes con prioridad.
*   **Subsetting Automático:** Ajusta los archivos para incluir solo los caracteres estrictamente necesarios.
*   **Variable Fonts:** Manejo nativo que reduce el número de descargas al incluir múltiples estilos en un solo archivo.

> [!IMPORTANT]
> El tamaño de las fuentes impacta directamente en el **LCP**. Prefiere siempre el formato `.woff2`, usa solo los pesos necesarios y prioriza las fuentes que aparecen "above the fold" (en la parte visible inicial).

---

Con `next/font`, la tipografía web se convierte en una parte optimizada, privada y fácil de mantener dentro de tu flujo de desarrollo.
