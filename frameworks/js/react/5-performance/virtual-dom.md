
📄 virtual-dom.md

Concepto

El Virtual DOM es una representación liviana del DOM real en memoria, como un árbol de objetos JavaScript. React lo usa para optimizar las actualizaciones de la interfaz.

¿Por qué existe?

Manipular el DOM real es lento porque cada cambio puede provocar reflows y repaints. El Virtual DOM permite agrupar cambios y aplicar la mínima cantidad de mutaciones al DOM real.
Algoritmo básico de React

- Render inicial: React crea un árbol Virtual DOM a partir del JSX.

- Actualización: Cuando cambia el estado o las props, React crea un nuevo árbol Virtual DOM.

- Diffing: React compara el nuevo árbol con el anterior (algoritmo de diferenciación).

- Reconciliación: React calcula el conjunto mínimo de operaciones necesarias para actualizar el DOM real.

- Commit: React aplica esos cambios al DOM real.

Ejemplo conceptual

```jsx
// Virtual DOM simplificado (no es exactamente así)
const vDOM = {
  type: 'div',
  props: { className: 'container' },
  children: [
    { type: 'h1', props: {}, children: ['Hola'] },
    { type: 'button', props: { onClick: fn }, children: ['Click'] }
  ]
};
```

Ventajas del Virtual DOM

- Rendimiento: evita operaciones costosas del DOM real.

- Abstracción: React puede generar DOM para web, Native para móviles, etc.

- Declarativo: no necesitas manipular el DOM manualmente.

Desventajas

- No es el más rápido posible: para apps con actualizaciones ultra frecuentes (animaciones 60fps), puede haber soluciones más óptimas (manipulación directa del DOM, WebGL, etc.).

- Costo de memoria: mantener dos árboles virtuales consume RAM.

¿Es realmente más rápido?

Depende. Para la mayoría de aplicaciones, el Virtual DOM es suficientemente rápido. El verdadero beneficio es la simplicidad conceptual y la consistencia.
Comparativa con otros enfoques

- Manipulación manual del DOM: más rápido en manos expertas, pero propenso a errores y código verboso.

- Svelte: compila en tiempo de build, no usa Virtual DOM, actualiza el DOM directamente. Para muchos casos es más rápido.

- Solid: similar a Svelte, pero con sintaxis similar a React.

Conceptos erróneos comunes

- "El Virtual DOM es más rápido que el DOM real" → Falso. El Virtual DOM es una capa de abstracción; el DOM real sigue siendo la base. La optimización está en minimizar las operaciones.

- "React usa Virtual DOM para todo" → React también puede usar dangerouslySetInnerHTML o findDOMNode (legado).

Buenas prácticas

- No pienses demasiado en el Virtual DOM; confía en React, pero evita patrones que causen re-renderizados masivos (ej. modificar el estado raíz frecuentemente).

- Usa key correctamente para ayudar al algoritmo de diffing.
