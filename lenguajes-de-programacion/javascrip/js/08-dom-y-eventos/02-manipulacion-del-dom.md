## Archivo: `02-manipulacion-del-dom.md`


Manipular el DOM implica crear, modificar o eliminar nodos y sus atributos.
Crear elementos y texto

    document.createElement('tag'): crea un elemento del tipo dado.

    document.createTextNode('texto'): crea un nodo de texto. También se puede simplemente asignar a textContent o usar innerHTML.

```js
const p = document.createElement('p');
p.textContent = 'Hola mundo';
```

### Insertar nodos en el árbol

    parent.appendChild(nodo): añade como último hijo.

    parent.insertBefore(nuevo, referencia): inserta antes del nodo referencia existente.

    parent.replaceChild(nuevo, viejo): reemplaza un hijo.

    element.remove(): elimina el propio elemento.

    parent.removeChild(hijo): elimina un hijo.

Métodos modernos (más flexibles):

    parent.append(...nodosOstrings): inserta al final, acepta múltiples nodos y texto.

    parent.prepend(...nodosOstrings): inserta al principio.

    element.before(...): hermano anterior.

    element.after(...): hermano posterior.

    element.replaceWith(...): reemplaza el elemento.

```js
const div = document.createElement('div');
div.append('Texto', document.createElement('br'), 'más texto');
```

### Manipulación de contenido

    element.textContent: obtiene/establece el texto plano de todo el subárbol. Más seguro y eficiente que innerHTML si no necesitas HTML.

    element.innerHTML: obtiene/establece el contenido HTML como string. ¡Cuidado con XSS! No insertar contenido de usuario sin sanitizar.

    element.outerHTML: incluye el propio elemento en la cadena HTML.

    element.innerText: similar a textContent pero tiene en cuenta estilos y devuelve solo el texto visible; puede ser más lento.

### Atributos y propiedades

    Atributo HTML: definido en la etiqueta, accedible con getAttribute('nombre') y setAttribute('nombre', 'valor'). Siempre son strings.

    Propiedad de DOM: los elementos tienen propiedades en js que reflejan algunos atributos, pero pueden tener tipos distintos (ej. checked es booleano, value de input es el actual).

```js
input.getAttribute('value'); // valor inicial
input.value; // valor actual
```

    element.hasAttribute('attr'), element.removeAttribute('attr').

    data-* atributos: acceso mediante element.dataset.propiedad.

    Clases: element.classList permite add('clase'), remove('clase'), toggle('clase'), contains('clase'). Preferible a manipular className.

### Estilos

    element.style.propiedad = 'valor' para estilos en línea. Las propiedades se escriben en camelCase: backgroundColor.

    element.style.cssText para asignar varias a la vez.

    getComputedStyle(element) devuelve el objeto de estilos computados (solo lectura).

```js
const estilos = window.getComputedStyle(elemento);
console.log(estilos.marginTop);
```

### Fragmentos y rendimiento

Si necesitas hacer muchas inserciones, usa un DocumentFragment para evitar múltiples reflows. El fragmento se construye en memoria y luego se inserta de una vez.
```js
const frag = document.createDocumentFragment();
for (let i=0; i<1000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  frag.appendChild(li);
}
ul.appendChild(frag);
```

### Clonar y eliminar

    element.cloneNode(true): copia profunda; false copia superficial.

    element.remove(): desaparece el nodo del DOM.

### Cuidado con XSS

Nunca uses innerHTML o outerHTML con contenido no confiable. Utiliza textContent o sanitizadores como DOMPurify.