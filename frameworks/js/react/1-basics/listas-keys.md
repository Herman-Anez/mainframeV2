# 📋 Listas y Keys: Iteración Eficiente

El renderizado de listas es una de las tareas más comunes en React. Se utiliza el método nativo `.map()` de JavaScript para transformar arrays de datos en colecciones de elementos JSX.

---

## 🏗️ Renderizado con `.map()`

Para renderizar una lista, simplemente iteramos sobre el array y devolvemos el JSX deseado por cada elemento.

```jsx
const nombres = ['Ana', 'Luis', 'Carlos'];

<ul>
  {nombres.map(nombre => <li key={nombre}>{nombre}</li>)}
</ul>
```

---

## 🔑 La Prop `key`

La prop `key` es un atributo especial que debes incluir al crear listas de elementos.

*   **Propósito**: Ayuda a React a identificar qué elementos han cambiado, se han añadido o se han eliminado, optimizando el proceso de reconciliación.
*   **Unicidad**: Cada `key` debe ser única entre elementos hermanos (no es necesario que sean únicas globalmente).
*   **Estabilidad**: La `key` no debe cambiar entre renderizados (evita usar `Math.random()`).

> [!CAUTION]
> **No uses índices del array** (`index`) como `key` si la lista es dinámica (si se puede reordenar, filtrar o eliminar elementos). Esto puede causar bugs visuales y problemas de estado impredecibles.

---

## 💡 Buenas Prácticas

### Uso de IDs Únicos (Recomendado)
Siempre que sea posible, usa el ID proveniente de tu base de datos u objeto de datos.

```jsx
{usuarios.map(usuario => (
  <li key={usuario.id}>{usuario.nombre}</li>
))}
```

### Fragmentos con `key`
Si necesitas devolver múltiples elementos por cada iteración sin añadir un contenedor extra, usa `React.Fragment`.

```jsx
<dl>
  {items.map(item => (
    <React.Fragment key={item.id}>
      <dt>{item.term}</dt>
      <dd>{item.description}</dd>
    </React.Fragment>
  ))}
</dl>
```

---

## 🚀 Patrones Avanzados

### Extraer componentes en listas
Mantén la legibilidad extrayendo la lógica del elemento individual a su propio componente. La `key` debe ir en el nivel donde se realiza el `.map()`.

```jsx
function Lista({ items }) {
  return (
    <ul>
      {items.map(item => <ItemComponent key={item.id} item={item} />)}
    </ul>
  );
}
```

### Filtrado y Transformación
Es común filtrar los datos justo antes de mapearlos para renderizar solo lo necesario.

```jsx
{tareas
  .filter(t => !t.completada)
  .map(t => <Tarea key={t.id} {...t} />)
}
```

---

## ⚠️ Consideraciones Importantes

*   **Advertencias**: Si olvidas la `key`, React mostrará una advertencia en la consola y usará el índice por defecto, lo que puede degradar el rendimiento.
*   **Acceso**: La prop `key` no es accesible desde el componente hijo; React la reserva para uso interno. Si necesitas el mismo valor, pásalo con otro nombre (ej: `id={item.id}`).

---

<div align="center">

[⬅️ Volver al Índice](../README.md)

</div>

