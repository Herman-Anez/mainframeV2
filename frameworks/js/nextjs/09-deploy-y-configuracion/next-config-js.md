# Configuración de `next.config.js`

`next.config.js` es el núcleo de personalización de Next.js. Permite ajustar desde el proceso de empaquetado hasta el comportamiento del enrutamiento y optimizaciones avanzadas. Al ser un módulo de Node.js, se ejecuta durante la fase de construcción y arranque del servidor.

## Estructura Básica

Utiliza JSDoc para habilitar el autocompletado y validación de tipos en tu editor.

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,   // Recomendado: ayuda a detectar problemas en desarrollo
  swcMinify: true,         // Usa el compilador SWC para minificar el código
  // Otras configuraciones...
}

module.exports = nextConfig
```

---

## Opciones Esenciales

### 1. Gestión de Imágenes (`images`)
Configuración necesaria para optimizar imágenes, especialmente si provienen de fuentes externas.

```javascript
images: {
  remotePatterns: [
    {
      protocol: 'https',
      hostname: '**.example.com',
      pathname: '/uploads/**',
    },
  ],
  formats: ['image/avif', 'image/webp'],
  deviceSizes: [640, 1080, 1920],
}
```

### 2. Redirecciones y Reescrituras
Permiten gestionar el flujo de URLs del lado del servidor.

*   **`redirects`:** Cambian la URL visible y el código de estado (SEO).
*   **`rewrites`:** Mapean internamente una URL a otra sin que el usuario lo note (útil para proxies de APIs).

```javascript
async redirects() {
  return [
    { source: '/old-path', destination: '/new-path', permanent: true }
  ]
}

async rewrites() {
  return [
    { source: '/api/:path*', destination: 'https://api.external.com/:path*' }
  ]
}
```

---

## Configuración del Compilador

Puedes ajustar cómo el compilador de Next.js procesa tu código sin necesidad de plugins externos.

```javascript
compiler: {
  // Elimina console.log solo en producción
  removeConsole: process.env.NODE_ENV === 'production',
  // Soporte nativo para styled-components
  styledComponents: true,
}
```

---

## Opciones de Salida (`output`)

Determina cómo se empaqueta la aplicación para su despliegue.

| Valor | Propósito |
| :--- | :--- |
| **`standalone`** | Genera un bundle mínimo con solo lo necesario para Node.js. Ideal para Docker. |
| **`export`** | Genera un sitio de archivos estáticos (HTML/CSS/JS). No requiere servidor Node. |

---

## Funcionalidades Experimentales

Muchas características nuevas se habilitan mediante la clave `experimental`. Úsalas con precaución en producción.

```javascript
experimental: {
  staleTimes: {
    dynamic: 30, // Tiempo de caché de navegación para rutas dinámicas
    static: 300, // Tiempo para rutas estáticas
  },
  turbo: {
    // Configuración específica para el empaquetador Turbopack
  },
}
```

---

## Buenas Prácticas

1.  **Tipado Dinámico:** Si necesitas lógica basada en el entorno (dev vs build), puedes exportar una función en lugar de un objeto:
    ```javascript
    module.exports = (phase, { defaultConfig }) => {
      if (phase === 'phase-development-server') {
        return { /* config de desarrollo */ }
      }
      return { /* config de producción */ }
    }
    ```
2.  **Modularización:** Si el archivo se vuelve demasiado grande, separa las redirecciones o configuraciones de plugins en archivos independientes.
3.  **Seguridad:** Nunca incluyas secretos directamente en este archivo si planeas subirlos al repositorio. Usa variables de entorno.

> [!IMPORTANT]
> Los cambios en `next.config.js` requieren un reinicio del servidor de desarrollo para surtir efecto.

---

`next-config-js` es la herramienta más potente para adaptar el framework a las necesidades específicas de tu proyecto, garantizando control total sobre el comportamiento de la aplicación.
