# estilos/tailwind.md

## Tailwind CSS

Framework de utilidades (utility-first) que proporciona clases CSS atómicas.
Configuración rápida en React

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Configurar tailwind.config.js con las rutas de tus componentes:
js

content: ['./src/**/*.{js,jsx,ts,tsx}'],

Importar Tailwind en index.css:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Uso básico

```tsx
function Boton() {
  return (
    <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700">
      Click
    </button>
  );
}
```

º

Ventajas

- No necesitas escribir CSS personalizado.

- Muy rápido de desarrollar.

- Bundle pequeño (purga clases no usadas en producción).

- Diseño consistente gracias a la configuración de tema.

Desventajas

- JSX se vuelve verboso (puedes extraer componentes).

- Curva de aprendizaje de las clases.

- Dependencia de un framework de utilidades.

Extracción de componentes con @apply

En tu archivo CSS (si usas @layer components):

```css
.btn-primary {
  @apply bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700;
}
```

## Integración con clsx o classnames

Para combinar clases condicionalmente:

```tsx

import clsx from 'clsx';
<div className={clsx('base-class', { 'bg-red': error, 'bg-green': success })} />
```

## Plugins útiles

- @tailwindcss/forms – para resetear estilos de formularios.

- @tailwindcss/typography – para contenido HTML rico (blog, etc.).

## Personalización

En tailwind.config.js puedes extender colores, fuentes, breakpoints, etc.
🧠 Resumen de buenas prácticas generales

- Organiza los estilos según la estrategia que elijas: no mezcles CSS Modules con Tailwind a menos que tengas una razón fuerte.

- Prefiere componentes pequeños y reutilizables.

- Nombres claros para props y estados.

- Mantén los archivos cerca de su componente (cada carpeta de componente puede tener su Componente.jsx, Componente.module.css, etc.).

- Documenta decisiones en tus archivos markdown para futuras consultas.
