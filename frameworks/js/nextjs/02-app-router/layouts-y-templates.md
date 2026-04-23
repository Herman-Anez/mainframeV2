# Layouts y Templates en App Router

Next.js proporciona dos mecanismos para definir la estructura que envuelve las páginas: **layouts** y **templates**. Ambos se basan en los archivos `layout.js` y `template.js` dentro de la carpeta `app/`.

## Layout (`layout.js`)

Un **layout** es un componente que envuelve las páginas de un segmento y **persiste su estado** entre navegaciones. El layout raíz (`app/layout.js`) es obligatorio y define la estructura HTML principal.

### Características clave:

*   Solo se renderiza una vez cuando se monta, y **no se vuelve a renderizar** al navegar entre páginas hijas (a menos que cambie `searchParams` o `params` del layout anidado).
*   Ideal para barras de navegación, pies de página, menús laterales.
*   Recibe `children` (la página o segmento interior) y opcionalmente `params`.
*   Puede ser asíncrono (**Server Component**) para obtener datos para el layout (p. ej., datos del usuario).

### Ejemplo: layout con fetching

```jsx
// app/dashboard/layout.js
export default async function DashboardLayout({ children, params }) {
  const user = await fetchUser(params.userId)

  return (
    <div className="dashboard">
      <aside>
        <UserMenu user={user} />
      </aside>
      <main>{children}</main>
    </div>
  )
}
```

> [!NOTE]
> Debido a que el layout persiste, el menú lateral no pierde su estado (por ejemplo, scroll, selección de elemento) al cambiar de página dentro del dashboard.

### Anidamiento de layouts

Los layouts se anidan según la jerarquía de carpetas. Por ejemplo:

```text
app/
├── layout.js          (RootLayout)
├── products/
│   ├── layout.js      (ProductsLayout)
│   └── [category]/
│       ├── layout.js  (CategoryLayout)
│       └── page.js
```

Cada layout envuelve al siguiente. El flujo: `RootLayout` → `ProductsLayout` → `CategoryLayout` → `page`.

Al navegar de `/products/ropa` a `/products/electronica`, `ProductsLayout` y `RootLayout` se mantienen, mientras que `CategoryLayout` y la página cambian. Sin embargo, si `CategoryLayout` tiene datos propios dependientes de `params.category`, se ejecutará el renderizado del servidor para ese layout (porque `params` cambió).

## Template (`template.js`)

Un **template** es similar a un layout, pero se crea una **nueva instancia** del componente cada vez que el usuario navega a una página dentro de ese segmento. **No persiste el estado.**

### Cuándo usarlo:

*   Para animaciones de entrada/salida usando `motion` o `framer-motion`, donde necesitas que el componente se monte/desmonte.
*   Para reinicializar ciertos estados locales (por ejemplo, un formulario que debe vaciarse al cambiar de página).
*   Cuando dependes de `useEffect` para cierta lógica que debe ejecutarse al entrar a la página.

### Ejemplo:

```jsx
// app/dashboard/template.js
'use client'

import { motion } from 'framer-motion'

export default function DashboardTemplate({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      {children}
    </motion.div>
  )
}
```

Como no persiste, al navegar entre páginas del dashboard se reproduce la animación.

## Uso conjunto

Puedes tener `layout.js` y `template.js` en la misma carpeta; ambos envolverán la página. El orden es: `layout` → `template` → `page`.

```jsx
// Layout (persistente)
export default function Layout({ children }) {
  return <div><Nav />{children}</div>
}

// Template (se re-monta)
export default function Template({ children }) {
  return <div className="fade">{children}</div>
}

// Page
export default function Page() {
  return <h1>Contenido</h1>
}
```

**Estructura resultante:** `<Layout><Template><Page/></Template></Layout>`

## Pasar información entre layouts y páginas

No hay un mecanismo directo para pasar props de layout a page. Utiliza **React Context** (Client Component) o cookies/headers accesibles en Server Components. También puedes usar **Server Actions** para modificar datos del layout desde la página.

## Layouts y Server Actions

Puedes colocar Server Actions en el layout (ejemplo: cerrar sesión) y pasarlas a componentes cliente.

## Layouts dinámicos y revalidación

Si un layout obtiene datos con `fetch`, puedes configurar `revalidate` para ISR, igual que en páginas.

---

Los layouts constituyen el núcleo del App Router, facilitando la creación de interfaces complejas con mínimo esfuerzo y código repetitivo.