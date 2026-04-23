# 🧱 Componentes: El Corazón de React

Los componentes son las piezas fundamentales de la interfaz de usuario. Son independientes, reutilizables y permiten dividir la UI en partes lógicas y manejables.

---

## 🏗️ Tipos de Componentes

### 🟢 Componentes Funcionales (Recomendado)

Son funciones de JavaScript que devuelven JSX. Gracias a los **Hooks**, hoy en día pueden manejar estado y ciclo de vida de forma eficiente.

```jsx
const Welcome = ({ name }) => {
  return <h1>Hola, {name}</h1>;
};
function Saludo(props) {
  return <h1>Hola, {props.nombre}</h1>;
}
```

### 🟠 Componentes de Clase (Legado/Obsoleto)

> [!CAUTION]
> Eran el estándar antes de 2019. Aunque siguen funcionando, la comunidad y el equipo de React recomiendan usar componentes funcionales. No se recomienda su uso en proyectos nuevos.

```jsx
class Welcome extends React.Component {
  render() {
    return <h1>Hola, {this.props.name}</h1>;
  }
}
```

---

## 🎭 Categorías según su propósito

Una buena arquitectura divide los componentes según su responsabilidad:

* **Presentacionales ("Tontos")**: Solo reciben props y renderizan UI. No deben tener lógica de negocio pesada ni estado (normalmente).
* **Contenedores ("Inteligentes")**: Manejan la lógica, el estado y los efectos secundarios. Suelen envolver componentes presentacionales.
* **Componentes de Alto Orden (HOC)**: Funciones que reciben un componente y devuelven uno nuevo con funcionalidades extra.

---

## 📏 Reglas y Convenciones

1. **PascalCase**: Los nombres de los componentes **siempre** deben empezar con mayúscula (ej: `MyButton`, no `myButton`). Esto permite a React distinguirlos de las etiquetas HTML estándar.
2. **Inmutabilidad**: Un componente nunca debe modificar sus propias `props`. Deben tratarse como valores de solo lectura.
3. **Responsabilidad Única**: Si un componente se vuelve demasiado complejo, es una señal para dividirlo en componentes más pequeños (Principio SOLID).

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
> Piensa en los componentes como funciones puras: **Props (Entrada) → JSX (Salida)**.

---

[⬅️ Volver al Índice](../README.md)