# 📝 JSX: JavaScript XML

JSX es una extensión de sintaxis para JavaScript que permite escribir estructuras similares a HTML dentro de tus archivos JS. Aunque no es obligatorio, es el estándar de oro en React por su expresividad y facilidad de uso.

## 🔍 ¿Cómo funciona?

Bajo el capó, los navegadores no entienden JSX. Herramientas como **Babel** o **SWC** transforman tu JSX en llamadas a funciones estándar de `React.createElement`.

### Ejemplo de transformación

```jsx
// Lo que escribes
const element = <h1 className="title">Hola Mundo</h1>;

// Lo que el navegador recibe
const element = React.createElement('h1', { className: 'title' }, 'Hola Mundo');
```

---

## 📏 Reglas de Oro

Para que el compilador sea feliz, debes seguir estas reglas fundamentales:

1.  **Un solo elemento raíz**: Todo componente o expresión debe devolver un único elemento padre.
    > [!TIP]
    > Usa Fragmentos (`<> ... </>`) si no quieres añadir nodos extra al DOM.
2.  **Cierre obligatorio**: Todas las etiquetas deben cerrarse, incluso las vacías (ej: `<img />`, `<br />`).
3.  **CamelCase para atributos**: En lugar de `onclick`, usa `onClick`. `class` se convierte en `className`.
4.  **JavaScript en llaves**: Puedes inyectar cualquier expresión válida de JS usando `{ }`.

---

## 💡 Ejemplo Práctico

```jsx
const UserProfile = () => {
  const user = { name: "Ana", age: 25 };

  return (
    <div className="card">
      <h2>Bienvenida, {user.name}</h2>
      <p>Edad: {user.age > 18 ? "Adulto" : "Menor"}</p>
      <div style={{ backgroundColor: '#f0f0f0', padding: '10px' }}>
        Perﬁl verificado
      </div>
    </div>
  );
};
```

---


## JSX como valor

Puedes guardar JSX en variables, devolverlo desde funciones, pasarlo como props.

## 🛡️ Seguridad (Inyección XSS)

React se encarga de **escapar todos los valores** antes de renderizarlos. Esto significa que nunca podrás inyectar código malicioso accidentalmente a través de una variable de texto.
Nunca uses dangerouslySetInnerHTML a menos que confíes plenamente en el contenido.

---

[⬅️ Volver al Índice](../README.md)
