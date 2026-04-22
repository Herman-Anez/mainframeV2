# componentes.md

## Definición

Un componente es una pieza de UI reutilizable e independiente. Puede ser una función o una clase. Recibe props y devuelve JSX.

## Componente funcional (moderno)

```JSX
function Saludo(props) {
  return <h1>Hola, {props.nombre}</h1>;
}
```

- Desde React 16.8 pueden usar hooks (estado, efectos, etc.).

- Son más simples y ligeros.

## Componente de clase (legado)

```jsx
class Saludo extends React.Component {
  render() {
    return <h1>Hola, {this.props.nombre}</h1>;
  }
}
```

- Necesitan render().

- Usaban this.state y ciclo de vida (componentDidMount, etc.). Hoy se recomienda funciones + hooks.

## Tipos de componentes según su función

- Presentacionales (tontos): Solo reciben props y renderizan UI. Sin estado propio.

- Contenedores (inteligentes): Manejan lógica, estado, efectos secundarios.

- Componentes puros: Dado las mismas props, siempre renderizan el mismo JSX.

## Reglas importantes

- Los nombres de componentes deben comenzar con mayúscula (distingue de etiquetas HTML).

- Un componente no debe modificar sus props (son de solo lectura).

- Todo componente debe ser una función pura respecto a sus props y estado (para evitar efectos colaterales).

## Composición

Se recomienda composición sobre herencia. Puedes anidar componentes y usar props.children:

```tsx
function Contenedor({ children }) {
  return <div className="card">{children}</div>;
}
```

## Extracción de componentes

Cuando una parte de la UI se repite o es compleja, conviene extraerla en un componente independiente.
[back](../index.md)
