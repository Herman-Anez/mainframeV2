# 🧱 Componentes: El Corazón de React

Los componentes son las piezas fundamentales de la interfaz de usuario. Son independientes, reutilizables y permiten dividir la UI en partes lógicas y manejables.

---

## 🏗️ Tipos de Componentes

### 1. Componentes Funcionales (Recomendado)

Son funciones de JavaScript que devuelven JSX. Gracias a los **Hooks**, hoy en día pueden manejar estado y ciclo de vida.

```jsx
const Welcome = ({ name }) => {
  return <h1>Hola, {name}</h1>;
};
function Saludo(props) {
  return <h1>Hola, {props.nombre}</h1>;
}
```

### 2. Componentes de Clase (Legado)

Eran el estándar antes de 2019. Aunque siguen funcionando, la comunidad y el equipo de React recomiendan usar componentes funcionales.

```jsx
class Welcome extends React.Component {
  render() {
    return <h1>Hola, {this.props.name}</h1>;
  }
}
```

---

## Tipos de componentes según su función

- Presentacionales (tontos): Solo reciben props y renderizan UI. Sin estado propio.

- Contenedores (inteligentes): Manejan lógica, estado, efectos secundarios.

- Componentes puros: Dado las mismas props, siempre renderizan el mismo JSX.

## 📏 Reglas y Convenciones

1. **PascalCase**: Los nombres de los componentes **siempre** deben empezar con mayúscula (ej: `MyButton`, no `myButton`). Esto permite a React distinguirlos de las etiquetas HTML estándar.
2. **Inmutabilidad**: Un componente nunca debe modificar sus propias `props`. Deben tratarse como valores de solo lectura.
3. **Responsabilidad Única**: Si un componente se vuelve demasiado complejo, es una señal para dividirlo en componentes más pequeños.

---

## 🧩 Composición y `children`

React favorece la **composición sobre la herencia**. Puedes pasar otros componentes o elementos como contenido usando la prop especial `children`.

```jsx
const Card = ({ children, title }) => {
  return (
    <div className="card">
      <h3>{title}</h3>
      <div className="content">
        {children}
      </div>
    </div>
  );
};

// Uso:
<Card title="Mi Perfil">
  <p>Este es el contenido interno del card.</p>
</Card>
```

> [!TIP]
> Piensa en los componentes como funciones matemáticas: **Props (Input) → JSX (Output)**.

---
[⬅️ Volver al Índice](../README.md)