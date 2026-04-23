# Rutas Estáticas, Dinámicas y Paralelas en App Router

El **App Router** ofrece un modelo de enrutamiento mucho más potente que el Pages Router. Además de las rutas estáticas y dinámicas, introduce rutas paralelas e interceptación de rutas.

## Rutas Estáticas

Simplemente crea una carpeta con un archivo `page.js`. Next.js asigna la URL automáticamente basándose en la jerarquía de carpetas. El archivo `page.js` exporta por defecto un componente (Server o Client).

*   `app/contacto/page.js` → `/contacto`
*   `app/acerca/nosotros/page.js` → `/acerca/nosotros`

## Rutas Dinámicas (Segmentos Variables)

Se indican con carpetas entre corchetes: `[id]`, `[slug]`. Los parámetros se reciben mediante la prop `params`.

*   `app/productos/[id]/page.js` → `/productos/1`, `/productos/abc`, etc.

### Implementación en Server Components:

```jsx
export default function Producto({ params }) {
  const { id } = params
  return <h1>Producto: {id}</h1>
}
```

**Ejemplo en TypeScript:**
```tsx
type Props = { params: { id: string } }

export default function Producto({ params }: Props) {
  /* ... */
}
```

### Implementación en Client Components:

```jsx
'use client'
import { useParams } from 'next/navigation'

export default function Producto() {
  const params = useParams() // { id: '...' }
  return <h1>{params.id}</h1>
}
```

## Rutas Catch-all (Captura Todas)

Se definen con `[...slug]` y capturan cualquier cantidad de segmentos.

*   `app/docs/[...slug]/page.js` → `/docs/intro`, `/docs/guia/instalacion`.
*   `params.slug` será un array de strings: `['intro']`, `['guia', 'instalacion']`.

> [!TIP]
> Para que la ruta base también coincida (sin segmentos extras), usa **`[[...slug]]`** (catch-all opcional).
> *   `app/docs/[[...slug]]/page.js` → `/docs` (`slug` = `undefined`/`[]`), `/docs/uno` (`slug` = `['uno']`).

## Rutas Paralelas

Las rutas paralelas permiten renderizar múltiples árboles de páginas en la misma vista, cada uno con su propio enrutamiento. Se implementan mediante **slots**: carpetas con el prefijo `@`.

### Ejemplo de estructura:

```text
app/
├── layout.js
├── page.js              (página principal)
├── @analytics/
│   └── page.js          (slot analytics)
├── @team/
│   └── page.js          (slot team)
└── dashboard/
    ├── layout.js        (layout que define los slots en la misma vista)
    ├── @analytics/
    │   ├── page.js      (analytics en /dashboard)
    │   └── reports/
    │       └── page.js  (analytics en /dashboard/reports)
    └── @team/
        ├── page.js
        └── settings/
            └── page.js
```

### En `app/layout.js` o `app/dashboard/layout.js`:

Los slots se reciben como props:

```jsx
export default function DashboardLayout({ children, analytics, team }) {
  return (
    <div className="dashboard">
      <aside>{children}</aside>   {/* contenido principal opcional */}
      <main>
        <section>{team}</section>
        <section>{analytics}</section>
      </main>
    </div>
  )
}
```

### Características de las Rutas Paralelas:

*   **Interfaces complejas:** Construcción de dashboards sin necesidad de estado global para subrutas.
*   **Streaming:** Carga independiente por slot.
*   **Manejo de estados:** La navegación en un slot mantiene el estado de los demás.
*   **Independencia:** Cada slot (carpeta `@...`) funciona como una ruta paralela autónoma.

> [!NOTE]
> Si un slot no tiene una ruta activa para la URL actual, puedes mostrar un archivo **`default.js`** para definir el contenido por defecto. Crea este archivo en el slot para asegurar que siempre haya contenido renderizado.

## Beneficios de las Rutas Paralelas

1.  **Construcción de interfaces complejas:** dashboards sin necesidad de estado global para manejar subrutas.
2.  **Carga independiente y streaming:** cada slot se carga de forma autónoma.
3.  **Mejor organización del código:** cada slot es independiente y modular.

### Rutas de interceptación (ver capítulo siguiente)

Las rutas paralelas suelen usarse junto con rutas de interceptación para crear modales, feeds, etc.

---

Dominar rutas estáticas, dinámicas y paralelas te da un control total sobre la estructura de URLs y la composición de la UI en el App Router.
