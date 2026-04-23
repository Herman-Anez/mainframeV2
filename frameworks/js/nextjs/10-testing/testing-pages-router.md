## Archivo: `10-testing/testing-pages-router.md`

Testing en Pages Router

Probar una aplicación Next.js con Pages Router implica combinar tests unitarios, de integración y end‑to‑end (E2E). La naturaleza híbrida (SSR/SSG) exige verificar tanto la lógica del servidor como la del cliente.
Herramientas recomendadas

    Jest como framework de testing unitario y de integración.

    React Testing Library (RTL) para probar componentes en un entorno simulado de navegador.

    Cypress o Playwright para E2E.

    MSW (Mock Service Worker) para interceptar peticiones en tests de cliente/integración.

### Configuración de Jest

Instala dependencias:
```bash
```
npm i -D jest @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom

En package.json añade los scripts y la configuración de Jest:
```json
```
"scripts": {
  "test": "jest --watch",
  "test:ci": "jest --ci"
},
"jest": {
  "testEnvironment": "jsdom",
  "setupFilesAfterSetup": ["<rootDir>/jest.setup.js"],
  "moduleNameMapper": {
    "^@/(.*)$": "<rootDir>/src/$1"
  }
}

Crea jest.setup.js:
```js
import '@testing-library/jest-dom'
```

Opcionalmente instala @types/jest para TypeScript.
Test unitario de una función de utilidad
```js
// utils/sum.js
export const sum = (a, b) => a + b
```

js

### // __tests__/sum.test.js
import { sum } from '../utils/sum'

### test('suma correctamente dos números', () => {
  expect(sum(2, 3)).toBe(5)
})

### Test de un componente básico (sin datos del servidor)
```jsx
// components/Saludo.js
export default function Saludo({ nombre }) {
  return <h1>Hola {nombre}</h1>
}
```

### jsx

### // __tests__/Saludo.test.jsx
import { render, screen } from '@testing-library/react'
import Saludo from '../components/Saludo'

### test('muestra el saludo con el nombre', () => {
  render(<Saludo nombre="Mario" />)
  expect(screen.getByText('Hola Mario')).toBeInTheDocument()
})

### Test de una página con getStaticProps

Podemos probar la función getStaticProps de forma aislada (es una función que retorna props).
```js
// pages/blog.js
export async function getStaticProps() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json())
  return { props: { posts } }
}
```

js

### // __tests__/blog.test.js
import { getStaticProps } from '../pages/blog'

### jest.mock('node-fetch')  // o fetch global con jest.fn()

### test('obtiene posts y los retorna como props', async () => {
  const mockPosts = [{ id: 1, title: 'A' }]
  global.fetch = jest.fn(() =>
    Promise.resolve({ json: () => Promise.resolve(mockPosts) })
  )

### const result = await getStaticProps({})
  expect(result.props.posts).toEqual(mockPosts)
})

Nota: En Next.js el fetch está disponible globalmente en el entorno de test si usas Node 18+, así que puedes mockearlo directamente.
Test de una página renderizada (SSG/SSR) con datos de servidor

Cuando la página recibe props desde el servidor, podemos renderizarla sin necesidad de ejecutar getStaticProps. Pasamos las props manualmente.
```jsx
// pages/blog.js
export default function Blog({ posts }) {
  return (
    <ul>
      {posts.map(p => <li key={p.id}>{p.title}</li>)}
    </ul>
  )
}
```

### jsx

### // __tests__/Blog.test.jsx
import { render, screen } from '@testing-library/react'
import Blog from '../pages/blog'

### test('renderiza lista de posts', () => {
  const posts = [{ id: 1, title: 'Un post' }]
  render(<Blog posts={posts} />)
  expect(screen.getByText('Un post')).toBeInTheDocument()
})

### Simular el router

Para componentes que usan useRouter o <Link>, podemos mockear next/router.
```js
// __tests__/helpers.js
jest.mock('next/router', () => ({
  useRouter: () => ({
    route: '/',
    pathname: '',
    query: {},
    asPath: '',
    push: jest.fn(),
    replace: jest.fn(),
  }),
}))
```

Para next/link, RTL lo reconoce porque renderiza un <a>, así que podemos comprobar el atributo href.
Test de API Routes

Las API Routes son funciones que reciben req y res. Podemos probarlas con httpMocks o creando objetos mock.
```js
// pages/api/hola.js
export default function handler(req, res) {
  res.status(200).json({ mensaje: 'Hola' })
}
```

js

### import handler from '../pages/api/hola'
import { createMocks } from 'node-mocks-http'

### test('devuelve mensaje de hola', async () => {
  const { req, res } = createMocks({ method: 'GET' })
  await handler(req, res)

### expect(res._getStatusCode()).toBe(200)
  expect(JSON.parse(res._getData())).toEqual({ mensaje: 'Hola' })
})

### Integración con Cypress

Cypress se ejecuta contra la aplicación corriendo. Para Pages Router, es similar a cualquier React app. Un ejemplo de test E2E:
```js
// cypress/e2e/home.cy.js
describe('Página principal', () => {
  it('muestra el título', () => {
    cy.visit('/')
    cy.contains('Bienvenido').should('be.visible')
  })
})
```

Cypress maneja la navegación igual que un navegador real. Para SSR/SSG no hay diferencia porque el HTML ya viene renderizado.
Mock de fetch en el frontend con MSW

Para testear componentes que llaman a APIs en el cliente, MSW permite interceptar y simular respuestas.
```js
// __tests__/setupMSW.js
import { rest } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  rest.get('/api/perfil', (req, res, ctx) =>
    res(ctx.json({ nombre: 'Test' }))
  )
)
beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

Con esto, los componentes que usan fetch('/api/perfil') reciben el mock.

El testing en Pages Router es directo: separas la lógica de servidor de los componentes y aplicas técnicas estándar de React testing con algunos mocks específicos de Next.js.