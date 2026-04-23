
## 📘 00-introduccion/instalacion-y-setup.md

### Instalación y configuración inicial

#### Requisitos previos

- Node.js 18.17 o superior (recomendado).
- Gestor de paquetes: `npm`, `yarn`, `pnpm` o `bun`.

#### Crear un proyecto nuevo

```bash
npx create-next-app@latest mi-proyecto
```

El instalador interactivo te preguntará:

- **TypeScript:** Recomendado (Sí).
- **ESLint:** Recomendado (Sí).
- **Tailwind CSS:** Opcional, pero útil.
- **Directorio src/:** Si prefieres tener las carpetas `app/` y `pages/` dentro de `src/`.
- **App Router:** ¿Usar el nuevo App Router? (Sí/No). Puedes elegir Pages Router para seguir esta sección.
- **Alias de importación:** Por defecto `@/*`.

#### Estructura básica (Pages Router)

```text
mi-proyecto/
├── pages/
│   ├── api/
│   │   └── hello.js       // API route
│   ├── _app.js             // Componente global (layouts, estados)
│   ├── _document.js        // Estructura HTML personalizada
│   └── index.js            // Página principal "/"
├── public/                 // Archivos estáticos
├── styles/                 // CSS global o módulos
├── next.config.js          // Configuración de Next.js
├── package.json
└── ...
```

#### Ejecutar el proyecto

```bash
npm run dev        # Inicia servidor de desarrollo en http://localhost:3000
npm run build      # Crea la versión de producción
npm start          # Inicia el servidor en modo producción
```

**Personalizar el puerto:**

```bash
npm run dev -- -p 4000
```

#### Tu primera página

Crea `pages/index.js`:

```jsx
export default function Home() {
  return <h1>¡Hola Next.js con Pages Router!</h1>;
}
```

Visita `http://localhost:3000` y verás el resultado.

#### Instalación manual en un proyecto existente

Si ya tienes un proyecto, instala:

```bash
npm install next react react-dom
```

Luego configura los scripts en `package.json`:

```json
"scripts": {
  "dev": "next dev",
  "build": "next build",
  "start": "next start"
}
```

Crea la carpeta `pages/` con un archivo `index.js`. Ya puedes empezar.

---
