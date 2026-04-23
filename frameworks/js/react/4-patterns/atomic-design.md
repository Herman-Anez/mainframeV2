# ⚛️ Atomic Design: Estructura y Jerarquía

**Atomic Design** es una metodología para diseñar sistemas de componentes, propuesta por Brad Frost. En React, este patrón ayuda a crear interfaces altamente modulares, escalables y fáciles de mantener al dividir los componentes en niveles de complejidad.

---

## 🏗️ Los 5 Niveles Atómicos

### 1. 🧪 Átomos
Componentes básicos e indivisibles. Son los ladrillos fundamentales: botones, entradas de texto, etiquetas, iconos.

```jsx
// Átomo: Button
function Button({ children, onClick, variant = 'primary' }) {
  return <button className={`btn btn-${variant}`} onClick={onClick}>{children}</button>;
}

// Átomo: Input
function Input({ type = 'text', placeholder }) {
  return <input type={type} placeholder={placeholder} className="input-field" />;
}
```

### 2. 🧬 Moléculas
Combinación de dos o más átomos que funcionan como una unidad lógica simple.

```jsx
// Molécula: SearchBar (Input + Button)
function SearchBar({ onSearch }) {
  return (
    <div className="search-bar">
      <Input placeholder="Buscar..." />
      <Button onClick={onSearch}>🔍</Button>
    </div>
  );
}
```

### 3. 🦠 Organismos
Componentes complejos formados por moléculas y átomos. Representan secciones completas y funcionales de la UI.

```jsx
// Organismo: Header (Logo + SearchBar + Nav)
function Header() {
  return (
    <header className="site-header">
      <Logo />
      <SearchBar />
      <Navigation />
    </header>
  );
}
```

### 4. 📐 Plantillas (Templates)
Esqueletos de página que definen la estructura (layout) pero sin contenido real. No manejan lógica de datos, solo el "dónde" va cada cosa.

```jsx
// Plantilla: StandardLayout
function StandardLayout({ header, content, footer }) {
  return (
    <div className="layout-container">
      {header}
      <main className="main-content">{content}</main>
      {footer}
    </div>
  );
}
```

### 5. 📄 Páginas
Instancias concretas de las plantillas donde se inyectan los datos reales del negocio. Es el nivel donde ocurre el fetching de datos y la conexión con el estado global.

```jsx
function HomePage() {
  const products = useProducts(); // Lógica de datos

  return (
    <StandardLayout
      header={<Header />}
      content={<ProductGrid items={products} />}
      footer={<Footer />}
    />
  );
}
```

---

## 📁 Estructura de Proyecto Sugerida

Para mantener el orden, se recomienda replicar la jerarquía en el sistema de archivos:

```bash
src/
└── components/
    ├── atoms/
    │   ├── Button/
    │   └── Input/
    ├── molecules/
    │   └── SearchBar/
    ├── organisms/
    │   └── Header/
    ├── templates/
    │   └── MainLayout/
    └── pages/
        └── Dashboard/
```

---

## ⚖️ Ventajas y Limitaciones

### ✅ Ventajas
*   **Reutilización Extrema**: Los átomos y moléculas se usan en toda la app.
*   **Consistencia Visual**: Todo el sistema hereda los mismos fundamentos.
*   **Escalabilidad**: Ideal para equipos grandes y Design Systems complejos.

### ❌ Desventajas
*   **Sobre-ingeniería**: Puede ser excesivo para aplicaciones pequeñas.
*   **Ambigüedad**: A veces es difícil decidir si algo es una molécula o un organismo.
*   **Verboso**: Crea muchas carpetas y archivos pequeños.

---

## 💡 Consejos de Implementación

*   **No seas rígido**: Si la clasificación te quita más tiempo del que te ahorra, simplifica la estructura.
*   **Usa Storybook**: Es el compañero perfecto de Atomic Design para documentar y probar componentes de forma aislada.
*   **Enfoque de Negocio**: En el nivel de **Páginas**, enfócate en la lógica. En los niveles inferiores, enfócate en la UI y la accesibilidad.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
