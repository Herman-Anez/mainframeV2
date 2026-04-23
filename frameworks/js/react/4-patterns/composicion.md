# 🧱 Composición: El ADN de React

La **composición** es el principio fundamental de React que consiste en construir componentes complejos a partir de piezas más pequeñas, simples y reutilizables. A diferencia de la herencia (común en POO tradicional), React favorece la composición por su flexibilidad y desacoplamiento.

---

## 🏗️ Composición vs Herencia

*   **Herencia**: Consiste en extender clases (ej: `class Boton extends ComponenteBase`). React **no recomienda** este patrón ya que crea jerarquías rígidas y difíciles de refactorizar.
*   **Composición**: Consiste en incluir componentes dentro de otros mediante `props` o la prop especial `children`. Es el "modelo Lego".

---

## 🚀 Formas de Composición

### 1. `props.children` (Contenido Anidado)
Es la forma más natural de composición. Permite que un componente actúe como un "contenedor" sin conocer de antemano qué habrá dentro.

```jsx
function Card({ children }) {
  return <div className="card-styled">{children}</div>;
}

function App() {
  return (
    <Card>
      <h2>Título Reutilizable</h2>
      <p>Este contenido es inyectado mediante la prop children.</p>
    </Card>
  );
}
```

### 2. Slots (Props con Componentes)
Ideal cuando necesitas inyectar contenido en múltiples lugares específicos de un componente (ej: cabecera, lateral y pie).

```jsx
function Layout({ header, sidebar, children, footer }) {
  return (
    <div className="layout">
      <header>{header}</header>
      <div className="main">
        <aside>{sidebar}</aside>
        <content>{children}</content>
      </div>
      <footer>{footer}</footer>
    </div>
  );
}
```

### 3. Especialización
Un componente más específico renderiza uno más genérico y lo configura mediante props.

```jsx
function Dialog({ title, message, children }) {
  return (
    <div className="modal">
      <h1>{title}</h1>
      <p>{message}</p>
      {children}
    </div>
  );
}

function WelcomeDialog() {
  return (
    <Dialog 
      title="Bienvenido" 
      message="Gracias por visitarnos"
    >
      <button>Empezar</button>
    </Dialog>
  );
}
```

---

## ⚖️ Ventajas de la Composición

*   **Flexibilidad**: Puedes cambiar el orden o el tipo de los componentes hijos sin tocar el padre.
*   **Mantenibilidad**: Favorece componentes con **Responsabilidad Única**.
*   **Desacoplamiento**: El padre y el hijo solo se conocen a través de una interfaz mínima definida por las props.

---

## 🛡️ Contenedores vs Presentacionales

Este es un patrón de composición donde se separa la lógica de los datos de la representación visual.

```jsx
// Presentacional: Solo recibe datos y los muestra
function UserProfile({ user }) {
  return <div>Nombre: {user.name}</div>;
}

// Contenedor: Maneja la lógica y el estado
function UserProfileContainer({ userId }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);

  return user ? <UserProfile user={user} /> : <Spinner />;
}
```
----


Composición vs Configuración

En lugar de tener un componente enorme con muchas props booleanas para variantes, compón variantes como componentes separados.

```jsx
// ❌ Mal: muchas props de configuración
<Button primary large disabled icon="save" />

// ✅ Bien: composición
<PrimaryButton large>Guardar</PrimaryButton>
// o
<Button variant="primary" size="large">Guardar</Button> // pero sigue siendo configuración
```

Ventajas de la composición

- Reutilización de lógica y UI.

- Flexibilidad: puedes cambiar el orden o tipo de componentes hijos.

- Mantenibilidad: componentes pequeños con una sola responsabilidad.

- Sin acoplamiento entre padre e hijo más allá de la interfaz (children o props).

Composición con contexto

El contexto se combina perfectamente con la composición: un Provider envuelve componentes hijos.
Buenas prácticas

- Prefiere children para contenido desconocido o dinámico.

- Para slots múltiples, usa props con nombres (ej. header, footer, sidebar).

- No pases componentes por props a menos que sea necesario (render props).

- Extrae lógica repetida en custom hooks, no en componentes heredados.

---

## 💡 Buenas Prácticas

*   **Evita Props de Configuración Masivas**: En lugar de `<Button primary large disabled icon="..." />`, considera componer variantes específicas.
*   **Children para Dinamismo**: Usa `children` para componentes que son "cajas" genéricas.
*   **Hooks sobre Herencia**: Si necesitas compartir lógica no visual, usa **Custom Hooks** en lugar de intentar heredar de otras clases.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
