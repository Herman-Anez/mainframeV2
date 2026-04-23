## 📘 01-pages-router/api-routes-pages.md

### API Routes en Pages Router

Las API Routes permiten construir tu backend dentro del mismo proyecto Next.js, bajo la carpeta `pages/api/`.

#### Creando un endpoint básico

`pages/api/hola.js`:

```jsx
export default function handler(req, res) {
  res.status(200).json({ mensaje: 'Hola mundo' })
}
```

Accesible en `/api/hola`.

#### El objeto `req` (Request)

- `req.query`: query string parseado como objeto.
- `req.body`: cuerpo parseado.
- `req.cookies`: objeto con cookies.
- `req.method`: método HTTP (GET, POST, etc.).

#### El objeto `res` (Response)

- `res.status(code)` para establecer código HTTP.
- `res.json(data)` envía respuesta JSON.
- `res.send(data)` envía datos en bruto.
- `res.redirect(url)` redirige.

#### Manejo de diferentes métodos HTTP

```jsx
export default async function handler(req, res) {
  if (req.method === 'GET') {
    res.status(200).json({ data })
  } else if (req.method === 'POST') {
    res.status(201).json({ result })
  } else {
    res.setHeader('Allow', ['GET', 'POST'])
    res.status(405).end(`Método ${req.method} no permitido`)
  }
}
```

---

Conectando a una base de datos
jsx

import clientPromise from '../../lib/mongodb'

export default async function handler(req, res) {
  const client = await clientPromise
  const db = client.db('mi_db')
  const collection = db.collection('posts')

  if (req.method === 'GET') {
    const posts = await collection.find({}).toArray()
    res.json(posts)
  } else if (req.method === 'POST') {
    const result = await collection.insertOne(req.body)
    res.json(result)
  }
}

Middleware personalizado

Puedes envolver handlers con funciones middleware:
jsx

function withAuth(handler) {
  return async (req, res) => {
    const token = req.cookies.token
    if (!token) return res.status(401).json({ error: 'No autorizado' })
    // validar token...
    return handler(req, res)
  }
}

async function handler(req, res) { /*...*/ }

export default withAuth(handler)

Variables de entorno

Accede a secretos con process.env.SECRET. Estas variables no se exponen al cliente si no llevan el prefijo NEXT_PUBLIC_.
Limitaciones

    Las API Routes se ejecutan como funciones serverless en Vercel (o en Node si despliegas en servidor propio). No mantienen estado entre peticiones (websockets no funcionan bien en serverless).

    Para archivos grandes, el bodyParser por defecto tiene límite de 1MB. Puedes desactivarlo export const config = { api: { bodyParser: false } } y usar streaming.

    Para lógica de borde, se recomienda usar Edge API Routes (App Router), pero en Pages Router tienes un modelo probado.

Ejemplo completo: endpoint POST con validación
jsx

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Método no permitido' })
  }

  const { email, password } = req.body
  if (!email || !password) {
    return res.status(400).json({ error: 'Faltan datos' })
  }

  // Lógica de registro...
  res.status(200).json({ ok: true })
}

Las API Routes son ideales para formularios, webhooks, proxy de servicios externos o prototipos rápidos.
