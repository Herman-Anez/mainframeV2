# 🛠️ Props Drilling: El Problema de la Perforación

El **Props Drilling** (o "perforación de props") es una situación común en React donde los datos deben pasar a través de múltiples niveles de componentes intermedios que no los consumen, actuando únicamente como "pasamanos" hasta llegar a un componente profundo que realmente los necesita.

---

## ⚖️ Auditoría de Contenido

> [!NOTE]
> Este concepto es el precursor necesario para entender por qué existen soluciones como **Context API** o **Zustand**. No hay redundancia crítica aquí, pero se recomienda complementar con el archivo [Context API](./context-api.md).

---

## 🏗️ Ejemplo del Problema

```jsx
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
```

Aquí `Header` y `Navbar` solo pasan `user` sin usarlo directamente.

---

## ⚠️ ¿Por qué es problemático?

*   **Código frágil**: si cambias la estructura de componentes, tienes que modificar todos los intermediarios.
*   **Difícil de mantener**: componentes intermedios reciben props que no les conciernen.
*   **Dificulta la refactorización**.
*   **Ruido visual**: el código se vuelve verboso.

---

## 📊 Señales de que necesitas otra solución

*   Una prop pasa por más de 2-3 niveles sin ser usada.
*   Muchos componentes comparten el mismo dato global (tema, autenticación, idioma).
*   El árbol de componentes es profundo y anidado.

---

## 🚀 Soluciones al Props Drilling

### 1. Composición (elevar el contenido)

En lugar de pasar datos a través de intermediarios, pasa el componente ya construido (técnica de **Slot Composition**).

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

Sigue habiendo cierto drilling, pero más controlado y desacoplado.

### 2. Context API
Provee el dato en un nivel alto y lo consume donde sea necesario sin intermediarios. Ver [Context API](./context-api.md).

### 3. Estado global con librerías (Redux, Zustand, etc.)
Ideal para aplicaciones de gran escala.

### 4. Patrón de render props o children como función
Menos común en el React moderno, pero aún válido en ciertos casos de uso.

---

## 💡 Buenas Prácticas

*   **No optimices prematuramente**: para 2 niveles de profundidad, el props drilling suele ser preferible por su transparencia.
*   **Agrupa datos relacionados**: usa un objeto para pasar una única prop en lugar de múltiples props dispersas.
*   **Extrae componentes**: si un componente intermedio solo pasa props, quizás puede ser eliminado o fusionado mediante la composición.

---

[⬅️ Volver al Índice](../README.md)

