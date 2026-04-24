
## Archivo: `01-seleccion-del-dom.md`


El DOM (Document Object Model) es la representación en árbol de los documentos HTML/XML. Para interactuar con él, primero hay que seleccionar los nodos.
Métodos clásicos del objeto document
getElementById

Devuelve un único elemento (o null) cuyo atributo id coincida exactamente. Sensible a mayúsculas. Método más rápido.
```js
const el = document.getElementById('main');
```

### getElementsByClassName

Devuelve una HTMLCollection viva de elementos con la clase especificada. Se actualiza automáticamente si el DOM cambia.
```js
const items = document.getElementsByClassName('item');
```

### getElementsByTagName

Devuelve HTMLCollection viva de elementos con el nombre de etiqueta dado.
```js
const divs = document.getElementsByTagName('div');
```

### getElementsByName

Devuelve NodeList viva de elementos con name dado (muy usado en formularios).
```js
const radios = document.getElementsByName('genero');
```

### Métodos modernos: querySelector y querySelectorAll

Usan selectores CSS, mucho más flexibles.

    querySelector(selector): devuelve el primer elemento que coincida o null.

    querySelectorAll(selector): devuelve una NodeList estática (no viva) de todos los elementos que coinciden.

```js
const primerItem = document.querySelector('.item');
const todosItems = document.querySelectorAll('.item');
const input = document.querySelector('#form input[type="text"]');
```

Las NodeList estáticas no se actualizan si el DOM cambia después de la consulta. Se pueden iterar con forEach (moderno), pero no son arrays completos; hay que convertirlos con Array.from para usar map, filter, etc.
Diferencias entre colecciones vivas y estáticas

    HTMLCollection (viva): refleja cambios dinámicos. No tiene forEach (aunque puede usarse con índices).

    NodeList estática: snapshot del momento, más predecible. querySelectorAll la devuelve; childNodes devuelve una NodeList viva.

### Selección relativa a un elemento

Una vez obtenido un elemento, podemos buscar dentro de él:

### element.querySelector/All

    element.getElementsBy...

    Propiedades de navegación: parentNode, children, firstChild, lastChild, nextSibling, previousSibling, closest(selector).

closest recorre hacia arriba (ancestros) buscando la primera coincidencia, muy práctico para delegación de eventos.
Selección de elementos especiales

### document.body, document.head, document.documentElement (html)

### document.forms, document.images, document.links, etc. (colecciones HTML)

### Buenas prácticas

    Prefiere querySelector para búsquedas complejas.

    Usa getElementById cuando solo necesites un ID por rendimiento.

    Convierte NodeList a array si necesitas métodos funcionales: [...lista] o Array.from.

    Guarda referencias a elementos seleccionados frecuentemente para no reconsultar el DOM.

---
