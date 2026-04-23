# Optimización de imágenes con `next/image`

El componente `<Image>` de `next/image` sustituye a la etiqueta `<img>` nativa y proporciona optimizaciones automáticas que mejoran notablemente el rendimiento y la experiencia de usuario.

## Principales beneficios

*   **Tamaño y formato automático:** Sirve la imagen en el tamaño exacto requerido según el dispositivo y en formatos modernos (**WebP**, **AVIF**).
*   **Lazy Loading nativo:** Las imágenes se cargan solo cuando están cerca del viewport, ahorrando ancho de banda.
*   **Prevención de CLS (Cumulative Layout Shift):** Reserva el espacio automáticamente para evitar saltos de contenido mientras la imagen carga.
*   **Caché y compresión:** Las imágenes se optimizan bajo demanda y se cachean en el servidor o CDN.
*   **Calidad ajustable:** Permite reducir el peso del archivo sin una pérdida de nitidez perceptible.

## Uso básico

```jsx
import Image from 'next/image'
import logo from '../public/logo.png' // Importación estática

export default function Profile() {
  return (
    <Image
      src={logo}
      alt="Logo de la empresa"
      width={200}
      height={100}
      priority // Carga prioritaria para imágenes LCP
    />
  )
}
```

---

## Imágenes locales vs. remotas

*   **Locales:** Almacenadas en el proyecto (ej. `public/`). Al importarlas estáticamente, Next.js infiere sus dimensiones automáticamente.
*   **Remotas:** Provenientes de URLs externas. Debes configurar los dominios permitidos en `next.config.js` por seguridad.

**Configuración recomendada:**
```javascript
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
        port: '',
        pathname: '/images/**',
      },
    ],
  },
}
```

---

## Props esenciales

| Prop | Descripción |
| :--- | :--- |
| **`src`** | Ruta de la imagen (string o importación). |
| **`alt`** | Texto alternativo para accesibilidad (**obligatorio**). |
| **`width` / `height`** | Dimensiones para reservar espacio (obligatorio excepto en `fill`). |
| **`priority`** | Marca la imagen para carga inmediata (usar en la imagen principal/LCP). |
| **`fill`** | La imagen llena el contenedor padre (el padre debe tener `position: relative`). |
| **`sizes`** | Define el ancho de la imagen en distintos breakpoints para un responsive eficiente. |
| **`placeholder`** | Usa `'blur'` para mostrar una versión difuminada mientras carga. |

---

## Estrategia de tamaños (`sizes`)

El atributo `sizes` es clave para que el navegador descargue la resolución adecuada según el dispositivo.

```jsx
<Image
  src="/hero.jpg"
  fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  alt="Imagen Hero"
/>
```

> [!NOTE]
> En este ejemplo, en móviles la imagen ocupa el 100% del viewport, en tablets el 50% y en desktop el 33%. Esto evita descargar una imagen de 2000px en una pantalla de 400px.

---

## Imágenes con `fill`

Cuando no conoces el ancho/alto exacto o la imagen debe ser flexible, usa `fill`:

```jsx
<div style={{ position: 'relative', width: '100%', height: '400px' }}>
  <Image
    src="/banner.jpg"
    alt="Banner promocional"
    fill
    style={{ objectFit: 'cover' }}
    sizes="100vw"
  />
</div>
```

---

## Buenas prácticas

1.  **Prioridad (LCP):** Marca siempre con `priority` las imágenes que aparecen "above the fold" (cabeceras, banners principales).
2.  **Dimensiones:** Proporciona `width` y `height` correctos para evitar el parpadeo de diseño.
3.  **Formatos:** No desactives los formatos modernos (`webp`, `avif`) a menos que sea estrictamente necesario.
4.  **Imágenes de Usuario:** Usa `remotePatterns` restrictivos para imágenes que provengan de fuentes externas dinámicas.

> [!IMPORTANT]
> `next/image` utiliza un endpoint interno (`/_next/image`) para optimizar imágenes. En exportaciones estáticas (`next export`), este componente no funciona de forma nativa y requiere un proveedor externo o desactivar la optimización.

---

`next/image` elimina la complejidad técnica de la optimización de activos visuales, una de las causas principales de un bajo rendimiento web.
