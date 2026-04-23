# Turbopack: El empaquetador de nueva generación

**Turbopack** es el nuevo empaquetador de desarrollo para Next.js, escrito en **Rust** por el equipo de Vercel. Sustituye de forma incremental a Webpack, ofreciendo un rendimiento de recarga en caliente (**HMR**) hasta 10 veces más rápido en proyectos de gran escala.

## ¿Por qué Turbopack?

Webpack, aunque potente, tiene cuellos de botella inherentes al estar escrito en JavaScript y realizar una carga masiva de módulos. Turbopack se diseñó desde cero para aprovechar el paralelismo y la compilación nativa.

### Beneficios principales:
*   **Arranque instantáneo:** Compila solo los módulos necesarios bajo demanda.
*   **HMR Ultrarrápido:** Los cambios se reflejan en milisegundos, incluso en aplicaciones con miles de componentes.
*   **Caché Granular:** Comparte caché entre builds y sesiones, evitando recompilar código que no ha cambiado.
*   **Integración Nativa:** Optimizado para React Server Components (RSC) y streaming.

---

## Estado actual y Disponibilidad

Desde Next.js 14, Turbopack es la opción recomendada para desarrollo en proyectos con el App Router.

> [!IMPORTANT]
> Actualmente, Turbopack está enfocado en el entorno de **desarrollo** (`next dev`). El proceso de producción (`next build`) sigue utilizando Webpack de forma estable, aunque se están realizando avances para alcanzar la paridad total en futuras versiones.

## Cómo habilitar Turbopack

En un proyecto existente, lanza el servidor de desarrollo con el flag `--turbo`:

```bash
next dev --turbo
```

**Configuración opcional en `next.config.js`:**
```javascript
module.exports = {
  experimental: {
    turbo: {
      // Configuraciones avanzadas aquí
    },
  },
}
```

---

## Migración desde Webpack

La mayoría de las configuraciones personalizadas de Webpack **no se aplican** en Turbopack. Sin embargo, Turbopack ya incluye soporte nativo para las necesidades más comunes:
*   CSS y SASS
*   Optimización de Imágenes
*   Resolución de módulos de Node.js

### Limitaciones conocidas:
*   **Plugins:** Los plugins de Webpack no son compatibles directamente.
*   **Loaders:** No todos los loaders tienen un equivalente directo todavía.
*   **Producción:** Como se mencionó, `next build` aún depende principalmente de Webpack por defecto.

---

## Integración con el ecosistema

Turbopack se complementa perfectamente con **Turborepo** (el sistema de gestión de monorepos), aunque son herramientas distintas. Mientras que Turbopack empaqueta el código, Turborepo orquesta las tareas entre múltiples paquetes, ofreciendo un flujo de trabajo de alto rendimiento extremo.

## ¿Deberías usarlo hoy?

> [!TIP]
> Si estás iniciando un proyecto nuevo con Next.js 14+ y no requieres configuraciones complejas de Webpack, **usa Turbopack**. La diferencia en la velocidad de iteración transformará tu flujo de trabajo diario.

---

Turbopack representa la mayor innovación en la experiencia de desarrollo de Next.js, eliminando los tiempos de espera y permitiendo un ciclo de feedback casi instantáneo.
