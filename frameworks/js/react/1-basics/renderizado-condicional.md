
# renderizado-condicional

Formas de renderizar condicionalmente

## if / else fuera del JSX

```tsx
function Componente({ autenticado }) {
  if (autenticado) {
    return <Dashboard />;
  } else {
    return <Login />;
  }
}
```

## Operador ternario dentro del JSX

```tsx
<div>
  {autenticado ? <Dashboard /> : <Login />}
</div>
```

## && lógico (para mostrar o no mostrar)

```tsx
<div>
  {autenticado && <Dashboard />}
  {/* Si autenticado es true, muestra Dashboard; si false, no muestra nada */}
</div>
```

Cuidado: si autenticado es 0 o "" se renderizará ese valor. Mejor usar !!autenticado && ... o convertir a booleano.


## Variables que contienen JSX

```tsx
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

## Retorno anticipado (early return) en componentes

```tsx
function Lista({ items }) {
  if (!items.length) {
    return <p>No hay elementos</p>;
  }
  return <ul>{items.map(...)}</ul>;
}
```

Comparación de patrones

- Ternario: cuando hay dos opciones claras.

- &&: para mostrar u ocultar un solo elemento.

- If/else o early return: cuando hay muchas condiciones o el JSX es extenso.

## Renderizado condicional con switch

```tsx
function Estado({ status }) {
  switch(status) {
    case 'loading': return <Spinner />;
    case 'error': return <Error />;
    default: return <Ok />;
  }
}
```

## No usar && con números

```tsx
{contador && <p>Valor: {contador}</p>}
// Si contador === 0, renderiza "0" (porque 0 es falsy pero React lo muestra)
// Solución: {contador !== 0 && ...}
```
