
📄 8-advanced/suspense.md
Concepto

Suspense es un componente de React que permite "esperar" a que se cumpla una condición (generalmente una promesa) antes de renderizar el contenido principal, mostrando un fallback mientras tanto.
Historia de Suspense

- React 16.6: Suspense para React.lazy (carga de componentes).

- React 18: Suspense para data fetching (con librerías compatibles como Relay, SWR, React Query, o implementaciones manuales).

Suspense para React.lazy (carga de componentes)

```jsx
const Profile = lazy(() => import('./Profile'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <Profile />
    </Suspense>
  );
}
```

Suspense para data fetching (React 18+)

Requiere que la fuente de datos soporte Suspense (ej. Relay, o un wrapper manual con use hook experimental).

```jsx
// Ejemplo conceptual con un wrapper
const resource = fetchUserResource(userId); // resource.read() lanza promesa

function UserProfile() {
  const user = resource.read(); // Si la promesa no se resolvió, Suspense la captura
  return <div>{user.name}</div>;
}

function App() {
  return (
    <Suspense fallback="Cargando usuario...">
      <UserProfile />
    </Suspense>
  );
}
```

Uso con use (hook experimental, React 19+)

```jsx
import { use } from 'react';

function UserProfile({ userPromise }) {
  const user = use(userPromise); // Similar a .read() pero integrado
  return <div>{user.name}</div>;
}

function Page() {
  const userPromise = fetchUser();
  return (
    <Suspense fallback="Cargando...">
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}
```

Suspense en el servidor (streaming SSR)

Permite enviar el HTML del esqueleto inmediatamente y luego inyectar el contenido cargado de forma asíncrona.

```jsx
// Next.js App Router ya hace esto automáticamente
<Suspense fallback={<ProductSkeleton />}>
  <ProductDetails id={id} />
</Suspense>
```

Suspense múltiple (anidado)

Puedes anidar Suspense boundaries. Cada uno maneja su propia carga.

```jsx
<Suspense fallback="Cargando layout">
  <Layout>
    <Suspense fallback="Cargando sidebar">
      <Sidebar />
    </Suspense>
    <Suspense fallback="Cargando contenido">
      <MainContent />
    </Suspense>
  </Layout>
</Suspense>
```

Comportamiento de Suspense

- Si un componente hijo "suspende" (lanza una promesa), el Suspense más cercano captura y muestra el fallback.

- Cuando la promesa se resuelve, React vuelve a renderizar el hijo y reemplaza el fallback.

- Los estados de Suspense pueden ser transitorios (muestra fallback mientras carga) o persistentes (si la promesa falla, debes manejarlo con Error Boundary).

Manejo de errores con Suspense

Suspense no captura errores. Necesitas un Error Boundary:

```jsx
<ErrorBoundary fallback={<ErrorUI />}>
  <Suspense fallback="Cargando...">
    <ComponenteConDatos />
  </Suspense>
</ErrorBoundary>
```

Buenas prácticas

- No abuses de Suspense: úsalo para secciones que cargan datos asíncronos significativos.

- Coloca Suspense en niveles apropiados: no uno gigante que envuelva toda la app.

- Proporciona fallbacks útiles (skeletons, spinners, mensajes).

- Combina con startTransition para evitar mostrar fallbacks parpadeantes en actualizaciones de datos.

Limitaciones actuales

- Data fetching con Suspense requiere librerías especializadas (Relay, SWR con suspense, React Query con suspense: true).

- El use hook sigue experimental en React 18 (estable en React 19).

- No funciona con efectos secundarios (useEffect) para cargar datos.