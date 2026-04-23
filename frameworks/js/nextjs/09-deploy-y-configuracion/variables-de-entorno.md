
## Archivo: `09-deploy-y-configuracion/variables-de-entorno.md`

Variables de entorno en Next.js

Next.js facilita el manejo de variables de entorno mediante archivos .env y una convención de prefijos que define qué se expone al navegador. Un mal manejo puede exponer datos sensibles al cliente, por lo que es crucial entender las reglas.
Archivos .env

Next.js carga automáticamente los siguientes archivos, por orden de prioridad:

### .env (todos los entornos)

### .env.local (local, nunca se sube a git)

### .env.development (solo en next dev)

### .env.production (solo en next build / next start)

### .env.test (solo cuando NODE_ENV === 'test')

Prioridad: las variables definidas en archivos más específicos sobrescriben a las más generales (.env.local gana a .env).
Prefijo NEXT_PUBLIC_

Para que una variable de entorno esté disponible en el navegador (Client Components), debes prefijarla con NEXT_PUBLIC_. En caso contrario, solo estará disponible en el entorno Node.js (Server Components, API Routes, next.config.js).
```text
```
NEXT_PUBLIC_ANALYTICS_ID=UA-123456    # accesible en cliente
DATABASE_URL=postgres://...           # solo servidor

Acceso en cualquier lugar:
```js
```
console.log(process.env.NEXT_PUBLIC_ANALYTICS_ID)

### Uso en Server Components y API Routes

En Server Components, getServerSideProps, getStaticProps, Route Handlers y middleware, puedes acceder a todas las variables sin restricción, siempre que el código se ejecute en el servidor.

En next.config.js, process.env está disponible como en cualquier módulo Node.
Variables en el middleware (Edge Runtime)

El middleware se ejecuta en Edge Runtime. Las variables de entorno se deben definir en el momento del build (o mediante Vercel/plataforma), no se pueden leer dinámicamente de archivos .env. En desarrollo local, las variables del archivo .env sí están disponibles. En producción, asegúrate de configurarlas en el panel de la plataforma.
Exposición al cliente con env en next.config.js

La propiedad env de next.config.js expone variables al cliente en tiempo de build. Es una alternativa al prefijo NEXT_PUBLIC_, pero menos recomendada porque las inyecta directamente en el JavaScript.
```js
```
module.exports = {
  env: {
    API_URL: process.env.API_URL,  // cuidado: expone al cliente si no filtras
  },
}

Si API_URL no tiene NEXT_PUBLIC_, no estará disponible en cliente a menos que uses esta opción (lo que puede ser inseguro). Mejor usa NEXT_PUBLIC_ explícitamente.
Variables en tiempo de ejecución vs build

Las variables de entorno se congelan en el momento del build para el cliente. Si necesitas valores que cambien en runtime (ej. en un contenedor Docker), debes:

    Para Server Components/API: usar getServerSideProps o Route Handlers que lean process.env en cada petición (en producción con next start, las variables de entorno del sistema están disponibles).

    Para el cliente: no hay forma directa. Puedes pasar valores desde el servidor al cliente como props o a través de una API.

Técnica común: exponer un endpoint /api/config que devuelva variables públicas que puedan cambiar en runtime.
Secretos y seguridad

    Jamás expongas claves de API o secretos en variables NEXT_PUBLIC_.

    En Server Components, las variables no prefijadas nunca se envían al cliente.

    Si necesitas usar una clave en Server Side pero también referenciarla en un Client Component (por ejemplo, para iniciar un SDK), el SDK debe inicializarse con una clave pública, no un secreto. La clave pública sí puede ser NEXT_PUBLIC_.

### Ejemplo de configuración completa

.env.local:
```text
```
DATABASE_URL=postgres://...
NEXT_PUBLIC_SITE_URL=https://misitio.com

En app/server-page.js:
```tsx
export default async function ServerPage() {
  const dbUrl = process.env.DATABASE_URL   // OK, solo servidor
  // ...
}
```

En un Client Component:
```tsx
'use client'
export default function Component() {
  const url = process.env.NEXT_PUBLIC_SITE_URL   // OK
}
```

El manejo cuidadoso de las variables de entorno es esencial para la seguridad y la flexibilidad en el despliegue.