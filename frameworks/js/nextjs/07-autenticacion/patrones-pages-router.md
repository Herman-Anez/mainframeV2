# Patrones de Autenticación en Pages Router

En el **Pages Router**, la autenticación se implementa combinando la obtención de datos del lado del servidor (`getServerSideProps`) con **API Routes** para manejar el flujo de sesión y **cookies httpOnly** para el almacenamiento seguro de tokens.

---

## Autenticación basada en Cookies httpOnly

Este enfoque previene ataques **XSS** al almacenar el token de sesión en una cookie inaccesible para JavaScript.

### 1. API de Login: `pages/api/login.js`
Valida credenciales, genera un token y establece la cookie de sesión.

```javascript
import { serialize } from 'cookie'
import { signToken } from '../../../lib/jwt'

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end()

  const { email, password } = req.body
  const user = await validateUser(email, password)
  
  if (!user) return res.status(401).json({ error: 'Credenciales inválidas' })

  const token = await signToken(user)
  
  res.setHeader('Set-Cookie', serialize('token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/',
    maxAge: 60 * 60 * 24, // 1 día
  }))

  res.status(200).json({ ok: true })
}
```

### 2. Protección de Páginas
Verifica la cookie en `getServerSideProps` para decidir si renderizar la página o redirigir.

```jsx
// pages/dashboard.js
import { verifyToken } from '../lib/jwt'

export async function getServerSideProps({ req }) {
  const token = req.cookies.token
  
  if (!token) {
    return { redirect: { destination: '/login', permanent: false } }
  }

  try {
    const usuario = await verifyToken(token)
    return { props: { usuario } }
  } catch {
    return { redirect: { destination: '/login', permanent: false } }
  }
}

export default function Dashboard({ usuario }) {
  return <div>Bienvenido, {usuario.nombre}</div>
}
```

---

## Autenticación con NextAuth.js (v4)

NextAuth simplifica la integración de proveedores OAuth (Google, GitHub) y credenciales personalizadas.

### Configuración: `pages/api/auth/[...nextauth].js`
```javascript
import NextAuth from 'next-auth'
import GithubProvider from 'next-auth/providers/github'

export default NextAuth({
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_ID,
      clientSecret: process.env.GITHUB_SECRET,
    }),
    // ... otros proveedores
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) token.role = (user as any).role
      return token
    },
    async session({ session, token }) {
      if (session.user) (session.user as any).role = token.role
      return session
    }
  },
  secret: process.env.NEXTAUTH_SECRET,
})
```

### Proteger Páginas con NextAuth
Usa `getServerSession` para una verificación robusta en el servidor.

```javascript
import { getServerSession } from 'next-auth/next'
import { authOptions } from './api/auth/[...nextauth]'

export async function getServerSideProps(context) {
  const session = await getServerSession(context.req, context.res, authOptions)
  
  if (!session) {
    return { redirect: { destination: '/auth/login', permanent: false } }
  }
  
  return { props: { session } }
}
```

---

## Consideraciones de Seguridad

*   **Cookies httpOnly:** Requieren HTTPS en producción (`secure: true`).
*   **Políticas de SameSite:** Usa `sameSite: 'strict'` o `'lax'` para mitigar ataques CSRF.
*   **Stateless vs Stateful:** Por defecto, NextAuth usa JWT (stateless). Si necesitas invalidar sesiones de forma remota, configura un **adaptador de base de datos**.
*   **Props Sensibles:** No pases información crítica (como el token o contraseñas) a las `props` del componente, ya que se serializan y son visibles en el HTML del cliente.

> [!IMPORTANT]
> A diferencia del App Router, el Pages Router requiere implementar la protección manualmente en cada página mediante `getServerSideProps` o un HOC de cliente, aunque el uso de `middleware` global también es posible en versiones recientes.