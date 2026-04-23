## 📘 01-pages-router/diferencias-con-app-router.md

### Diferencias entre Pages Router y App Router

Next.js 13 introdujo el App Router, un nuevo paradigma construido sobre React Server Components, streaming y layouts anidados.

#### 1. Directorio y convención

| Pages Router | App Router |
| :--- | :--- |
| Carpeta `pages/`. Cada archivo es una ruta. | Carpeta `app/`. Las carpetas definen rutas y deben contener `page.js`. |
| Archivos especiales: `_app.js`, `_document.js`. | Archivos especiales: `layout.js`, `loading.js`, `error.js`, `not-found.js`. |

#### 2. Componentes por defecto: Servidor vs Cliente

- **Pages Router:** Los componentes son de cliente por defecto. El JavaScript de la página se envía al navegador.
- **App Router:** Todos los componentes son **React Server Components** por defecto. Para añadir interactividad, se marca `'use client'`.

#### 3. Layouts y persistencia

- **Pages Router:** Cada página se monta y desmonta completamente. Los layouts se implementan manualmente.
- **App Router:** Los layouts (`layout.js`) se anidan y persisten al navegar. Solo se recarga la parte de `page.js`.

#### 4. Obtención de datos

- **Pages Router:** `getServerSideProps`, `getStaticProps`.
- **App Router:** Los Server Components obtienen datos directamente usando `fetch` asíncrono en el cuerpo del componente.

#### 5. Server Actions

- **Pages Router:** No existen. Mutaciones vía API Routes.
- **App Router:** Las Server Actions permiten ejecutar funciones del servidor directamente desde formularios en el cliente.

#### 10. Migración y convivencia

Puedes tener ambos routers en el mismo proyecto (carpeta `pages/` y `app/`). Sin embargo, Next.js recomienda adoptar gradualmente el App Router para nuevos proyectos, ya que aprovecha las últimas innovaciones de React.

#### 🤔 ¿Cuándo seguir con Pages Router?

- Proyectos grandes y estables donde una migración completa no es prioritaria.
- Equipos acostumbrados al modelo clásico y que no necesitan Server Components.
- Ciertas librerías del ecosistema React aún podrían no ser totalmente compatibles con RSC.

---

> [!TIP]
> El App Router es el futuro, pero el Pages Router seguirá siendo mantenido y es perfectamente válido para producción.
