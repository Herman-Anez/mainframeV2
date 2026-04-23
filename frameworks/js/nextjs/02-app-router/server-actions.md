# Server Actions en App Router

Las **Server Actions** son funciones asíncronas ejecutadas en el servidor, pero que pueden ser invocadas desde Client Components o incluso desde formularios HTML sin necesidad de crear un API endpoint. Fueron introducidas como característica experimental y ahora son estables (Next.js 14+).

## Definición

Una Server Action se define con la directiva `'use server'` al inicio de un archivo o dentro de una función asíncrona. Pueden residir en Server Components, en archivos separados o incluso en Client Components (con restricciones).

### Forma 1: Directiva en archivo independiente

```javascript
// app/actions.js
'use server'

import { revalidatePath } from 'next/cache'

export async function createPost(formData) {
  const title = formData.get('title')
  // Validar y guardar en BD
  await db.post.create({ data: { title } })
  // Revalidar la página de lista
  revalidatePath('/posts')
}
```

### Forma 2: Dentro de un Server Component

```javascript
// app/new-post/page.js
import { revalidatePath } from 'next/cache'

export default function NewPost() {
  async function handleSubmit(formData) {
    'use server'
    // ... lógica de guardado
    revalidatePath('/posts')
  }

  return (
    <form action={handleSubmit}>
      <input name="title" />
      <button>Crear</button>
    </form>
  )
}
```

## Invocación desde formularios

La forma más natural es usar el atributo `action` de un `<form>`. El navegador enviará automáticamente un POST a la Server Action si está en un Client Component y se usa con JavaScript habilitado (**progressive enhancement**). Sin JS, el formulario funciona igual (se ejecuta la acción en el servidor).

```jsx
// Client Component
'use client'

import { createPost } from '@/app/actions'

export default function Form() {
  return (
    <form action={createPost}>
      <input type="text" name="title" required />
      <button type="submit">Enviar</button>
    </form>
  )
}
```

### Manejo de estados de carga

Puedes usar `useFormStatus` y `useFormState` (hooks de `react-dom`) para estados de carga y manejo de resultados.

**Ejemplo con `useFormStatus`:**

```jsx
'use client'
import { useFormStatus } from 'react-dom'

function SubmitButton() {
  const { pending } = useFormStatus()
  return (
    <button disabled={pending}>
      {pending ? 'Guardando...' : 'Guardar'}
    </button>
  )
}
```

## Acceso al request y cookies

Dentro de una Server Action puedes leer cookies y headers con las funciones de `next/headers` (que son dinámicas):

```javascript
import { cookies, headers } from 'next/headers'

export async function updatePreferences(formData) {
  const cookieStore = cookies()
  const token = cookieStore.get('token')
  const userAgent = headers().get('user-agent')
  // ...
}
```

## Redirecciones y manejo de errores

Puedes redirigir después de ejecutar una acción usando `redirect` de `next/navigation`:

```javascript
import { redirect } from 'next/navigation'

export async function login(formData) {
  // verificar credenciales...
  redirect('/dashboard')
}
```

> [!TIP]
> Para manejar errores y mostrarlos en el cliente, puedes retornar un objeto serializable desde la acción y usar `useFormState` o simplemente lanzar una excepción que capture el error boundary.

## Revalidación de datos

Uno de los usos principales es mutar datos y luego revalidar la caché asociada para que la interfaz se actualice automáticamente:

```javascript
import { revalidatePath, revalidateTag } from 'next/cache'

export async function addComment(commentData) {
  await db.comment.create(...)
  revalidatePath('/posts/[slug]')  // revalida la página de ese post
  // o revalidateTag('comments')
}
```

## Invocación desde manejadores de eventos

Aunque lo común es mediante `action`, también puedes invocar Server Actions desde un `onClick` o `useEffect` usando la función exportada como cualquier función asíncrona normal. Se recomienda envolverla en `startTransition` para manejar el estado de carga.

```jsx
'use client'
import { createPost } from '@/app/actions'
import { useTransition } from 'react'

export default function CreateButton() {
  const [isPending, startTransition] = useTransition()

  const handleClick = () => {
    startTransition(async () => {
      await createPost(new FormData()) // construyes FormData manualmente si es necesario
    })
  }

  return <button onClick={handleClick} disabled={isPending}>Crear</button>
}
```

## Seguridad

*   **Protección CSRF:** Next.js protege las Server Actions con CSRF automáticamente (envía un token en un header al hacer llamadas desde el cliente).
*   **Origen:** Las Server Actions solo pueden ser llamadas desde el mismo proyecto (mismo origen) por defecto.
*   **Payload:** El tamaño máximo del payload es **1 MB** (configurable en `next.config.js` con `serverActions.bodySizeLimit`).
*   **Secretos:** No expongas secretos en el código que se envía al cliente. Todo lo exportado de un archivo con `'use server'` es seguro (solo el identificador de la acción se envía al cliente).

## Cuándo usar Server Actions vs Route Handlers

| Característica | Server Actions | Route Handlers |
| :--- | :--- | :--- |
| **Uso principal** | Mutaciones ligadas a la UI (formularios, likes) | APIs públicas, webhooks, integraciones externas |
| **Ventaja** | Revalidación automática y Progressive Enhancement | Control total sobre HTTP (CORS, Status, Streaming) |
| **Invocación** | Atributo `action` o funciones asíncronas | Llamadas `fetch` desde cualquier lugar |

---

Las Server Actions simplifican el patrón tradicional de crear endpoints API para cada formulario, reuniendo la lógica del servidor con la interfaz de usuario.