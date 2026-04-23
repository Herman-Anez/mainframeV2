atomic-design.md

Atomic Design es una metodología para diseñar sistemas de componentes, propuesta por Brad Frost. No es exclusiva de React, pero se lleva muy bien con componentes funcionales.
Los 5 niveles atómicos

## Átomos

Componentes básicos e indivisibles: botones, inputs, etiquetas, íconos.
```jsx
// Átomo: Button
function Button({ children, onClick, variant = 'primary' }) {
  return <button className={`btn btn-${variant}`} onClick={onClick}>{children}</button>;
}

// Átomo: Input
function Input({ type = 'text', placeholder }) {
  return <input type={type} placeholder={placeholder} className="input" />;
}
```


## Moléculas

Combinación de dos o más átomos que funcionan juntos como una unidad.
```jsx
// Molécula: SearchField (Input + Button)
function SearchField({ onSearch }) {
  const [query, setQuery] = useState('');
  return (
    <div className="search-field">
      <Input value={query} onChange={(e) => setQuery(e.target.value)} />
      <Button onClick={() => onSearch(query)}>Buscar</Button>
    </div>
  );
}
```


## Organismos

Componentes más complejos formados por moléculas, átomos y/o otros organismos. Representan secciones de la interfaz.
```jsx
// Organismo: Header (Logo + SearchField + NavMenu)
function Header() {
  return (
    <header className="header">
      <Logo />
      <SearchField onSearch={handleGlobalSearch} />
      <NavMenu items={['Inicio', 'Productos', 'Contacto']} />
    </header>
  );
}
```


## Plantillas (Templates)

Combinan organismos en una estructura de página sin contenido final (esqueletos). No tienen lógica de datos, solo layout.
```jsx
// Template: ProductPageTemplate
function ProductPageTemplate({ header, sidebar, content, footer }) {
  return (
    <div className="page">
      {header}
      <div className="layout">
        <aside>{sidebar}</aside>
        <main>{content}</main>
      </div>
      {footer}
    </div>
  );
}
```


## Páginas

Instancias concretas de plantillas con datos reales. Son los componentes que se enrutan.
```jsx
function ProductPage({ productId }) {
  const { product, related } = useProductData(productId);
  return (
    <ProductPageTemplate
      header={<Header />}
      sidebar={<ProductSidebar product={product} />}
      content={<ProductContent product={product} related={related} />}
      footer={<Footer />}
    />
  );
}
```


Estructura de carpetas sugerida para Atomic Design

```bash
src/
├── components/
│   ├── atoms/
│   │   ├── Button/
│   │   ├── Input/
│   │   └── Icon/
│   ├── molecules/
│   │   ├── SearchField/
│   │   └── ProductCard/
│   ├── organisms/
│   │   ├── Header/
│   │   └── ProductList/
│   ├── templates/
│   │   └── ProductPageTemplate/
│   └── pages/
│       └── ProductPage/
```

Ventajas

- Reutilización máxima.

- Consistencia en toda la aplicación.

- Escalabilidad para equipos grandes.

- Fácil testing de componentes pequeños.

Desventajas

- Sobreesfuerzo para apps pequeñas.

- Dificultad para clasificar algunos componentes (¿molécula u organismo?).

- Verboso en carpetas.

Consejos prácticos

- No es necesario seguir al pie de la letra; adapta el concepto.

- Usa Atomic Design principalmente para sistemas de diseño (bibliotecas de componentes).

- Combínalo con Storybook para documentar cada nivel.

Alternativas similares

- Componentes compuestos (sin jerarquía estricta).

- Domain-driven design (componentes por dominio funcional).

