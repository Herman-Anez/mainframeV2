## 📘 01-pages-router/rutas-estaticas-y-dinamicas.md

### Rutas estáticas y dinámicas en Pages Router

El sistema de archivos de `pages/` soporta dos tipos de rutas: estáticas (archivos con nombre fijo) y dinámicas (archivos con corchetes).

#### Rutas estáticas

Cualquier archivo que no use corchetes se convierte en una ruta fija.

- `pages/contacto.js` → `/contacto`
- `pages/productos/categoria.js` → `/productos/categoria`

#### Rutas dinámicas básicas

Las rutas dinámicas permiten capturar segmentos variables de la URL. Se definen encerrando el nombre del parámetro entre corchetes.

- `pages/posts/[id].js` → `/posts/1`, `/posts/abc`, etc.

Dentro del componente de página, se accede al parámetro mediante `useRouter`:

```jsx
import { useRouter } from 'next/router'

export default function Post() {
  const router = useRouter()
  const { id } = router.query

  return <h1>Artículo: {id}</h1>
}
```

`router.query` es un objeto que contiene los parámetros de la URL.

> [!WARNING]
> En el primer renderizado `router.query` puede estar vacío (pre-renderizado estático o en cliente), por eso debes manejar el estado de carga.

#### Rutas dinámicas anidadas

- `pages/posts/[id]/comments.js` → `/posts/1/comments`
El hook `useRouter` devolverá `{ id: '1' }` en `query`.

#### Rutas catch-all (captura todas)

Permiten capturar múltiples segmentos de la ruta. Se utiliza `[...nombre]`.

- `pages/docs/[...slug].js` → `/docs`, `/docs/intro`, `/docs/guia/instalacion`, etc.

El valor de `slug` será un array de strings.

```jsx
import { useRouter } from 'next/router'

export default function Docs() {
  const router = useRouter()
  const { slug = [] } = router.query // ¡siempre array!

  return <h1>Ruta completa: {slug.join('/')}</h1>
}
```

#### Rutas catch-all opcionales

Para que la ruta también coincida sin el parámetro (es decir, la ruta base), se usa doble corchete: `[[...slug]]`.

- `pages/productos/[[...filtros]].js`
  - `/productos` → `filtros` será `undefined` o `[]`.
  - `/productos/electronica/2024` → `filtros = ['electronica', '2024']`.

#### Enlaces y prefetching

El componente `Link` funciona perfectamente con rutas dinámicas:

```jsx
<Link href={`/posts/${post.id}`}>{post.title}</Link>
```

Para prefetching automático, Next.js solo precarga la página si el enlace es visible (predeterminado) o si se usa `prefetch={true}`. Puedes deshabilitarlo con `prefetch={false}`.

#### Navegación superficial (Shallow Routing)

Permite cambiar la URL sin ejecutar métodos de obtención de datos (`getServerSideProps`, etc.). Útil para filtros que solo afectan el lado del cliente.

```jsx
router.push('/productos?color=rojo', undefined, { shallow: true })
```

#### Consideraciones

1. Siempre valida el tipo de `query.params` porque inicialmente pueden estar vacíos.
2. Evita usar `router.query` directamente en el renderizado si tu página depende del dato; mejor usa un estado o maneja `isReady`.

```jsx
const router = useRouter()
if (!router.isReady) return <div>Cargando...</div>
```

---
