# props-drilling.md

Props drilling (o "perforación de props") es la situación en la que datos deben pasar a través de múltiples niveles de componentes intermedios que no necesitan esos datos, solo para llegar a un componente profundo que sí los necesita.
Ejemplo del problema

```jsx
```

function App() {
  const [user, setUser] = useState({ name: 'Ana' });
  return <Header user={user} />;
}

function Header({ user }) {
  return <Navbar user={user} />;
}

function Navbar({ user }) {
  return <Avatar user={user} />;
}

function Avatar({ user }) {
  return <img src={user.avatar} />;
}

Aquí Header y Navbar solo pasan user sin usarlo directamente.
¿Por qué es problemático?

- Código frágil: si cambias la estructura de componentes, tienes que modificar todos los intermediarios.

- Difícil de mantener: componentes intermedios reciben props que no les conciernen.

- Dificulta la refactorización.

- Ruido visual: el código se vuelve verboso.

Señales de que necesitas otra solución

- Una prop pasa por más de 2-3 niveles sin ser usada.

- Muchos componentes comparten el mismo dato global (tema, autenticación, idioma).

- El árbol de componentes es profundo y anidado.

Soluciones a props drilling

## Composición (elevar el contenido)

En lugar de pasar datos a través de intermediarios, pasa el componente ya construido.

```jsx
function App() {
  const [user, setUser] = useState({ name: 'Ana' });
  return <Header avatar={<Avatar user={user} />} />;
}
function Header({ avatar }) {
  return <Navbar avatar={avatar} />;
}
function Navbar({ avatar }) {
  return <div>{avatar}</div>;
}
```

Sigue habiendo cierto drilling, pero más controlado.

## Context API

Provee el dato en un nivel alto y lo consume donde sea necesari## (Ver siguiente archivo)

## Estado global con librerías (Redux, Zustand, etc.)

## Patrón de render props o children como función (menos común hoy)

Buenas prácticas

- No optimices prematuramente: para 2 niveles, props drilling está bien.

- Agrupa datos relacionados en un objeto para pasar menos props.

- Extrae componentes: si un componente intermedio solo pasa props, quizás puede ser eliminado o fusionado.
