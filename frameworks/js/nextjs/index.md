
## Archivo: `11-typescript/configuracion.md`

Configuración de TypeScript en Next.js

Next.js tiene soporte nativo para TypeScript, por lo que no necesitas configurar compiladores adicionales. Basta con usar la extensión .ts o .tsx y Next se encarga del resto.
Crear proyecto con TypeScript

Al ejecutar create-next-app, la opción “TypeScript” viene activada por defecto, generando tsconfig.json.
```bash
```
npx create-next-app@latest mi-app

Si migras un proyecto existente, crea un tsconfig.json vacío y ejecuta npm run dev. Next.js lo rellenará automáticamente con la configuración recomendada.
tsconfig.json por defecto
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

Los puntos más relevantes:

    strict: true habilita todas las verificaciones estrictas (recomendado).

    paths: permite importar con alias @/ (ajusta según tu carpeta src o raíz).

    plugins: [{ name: 'next' }]: habilita el plugin del lenguaje Next en editores como VS Code, mejorando el autocompletado.

    .next/types contiene tipos generados por Next (ej. para rutas).

### Tipos adicionales

Instala @types/react y @types/node si no están.
```bash
```
npm i -D @types/react @types/node

### TypeScript en next.config.js

Puedes renombrar next.config.js a next.config.ts para usar TypeScript. Next.js lo transpilará antes de usarlo.
```ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  reactStrictMode: true,
}
export default config
```

### Tipos para Pages Router

Next exporta tipos específicos que puedes usar para tipar páginas:

    NextPage para componentes de página.

    GetServerSideProps, GetStaticProps, GetStaticPaths para las funciones de obtención de datos.

```tsx
import { GetServerSideProps, NextPage } from 'next'

type Post = { id: number; title: string }

interface Props {
  posts: Post[]
}

export const getServerSideProps: GetServerSideProps<Props> = async () => {
  const posts: Post[] = await fetch('...').then(r => r.json())
  return { props: { posts } }
}

const Blog: NextPage<Props> = ({ posts }) => (
  <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
)

export default Blog
```

Para getStaticPaths:
```ts
export const getStaticPaths: GetStaticPaths = async () => {
  // ...
}
```

### Tipos para App Router

El App Router usa sus propios tipos, a menudo inferidos automáticamente. Por ejemplo, los parámetros de ruta (params) y searchParams tienen tipado automático en muchos casos con el plugin de Next. Pero es bueno especificarlos:
```tsx
// app/blog/[slug]/page.tsx
type Props = {
  params: { slug: string }
  searchParams?: { [key: string]: string | string[] | undefined }
}

export default function Page({ params }: Props) {
  return <h1>{params.slug}</h1>
}
```

Para generateMetadata:
```ts
import { Metadata } from 'next'

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  return { title: params.slug }
}
```

### Tipos para Server Actions

Puedes definir Server Actions con FormData o tipos personalizados:
```ts
'use server'

export async function actualizar(formData: FormData): Promise<void> {
  const nombre = formData.get('nombre') as string
  // ...
}
```

### Strict mode y any

Es tentador usar any cuando los tipos de Next se vuelven complejos. Intenta evitarlo, especialmente en funciones de obtención de datos y páginas. Las herramientas de Next y TypeScript evolucionan constantemente, y cada vez es más fácil tener tipos precisos.
Módulos externos sin tipos

Si una librería no tiene tipos, puedes declarar un módulo en *.d.ts. Por ejemplo, js-cookie:
```ts
// types/global.d.ts
declare module 'js-cookie' {
  export function get(name: string): string | undefined
  export function set(name: string, value: string, options?: any): void
}
```

La configuración de TypeScript en Next.js está diseñada para funcionar de inmediato, pero conocer los detalles te permitirá aprovechar al máximo el autocompletado y la seguridad de tipos.
---

## Archivo: `11-typescript/tipos-utiles.md`

Tipos útiles de Next.js y TypeScript

Next.js proporciona una gran cantidad de tipos para mejorar la productividad y evitar errores. A continuación, un compendio de los más utilizados.
Tipos para Pages Router
Tipo	Uso
NextPage	Componente de página opcionalmente tipado por props.
NextPageWithLayout	Permite definir un método getLayout en la página.
GetServerSideProps	Tipa la función getServerSideProps.
GetStaticProps	Tipa la función getStaticProps.
GetStaticPaths	Tipa la función getStaticPaths.
InferGetServerSidePropsType	Infiere el tipo de las props a partir de getServerSideProps.
InferGetStaticPropsType	Similar para getStaticProps.

Ejemplo de InferGetStaticPropsType (evita redundancia):
```tsx
import { InferGetStaticPropsType } from 'next'

export async function getStaticProps() {
  const data = await fetchData()
  return { props: { data } }
}

export default function Page({ data }: InferGetStaticPropsType<typeof getStaticProps>) {
  // data está tipado correctamente
}
```

### Tipos para App Router

Los tipos principales provienen de next y next/navigation.

PageProps (informal): aunque no existe un tipo exportado llamado PageProps, puedes definir uno basado en los parámetros esperados.
```tsx
type Props = {
  params: { id: string }
  searchParams: { [key: string]: string | string[] | undefined }
}
```

Metadata y ResolvingMetadata: para generar metadatos.
```ts
import type { Metadata, ResolvingMetadata } from 'next'

export async function generateMetadata(
  { params }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const previousOpenGraph = (await parent).openGraph ?? {}
  return {
    title: 'Nuevo',
    openGraph: { ...previousOpenGraph, title: 'Nuevo' },
  }
}
```

Web Request y NextRequest / NextResponse: en Route Handlers y middleware.
```ts
import { NextRequest, NextResponse } from 'next/server'

export function middleware(req: NextRequest) {
  // ...
}
```

React.ReactNode en layouts y children.
```tsx
export default function Layout({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}
```

### Tipos de next/navigation
Hook / Función	Tipo / Retorno
useRouter	NextRouter
usePathname	string
useSearchParams	ReadonlyURLSearchParams
useParams	{ [key: string]: string | string[] }
redirect	never (no retorna)
notFound	never

Al mockear en tests, es útil conocer estos tipos.
Tipos para next/headers

Las funciones cookies() y headers() devuelven objetos con métodos tipados.
```ts
import { cookies } from 'next/headers'

export function getToken() {
  const cookieStore = cookies()
  const token = cookieStore.get('token') // { name: string, value: string } | undefined
}
```

### Tipos para Server Actions

Puedes tipar el parámetro formData o usar tipos convencionales cuando se invocan desde eventos.
```ts
'use server'
export async function submit(data: { name: string; email: string }) {
  // ...
}
```

Si se usa desde un formulario con action={submit}, se debe usar FormData. Pero puedes crear una función intermedia:
```ts
export async function handleSubmit(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string
  await submit({ name, email })
}
```

### Tipos para next.config.ts
```ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  env: {
    miVariable: process.env.MI_VARIABLE, // error si no existe en el entorno
  },
}
```

### Tipos para next/image

El componente Image acepta ImageProps (exportado) que extiende los atributos de imagen HTML con propiedades específicas.
```tsx
import Image, { ImageProps } from 'next/image'
type Props = Omit<ImageProps, 'src' | 'alt'> & {
  imagen: string
  descripcion: string
}
```

### Tipos en getStaticPaths con i18n

Cuando usas locales, GetStaticPathsContext incluye locales y defaultLocale.
```ts
export const getStaticPaths: GetStaticPaths = async (context) => {
  const { locales } = context
  // ...
}
```

### NextApiRequest y NextApiResponse (Pages Router API)
```ts
import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse<Data>) {
  // ...
}
```

### Tipos para contexto en layouts anidados

No hay un tipo integrado para params en layouts, porque pueden variar. Pero puedes crear una interfaz:
```tsx
interface DashboardLayoutProps {
  children: React.ReactNode
  params: { userId: string }
}
```

### Utiliza satisfies para seguridad extra

Con TypeScript 4.9+ puedes emplear satisfies para verificar que un objeto cumple un tipo sin cambiar su inferencia. Muy útil en configuraciones.
```ts
const metadata = {
  title: 'Mi app',
} satisfies Metadata
```

Estos tipos reducen los errores en tiempo de compilación y mejoran la experiencia de desarrollo.
---

## Archivo: `12-cli-y-scripts/comandos-next.md`

CLI de Next.js y scripts personalizados

Next.js incluye una interfaz de línea de comandos (CLI) con múltiples comandos para desarrollo, construcción y análisis. También ofrece un conjunto de scripts que se integran en package.json.
Comandos principales de la CLI
Comando	Descripción
next dev	Inicia el servidor de desarrollo con Hot Module Replacement en localhost:3000.
next build	Compila la aplicación para producción (optimizada).
next start	Inicia el servidor en modo producción (requiere next build previo).
next lint	Ejecuta ESLint en los archivos del proyecto.
next telemetry	Habilita/deshabilita la telemetría (datos anónimos de uso a Vercel).
next info	Muestra información del entorno (útil para reportar bugs).
next dev
```bash
```
next dev [opciones]

Opciones comunes:

    -p, --port <puerto>: cambiar el puerto (por defecto 3000).

    -H, --hostname <host>: por defecto localhost. Usa 0.0.0.0 para exponer en red local.

    --turbo: usa Turbopack para compilaciones más rápidas (si está disponible).

Ejemplos:
```bash
```
next dev -p 4000
next dev --turbo

### next build
```bash
```
next build

Genera una carpeta .next con el bundle optimizado. Analiza las páginas y muestra si son estáticas ○, dinámicas λ, o requieren ISR. Es compatible con perfiles: next build --profile habilita el perfilador de Webpack/Turbopack.
next start
```bash
```
next start [opciones]

Similar a next dev en opciones de puerto y host. Inicia la aplicación en modo producción (después de next build). Ideal para pruebas locales de la build final.
next lint
```bash
```
next lint [opciones]

Ejecuta ESLint con la configuración base de Next.js. Opciones:

    --fix: corrige automáticamente errores.

    --dir <directorio>: limita el escaneo a un directorio.

    --file <archivo>: analiza un solo archivo.

Por defecto, el comando se configura en package.json como "lint": "next lint".
next telemetry
```bash
```
next telemetry [status/enable/disable]

Muestra el estado o modifica la telemetría. Los datos recopilados son anónimos y se limitan a características usadas, rendimiento de build, etc.
next info
```bash
```
next info

Imprime información relevante del entorno: versión de Next, Node, sistema operativo, configuraciones. Muy útil al abrir una issue en GitHub.
Scripts recomendados en package.json
```json
```
"scripts": {
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "next lint",
  "lint:fix": "next lint --fix",
  "type-check": "tsc --noEmit",
  "format": "prettier --write .",
  "test": "jest --watch",
  "test:ci": "jest --ci",
  "prepare": "husky install"
}

### create-next-app

Aunque no es parte de la CLI en sí, create-next-app es el generador oficial:
```bash
```
npx create-next-app@latest [nombre] [opciones]

Opciones interactivas: TypeScript, ESLint, Tailwind, src directory, App Router, import alias. También acepta flags:
```bash
```
npx create-next-app@latest --ts --tailwind --app mi-app

### Personalización avanzada

Puedes crear scripts personalizados que invoquen la Next.js CLI desde Node.js. Por ejemplo, un script que genere sitemaps después del build:
```js
// scripts/generate-sitemap.js
const { execSync } = require('child_process')
execSync('next build', { stdio: 'inherit' })
// luego generas el sitemap...
```

### Uso de next export (legado)

Hasta Next.js 13, next export era el comando para salida estática. Ahora se configura con output: 'export' y next build crea directamente la carpeta out.
Modo de depuración

Para depurar el servidor Next.js (con Node inspector), ejecuta:
```bash
```
NODE_OPTIONS='--inspect' next dev

Luego conecta el inspector de Chrome o VS Code.

La CLI de Next.js es concisa pero potente, y al combinarla con scripts personalizados puedes automatizar tareas de desarrollo y despliegue con facilidad.

Con estos archivos, has completado todo el temario hasta 12-cli-y-scripts. Si necesitas profundizar en algún punto o añadir algún otro módulo (por ejemplo, next-auth avanzado, etc.), estoy a tu disposición.
