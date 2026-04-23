# 🖥️ Server Side Rendering (SSR) en React

El **SSR** es una técnica que consiste en renderizar tu aplicación React en el servidor, generando un HTML completo que se envía al navegador. Esto permite que el usuario vea contenido casi instantáneamente, mejorando el SEO y el rendimiento percibido.

---

## 🚀 ¿Por qué usar SSR?

| Beneficio | Descripción |
| :--- | :--- |
| **SEO Superior** | Los motores de búsqueda indexan HTML puro, no necesitan ejecutar JS. |
| **FCP más rápido** | El First Contentful Paint es casi inmediato al recibir HTML ya renderizado. |
| **Accesibilidad** | El contenido básico está disponible incluso si el JS falla o está desactivado. |

---

## 🛠️ Implementación con React Puro (Express)

Aunque frameworks como **Next.js** automatizan esto, entender cómo funciona "bajo el capó" con React puro es fundamental.

### 1. El Servidor (Node.js + Express)
Usamos `renderToString` de `react-dom/server` para convertir componentes en texto HTML.

```jsx
import express from 'express';
import React from 'react';
import { renderToString } from 'react-dom/server';
import App from './src/App';

const app = express();

app.get('*', (req, res) => {
  const html = renderToString(<App url={req.url} />);

  res.send(`
    <!DOCTYPE html>
    <html>
      <head><title>My SSR App</title></head>
      <body>
        <div id="root">${html}</div>
        <script src="/bundle.js"></script>
      </body>
    </html>
  `);
});
```

---

## 💧 Hidratación (Hydration)

Una vez que el HTML llega al navegador, React debe "tomar el control" de ese DOM estático para hacerlo interactivo. Este proceso se llama **Hidratación**.

> [!CAUTION]
> En el cliente, debes usar `hydrateRoot` en lugar de `createRoot` para evitar que React destruya y recree el DOM enviado por el servidor.

```jsx
// client.js
import { hydrateRoot } from 'react-dom/client';
import App from './App';

hydrateRoot(document.getElementById('root'), <App />);
```

---

## 📡 Carga de Datos y Estado Inicial

Uno de los mayores retos es sincronizar los datos que el servidor usó para renderizar con los que el cliente espera encontrar.

1.  **En el Servidor**: Obtienes los datos, renderizas y los inyectas en un objeto global (ej: `window.__INITIAL_DATA__`).
2.  **En el Cliente**: El componente lee de ese objeto global para inicializar su estado, evitando un "flash" de contenido vacío.

---

## ⚡ Streaming SSR (React 18+)

React 18 introdujo `renderToPipeableStream`, que permite enviar el HTML al navegador por partes a medida que se genera, en lugar de esperar a que todo el árbol esté listo.

```jsx
const stream = renderToPipeableStream(<App />, {
  onShellReady() {
    res.setHeader('Content-Type', 'text/html');
    stream.pipe(res);
  }
});
```

---

## 📏 Reglas de Oro en SSR

1.  **Sin Efectos en el Servidor**: `useEffect` y `useLayoutEffect` **no se ejecutan** en el servidor.
2.  **Evita el DOM**: No uses `window`, `document` o `localStorage` directamente fuera de los efectos.
3.  **Consistencia**: El HTML generado en el servidor debe ser idéntico al primer renderizado en el cliente, o verás un "Hydration Mismatch error".

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
