# 🛣️ React Router v6

React Router es la librería estándar para manejar el enrutamiento declarativo en aplicaciones React. Permite sincronizar la interfaz de usuario con la URL, manejando navegación, parámetros y rutas anidadas de forma fluida.

---

## 🚀 Configuración Básica

```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Inicio</Link>
        <Link to="/about">Acerca de</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```

## Componentes principales

### BrowserRouter

- Usa la API de historial de HTML5 (URLs limpias, sin hash).

- Debe envolver toda la aplicación.

### HashRouter (alternativa)

- Usa el hash de la URL (ej. /#/about). Útil para entornos estáticos sin servidor configurado.

### Routes y Route

- Routes evalúa las rutas de forma exclusiva (solo renderiza la primera que coincida).

- Route define la correspondencia entre path y element.

### Link y NavLink

- Link: navegación sin recarga de página.

- NavLink: similar, pero añade atributos active o aria-current cuando coincide la ruta.

```jsx
<NavLink to="/about" className={({ isActive }) => isActive ? 'active' : ''}>
  About
</NavLink>
```

---

## 📂 Rutas Anidadas y Layouts

Las rutas anidadas permiten reflejar jerarquías de UI en la URL. El componente `<Outlet />` es fundamental aquí: indica dónde deben renderizarse las rutas Hijas dentro del Padre.

```jsx
const DashboardLayout = () => (
  <div className="layout">
    <Sidebar />
    <main>
      <Outlet /> {/* Aquí aparecerán las sub-rutas */}
    </main>
  </div>
);

// Configuración
<Routes>
  <Route path="dashboard" element={<DashboardLayout />}>
    <Route index element={<Stats />} /> {/* /dashboard */}
    <Route path="profile" element={<Profile />} /> {/* /dashboard/profile */}
  </Route>
</Routes>
```
----


Rutas dinámicas y parámetros
Parámetros de ruta (useParams)

```jsx
<Route path="/producto/:id" element={<Producto />} />

function Producto() {
  const { id } = useParams();
  return <div>Producto ID: {id}</div>;
}
```

Parámetros de consulta (query string)

```jsx
import { useSearchParams } from 'react-router-dom';

function Busqueda() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  const setQuery = (q) => setSearchParams({ q });
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

Rutas anidadas (layout routes)

```jsx
function Layout() {
  return (
    <div>
      <Header />
      <Outlet /> {/*Aquí se renderizan las rutas hijas*/}
      <Footer />
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="about" element={<About />} />
          <Route path="productos" element={<Productos />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

---

## ⚓ Hooks Esenciales

| Hook | Propósito |
| :--- | :--- |
| **`useParams()`** | Obtiene parámetros variables de la URL (ej: `/user/:id`). |
| **`useNavigate()`** | Permite cambiar de ruta programáticamente (después de un login, etc.). |
| **`useLocation()`** | Devuelve el objeto de la ubicación actual (pathname, state, etc.). |
| **`useSearchParams()`** | Permite leer y modificar los parámetros de consulta (ej: `?query=react`). |

### Ejemplo: Navegación Programática
```jsx
const navigate = useNavigate();

const handleLogout = () => {
  auth.logout();
  navigate('/login', { replace: true });
};
```

---

## 🛡️ Rutas Protegidas

Un patrón común para manejar la autenticación es crear un componente envoltorio que verifique el estado del usuario.

```jsx
const PrivateRoute = ({ children }) => {
  const { user } = useAuth();
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

// Uso en la configuración
<Route path="/admin" element={
  <PrivateRoute>
    <AdminPanel />
  </PrivateRoute>
} />
```
---

Rutas con layout condicional (ej. dashboard vs landing)

```jsx
<Routes>
  <Route element={<PublicLayout />}>
    <Route path="/" element={<Home />} />
    <Route path="/login" element={<Login />} />
  </Route>
  <Route element={<PrivateLayout />}>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/perfil" element={<Perfil />} />
  </Route>
</Routes>
```

Manejo de rutas no encontradas (404)

```jsx
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
  <Route path="*" element={<NotFound />} />
</Routes>
```

---
Lazy loading con React Router v6

```jsx
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Perfil = lazy(() => import('./pages/Perfil'));

// En el componente de rutas
<Suspense fallback={<div>Cargando...</div>}>
  <Routes>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/perfil" element={<Perfil />} />
  </Routes>
</Suspense>
---
## ⚡ Lazy Loading (Carga bajo demanda)

Para mejorar el rendimiento, carga tus páginas solo cuando el usuario las visite:

```jsx
import { lazy, Suspense } from 'react';

const Admin = lazy(() => import('./pages/Admin'));

<Suspense fallback={<div>Cargando...</div>}>
  <Routes>
    <Route path="/admin" element={<Admin />} />
  </Routes>
</Suspense>
```

----

Historial y navegación

React Router expone el objeto navigate y también puedes acceder al historial:

```jsx
import { unstable_HistoryRouter as HistoryRouter } from 'react-router-dom';
import { createBrowserHistory } from 'history';
const history = createBrowserHistory();
<HistoryRouter history={history}>
  <App />
</HistoryRouter>

```

## Hooks útiles

|Hook|Uso|
|-|-|
|useParams()|Obtener parámetros de ruta|
|useLocation()|Obtener objeto location (pathname, search, state)|
|useNavigate()|Navegar programáticamente|
|useSearchParams()|Leer/modificar query string|
|useMatch()|Verificar si una ruta coincide con el patrón actual|
|useRoutes()|Definir rutas como objeto (alternativa a JSX)|

## Ejemplo de useLocation con state

```jsx
// Enviar estado
navigate('/profile', { state: { fromNotification: true } });

// Leer estado
const location = useLocation();
const fromNotification = location.state?.fromNotification;
```

Rutas relativas y anidadas automáticas

En v6, las rutas son relativas por defecto dentro de componentes anidados.

```jsx
<Route path="productos" element={<Productos />}>
  <Route path=":id" element={<ProductoDetalle />} /> {/*relativo a /productos*/}
</Route>
```

Configuración con useRoutes (alternativa basada en objeto)

```jsx
const routes = useRoutes([
  { path: '/', element: <Home /> },
  { path: '/about', element: <About /> },
  {
    path: '/dashboard',
    element: <PrivateLayout />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'settings', element: <Settings /> }
    ]
  }
]);
return routes;
```

Renderizado condicional de rutas según rol (RBAC)

```jsx
function AppRoutes() {
  const { user, role } = useAuth();
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      {role === 'admin' && <Route path="/admin" element={<AdminPanel />} />}
      <Route path="/perfil" element={<Perfil />} />
    </Routes>
  );
}

Scroll restoration (volver arriba al cambiar de ruta)
```

```jsx
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => window.scrollTo(0, 0), [pathname]);
  return null;
}

// En App
<BrowserRouter>
  <ScrollToTop />
  <Routes>...</Routes>
</BrowserRouter>
```

Rutas con transiciones (animaciones)

Usando react-transition-group o framer-motion junto con useLocation.

```jsx

import { AnimatePresence, motion } from 'framer-motion';

function App() {
  const location = useLocation();
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<motion.div initial={{opacity:0}} animate={{opacity:1}}>Home</motion.div>} />
      </Routes>
    </AnimatePresence>
  );
}
```

Buenas prácticas

- Organiza rutas en un archivo separado (routes.jsx o AppRoutes.jsx).

- Usa constantes para los pathnames (evita strings mágicos).

- Protege rutas a nivel de layout, no por cada componente.

- Suspense para lazy loading a nivel de ruta.

- Manejo de 404 con path="*".

- No anidar BrowserRouter (solo uno por aplicación).

- Para servidores SPA, configura fallback a index.html (para que rutas profundas no den 404).

Migración desde v5 a v6

|v5|v6|
|-|-|
|`<Switch>`|`<Routes>`|
|component prop|element prop|
|useHistory()|useNavigate()|
|`<Redirect>`|`<Navigate>`|

exactpor defecto Ya no se usa (las rutas son exactas por defecto)
Rutas anidadas con render Outlet
Ejemplo completo de archivo de rutas

```jsx
// routes.jsx
import { lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import PrivateRoute from './components/PrivateRoute';

const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const NotFound = lazy(() => import('./pages/NotFound'));

export default function AppRoutes() {
  return (
    <Suspense fallback={<div>Cargando...</div>}>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="about" element={<About />} />
          <Route element={<PrivateRoute />}>
            <Route path="dashboard" element={<Dashboard />} />
          </Route>
        </Route>
        <Route path="404" element={<NotFound />} />
        <Route path="*" element={<Navigate to="/404" replace />} />
      </Routes>
    </Suspense>
  );
}
```

Integración con TypeScript

```tsx
type ProductoParams = {
  id: string;
};

function Producto() {
  const { id } = useParams<ProductoParams>();
  return <div>{id}</div>;
}
```

--------------

 6-routing/react-router.md
Concepto

React Router es la librería estándar para manejar navegación y rutas en aplicaciones React. Permite sincronizar la UI con la URL, crear rutas anidadas, manejar parámetros, redirecciones, y más.
Instalación
bash

npm install react-router-dom

Componentes principales (v6)
1. BrowserRouter

Envuelve la aplicación para habilitar el enrutamiento usando la API de historial HTML5.
jsx

import { BrowserRouter } from 'react-router-dom';

ReactDOM.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>,
  document.getElementById('root')
);

2. Routes y Route

Routes contiene múltiples Route que renderizan el componente correspondiente según la URL.
jsx

import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/contacto" element={<Contacto />} />
    </Routes>
  );
}

3. Link y NavLink

Para navegación sin recargar la página.
jsx

import { Link, NavLink } from 'react-router-dom';

function Menu() {
  return (
    <nav>
      <Link to="/">Inicio</Link>
      <NavLink to="/about" className={({ isActive }) => isActive ? 'activo' : ''}>
        Acerca de
      </NavLink>
    </nav>
  );
}

Parámetros de ruta
Parámetros URL (:id)
jsx

<Route path="/productos/:id" element={<ProductoDetalle />} />

// En el componente ProductoDetalle
import { useParams } from 'react-router-dom';
function ProductoDetalle() {
  const { id } = useParams();
  // fetch producto con id
}

Parámetros de query string (?search=...&page=2)
jsx

import { useSearchParams } from 'react-router-dom';

function Busqueda() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  
  const handleSearch = (e) => {
    setSearchParams({ q: e.target.value });
  };
  // ...
}

Rutas anidadas

Las rutas pueden anidarse para reflejar jerarquías de UI.
jsx

// Layout principal
function Layout() {
  return (
    <div>
      <Header />
      <Outlet /> {/* Aquí se renderizan las rutas hijas */}
      <Footer />
    </div>
  );
}

// Definición de rutas
<Routes>
  <Route path="/" element={<Layout />}>
    <Route index element={<Home />} />
    <Route path="productos" element={<Productos />}>
      <Route path=":id" element={<ProductoDetalle />} />
    </Route>
    <Route path="*" element={<NotFound />} />
  </Route>
</Routes>

Navegación programática
jsx

import { useNavigate } from 'react-router-dom';

function Login() {
  const navigate = useNavigate();
  
  const handleSubmit = async () => {
    await login();
    navigate('/dashboard', { replace: true }); // replace evita historial
  };
}

Redirecciones
jsx

// En v6, se usa <Navigate />
import { Navigate } from 'react-router-dom';

function RutaPrivada({ children }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" replace />;
}

// En la definición de rutas
<Route path="/dashboard" element={<RutaPrivada><Dashboard /></RutaPrivada>} />

Rutas protegidas con contexto
jsx

function AppRoutes() {
  const { user } = useAuth();
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={user ? <Dashboard /> : <Navigate to="/login" />} />
    </Routes>
  );
}

Lazy loading con React Router
jsx

import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));

<Suspense fallback={<div>Cargando...</div>}>
  <Routes>
    <Route path="/dashboard" element={<Dashboard />} />
  </Routes>
</Suspense>

Comparación con otras soluciones

    React Router: más popular, completa, para SPA.

    TanStack Router: más nuevo, tipado, rendimiento.

    Next.js Router: enrutamiento basado en archivos (App Router).

Buenas prácticas

    Coloca BrowserRouter lo más alto posible.

    Usa NavLink para estilos activos.

    Define rutas con path relativo en rutas anidadas.

    Usa useLocation para acceder a la URL actual y rastreo analítico.

jsx

const location = useLocation();
useEffect(() => {
  ga.sendPageView(location.pathname);
}, [location]);
----


[⬅️ Volver al Índice](../README.md)

