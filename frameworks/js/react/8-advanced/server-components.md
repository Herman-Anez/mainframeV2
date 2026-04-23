# server-components.md

Concepto

React Server Components (RSC) es una arquitectura que permite renderizar componentes en el servidor, con un modelo de datos que puede ser asíncrono y acceso directo a bases de datos o sistemas de archivos, sin enviar JavaScript al cliente.
Diferencia con SSR tradicional

- SSR (Server Side Rendering): renderiza la aplicación completa en el servidor, envía HTML y luego hidrata (re-ejecuta todo el JavaScript en el cliente). Los componentes son los mismos en servidor y cliente.

- RSC: los Server Components nunca se envían al cliente. Solo envían su output (una representación especial similar a JSON). No hay hidratación para ellos. Se combinan con Client Components (marcados con "use client").

Tipos de componentes en RSC

1. Server Component (por defecto en frameworks como Next.js App Router)

```jsx
// Este archivo NO tiene "use client" → Server Component
import { db } from '@/lib/db';

async function UserList() {
  const users = await db.user.findMany(); // Acceso directo a DB
  return (
    <ul>
      {users.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  );
}
```

- Puede ser async (usar await directamente).

- No puede usar hooks (useState, useEffect), ni eventos del navegador (onClick).

- No puede usar contexto del cliente (aunque puede pasar props a client components).

1. Client Component

```jsx
'use client'; // Obligatorio al inicio

import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c+1)}>{count}</button>;
}
```

- Todo lo que requiere interactividad (estado, efectos, eventos) debe ser Client Component.

Patrón de composición

Los Server Components pueden importar Client Components, y viceversa (pero Client Components no pueden importar Server Components directamente; deben recibirlos por props o children).

```jsx
// ServerComponent.jsx
import ClientButton from './ClientButton';

async function Page() {
  const data = await fetchData();
  return (
    <div>
      <ClientButton label="Click me" />
      <p>{data.content}</p>
    </div>
  );
}
```

Ventajas de RSC

- Bundle cero para el servidor: los Server Components no añaden JavaScript al cliente.

- Acceso directo a recursos backend (DB, sistema de archivos, microservicios) sin API intermediaria.

- Código más seguro: la lógica sensible permanece en el servidor.

- Mejor rendimiento inicial: menos JavaScript que descargar y ejecutar.

- Caché automática a nivel de componente (en frameworks como Next.js).

Limitaciones

- No es compatible con componentes que necesitan interactividad (hooks, eventos).

- No funciona con useContext del lado del cliente (aunque existe react-server-dom context especial).

- Curva de aprendizaje y cambio de mentalidad (separación explícita entre servidor y cliente).

Frameworks que soportan RSC

- Next.js 13+ (App Router): la implementación más madura.

- Gatsby (experimental).

- Vite + react-server-dom (configuración manual, compleja).

Ejemplo práctico en Next.js App Router

```jsx
// app/products/page.jsx (Server Component)
import { Suspense } from 'react';
import ProductList from './ProductList';
import AddToCartButton from './AddToCartButton'; // Client Component

async function getProducts() {
  const res = await fetch('<https://api.example.com/products>', { cache: 'force-cache' });
  return res.json();
}

export default async function ProductsPage() {
  const products = await getProducts();
  return (
    <div>
      <h1>Productos</h1>
      <Suspense fallback={<div>Cargando...</div>}>
        <ProductList products={products} />
      </Suspense>
      {products.map(p => <AddToCartButton key={p.id} productId={p.id} />)}
    </div>
  );
}
```

Buenas prácticas

- Mover toda la lógica de datos a Server Components.

- Client Components deben ser pequeños y específicos para interactividad.

- No asumas que RSC es para todo: aplicaciones altamente interactivas (editores, juegos) aún necesitan muchos Client Components.

- Usa "use client" solo en hojas (componentes que necesitan estado/eventos).
