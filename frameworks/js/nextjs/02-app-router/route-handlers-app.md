# Route Handlers en App Router

Los **Route Handlers** reemplazan a las API Routes del Pages Router dentro del App Router. Se definen en archivos `route.js` (o `route.ts`) y te permiten crear endpoints HTTP personalizados sin renderizar una página.

## Configuración básica

En cualquier carpeta de `app/` que **no** contenga `page.js`, puedes crear un archivo `route.js`. La carpeta define la ruta base y el archivo exporta funciones nombradas según el método HTTP.

```javascript
// app/api/hello/route.js
export async function GET(request) {
  return new Response(JSON.stringify({ message: 'Hola mundo' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  })
}
```

> [!WARNING]
> Al igual que las API Routes, las rutas son servidas por Next.js y pueden coexistir con páginas, pero una carpeta **no puede** tener `page.js` y `route.js` simultáneamente.

## Métodos HTTP soportados

Exporta funciones con los nombres de los métodos HTTP que deseas manejar: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`. Si un método no está definido, Next.js retorna `405 Method Not Allowed` automáticamente.

```javascript
export async function POST(request) {
  const body = await request.json()
  // procesar...
  return new Response(JSON.stringify({ success: true }), { status: 201 })
}
```

### El objeto `Request` y `Response`

Los Route Handlers reciben un objeto **Web Request** estándar (no el `req` de Node.js). Esto los hace compatibles con entornos Edge y Node.

*   `request.url`: URL completa.
*   `request.method`: método HTTP.
*   `request.headers`: cabeceras (tipo `Headers`).
*   `request.json()`, `request.formData()`, etc.
*   `request.cookies`: representación de cookies (Next.js extiende la API Web).

### Uso de `NextRequest` y `NextResponse`

Puedes usar `NextRequest` (de `next/server`) que extiende `Request` con propiedades adicionales como `nextUrl`, `cookies`, `geo` (en Edge).

```javascript
import { NextResponse } from 'next/server'

export async function GET(request) {
  // Acceso a query params de manera fácil
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')
  // ...
  return NextResponse.json({ id })
}
```

#### `NextResponse` Helpers:
*   `NextResponse.json(data, options)` → Response con JSON.
*   `NextResponse.redirect(url, status?)` → Redirección.
*   `NextResponse.next()` → Continúa con el siguiente manejador (útil en middleware).
*   `NextResponse.rewrite(destination)` → Reescribe la URL internamente.

### Segmentos dinámicos

Al igual que las páginas, las rutas pueden ser dinámicas. La carpeta `[id]` contendrá un `route.js` que recibe `params` en un segundo argumento.

```javascript
// app/api/items/[id]/route.js
export async function GET(request, { params }) {
  const id = params.id
  const item = await getItem(id)
  return NextResponse.json(item)
}
```

> [!NOTE]
> Los parámetros son accesibles de forma síncrona en la firma de la función.

## Configuración del Runtime y Caché

Los Route Handlers permiten configurar el runtime y opciones de caché mediante exportaciones constantes:

```javascript
export const runtime = 'edge' // 'nodejs' (por defecto)
export const dynamic = 'force-dynamic' // para que no se cachee
export const revalidate = 60 // ISR para endpoint GET
```

## Streams y procesamiento de archivos

Puedes devolver streams directamente. Por ejemplo, para leer un archivo grande:

```javascript
import { NextResponse } from 'next/server'

export async function GET() {
  const readableStream = new ReadableStream({...})
  return new Response(readableStream, {
    headers: { 'Content-Type': 'application/octet-stream' },
  })
}
```

## CORS y cabeceras personalizadas

Configura las cabeceras CORS dentro del handler o en `next.config.js`.

```javascript
export async function GET() {
  return new Response(JSON.stringify(data), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST',
    },
  })
}
```

## Comparación con API Routes (Pages)

| Característica | API Routes (Pages) | Route Handlers (App) |
| :--- | :--- | :--- |
| **Objeto Request** | `req` (http.IncomingMessage) | `request` (Web Request) |
| **Objeto Response** | `res` (http.ServerResponse) | Devuelves `Response` directamente |
| **Runtime** | Solo Node.js | Node.js o Edge Runtime |
| **Acceso a datos** | `req.query`, `req.body` | `request.nextUrl.searchParams`, `request.json()` |
| **Estructura** | `pages/api/*` | Integrados en `app/*` |

## Buenas prácticas

*   **Mantén los Route Handlers delgados:** delegar lógica a servicios.
*   **Usa Server Actions** para mutaciones asociadas a interfaz de usuario; los Route Handlers son para endpoints públicos/API.
*   **Combínalos con Middleware** (`middleware.js`) para proteger rutas.
*   **Aprovecha los segmentos dinámicos** para mantener un diseño RESTful.

---

Los Route Handlers te dan un backend ligero y completamente integrado con el resto de tu aplicación Next.js.