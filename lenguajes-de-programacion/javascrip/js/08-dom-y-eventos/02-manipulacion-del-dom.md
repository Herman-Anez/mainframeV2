# Manipulación del DOM

Manipular el DOM implica crear, modificar o eliminar nodos, así como gestionar sus atributos y estilos.

---

## Crear elementos y texto

- **`document.createElement('tag')`**: Crea un nuevo elemento del tipo especificado.
- **`document.createTextNode('texto')`**: Crea un nodo de texto. Alternativamente, se puede asignar texto directamente a `textContent`.

```js
const p = document.createElement('p');
p.textContent = 'Hola mundo';
```

---

## Insertar y eliminar nodos en el árbol

### Métodos clásicos
- **`parent.appendChild(nodo)`**: Añade el nodo como el último hijo del padre.
- **`parent.insertBefore(nuevo, referencia)`**: Inserta el nuevo nodo antes del nodo de referencia existente.
- **`parent.replaceChild(nuevo, viejo)`**: Reemplaza un nodo hijo por otro.
- **`parent.removeChild(hijo)`**: Elimina un nodo hijo específico.

### Métodos modernos (más flexibles)
- **`parent.append(...nodosOstrings)`**: Inserta al final; acepta múltiples nodos y strings directamente.
- **`parent.prepend(...nodosOstrings)`**: Inserta al principio del contenedor.
- **`element.before(...nodes)`**: Inserta como hermano anterior.
- **`element.after(...nodes)`**: Inserta como hermano posterior.
- **`element.replaceWith(...nodes)`**: Reemplaza el elemento actual con los nuevos nodos/strings.
- **`element.remove()`**: Elimina el propio elemento del DOM.

```js
const div = document.createElement('div');
div.append('Texto', document.createElement('br'), 'más texto');
```

---

## Manipulación de contenido

- **`element.textContent`**: Obtiene o establece el texto plano de todo el subárbol. Es más seguro y eficiente que `innerHTML` si no se requiere procesar HTML.
- **`element.innerHTML`**: Obtiene o establece el contenido HTML como una cadena. 
- **`element.outerHTML`**: Incluye al propio elemento en la representación HTML.
- **`element.innerText`**: Similar a `textContent`, pero respeta el estilo CSS (solo devuelve texto visible) y puede ser más lento debido al cálculo de diseño (*layout*).

> [!CAUTION]
> **Seguridad XSS:** Nunca insertes contenido generado por el usuario directamente mediante `innerHTML`. Utiliza `textContent` o sanitiza los datos primero.

---

## Atributos y propiedades

- **Atributos HTML:** Definidos en el marcado, se gestionan con `getAttribute('nombre')`, `setAttribute('nombre', 'valor')`, `hasAttribute()` y `removeAttribute()`. Siempre operan con strings.
- **Propiedades del DOM:** Son propiedades del objeto JavaScript que reflejan atributos pero pueden tener tipos diferentes (ej: `checked` es booleano, `value` refleja el valor actual del input).

```js
input.getAttribute('value'); // Valor inicial definido en HTML
input.value;                 // Valor actual en tiempo de ejecución
```

- **`data-*` atributos:** Se acceden de forma sencilla mediante `element.dataset.propiedad`.
- **Clases:** Usa `element.classList` para una gestión limpia: `.add()`, `.remove()`, `.toggle()` y `.contains()`. Evita manipular `className` directamente como un string.

---

## Estilos

- **Estilos en línea:** Se modifican mediante `element.style.propiedad = 'valor'`. Las propiedades usan *camelCase* (ej: `backgroundColor`).
- **Asignación múltiple:** `element.style.cssText` permite definir varias reglas a la vez como un string.
- **Lectura de estilos:** `window.getComputedStyle(element)` devuelve un objeto con todos los estilos finales aplicados (lectura únicamente).

```js
const estilos = window.getComputedStyle(elemento);
console.log(estilos.marginTop);
```

---

## Fragmentos y rendimiento

> [!TIP]
> Si necesitas realizar múltiples inserciones de una sola vez, utiliza un `DocumentFragment` para evitar múltiples *reflows* (re-cálculos de diseño) del navegador. El fragmento se construye en memoria y se vuelca al DOM en una única operación.

```js
const frag = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  frag.appendChild(li);
}
ul.appendChild(frag);
```

---

## Clonar y eliminar

- **`element.cloneNode(true)`**: Realiza una copia profunda (incluye hijos); `false` realiza una copia superficial.
- **`element.remove()`**: Elimina el nodo del árbol de forma directa.

---

## Cuidado con XSS

> [!IMPORTANT]
> Mantén la integridad de tu aplicación evitando el uso de `innerHTML` con contenido no confiable. Si es estrictamente necesario, utiliza librerías de sanitización como **DOMPurify**.
---
[back](../index)
