# estilos/styled-components.md

Styled-components (CSS-in-JS)

Librería para escribir CSS dentro de JavaScript, creando componentes estilizados.
Instalación

```bash
npm install styled-components
```

Uso básico

```tsx
import styled from 'styled-components';

const Boton = styled.button`
  background: blue;
  color: white;
  padding: 10px;
  border-radius: 5px;

  &:hover {
    background: darkblue;
  }
`;

function App() {
  return <Boton>Click</Boton>;
}
```

Adaptación basada en props

```tsx
const Boton = styled.button`
  background: ${props => props.primario ? 'green' : 'gray'};
`;
<Boton primario>Guardar</Boton>
```

Estilos anidados y pseudoclases

Soporta sintaxis similar a SCSS: &:hover, & > span, etc.
Extender estilos

```tsx
const BotonGrande = styled(Boton)`
  font-size: 24px;
`;
```

Ventajas

- Estilos completamente encapsulados.

- Temas dinámicos con ThemeProvider.

- Props controlan los estilos directamente.

- Elimina clases CSS globales.

Desventajas

- Añade runtime (aunque se puede compilar con babel-plugin-styled-components).

- Mayor curva de aprendizaje.

- Puede complicar el debugging en herramientas de navegador.

Uso con attrs

```tsx
const Input = styled.input.attrs(props => ({
  type: 'text',
  placeholder: props.placeholder || 'Escribe algo'
}))`
  border: 1px solid #ccc;
`;
```

Temas

```tsx
import { ThemeProvider } from 'styled-components';

const tema = { primary: 'blue' };
<ThemeProvider theme={tema}>
  <App />
</ThemeProvider>

// En el componente
const Boton = styled.button`
  background: ${props => props.theme.primary};
`;
```

[back](../index.md)
