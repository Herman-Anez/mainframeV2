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