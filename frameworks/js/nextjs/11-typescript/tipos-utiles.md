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
