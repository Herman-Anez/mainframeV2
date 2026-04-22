# composicion.md

La composición en React es el principio de construir componentes complejos a partir de componentes más pequeños y reutilizables, combinándolos como piezas de Lego. React favorece la composición sobre la herencia.
Composición vs Herencia

- Herencia: extender clases (ej. class Boton extends ComponenteBase). React no la recomienda para reutilizar lógica.

- Composición: incluir un componente dentro de otro mediante props o children.

## Formas de composición

### props.children (contenido anidado)

```jsx
function Card({ children }) {
  return <div className="card">{children}</div>;
}

function App() {
  return (
    <Card>
      <h2>Título</h2>
      <p>Contenido</p>
    </Card>
  );
}
```

### Props con componentes (especialización)

```jsx
function Dialog({ title, message, buttons }) {
  return (
    <div className="dialog">
      <h2>{title}</h2>
      <p>{message}</p>
      <div className="buttons">{buttons}</div>
    </div>
  );
}

// Uso
<Dialog
  title="Confirmar"
  message="¿Estás seguro?"
  buttons={
    <>
      <button>Cancelar</button>
      <button>Confirmar</button>
    </>
  }
/>
```

### Props que reciben componentes (render props simplificadas)

```jsx
function ListaDeItems({ items, renderItem }) {
  return <ul>{items.map(item => <li key={item.id}>{renderItem(item)}</li>)}</ul>;
}

<ListaDeItems
  items={usuarios}
  renderItem={user => <span>{user.nombre} ({user.email})</span>}
/>
```

### HOCs (aunque son una forma de composición, se tratan aparte)

Un HOC es una función que recibe un componente y devuelve otro componente.
Patrón de contenedor vs presentacional (composición)

```jsx
// Presentacional: solo UI
function UserProfile({ user }) {
  return <div>{user.name}</div>;
}

// Contenedor: lógica y datos
function UserProfileContainer({ userId }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);
  return <UserProfile user={user} />;
}
```

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
