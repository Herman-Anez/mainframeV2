# Middleware en Next.js para Autenticación

El **Middleware** de Next.js se ejecuta antes de que una solicitud se complete, permitiendo interceptar peticiones, modificar cabeceras, redirigir o verificar autenticación de forma centralizada. Corre en el **Edge Runtime**, por lo que debe ser extremadamente ligero y rápido.

## Conceptos Básicos

* **Ubicación:** Archivo `middleware.ts` (o `.js`) en la raíz del proyecto (al mismo nivel que `app/` o `pages/`).
* **Función:** Exporta una función `middleware` que recibe `NextRequest` y retorna una `NextResponse`.
* **Filtrado:** Se aplica a todas las rutas por defecto, pero puedes restringirlo con un objeto `config.matcher`.

### Ejemplo: Redirección por Autenticación

```ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(req: NextRequest) {
  const token = req.cookies.get('token')
  const isAuthPage = req.nextUrl.pathname.startsWith('/login')

  // Redirigir a login si no hay token y no es la página de auth
  if (!token && !isAuthPage) {
    return NextResponse.redirect(new URL('/login', req.url))
  }
  
  // Redirigir a dashboard si ya hay token e intenta entrar a login
  if (token && isAuthPage) {
    return NextResponse.redirect(new URL('/dashboard', req.url))
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login'],
}
```

> [!TIP]
> El `matcher` es fundamental para el rendimiento; asegúrate de que el middleware solo se ejecute en las rutas que realmente necesitan verificación.

---

## Integración con NextAuth (v5)

NextAuth proporciona un helper para integrar su lógica de sesión directamente en el middleware. Puedes envolver tu lógica con `auth()` o usar `auth` como middleware directamente.

```ts
// middleware.ts
import { auth } from '@/auth'
import { NextResponse } from 'next/server'

export default auth((req) => {
  const isLogged = !!req.auth
  const isAdmin = req.auth?.user?.role === 'admin'
  const path = req.nextUrl.pathname

  // Protección de rutas de administración
  if (path.startsWith('/admin') && !isAdmin) {
    return NextResponse.redirect(new URL('/403', req.url))
  }
  
  // Protección de rutas de usuario
  if (path.startsWith('/dashboard') && !isLogged) {
    return NextResponse.redirect(new URL('/login', req.url))
  }
  
  return NextResponse.next()
})

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*'],
}
```

---

## Capacidades del Middleware (Acceso a cookies, headers y geolocalización)

El middleware tiene acceso a metadatos de la solicitud que permiten decisiones granulares:

* **`req.cookies`**: Cookies de la solicitud (objeto iterable).
* **`req.headers`**: Cabeceras HTTP.
* **`req.geo`**: Información geográfica (país, ciudad, etc.) — *Solo en Vercel/Edge*.
* **`req.nextUrl`**: Objeto URL con información detallada de la ruta.

> [!NOTE]
> Puedes usar `NextResponse.rewrite(destination)` para realizar reescrituras internas donde el cliente no ve el cambio de URL, ideal para i18n o A/B testing.

---

## Limitaciones del Edge Runtime

Debido a que el middleware corre en el Edge, existen restricciones importantes:

* **Sin Node.js nativo:** No puedes usar `fs`, `path`, `crypto` (versión Node) ni librerías que dependan de ellas.
* **Sin `req.body`**: El cuerpo de la solicitud no está disponible en el middleware. Para validar datos POST, usa **Route Handlers** o **Server Actions**.
* **Velocidad:** Debe ser una función de ejecución rápida. Evita llamadas a APIs pesadas o procesos síncronos largos.

---

## Buenas Prácticas

1. **Matcher Restrictivo:** Evita usar `*` que abarque todo el sitio. Prefiere patrones específicos como `['/app/:path*', '/api/auth/:path*']`.
2. **Evitar Bucles:** Verifica siempre la URL actual antes de redirigir (ej. no redirijas a `/login` si el usuario ya está en `/login`).
3. **Seguridad en APIs:** El middleware también protege los **Route Handlers**. Úsalo para validar tokens en tus endpoints `/api`.

> [!IMPORTANT]
> El middleware es una herramienta de **control de acceso**, no de procesamiento de datos pesados. Su objetivo principal es decidir si una solicitud debe proceder, ser redirigida o bloqueada.

### Evitar bucles de redirección

Al redirigir, asegúrate de no crear un bucle. Por ejemplo, no redirijas a /login si ya estás en /login. Siempre verifica la URL actual.
Combinación con internacionalización

Si usas next-intl u otra solución de i18n, el middleware debe combinarse con la lógica de idiomas. Puedes encadenar middlewares o integrar la verificación de sesión dentro del middleware de i18n.
Rendimiento y buenas prácticas

    Define un matcher lo más restrictivo posible para que el middleware solo se ejecute en las rutas necesarias.

    Evita usar * que abarque todo; prefiere patrones como ['/app/:path*', '/api/auth/:path*'].

    El middleware no debe bloquear la respuesta; siempre devuelve una NextResponse sin demora.

### Middleware para APIs (Route Handlers)

El middleware también se ejecuta en las API routes del App Router. Puedes protegerlas de la misma manera:

```ts
if (req.nextUrl.pathname.startsWith('/api/admin') && !req.auth?.user?.isAdmin) {
  return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
}
```

El middleware de autenticación es una herramienta central en el App Router para garantizar la seguridad sin tocar cada página o endpoint individualmente.

Con estos cinco archivos, tienes cubierta una parte fundamental del desarrollo de aplicaciones Next.js: la visibilidad en buscadores y la autenticación robusta. Si necesitas continuar con despliegue, testing o internacionalización, avísame.
