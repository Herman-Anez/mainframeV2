# Error Boundaries

## Concepto

Un **Error Boundary** es un componente de React que **captura errores de JavaScript** en cualquier lugar de su árbol de componentes hijo, los registra y muestra una interfaz de fallback en lugar de que el componente se desmonte o la aplicación se rompa por completo.

**Nota importante**: Los Error Boundaries solo capturan errores durante el **renderizado**, en métodos de ciclo de vida y en constructores. No capturan errores en:

- Manejadores de eventos (`onClick`, `onChange`, etc.)
- Código asíncrono (`setTimeout`, `requestAnimationFrame`)
- Renderizado en el servidor
- Errores lanzados dentro del propio Error Boundary

## ¿Por qué son necesarios?

Antes de React 16, un error en un componente causaba que toda la aplicación se desmontara, mostrando una pantalla en blanco. Los Error Boundaries permiten aislar el error y mostrar una UI alternativa, manteniendo el resto de la aplicación funcionando.

## Creación de un Error Boundary

Debe ser un **componente de clase** (no existe hook equivalente aún). Implementa `static getDerivedStateFromError()` y/o `componentDidCatch()`.

```jsx
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    // Actualiza el estado para mostrar el fallback en el siguiente render
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Puedes enviar el error a un servicio de reporte (ej. Sentry, LogRocket)
    console.error('Error capturado:', error, errorInfo);
    // Ejemplo: logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Puedes renderizar cualquier UI de fallback
      return <h1>Algo salió mal.</h1>;
    }
    return this.props.children;
  }
}
```

Uso básico

```jsx
<ErrorBoundary>
  <MiComponentePeligroso />
</ErrorBoundary>
```

Personalización del fallback

Puedes pasar un fallback personalizado mediante props:

```jsx
```

class ErrorBoundary extends React.Component {
  // ... mismo estado y métodos
  render() {
    if (this.state.hasError) {
      return this.props.fallback || <h1>Error inesperado</h1>;
    }
    return this.props.children;
  }
}

// Uso
<ErrorBoundary fallback={<div>Error en el perfil</div>}>
  <PerfilUsuario />
</ErrorBoundary>

Múltiples Error Boundaries

Puedes anidarlos para aislar errores en diferentes partes de la UI.
jsx

<ErrorBoundary fallback={<ErrorWidget />}>
  <Sidebar />
  <ErrorBoundary fallback={<ErrorContenido />}>
    <ContenidoPrincipal />
  </ErrorBoundary>
</ErrorBoundary>

Manejo de errores en eventos

Los Error Boundaries no capturan errores en manejadores de eventos. Para esos casos, usa try/catch:

```jsx
function BotonPeligroso() {
  const [error, setError] = useState(null);

  const handleClick = () => {
    try {
      puedeLanzarError();
    } catch (e) {
      setError(e);
    }
  };

  if (error) return <div>Error: {error.message}</div>;
  return <button onClick={handleClick}>Click</button>;
}
```

Recuperación después de un error

Puedes añadir un botón para reiniciar el estado del Error Boundary y reintentar:

```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  resetError = () => {
    this.setState({ hasError: false });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <p>Algo falló.</p>
          <button onClick={this.resetError}>Reintentar</button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

Integración con react-router

Envuelve rutas completas para que una página con error no rompa toda la app.

```jsx
<ErrorBoundary>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/productos" element={<Productos />} />
  </Routes>
</ErrorBoundary>
```

Limitaciones conocidas

- Solo funciona en componentes de clase. No hay useErrorBoundary hook oficial (aunque librerías como react-error-boundary ofrecen una API funcional).

- No captura errores en componentes asíncronos (lazy, suspense) – esos requieren manejo aparte.

- No captura errores en SSR.

Librería recomendada: react-error-boundary

Ofrece una API más amigable con hooks y utilidades adicionales.
bash

npm install react-error-boundary

```jsx
import { ErrorBoundary } from 'react-error-boundary';

function Fallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <p>Algo salió mal:</p>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Reintentar</button>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary
      FallbackComponent={Fallback}
      onReset={() => {
        // reiniciar estado de la aplicación
      }}
    >
      <MiApp />
    </ErrorBoundary>
  );
}
```

También ofrece hook useErrorHandler para manejar errores en eventos.
Buenas prácticas

- Coloca Error Boundaries estratégicamente: no uno gigante que oculte toda la UI, ni demasiados pequeños que compliquen.

- Proporciona fallbacks útiles que permitan al usuario recuperarse (recargar, volver atrás, reportar error).

- Registra los errores en un servicio de monitoreo (Sentry, LogRocket, etc.) dentro de componentDidCatch.

- No uses Error Boundaries para control de flujo (ej. validación de formularios) – para eso usa estado local.

Ejemplo completo con reporte a Sentry

```jsx
import * as Sentry from '@sentry/react';

class SentryErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    Sentry.captureException(error, { extra: errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return <div>Error reportado a nuestro equipo.</div>;
    }
    return this.props.children;
  }
}
```

Conclusión

Los Error Boundaries son esenciales para aplicaciones React robustas. Permiten aislar fallos y mantener la experiencia de usuario. Aunque requieren componentes de clase, librerías como react-error-boundary simplifican su uso en aplicaciones funcionales.
