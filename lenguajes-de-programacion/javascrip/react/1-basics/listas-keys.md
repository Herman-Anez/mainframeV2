# listas-keys.md

Renderizado de listas con map()

```tsx
const nombres = ['Ana', 'Luis', 'Carlos'];
<ul>
  {nombres.map(nombre => <li key={nombre}>{nombre}</li>)}
</ul>
```

La prop key

    Ayuda a React a identificar qué elementos cambiaron, se añadieron o eliminaron.

    Debe ser única entre hermanos.

    Estable (no cambia entre renders).

    No usar índices del array como key si la lista es dinámica (reordenamiento, inserciones/eliminaciones). Los índices pueden causar bugs sutiles.

Buenas prácticas para keys

```tsx
// Ideal: usar id único del objeto
{usuarios.map(usuario => <li key={usuario.id}>{usuario.nombre}</li>)}

// Aceptable solo si la lista es estática y sin filtrados/reordenamientos
{items.map((item, index) => <li key={index}>{item}</li>)}
```

¿Qué pasa si no pongo key?

React mostrará una advertencia y usará el índice por defecto, lo que puede causar problemas de rendimiento y estado incorrecto.
key no es accesible como prop

No puedes leer props.key en el componente hijo. React la usa internamente.
Fragmentos con key

```tsx
<>
  {lista.map(item => (
    <React.Fragment key={item.id}>
      <dt>{item.term}</dt>
      <dd>{item.description}</dd>
    </React.Fragment>
  ))}
</>
```

Extraer componentes en listas

```tsx
function Lista({ items }) {
  return (
    <ul>
      {items.map(item => <ItemComponent key={item.id} item={item} />)}
    </ul>
  );
}
```

Uso de filter antes de map

```tsx
{tareas.filter(t => t.completada).map(t => <Tarea key={t.id} {...t} />)}
```

[back](../index.md)
