## 📘 01-pages-router/getStaticProps-y-getStaticPaths.md

### getStaticProps y getStaticPaths: Generación de sitios estáticos (SSG)

Next.js permite generar páginas estáticas en tiempo de compilación. Para rutas dinámicas, necesitas también `getStaticPaths`.

#### getStaticProps

Se ejecuta durante la compilación (build) y genera HTML estático. Los datos se obtienen una vez y se reutilizan.

```jsx
export async function getStaticProps(context) {
  const res = await fetch('https://.../posts')
  const posts = await res.json()

  return {
    props: { posts },
    revalidate: 10, // ISR: regenera cada 10 segundos (opcional)
  }
}
```

**Ventajas:**

- Máximo rendimiento (servido desde CDN, sin cálculos por petición).
- SEO perfecto.

#### getStaticPaths

Define qué rutas dinámicas deben pre-renderizarse de forma estática. Se usa solo en páginas con rutas dinámicas (`[id].js`).

```jsx
export async function getStaticPaths() {
  const res = await fetch('https://.../posts')
  const posts = await res.json()

  const paths = posts.map((post) => ({
    params: { id: post.id.toString() },
  }))

  return {
    paths,
    fallback: false, // o true / 'blocking'
  }
}
```

#### Opciones de fallback

| Valor | Comportamiento |
| :--- | :--- |
| `false` | Cualquier ruta no pre-renderizada retorna 404. |
| `true` | La página se genera en el servidor en la primera solicitud. Muestra estado de carga. |
| `'blocking'` | Similar a `true`, pero espera a que la página se genere (SSR temporal). |

#### Generación incremental (ISR)

Al añadir `revalidate` en `getStaticProps`, permites que Next.js actualice la página estática en segundo plano sin rebuild completo.

```jsx
return {
  props: { data },
  revalidate: 60, // segundos
}
```

---
