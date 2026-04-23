## 📘 00-introduccion/que-es-nextjs.md

### ¿Qué es Next.js?

Next.js es un framework de React creado por Vercel que permite construir aplicaciones web modernas aprovechando renderizado híbrido (estático y servidor), enrutamiento basado en el sistema de archivos, optimizaciones automáticas y una excelente experiencia de desarrollo.

Es la capa sobre React que resuelve problemas comunes como el renderizado del lado del servidor (SSR), la generación de sitios estáticos (SSG), la división de código y la configuración de herramientas complejas.

### 🌟 Características principales

- **Renderizado flexible:** Puedes elegir por página si usar SSR, SSG, ISR (Incremental Static Regeneration) o incluso renderizado del lado del cliente.
- **Enrutamiento basado en archivos:** Sin necesidad de `react-router`, la estructura de carpetas define las rutas.
- **Optimizaciones automáticas:** Imágenes, fuentes, scripts y bundles se optimizan de forma nativa.
- **Soporte TypeScript total:** Tipos incluidos y configuración automática.
- **API Routes:** Permite construir endpoints de backend dentro del mismo proyecto.
- **Internacionalización:** Sistema de rutas con prefijo de idioma, detección automática.
- **Ecosistema:** Amplia comunidad y despliegue instantáneo en Vercel.

### 📜 Historia breve

Lanzado en 2016, revolucionó la forma de hacer sitios web con React al ofrecer SSR y SSG sencillos. Con la versión 13, introdujo el **App Router**, basado en React Server Components, marcando un nuevo paradigma. Actualmente, conviven el **Pages Router** (estable) y el **App Router** (recomendado para nuevos proyectos).

### 🤔 ¿Por qué usar Next.js en lugar de React solo?

Un proyecto con React puro necesita configurar manualmente:

- Webpack o Vite para bundling.
- React Router para navegación.
- Herramientas para SSR (como Express con `renderToString`).
- Soluciones de SEO personalizadas.
- Caché y optimización de imágenes.

Next.js proporciona todo esto de serie, con convenciones claras y decisiones técnicas probadas.

---
