## 📘 01-pages-router/getServerSideProps.md

### getServerSideProps: Renderizado en cada solicitud

`getServerSideProps` (SSR) es una función que se ejecuta en el servidor en cada petición. Permite generar la página con datos frescos antes de enviarla al cliente. Se define dentro del archivo de la página y debe ser exportada.

#### Sintaxis básica

```jsx
export async function getServerSideProps(context) {
  return {
    props: {
      // datos que recibirá el componente
    },
  }
}

export default function Page({ data }) {
  return <div>{data}</div>
}
```

#### El objeto `context`

Contiene información sobre la solicitud actual:

- `params`: Parámetros de ruta dinámica (ej. `{ id: '5' }`).
- `req`: El objeto `http.IncomingMessage` (solo en servidor).
- `res`: El objeto `http.ServerResponse`.
- `query`: El query string de la URL.
- `resolvedUrl`: La URL completa resuelta.

**Ejemplo usando params:**

```jsx
// pages/posts/[pid].js
export async function getServerSideProps({ params }) {
  const res = await fetch(`https://.../posts/${params.pid}`)
  const post = await res.json()

  return { props: { post } }
}
```

#### Cuándo usar `getServerSideProps`

- Datos que cambian a menudo (precios de acciones, noticias en tiempo real).
- Contenido personalizado según el usuario (sesiones, cookies).
- Páginas que necesitan leer `req` (cabeceras de autenticación, geolocalización).

#### Rendimiento

> [!CAUTION]
> Como se ejecuta en cada solicitud, puede aumentar el tiempo de respuesta y la carga del servidor.

Para reducir el trabajo, puedes agregar un encabezado de cache con `res.setHeader('Cache-Control', ...)`:

```jsx
export async function getServerSideProps({ res }) {
  res.setHeader('Cache-Control', 'public, s-maxage=10, stale-while-revalidate=59')
  // ...
}
```

#### Redirecciones y notFound

```jsx
export async function getServerSideProps(context) {
  const data = await fetchData()

  if (!data) {
    return {
      notFound: true, // muestra la página 404
    }
  }

  if (shouldRedirect) {
    return {
      redirect: {
        destination: '/nueva-ruta',
        permanent: false, // 307 (temporal), o true para 308
      },
    }
  }

  return { props: { data } }
}
```

#### Con TypeScript

```tsx
import type { GetServerSideProps } from 'next'

type Post = { id: number; title: string }

export const getServerSideProps: GetServerSideProps<{ post: Post }> = async (ctx) => {
  // ...
  return { props: { post } }
}
```

#### Acceso a cookies

Para leer cookies, usa el objeto `req` de Node (o librerías como `cookie` o `next-cookies`).

```jsx
export async function getServerSideProps({ req }) {
  const token = req.cookies.token
  // validar...
}
```

#### Consideraciones importantes

- Esta función solo se ejecuta en el servidor, nunca en el cliente.
- No se puede usar dentro de componentes, solo en páginas.
- El código no se incluye en el bundle del cliente.

---
