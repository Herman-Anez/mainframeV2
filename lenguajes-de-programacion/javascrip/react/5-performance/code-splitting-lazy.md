code-splitting-lazy.md

Concepto

Code splitting (división de código) y lazy loading (carga diferida) son técnicas para reducir el tamaño del bundle inicial, cargando solo el código necesario para la vista actual.
División de código en React

## React.lazy + Suspense

```jsx
import { lazy, Suspense } from 'react';

const ComponentePesado = lazy(() => import('./ComponentePesado'));

function App() {
  return (
    <div>
      <h1>Mi app</h1>
      <Suspense fallback={<div>Cargando...</div>}>
        <ComponentePesado />
      </Suspense>
    </div>
  );
}
```

## Lazy con rutas (React Router)

```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { lazy, Suspense } from 'react';

const Home = lazy(() => import('./pages/Home'));
const Productos = lazy(() => import('./pages/Productos'));
const Contacto = lazy(() => import('./pages/Contacto'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div>Cargando página...</div>}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/productos" element={<Productos />} />
          <Route path="/contacto" element={<Contacto />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

Estrategias de división

- Por rutas: cada página es un chunk separado.

- Por componentes pesados: gráficos, editores de texto, calendarios, mapas.

- Por librerías: si una librería es grande y no se usa siempre (ej. moment.js, lodash), se puede cargar bajo demanda.

Límites de errores con lazy

Si falla la carga de un componente lazy, puedes usar un Error Boundary:

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  render() {
    if (this.state.hasError) return <div>Error al cargar</div>;
    return this.props.children;
  }
}

// Uso
<ErrorBoundary>
  <Suspense fallback="Cargando...">
    <ComponenteLazy />
  </Suspense>
</ErrorBoundary>
```

Prefetching (carga anticipada)

Puedes cargar un componente antes de que se necesite (ej. cuando el usuario pasa el mouse sobre un enlace):

```jsx
const prefetchComponente = () => import('./ComponentePesado');

<Link 
  to="/ruta"
  onMouseEnter={prefetchComponente}
>
  Ir
</Link>
```

Configuración de Webpack/Vite

Ambos soportan import() dinámico nativamente. Puedes personalizar los nombres de los chunks:

```jsx
const Componente = lazy(() => import(/* webpackChunkName: "mi-componente" */ './Componente'));
```

División de código con React 18+ y Server Components

En Next.js App Router, los Server Components permiten división automática. En React 18 con frameworks como Vite, sigue funcionando React.lazy.

Buenas prácticas

- No dividas componentes demasiado pequeños (cada chunk tiene overhead).

- Coloca Suspense en un nivel adecuado (no uno por cada componente lazy).

- Prueba que la experiencia de carga sea buena (no mostrar fallbacks parpadeantes).

- Monitorea el tamaño de los bundles con herramientas como webpack-bundle-analyzer.

Limitaciones

- React.lazy no funciona con Server Side Rendering (SSR) nativo. Necesitas librerías como loadable-components.

- Solo funciona con exports por defecto (export default).
