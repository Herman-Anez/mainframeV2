# Interceptación de rutas en App Router

La **interceptación de rutas** permite interceptar una navegación y mostrar una versión alternativa de la página de destino, manteniendo el contexto actual. Esto es ideal para modales, galerías, o feeds de detalle que no quieres que reemplacen la página completa.

## Cómo funciona

Se utilizan convenciones de nomenclatura especiales en las carpetas para indicar que una ruta debe interceptar a otra. Se basan en la notación de segmentos relativos:

*   **`(.)`** → intercepta el mismo nivel
*   **`(..)`** → intercepta un nivel superior
*   **`(..)(..)`** → intercepta dos niveles superiores
*   **`(...)`** → intercepta desde la raíz

La carpeta de interceptación se coloca al mismo nivel que la ruta interceptada, usando la notación.

### Ejemplo: Modal de foto

Supongamos la ruta `/feed` (feed de fotos) y `/photo/[id]` (página de detalle completa). Queremos que al hacer clic en una foto desde el feed, se abra un modal en lugar de navegar a la página completa.

**Estructura:**

```text
app/
├── feed/
│   ├── page.js           # lista de fotos
│   └── (.)photo/         # intercepta /photo desde /feed
│       └── [id]/
│           └── page.js   # modal de la foto
├── photo/
│   └── [id]/
│       └── page.js       # página de detalle completa
└── layout.js
```

Cuando el usuario está en `/feed` y hace clic en una foto, Next.js busca coincidencias en el mismo nivel con `(.)`, encuentra `(.)photo/[id]/page.js` y la renderiza en lugar de la página real. Si el usuario recarga la página o accede directamente a `/photo/123`, se carga la ruta real `photo/[id]/page.js`.

## Implementación común con paralelas

Para que el modal se renderice sobre el feed sin perder el contenido de fondo, usarás rutas paralelas. Por ejemplo, un slot `@modal` que contenga la interceptación:

```text
app/
├── layout.js            (define children y modal slots)
├── @modal/
│   ├── default.js       (null, no muestra nada por defecto)
│   └── (.)photo/
│       └── [id]/
│           └── page.js  (contenido del modal)
├── feed/
│   ├── layout.js        (si es necesario)
│   └── page.js
└── photo/
    └── [id]/
        └── page.js
```

**En `app/layout.js`:**

```jsx
export default function RootLayout({ children, modal }) {
  return (
    <html lang="es">
      <body>
        {children}
        {modal}
      </body>
    </html>
  )
}
```

> [!NOTE]
> `modal` será renderizado en paralelo. `default.js` en `@modal` puede retornar `null` para no mostrar nada cuando no hay modal activo.

## Navegación entre interceptación y ruta real

*   Desde el feed, el `Link` a `/photo/123` activa la interceptación.
*   Si se comparte la URL `/photo/123`, se carga la página completa sin modal.
*   Puedes cerrar el modal con `router.back()` o redirigiendo a `/feed`.

### Estados de carga y error

Puedes añadir `loading.js` y `error.js` dentro de la ruta interceptada para manejar la carga del modal y errores, igual que cualquier otra ruta.

## Combinación con rutas paralelas

Las rutas paralelas permiten mantener la página original (feed) mientras la interceptación se superpone (modal). Es la forma recomendada para modales, diálogos, bandejas de notificaciones, etc.

## Notación adicional

*   **`(..)`** intercepta un nivel superior. Útil cuando desde `/dashboard/settings` quieres interceptar `/dashboard/help`.
*   **`(...)`** intercepta desde la raíz de `app/`, ideal para interceptar rutas profundas desde cualquier nivel sin preocuparte por la profundidad.

**Ejemplo con `(...)`:**
Carpeta `app/(...)photo/[id]/page.js` intercepta `photo/[id]` desde cualquier ruta.

## Diferencias con modales "hechos a mano"

La interceptación de rutas se basa en la navegación del lado del cliente. Es más performante porque la página de fondo no se desmonta ni pierde su estado. Además, la URL se actualiza normalmente (por defecto, usando push).

## Resumen práctico

*   Usa `(.)nombreRuta` para interceptar en el mismo nivel.
*   Combínalo con slots (`@modal`, `@sidebar`) para separar responsabilidades.
*   Define `default.js` para que los slots no muestren nada por defecto.
*   Aprovecha que la ruta real sigue existiendo para permitir acceso directo y compartir enlaces.

---

Con esta técnica puedes crear experiencias de usuario fluidas manteniendo URLs normales y navegación natural.
