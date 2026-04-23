hivo: `03-renderizado/streaming-y-suspense.md`

Streaming y Suspense en Next.js

El streaming es una técnica que permite al servidor enviar partes del HTML al cliente a medida que se generan, en lugar de esperar a que toda la página esté lista. Next.js lo implementa usando React Suspense y los Server Components, permitiendo una carga progresiva y mejores métricas.
Cómo funciona en Next.js

Cuando un Server Component se suspende (porque está esperando una promesa), Next.js no bloquea toda la respuesta. En su lugar, envía el shell de la aplicación (los layouts y componentes que ya están listos) y luego, a medida que los datos se resuelven, envía el HTML restante en el mismo stream HTTP.

El navegador puede empezar a pintar el HTML parcial inmediatamente, reduciendo el Time to First Byte (TTFB) y el First Contentful Paint (FCP).
Implementación con loading.js

La forma más simple de habilitar streaming es crear un archivo loading.js en el segmento que tarda. loading.js se convierte en el fallback de Suspense para esa ruta.

Estructura básica:
```text
app/
├── layout.js
└── posts/
    ├── page.js        (obtiene datos lentos)
    └── loading.js     (UI de carga)
```

Cuando se visita /posts, Next.js envía inmediatamente el layout (que ya está listo) y muestra loading.js dentro del área de posts. Una vez que page.js termina de obtener los datos, el HTML del componente se envía y reemplaza el loading.

Internamente: Next.js envuelve la página en un <Suspense fallback={<Loading />}>. Por eso el streaming funciona incluso fuera de loading.js si usas Suspense manualmente.
Suspense manual para mayor granularidad

Puedes envolver partes específicas de una página en <Suspense> para controlar exactamente qué se streamea primero.
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

En este caso, el servidor enviará el título y los filtros inmediatamente, y luego, cuando ListaProductos termine de cargar, enviará ese bloque. El HTML se construye de forma incremental.
Suspense y fetching paralelo

Si tienes múltiples componentes asíncronos, Next.js ejecuta los fetch en paralelo (si son independientes). Sin Suspense, esperaría a que todos terminen antes de enviar nada. Con Suspense, cada bloque se puede enviar apenas está listo.
Configuración del streaming

El streaming está habilitado por defecto en App Router. No necesitas ninguna configuración. En entornos que no soporten streaming (p. ej., algunos proxies), Next.js automáticamente espera la página completa (pero esto degrada el rendimiento).
Impacto en Edge Runtime

El streaming es especialmente efectivo en Edge, donde la latencia de red es baja pero la ejecución de código puede ser más limitada. Al enviar el HTML estático temprano, se solapa la descarga con la espera de datos dinámicos.
Diferencia con SSR tradicional

En SSR sin streaming, toda la página debe generarse antes de que el servidor envíe el primer byte. Con streaming, se envía inmediatamente el shell estático, mejorando la percepción de velocidad. También se aprovecha el soporte HTTP/1.1 chunked transfer y HTTP/2.
Errores durante streaming

Si un componente dentro de <Suspense> falla, el error se puede capturar con el error.js del segmento o con un Error Boundary dentro del mismo Suspense. El resto de la página sigue intacta.
Uso con Client Components

Los Client Components que se suspenden también participan del streaming si se envuelven en <Suspense>. Sin embargo, su JavaScript aún debe cargarse e hidratarse, pero la parte visual (HTML) puede mostrarse tan pronto llegue.
Desactivar streaming en un segmento

Si decides que no quieres streaming (por ejemplo, para depuración), puedes forzar el renderizado dinámico completo con export const dynamic = 'force-dynamic' y no usar <Suspense>. Next.js esperará a que todo el árbol se resuelva antes de responder.
Cuándo usar streaming

    Páginas con datos lentos (consultas a BD, APIs de terceros).

    Cualquier página donde quieras mejorar LCP mostrando la estructura antes.

    Dashboards con múltiples widgets independientes.

El streaming con Suspense transforma la experiencia del usuario al proporcionar retroalimentación visual casi inmediata mientras los contenidos se cargan por detrás. Es una de las características más potentes del App Router.

Con esto tienes los 12 archivos desarrollados a fondo. Si necesitas profundizar más en alguno o continuar con la siguiente tanda (optimización, middleware, i18n, etc.), no dudes en pedírmelo.
