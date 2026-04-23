# 🎭 Renderizado Condicional: Lógica Dinámica

El renderizado condicional en React funciona de la misma manera que las condiciones en JavaScript. Permite mostrar diferentes interfaces dependiendo del estado de la aplicación o de las props recibidas.

---

## 🏗️ Patrones Comunes

### 1. `if / else` (Fuera del JSX)
Ideal cuando la lógica de renderizado es compleja o el componente debe devolver estructuras completamente distintas.

```jsx
function Componente({ autenticado }) {
  if (autenticado) {
    return <Dashboard />;
  }
  return <Login />;
}
```

### 2. Operador Ternario (Dentro del JSX)
La solución más común para elegir entre dos opciones dentro de una estructura JSX existente.

```jsx
<div>
  {autenticado ? <Dashboard /> : <Login />}
</div>
```

### 3. Operador Lógico `&&` (Cortocircuito)
Útil cuando quieres mostrar un elemento solo si una condición es verdadera, y nada en caso contrario.

```jsx
<div>
  {autenticado && <Dashboard />}
</div>
```

> [!CAUTION]
> **Cuidado con los falsy values**: Si la condición es `0` o `""`, React renderizará ese valor en lugar de nada.
> **Solución**: `{contador > 0 && <p>Valor: {contador}</p>}` o `{!!texto && <p>{texto}</p>}`.

---

## 🚀 Técnicas Avanzadas

### Variables de Elementos
Puedes almacenar JSX en variables para mantener el `return` principal limpio y legible.

```jsx
let contenido;
if (cargando) {
  contenido = <Spinner />;
} else if (error) {
  contenido = <MensajeError />;
} else {
  contenido = <Datos />;
}

return <div>{contenido}</div>;
```

### Retorno Anticipado (Early Return)
Evita anidamientos excesivos saliendo de la función lo antes posible si no hay nada que renderizar o si hay un estado de carga/error.

```jsx
function Lista({ items }) {
  if (!items.length) {
    return <p>La lista está vacía</p>;
  }
  return <ul>{items.map(item => <Item key={item.id} {...item} />)}</ul>;
}
```

### Uso de `switch`
Excelente para manejar estados de máquinas de estado (ej: `loading`, `error`, `success`).

```jsx
function Estado({ status }) {
  switch(status) {
    case 'loading': return <Spinner />;
    case 'error': return <Error />;
    case 'success': return <Ok />;
    default: return null;
  }
}
```

---

## ⚖️ Comparación de Patrones

*   **Ternario**: Cuando tienes dos opciones claras ("A o B").
*   **&&**: Para mostrar u ocultar un elemento ("A o Nada").
*   **If/else o Switch**: Cuando hay lógica compleja o más de dos estados posibles.

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>
