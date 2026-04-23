# Streaming y Suspense en Next.js

El **streaming** es una técnica que permite al servidor enviar partes del HTML al cliente a medida que se generan, en lugar de esperar a que toda la página esté lista. Next.js lo implementa usando **React Suspense** y los **Server Components**, permitiendo una carga progresiva y mejores métricas de rendimiento.

## Cómo funciona en Next.js

Cuando un Server Component se suspende (porque está esperando una promesa), Next.js no bloquea toda la respuesta. En su lugar:
1.  Envía el **shell** de la aplicación (layouts y componentes listos).
2.  A medida que los datos se resuelven, envía el HTML restante en el mismo stream HTTP.
3.  El navegador pinta el HTML parcial inmediatamente, reduciendo el **Time to First Byte (TTFB)** y el **First Contentful Paint (FCP)**.

## Implementación con `loading.js`

La forma más simple de habilitar streaming es crear un archivo `loading.js` en el segmento. Este archivo se convierte automáticamente en el fallback de Suspense para esa ruta.

**Estructura básica:**
```text
app/
├── layout.js
└── posts/
    ├── page.js        (obtiene datos lentos)
    └── loading.js     (UI de carga)
```

> [!NOTE]
> Al visitar `/posts`, Next.js envía inmediatamente el layout y muestra `loading.js`. Una vez que `page.js` resuelve los datos, el HTML del componente reemplaza al de carga. Internamente, Next.js envuelve la página en un `<Suspense fallback={<Loading />}>`.

## Suspense manual para mayor granularidad

Puedes envolver partes específicas de una página en `<Suspense>` para controlar exactamente qué se streamea primero y de forma independiente.

```jsx
// app/productos/page.js
import { Suspense } from 'react'
import ListaProductos from './ListaProductos' // Server Component pesado
import Filtros from './Filtros'               // Server Component ligero

export default function Page() {
  return (
    <div>
      <h1>Productos</h1>
      <Filtros />
      <Suspense fallback={<div>Cargando productos...</div>}>
        <ListaProductos />
      </Suspense>
    </div>
  )
}
```

En este caso, el servidor enviará el título y los filtros de inmediato, y el bloque de productos se enviará incrementalmente apenas esté listo.

---

## Beneficios del Streaming

*   **Fetching paralelo:** Next.js ejecuta los fetch en paralelo. Con Suspense, cada bloque se envía apenas está listo sin esperar al resto.
*   **Percepción de velocidad:** Se envía inmediatamente el shell estático, mejorando drásticamente la experiencia del usuario.
*   **Resiliencia:** Si un componente dentro de `<Suspense>` falla, el error se captura localmente (vía `error.js`) y el resto de la página permanece funcional.

> [!IMPORTANT]
> El streaming está habilitado por defecto en el **App Router**. Es especialmente efectivo en entornos **Edge**, donde se solapa la descarga del shell con la espera de datos dinámicos.

---

## Comparación con SSR tradicional

| Característica | SSR Tradicional | Streaming con Suspense |
| :--- | :--- | :--- |
| **Envío de HTML** | Espera a que toda la página esté lista | Envío incremental por bloques |
| **TTFB** | Más alto (bloqueado por fetch) | Más bajo (shell instantáneo) |
| **Interactividad** | Toda la página se hidrata a la vez | Partes listas pueden hidratarse antes |

---

## ¿Cuándo usar streaming?

*   **Páginas con datos lentos:** Consultas complejas a BD o APIs de terceros.
*   **Optimización de LCP:** Para mostrar la estructura y navegación antes que el contenido pesado.
*   **Dashboards:** Donde múltiples widgets independientes cargan a ritmos distintos.

> [!TIP]
> Si deseas desactivar el streaming en un segmento específico para depuración, puedes forzar el renderizado dinámico completo con `export const dynamic = 'force-dynamic'` y evitar el uso de `<Suspense>`.

---

El streaming con Suspense transforma la experiencia del usuario al proporcionar retroalimentación visual casi inmediata mientras los contenidos se cargan progresivamente por detrás.
