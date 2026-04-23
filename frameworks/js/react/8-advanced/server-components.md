# 🖥️ React Server Components (RSC): El Cambio de Paradigma

Los **React Server Components (RSC)** representan una evolución en la arquitectura de React, permitiendo que ciertos componentes se rendericen exclusivamente en el servidor, reduciendo drásticamente la cantidad de JavaScript enviado al cliente.

---

## 🤔 ¿Qué son los RSC?

A diferencia del SSR tradicional, donde todos los componentes se envían al cliente para ser hidratados, los **Server Components** nunca abandonan el servidor. Solo se envía al cliente una representación ligera del resultado (un flujo serializado), lo que permite:
*   **JavaScript Cero**: El código de los Server Components no se incluye en el bundle del cliente.
*   **Acceso Directo al Backend**: Puedes realizar consultas a bases de datos o leer archivos directamente desde el componente.
*   **Seguridad**: La lógica sensible y las claves de API nunca se exponen al navegador.

---

## 🏗️ Diferencia entre SSR y RSC

| Característica | SSR (Server-Side Rendering) | RSC (Server Components) |
| :--- | :--- | :--- |
| **Código en el Cliente** | Sí (Todo el JS del componente se envía) | No (Solo el JS de los Client Components) |
| **Hidratación** | Sí (React re-ejecuta todo en el cliente) | No (Para los Server Components no hay hidratación) |
| **Interactividad** | Sí (Soporta hooks y eventos) | Limitada (Para interactividad se usan Client Components) |
| **Estado Local** | Sí (`useState`, `useEffect`) | Prohibido (No tienen acceso a hooks de cliente) |

---

## 🚀 Tipos de Componentes

### 1. Server Components (Por defecto)
En frameworks modernos como Next.js (App Router), todos los componentes son Server Components por defecto.

```jsx
// Obtención de datos asíncrona directamente en el servidor
async function UserProfile({ id }) {
  const user = await db.user.findUnique({ where: { id } }); // Acceso a DB

  return (
    <section>
      <h1>{user.name}</h1>
      <p>{user.bio}</p>
    </section>
  );
}
```

### 2. Client Components (`"use client"`)
Si necesitas interactividad (eventos, hooks, APIs del navegador), debes marcar el archivo como un componente de cliente.

```jsx
"use client"; // Esta directiva indica que el componente vive en el navegador

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

---

## 🖇️ Composición y Reglas

La regla de oro de la composición en RSC es que un **Server Component puede renderizar a un Client Component**, pero un Client Component **no puede importar directamente** a un Server Component.


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

### ✅ Patrón Correcto: Pasar Server como Children
```jsx
// Componente de Cliente
"use client";
export function Layout({ children }) {
  return <div className="interactive-shell">{children}</div>;
}

// Componente de Servidor
export async function Page() {
  return (
    <Layout>
      <AsyncDataComponent /> {/* El hijo puede ser un Server Component */}
    </Layout>
  );
}
```

---

## ⚡ Ventajas Competitivas

1.  **Rendimiento**: Menos JavaScript significa tiempos de carga (FCP y TTI) mucho más rápidos.
2.  **Mantenibilidad**: Se elimina la necesidad de crear APIs REST/GraphQL intermedias solo para alimentar componentes específicos.
3.  **Carga Secuencial**: Puedes usar `Suspense` para ir renderizando partes de la UI a medida que los datos llegan del servidor.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
