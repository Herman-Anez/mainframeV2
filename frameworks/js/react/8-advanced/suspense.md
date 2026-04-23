# ⏳ Suspense: Orquestación de Cargas Asíncronas

`Suspense` es un componente de React que permite "esperar" a que se cumpla una condición (generalmente la carga de datos o de un componente) antes de renderizar su contenido, mostrando una interfaz de repuesto (**fallback**) mientras el trabajo se completa.

---

## 🏗️ Evolución de Suspense

*   **React 16.6**: Lanzado originalmente para la división de código con `React.lazy`.
*   **React 18**: Evolucionó para soportar la obtención de datos (**Data Fetching**) y el renderizado en servidor por partes (**Streaming SSR**).
*   **React 19**: Introduce el hook `use()`, que simplifica enormemente la integración de Suspense con promesas.

---

## 🚀 Uso con React.lazy (Code Splitting)

Permite descargar componentes solo cuando son necesarios, reduciendo el tamaño del bundle inicial.

```jsx
const UserProfile = lazy(() => import('./UserProfile'));

function App() {
  return (
    <Suspense fallback={<p>Cargando página...</p>}>
      <UserProfile />
    </Suspense>
  );
}
```

---

## 📡 Suspense para Data Fetching (React 18+)

Para que un componente pueda "suspenderse" durante la carga de datos, la fuente de datos (la librería de Fetching) debe ser compatible con la API de Suspense.

```jsx
// Ejemplo conceptual con una promesa
function UserList({ userPromise }) {
  // En React 19 se usa el hook 'use'
  const users = use(userPromise); 
  
  return (
    <ul>
      {users.map(u => <li key={u.id}>{u.name}</li>)}
    </ul>
  );
}

function Page() {
  return (
    <Suspense fallback={<Skeleton />}>
      <UserList userPromise={fetchUsers()} />
    </Suspense>
  );
}
```

---

## 🖇️ Suspense Anidado

Puedes colocar múltiples `Suspense boundaries` para tener un control granular sobre qué partes de la página se muestran primero.

```jsx
<Suspense fallback={<FullPageSkeleton />}>
  <Header />
  <div className="content">
    {/* El contenido principal puede cargar independientemente del sidebar */}
    <Suspense fallback={<MainSkeleton />}>
      <MainContent />
    </Suspense>
    <Suspense fallback={<SidebarSkeleton />}>
      <Sidebar />
    </Suspense>
  </div>
</Suspense>
```

---

## 🛡️ Suspense + Error Boundaries

> [!IMPORTANT]
> `Suspense` no captura errores de carga (ej: una API que responde 404 o 500). Para manejar fallos en las promesas, **siempre** envuelve tu `Suspense` en un `Error Boundary`.

```jsx
<ErrorBoundary fallback={<ErrorMessage />}>
  <Suspense fallback={<Loading />}>
    <AsyncComponent />
  </Suspense>
</ErrorBoundary>
```

---

## 💡 Buenas Prácticas

1.  **Skeleton Screens**: Usa fallbacks que se parezcan a la estructura final de la página para evitar saltos visuales bruscos (Layout Shift).
2.  **Ubicación Estratégica**: No pongas un solo `Suspense` gigante para toda la app; colócalos en secciones lógicas que puedan hidratarse de forma independiente.
3.  **Transiciones**: Combina `Suspense` con `useTransition` para evitar que la UI vuelva al estado de "Cargando" si el usuario solo está cambiando de pestaña o filtrando datos.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>