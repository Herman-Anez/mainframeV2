# Fundamentos del App Router

El **App Router** es el sistema de enrutamiento introducido en Next.js 13 (estable desde 13.4) que reemplaza progresivamente al Pages Router. Está construido sobre **React Server Components**, **Streaming** y **Suspense**, y utiliza la carpeta `app/` en lugar de `pages/`.

## Convenciones del directorio `app/`

A diferencia del Pages Router, donde cada archivo dentro de `pages/` se convierte automáticamente en una ruta, en el App Router necesitas carpetas que contengan archivos especiales con nombres reservados:

| Archivo especial | Propósito |
| :--- | :--- |
| `page.js` / `page.tsx` | Define la interfaz de usuario única de una ruta. |
| `layout.js` | Envuelve a las páginas y persiste entre navegaciones dentro de la misma jerarquía. |
| `loading.js` | UI de carga que se muestra mientras la página o segmento espera datos (Suspense). |
| `error.js` | Aísla errores en una parte de la ruta sin colapsar la aplicación completa. |
| `template.js` | Similar a layout pero se vuelve a montar en cada navegación. |
| `not-found.js` | Se muestra cuando una ruta no existe. Reemplaza al `404.js` del Pages Router. |
| `route.js` / `route.ts` | Define controladores HTTP (API endpoints) sin componente visual. |

> [!NOTE]
> **Head.js (obsoleto):** Ha sido reemplazado por la API de Metadata, exportando un objeto `metadata` o la función `generateMetadata`.

## Rutas básicas

Una ruta se define por una carpeta dentro de `app/` que contenga un archivo `page.js`.

*   **Ejemplo:** `app/about/page.js` → `/about`
*   **Ejemplo:** `app/blog/page.js` → `/blog`

> [!TIP]
> Las carpetas que no contienen `page.js` o `route.js` se vuelven **privadas** (no accesibles desde la URL), permitiendo organizar componentes, hooks y utilidades sin exponer rutas.

## Jerarquía de archivos especiales

En una misma carpeta pueden coexistir varios archivos especiales, los cuales se anidan automáticamente en este orden:

```text
app/
├── layout.js          (Layout raíz obligatorio)
├── page.js            (Página principal "/")
├── about/
│   ├── layout.js      (Layout opcional para /about/*)
│   └── page.js        (Página "/about")
├── blog/
│   ├── layout.js      (Layout del blog)
│   ├── loading.js     (Carga mientras se resuelve /blog)
│   ├── error.js       (Error para /blog y sus hijos)
│   ├── page.js        ("/blog")
│   └── [slug]/
│       └── page.js    ("/blog/123")
```

### El layout raíz

Todo proyecto con App Router debe tener un layout raíz en `app/layout.js`. Este componente envuelve toda la aplicación y es el lugar para definir la estructura HTML, fuentes, metadatos globales y proveedores.

```jsx
export const metadata = {
  title: 'Mi aplicación',
  description: 'Descripción global',
}

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        <nav>Barra de navegación global</nav>
        {children}
      </body>
    </html>
  )
}
```

> [!IMPORTANT]
> Los layouts raíz son **Server Components** por defecto; no pueden usar hooks de cliente. Si necesitas proveedores de contexto (Redux, temas, etc.), debes crear un Client Component separado e importarlo.

## Ventajas del App Router

*   **Renderizado híbrido y granular:** Puedes combinar Server Components estáticos, dinámicos y Client Components en un mismo árbol.
*   **Layouts persistentes:** No se desmontan al navegar, lo que mejora la experiencia y reduce el parpadeo.
*   **Streaming y Suspense integrados:** Carga progresiva sin configuración compleja.
*   **Server Actions:** Mutaciones desde el cliente sin necesidad de crear rutas de API manuales.
*   **Caché más fino:** Control por fetch, segmentos y rutas con `revalidatePath` y `revalidateTag`.

---

| [« Anterior](../index.md) | [Siguiente Section: Server Components vs Client Components »](./server-components-vs-client.md) |
| :--- | :---: |