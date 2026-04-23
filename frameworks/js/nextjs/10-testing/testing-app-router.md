## Archivo: `10-testing/testing-app-router.md`

Testing en App Router

El App Router trae un modelo de React Server Components que cambia la forma de testear. No puedes renderizar Server Components en un entorno puramente cliente (jsdom), pero tenemos estrategias para probar tanto el comportamiento del servidor como la UI interactiva.
Enfoques de testing según el tipo de componente

    Funciones, lógica de negocio, auth.ts, utils: se prueban como funciones Node.js normales.

    Server Components (asíncronos): se prueban renderizándolos con @testing-library/react en un entorno que soporte async. Next.js recomienda usar render de @testing-library/react junto con jsdom y jest (con algunas adaptaciones). Para RSC puros (no clientes) podemos importar y renderizar directamente el componente, pasando las props que normalmente obtendría del servidor.

    Client Components: igual que en Pages Router, pero necesitan la directiva 'use client'; si se importan desde un test, debes mockear lo mínimo (por ejemplo, next/navigation).

    Route Handlers: se testean invocando las funciones exportadas con objetos Request simulados.

    Server Actions: se prueban como funciones asíncronas con argumentos simulados y luego verificamos efectos secundarios o revalidaciones.

    Middlewares: se prueban creando un NextRequest falso y llamando al middleware.

### Configuración de Jest para App Router

Instala las mismas dependencias que para Pages, además de next-router-mock o mocks manuales de next/navigation. A partir de Next.js 14, muchos proyectos utilizan Vitest por su mejor soporte ESM, pero Jest sigue siendo popular. Usaremos Jest con las transformaciones necesarias.

Para soportar next/dynamic, next/image, next/link, etc., necesitas mocks. La guía de testing de Next.js sugiere lo siguiente en jest.config.js:
```js
```
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterSetup: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^next/navigation$': '<rootDir>/__mocks__/next-navigation.js',
    '^next/image$': '<rootDir>/__mocks__/next-image.js',
    '^next/link$': '<rootDir>/__mocks__/next-link.js',
  },
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', { presets: ['next/babel'] }],
  },
}

Crea los mocks:

__mocks__/next-navigation.js:
```js
export const useRouter = jest.fn(() => ({
  push: jest.fn(),
  replace: jest.fn(),
  back: jest.fn(),
  prefetch: jest.fn(),
}))

export const usePathname = jest.fn(() => '/')
export const useSearchParams = jest.fn(() => new URLSearchParams())
export const notFound = jest.fn()
export const redirect = jest.fn()
```

__mocks__/next-image.js:
```js
const MockImage = (props) => <img {...props} />
export default MockImage
```

__mocks__/next-link.js:
```js
import React from 'react'
const MockLink = ({ children, href, ...rest }) => (
  <a href={href} {...rest}>{children}</a>
)
export default MockLink
```

### Test de un Server Component

Los Server Components asíncronos pueden ser renderizados con render de RTL si los envolvemos en un Suspense y los tratamos como un componente normal. Como no son 'use client', podemos importarlos y renderizarlos. Ejemplo:
```tsx
// app/productos/page.tsx
export default async function ProductosPage() {
  const res = await fetch('https://api.example.com/productos')
  const productos = await res.json()
  return <ul>{productos.map(p => <li key={p.id}>{p.nombre}</li>)}</ul>
}
```

Para testearlo, mockeamos fetch:
```tsx
// __tests__/ProductosPage.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import ProductosPage from '@/app/productos/page'
```

### beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve([{ id: 1, nombre: 'Pelota' }]),
    })
  ) as jest.Mock
})

### test('renderiza lista de productos', async () => {
  // El componente es async, se resuelve en el render
  render(await ProductosPage())
  expect(screen.getByText('Pelota')).toBeInTheDocument()
})

También podemos usar waitFor si el componente tiene Suspense.
Test de un Client Component

Funciona igual que en Pages Router, solo que debemos tener cuidado con las importaciones de next/navigation. Al mockearlas, el componente usará los mocks y podremos verificar llamadas a push.
```tsx
'use client'
import { useRouter } from 'next/navigation'

export default function BotonNavegar() {
  const router = useRouter()
  return <button onClick={() => router.push('/about')}>Ir</button>
}
```

### tsx

### import { render, screen, fireEvent } from '@testing-library/react'
import BotonNavegar from '@/components/BotonNavegar'
import { useRouter } from 'next/navigation'

### jest.mock('next/navigation')

### test('navega a /about al hacer clic', () => {
  const pushMock = jest.fn()
  ;(useRouter as jest.Mock).mockReturnValue({ push: pushMock })

### render(<BotonNavegar />)
  fireEvent.click(screen.getByText('Ir'))
  expect(pushMock).toHaveBeenCalledWith('/about')
})

### Test de Route Handlers

Exportas funciones GET, POST, etc. Simula un Request y llama a la función.
```ts
// app/api/hello/route.ts
export async function GET() {
  return Response.json({ message: 'Hola' })
}
```

ts

### import { GET } from '@/app/api/hello/route'

### test('retorna mensaje', async () => {
  const response = await GET()
  const data = await response.json()
  expect(response.status).toBe(200)
  expect(data).toEqual({ message: 'Hola' })
})

### Test de Server Actions

Son funciones normales, las importamos y las ejecutamos.
```ts
'use server'
export async function crearPost(formData: FormData) {
  // lógica...
}
```

ts

### import { crearPost } from '@/actions'
import { revalidatePath } from 'next/cache'

### jest.mock('next/cache', () => ({
  revalidatePath: jest.fn(),
}))

### test('crea un post y revalida', async () => {
  const formData = new FormData()
  formData.append('title', 'Nuevo')
  await crearPost(formData)
  expect(revalidatePath).toHaveBeenCalledWith('/posts')
})

### Test de Middleware

Crea un NextRequest simulado con la URL y cookies deseadas.
```ts
import { middleware, config } from '@/middleware'
import { NextResponse } from 'next/server'
```

### test('redirige a login si no hay token', async () => {
  const req = new Request('http://localhost/dashboard', { headers: {} })
  // Middleware espera NextRequest; podemos usar NextRequest o simular
  const res = await middleware(req as any)
  expect(res?.status).toBe(307) // redirección
})

### E2E con Cypress / Playwright

El testing E2E en App Router es similar a Pages, pero aprovecha que el streaming puede causar que el contenido aparezca de forma asíncrona. Playwright tiene mejor soporte para esperar por el contenido estático/dinámico. Ejemplo con Playwright:
```ts
import { test, expect } from '@playwright/test'
```

### test('página de productos muestra lista', async ({ page }) => {
  await page.goto('/productos')
  await expect(page.locator('li')).toHaveCount(10)
})

Playwright maneja el streaming: espera a que el HTML completo esté presente.

El testing en App Router requiere mockear las nuevas APIs (next/navigation, next/headers, etc.) pero mantiene la misma filosofía: aislar y probar cada capa (funciones, componentes cliente, endpoints). Con los mocks adecuados, la experiencia es fluida.
---
