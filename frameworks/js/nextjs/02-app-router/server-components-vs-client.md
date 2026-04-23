# React Server Components vs Client Components

En el **App Router**, Next.js trata a todos los componentes como **React Server Components (RSC)** por defecto. Para usar interactividad, estado o efectos, necesitas declarar explícitamente un **Client Component**.

## React Server Components (RSC)

Los Server Components se renderizan únicamente en el servidor (o en tiempo de build). Su resultado (HTML + formato especial de React) se envía al cliente sin JavaScript adicional.

### Características:

*   **Sin Hooks de Cliente:** No pueden usar `useState`, `useEffect`, `useContext`, `useReducer` ni ningún hook que requiera el ciclo de vida del navegador.
*   **Sin Eventos del DOM:** No pueden manejar eventos como `onClick` o `onSubmit` (a menos que sea una Server Action).
*   **Asíncronos por naturaleza:** Pueden usar `async/await` directamente en el cuerpo del componente.
*   **Acceso directo a recursos:** Tienen acceso directo a bases de datos, sistema de archivos y variables de entorno privadas.
*   **Seguridad y Rendimiento:** El código fuente nunca se expone al cliente, mejorando la seguridad y reduciendo el tamaño del bundle.

**Ejemplo:**

```jsx
// app/blog/page.js
export default async function BlogPage() {
  const posts = await fetch('https://api.example.com/posts', { next: { revalidate: 60 } })
  const data = await posts.json()

  return (
    <ul>
      {data.map(post => <li key={post.id}>{post.title}</li>)}
    </ul>
  )
}
```

> [!NOTE]
> Aquí `BlogPage` obtiene datos en el servidor y renderiza HTML puro, eliminando la necesidad de hidratación en el cliente para esta parte del árbol.

## Client Components

Se definen añadiendo la directiva `'use client'` en la primera línea del archivo. Esto indica a Next.js que el componente y sus dependencias deben enviarse al navegador.

### Cuándo usarlos:

*   **Manejo de estado:** `useState`, `useReducer`.
*   **Efectos y ciclo de vida:** `useEffect`, `useLayoutEffect`.
*   **Eventos del DOM:** `onClick`, `onChange`, etc.
*   **Contexto de cliente:** `useContext` con un provider de cliente.
*   **Librerías del navegador:** Gráficos, carruseles, APIs de geolocalización.

**Ejemplo:**

```jsx
'use client'

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

## Composición: La clave para optimizar

Es posible intercalar Server y Client Components. La regla de oro es: puedes renderizar un Client Component dentro de un Server Component, y pasar Server Components como `children` (o props) de un Client Component.

```jsx
// app/layout.js (Server Component raíz)
import ThemeProvider from './ThemeProvider' // Client Component (provee contexto)
import Navigation from './Navigation' // Server Component

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        <ThemeProvider>
          <Navigation /> {/* Server Component pasado como children */}
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

> [!IMPORTANT]
> `ThemeProvider` es un Client Component porque usa `useState` para el tema, pero los hijos que recibe pueden ser Server Components; estos no se hidratan como cliente, manteniendo **cero JS** para ellos.

## Límites de cliente (Client Boundaries)

Next.js genera un límite de cliente al importar un Client Component desde un Server Component. El bundle JS del Client Component incluirá todo el subárbol a partir de ese punto (a menos que se pasen Server Components como props).

### Buenas prácticas:

1.  **Server Components por defecto:** Úsalos para la estructura y fetching de datos.
2.  **Mueve el cliente a las hojas:** Extrae la interactividad en pequeños Client Components (p. ej., un botón de "Me gusta" vs. el post completo).
3.  **Props serializables:** Pasa datos desde Server a Client vía props que puedan convertirse a JSON.
4.  **No conviertas componentes grandes:** Evita declarar `'use client'` en componentes raíz si solo un pequeño botón necesita interactividad.

### Casos típicos de mezcla:

*   **Navegación interactiva:** El componente `Nav` es Server, pero el botón hamburguesa (estado abierto/cerrado) es Client.
*   **Formularios:** El formulario es Client (necesita `onSubmit` o estados locales), pero la acción que invoca es una Server Action.
*   **Temas:** Un provider Client a nivel raíz, pero las páginas internas son completamente Server.

---

Entender esta separación te permite maximizar el rendimiento y la experiencia de desarrollo en Next.js.