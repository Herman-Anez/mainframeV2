# estilos/css-modules.md

## CSS Modules

Permite escribir CSS con ámbito local (por componente). Evita colisiones de nombres.
Configuración

Create React App y Vite lo soportan por defecto. Los archivos deben terminar en .module.css.
Uso

```css
/* Boton.module.css */
.boton {
  background: blue;
  color: white;
}
.primario {
  background: green;
}
```

```tsx
import styles from './Boton.module.css';

function Boton() {
  return <button className={styles.boton}>Click</button>;
}
```

Clases múltiples

```tsx
<button className={`${styles.boton} ${styles.primario}`}>
  Click
</button>
// o usando arrays y join
```

Combinación con props

```tsx
<button className={`${styles.boton} ${props.importante ? styles.importante : ''}`}>
```

Ventajas

- Estilos encapsulados, sin fugas.

- Nombres de clase legibles (se generan hashes).

- Funciona con CSS puro.

Desventajas

- No tiene características de CSS-in-JS (temas dinámicos complejos).

- Los nombres se vuelven verbosos en el JSX.

Alternativa: SCSS Modules

Usa Boton.module.scss y tendrás anidación, variables, etc.
[back](../index.md)
