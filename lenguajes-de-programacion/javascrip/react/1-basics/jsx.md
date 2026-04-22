# ¿Qué es JSX?

JSX (JavaScript XML) es una extensión de sintaxis que permite escribir estructuras similares a HTML dentro de código JavaScript. No es obligatorio en React, pero es la forma recomendada por su legibilidad y potencia.
Transformación

JSX se compila (con Babel o swc) a llamadas React.createElement:
jsx

```JSX
// JSX
const elemento = <h1 className="saludo">Hola, mundo</h1>;// Compilado

const elemento = React.createElement('h1', { className: 'saludo' }, 'Hola, mundo');
```

## Reglas y características importantes

- Una sola raíz: Todo componente debe devolver un solo elemento envolvente. Puedes usar `<Fragment> o <> </>.`

- Etiquetas deben cerrarse: `<img />, <br />, <input />.`

- Expresiones JavaScript entre {}:

```jsx
const nombre = "Ana";
const element = <p>Bienvenida {nombre}</p>;
```

- Atributos con camelCase:

- - class → className

- - for → htmlFor

- - tabindex → tabIndex

Estilos en línea con objeto:

```jsx

<div style={{ backgroundColor: 'red', fontSize: '16px' }}>Texto</div>

/*Comentarios:*/ {/*comentario*/}
```

## JSX como valor

Puedes guardar JSX en variables, devolverlo desde funciones, pasarlo como props.
Seguridad contra inyección XSS

React escapa automáticamente los valores incrustados en JSX antes de renderizarlos. Nunca uses dangerouslySetInnerHTML a menos que confíes plenamente en el contenido.
Buenas prácticas

- Mantén JSX legible, extrae lógica compleja fuera del return.

- Usa paréntesis para envolver JSX multilínea.

- Prefiere fragmentos en lugar de div innecesarios.
[back](../index.md)
