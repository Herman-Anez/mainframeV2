# props.md

## Concepto

Las props (abreviatura de "properties") son datos de solo lectura que un componente padre pasa al hijo. Fluyen unidireccionalmente (de arriba abajo).

## Uso básico

```tsx
// Padre
<Saludo nombre="Carlos" edad={30} />

// Hijo
function Saludo(props) {
  return <p>{props.nombre}, edad: {props.edad}</p>;
}
```

## Desestructuración de props (recomendado)

```tsx
function Saludo({ nombre, edad }) {
  return <p>{nombre}, edad: {edad}</p>;
}
```

## Props por defecto (defaultProps)

```tsx
```

function Boton({ texto = "Click" }) { ... }
// o externamente:
Boton.defaultProps = { texto: "Click" };

PropTypes (validación de tipos)

Instala prop-types:

```tsx
import PropTypes from 'prop-types';

Saludo.propTypes = {
  nombre: PropTypes.string.isRequired,
  edad: PropTypes.number
};
```

## props.children

Para contenido anidado:

```tsx
<Card>
  <h2>Título</h2>
  <p>Contenido</p>
</Card>

function Card({ children }) {
  return <div className="card">{children}</div>;
}
```

## Spread de props (usar con cuidado)

```tsx
<MiComponente {...objetoDeProps} />
```

Puede pasar props no deseadas. Prefiere listar explícitamente.
Inmutabilidad

Las props no se pueden modificar dentro del componente hijo. Si necesitas cambiarlas, el padre debe pasar una función modificadora (callback).
Patrón de render props

Pasar una función como prop que devuelve JSX (tema más avanzado, pero mencionar aquí como derivación).
[back](../index.md)
