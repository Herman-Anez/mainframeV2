

## 📘 00-introduccion/comparacion-con-react.md


### Next.js vs React (con Vite / CRA)

Aunque Next.js está construido con React, las diferencias van mucho más allá de ser un simple “React con esteroides”. Aquí tienes una comparación detallada.

#### 1. Renderizado

| Característica | React (SPA tradicional) | Next.js |
| :--- | :--- | :--- |
| **Renderizado inicial** | Cliente: El HTML está casi vacío, el JS monta toda la app. | Servidor/Estático: El HTML llega completamente renderizado, mejor LCP. |
| **SEO** | Depende de soluciones externas (`react-helmet`, `prerender.io`). | Nativo, con metadatos por página y renderizado del lado del servidor. |
| **Carga en redes lentas** | Puede ser lenta, pues el bundle JS debe descargarse y ejecutarse. | Más rápido porque el HTML ya contiene el contenido. |
| **Opciones de renderizado** | Solo cliente (SPA). | Por página: SSG, SSR, ISR, CSR. |

#### 2. Enrutamiento

| React | Next.js |
| :--- | :--- |
| Requiere librerías (`react-router-dom`). Configuración manual de rutas. | Enrutamiento basado en archivos: una carpeta = una ruta. |
| Las rutas protegidas dependen de lógica en componentes. | Soporte automático para layouts, rutas dinámicas, anidadas, paralelas. Middleware nativo para interceptar peticiones basadas en cookies, headers, etc. |

#### 3. Obtención de datos

| React | Next.js |
| :--- | :--- |
| `useEffect` + `fetch`, `SWR`, `React Query`. Los datos se cargan después del montaje (a menos que se use un SSR casero). | Funciones dedicadas como `getServerSideProps`, `getStaticProps`, `fetch` nativo extendido en servidor, React Server Components. Los datos pueden cargarse antes de que el HTML llegue al cliente. |

#### 4. Rendimiento

- **División de código:** En React hay que configurarla con `React.lazy`. Next.js la hace automática por ruta.
- **Imágenes:** Next.js tiene `next/image` con lazy loading, formatos modernos y redimensionamiento automático. En React necesitas librerías externas.
- **Fuentes:** `next/font` elimina peticiones a Google Fonts y optimiza la carga.

#### 5. Configuración y tooling

- **React:** Necesitas crear un proyecto con Vite o CRA. Configurar ESLint, Prettier manualmente. El soporte SSR requiere Node.js y código extra.
- **Next.js:** `create-next-app` da un proyecto listo para producción. Configuración de TypeScript, ESLint y Tailwind incluida opcionalmente. Compilación y empaquetado con Turbopack (rápido en desarrollo).

#### 6. Despliegue

- **React:** Se genera una carpeta `dist` con archivos estáticos. Para SSR necesitas un servidor Node.js.
- **Next.js:** Puede exportarse como sitio estático (`output: 'export'`), ejecutarse como servidor Node.js, o desplugar en Vercel, Netlify, etc., aprovechando Edge Functions e ISR.

> [!TIP]
> **Conclusión:** Next.js es la opción recomendada por la documentación oficial de React para iniciar un proyecto, porque proporciona una solución completa con convenciones bien pensadas.

---






   
