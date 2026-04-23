# 💅 Styled Components: CSS-in-JS Moderno

**Styled-components** es la librería líder de CSS-in-JS para React. Permite escribir CSS real dentro de tus archivos de JavaScript, utilizando *tagged template literals* para crear componentes que ya vienen con sus propios estilos.

---

## 🏗️ Instalación

```bash
npm install styled-components
```

---

## 🚀 Uso Básico

```jsx
import styled from 'styled-components';

const Boton = styled.button`
  background: #3182ce;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;

  &:hover {
    background: #2b6cb0;
  }
`;

function App() {
  return <Boton>Click aquí</Boton>;
}
```

---

## 🖇️ Adaptación Basada en Props

Una de las mayores potencias de esta librería es que puedes inyectar lógica de JavaScript directamente en el CSS a través de las `props`.

```jsx
const Boton = styled.button`
  background: ${props => props.primario ? '#38a169' : '#718096'};
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
`;

// Uso
<Boton primario>Guardar cambios</Boton>
<Boton>Cancelar</Boton>
```

---

## 🎭 Estilos Anidados y Extensión

Styled-components soporta sintaxis de anidación similar a SASS (`&`) y permite heredar estilos de otros componentes.

### Extender Componentes

```jsx
const BotonGrande = styled(Boton)`
  font-size: 1.5rem;
  padding: 20px 40px;
`;
```

---

## 🌐 Temas Dinámicos (Theming)

Gracias al `ThemeProvider`, puedes inyectar un objeto de tema global que será accesible por todos tus componentes estilizados.

```jsx
import { ThemeProvider } from 'styled-components';

const temaOscuro = { 
  primary: '#2d3748',
  text: '#ffffff' 
};

<ThemeProvider theme={temaOscuro}>
  <App />
</ThemeProvider>

// Acceso en el componente
const Titulo = styled.h1`
  color: ${props => props.theme.text};
  background: ${props => props.theme.primary};
`;
```

---

## 🛠️ Atributos Dinámicos (`.attrs`)

Puedes usar `.attrs` para pasar atributos HTML estáticos o dinámicos sin ensuciar el JSX.

```jsx
const Input = styled.input.attrs(props => ({
  type: 'text',
  placeholder: props.placeholder || 'Escribe algo...'
}))`
  border: 2px solid #e2e8f0;
  padding: 8px;
`;
```

---

## ⚖️ Ventajas y Limitaciones

### ✅ Ventajas

* **Encapsulamiento Total**: Cero colisiones de CSS.
* **Props Reactivas**: El CSS cambia automáticamente con el estado de React.
* **Mantenimiento**: Los estilos viven junto al componente correspondiente.

### ❌ Desventajas

* **Runtime**: Añade una pequeña carga al navegador para procesar el CSS.
* **Aprendizaje**: Requiere acostumbrarse a la sintaxis de plantillas de cadena.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
