
# reconciliation.md

Concepto

La reconciliación es el algoritmo que React utiliza para comparar dos árboles del Virtual DOM y determinar qué cambios aplicar al DOM real.
Algoritmo de diffing (diferenciación)

React hace dos suposiciones principales para lograr un algoritmo O(n) (lineal) en lugar de O(n³):

- Dos elementos de diferente tipo producirán árboles diferentes. React destruye el primero y crea el nuevo desde cero.

- El atributo key permite identificar elementos que se mueven entre renders.

Reglas del algoritmo

## Comparación de nodos raíz

- Tipos diferentes (ej. <div> → <span>): React desmonta el árbol antiguo y monta el nuevo. Todos los componentes hijos se destruyen (se ejecutan efectos de limpieza) y se crean nuevos.

```jsx
// Antes
<div><Counter /></div>
// Después
<span><Counter /></span>
// Resultado: Counter se desmonta y remonta (pierde su estado interno)
```

- Mismo tipo (ej. <div> → <div>): React actualiza los atributos del elemento y luego recorre los hijos recursivamente.

## Comparación de elementos del mismo tipo

Cuando el tipo es el mismo, React actualiza las props del elemento existente para que coincidan con el nuevo. Luego recorre los hijos.

## Comparación de listas (importancia de key)

Sin key, React usa un algoritmo ingenuo que puede ser ineficiente. Con key, React puede reordenar, insertar y eliminar elementos de manera óptima.

```jsx
// Sin key (ineficiente)
<ul>
  <li>Ana</li>
  <li>Luis</li>
</ul>
// Después de invertir
<ul>
  <li>Luis</li>
  <li>Ana</li>
</ul>
// React destruye los dos li y crea otros nuevos (costoso)

// Con key
<ul>
  <li key="ana">Ana</li>
  <li key="luis">Luis</li>
</ul>
// React solo reordena los nodos existentes (eficiente)
```

¿Qué pasa con el estado durante la reconciliación?

- Si un componente se mantiene (mismo tipo, misma posición), React conserva su estado.

- Si un componente se elimina, se destruye su estado.

- Para forzar la reinicialización del estado, usa la key diferente.

```jsx
// Reiniciar estado de un formulario cambiando la key
const [resetKey, setResetKey] = useState(0);
<Form key={resetKey} /> // Cambiar resetKey para reiniciar el formulario
```

Ciclo de vida de la reconciliación (versión simplificada)

- Render (crea Virtual DOM)

- Diff (compara con versión anterior)

- Commit (aplica cambios al DOM real)

- Efectos (ejecuta useEffect, useLayoutEffect)

Algoritmo de reconciliación y Fibers (React 16+)

React 16 introdujo Fibers (re-arquitectura) que permite:

- Pausar, reanudar y priorizar el trabajo.

- Dividir la reconciliación en unidades de trabajo (frames).

- Hacer que el renderizado no bloquee el hilo principal.

Buenas prácticas para ayudar a la reconciliación

- Usa key únicas y estables (no índices de array si la lista es dinámica).

- No cambies innecesariamente el tipo de un componente raíz.

- Prefiere if condicional a display: none si el componente es costoso (así React lo desmonta).

Depuración de reconciliación

- React DevTools → Highlight updates cuando se renderizan componentes.

- why-did-you-render librería para detectar re-renderizados innecesarios.
