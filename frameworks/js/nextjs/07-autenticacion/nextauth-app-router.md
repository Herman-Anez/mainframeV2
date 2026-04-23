# Autenticación con NextAuth.js (Auth.js) en App Router

En el **App Router**, NextAuth.js (v5, ahora conocida como **Auth.js**) se integra de forma nativa mediante **Server Components**, **Server Actions** y **Middleware**. Su configuración es modular y aprovecha la arquitectura moderna de Next.js.

## Instalación y Configuración

```bash
npm install next-auth@beta
```

Crea un archivo `auth.ts` (o `.js`) en la raíz de `src` o en `lib/`. Aquí defines la configuración y exportas las funciones clave.

```ts
// auth.ts
import NextAuth from 'next-auth'
import GitHub from 'next-auth/providers/github'
import Credentials from 'next-auth/providers/credentials'

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID,
      clientSecret: process.env.GITHUB_CLIENT_SECRET,
    }),
    Credentials({
      credentials: {
        email: {},
        password: {},
      },
      authorize: async (credentials) => {
        const user = await validarCredenciales(credentials)
        return user ?? null
      },
    }),
  ],
  callbacks: {
    jwt({ token, user }) {
      if (user) token.role = (user as any).role
      return token
    },
    session({ session, token }) {
      if (session.user) (session.user as any).role = token.role
      return session
    },
  },
  pages: {
    signIn: '/login',
  },
})
```

### Exponer los Handlers
Debes configurar un **Route Handler** en `app/api/auth/[...nextauth]/route.ts`:

```ts
import { handlers } from '@/auth'
export const { GET, POST } = handlers
```

## Obtener la sesión en Server Components

Usa la función `auth` exportada para obtener la sesión de forma asíncrona y directa.

```tsx
// app/dashboard/page.tsx
import { auth } from '@/auth'
import { redirect } from 'next/navigation'

export default async function Dashboard() {
  const session = await auth()
  
  if (!session) {
    redirect('/api/auth/signin')
  }

  return <div>Bienvenido, {session.user?.name}</div>
}
```

> [!NOTE]
> La sesión se recupera automáticamente de las cookies, sin necesidad de pasar el objeto `request` manualmente.

## Uso en Client Components

Para componentes interactivos, envuelve tu aplicación con el `SessionProvider` (de `next-auth/react`).

**Layout raíz:**
```tsx
import { SessionProvider } from 'next-auth/react'
import { auth } from '@/auth'

export default async function RootLayout({ children }) {
  const session = await auth()
  return (
    <html lang="es">
      <body>
        <SessionProvider session={session}>
          {children}
        </SessionProvider>
      </body>
    </html>
  )
}
```

**Componente de Cliente:**
```tsx
'use client'
import { useSession, signIn, signOut } from 'next-auth/react'

export default function UserStatus() {
  const { data: session } = useSession()

  if (session) {
    return (
      <>
        <p>Conectado como {session.user?.email}</p>
        <button onClick={() => signOut()}>Cerrar sesión</button>
      </>
    )
  }
  
  return <button onClick={() => signIn()}>Iniciar sesión</button>
}
```

---

## Adaptadores y Base de Datos

Si necesitas persistir usuarios y sesiones, instala un adaptador compatible (ej. Prisma).

```ts
import { PrismaAdapter } from '@auth/prisma-adapter'
import prisma from '@/lib/prisma'

export const { handlers, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [...],
})
```

> [!IMPORTANT]
> Con un adaptador, las sesiones se almacenan en la base de datos, reduciendo el tamaño de la cookie y permitiendo un control más estricto sobre las sesiones activas.

---

## Seguridad y Mejores Prácticas

*   **Variables de Entorno:** Utiliza siempre `AUTH_SECRET` (o `NEXTAUTH_SECRET`) para firmar las cookies.
*   **Cookies Seguras:** NextAuth configura automáticamente cookies `httpOnly` y `secure` en producción.
*   **Protección en APIs:** Usa `auth()` dentro de tus **Route Handlers** para validar el acceso.

```ts
import { auth } from '@/auth'
import { NextResponse } from 'next/server'

export async function GET() {
  const session = await auth()
  if (!session) return NextResponse.json({ error: 'No autorizado' }, { status: 401 })
  // ... lógica protegida
}
```

---

NextAuth v5 (Auth.js) está optimizado para el App Router, reduciendo el código repetitivo y aprovechando al máximo la seguridad del lado del servidor.
