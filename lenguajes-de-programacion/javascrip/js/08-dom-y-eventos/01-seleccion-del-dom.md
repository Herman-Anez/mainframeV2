# Selección del DOM

El **DOM (Document Object Model)** es la representación en árbol de los documentos HTML/XML. Para interactuar con él, primero debemos seleccionar los nodos correspondientes.

---

## Métodos clásicos del objeto `document`

### `getElementById(id)`

Devuelve un único elemento (o `null`) cuyo atributo `id` coincida exactamente. Es sensible a mayúsculas y es el método de selección más rápido.

```js
const el = document.getElementById('main');
```

### `getElementsByClassName(className)`

Devuelve una **HTMLCollection "viva"** de elementos con la clase especificada. Se actualiza automáticamente si el DOM cambia.

```js
const items = document.getElementsByClassName('item');
```

### `getElementsByTagName(tagName)`

Devuelve una **HTMLCollection "viva"** de elementos con el nombre de etiqueta proporcionado.

```js
const divs = document.getElementsByTagName('div');
```

### `getElementsByName(name)`

Devuelve una **NodeList "viva"** de elementos con el atributo `name` dado (comúnmente usado en formularios).

```js
const radios = document.getElementsByName('genero');
```

---

## Métodos modernos: `querySelector` y `querySelectorAll`

Estos métodos utilizan selectores CSS, lo que los hace mucho más flexibles y potentes.

- **`querySelector(selector)`**: Devuelve el **primer** elemento que coincida con el selector o `null` si no hay coincidencias.
- **`querySelectorAll(selector)`**: Devuelve una **NodeList estática** (no viva) de todos los elementos que coinciden.

```js
const primerItem = document.querySelector('.item');
const todosItems = document.querySelectorAll('.item');
const input = document.querySelector('#form input[type="text"]');
```

> [!NOTE]
> Las **NodeList estáticas** no se actualizan si el DOM cambia después de la consulta. Se pueden iterar directamente con `.forEach()` (en navegadores modernos), pero no son arrays completos; para usar métodos como `.map()` o `.filter()`, deben convertirse con `Array.from()` o el operador spread `[...]`.

---

## Diferencias entre colecciones vivas y estáticas

- **HTMLCollection (viva):** Refleja cambios dinámicos en el DOM inmediatamente. No dispone del método `.forEach()` nativo (aunque se puede iterar con un bucle `for` clásico).
- **NodeList estática:** Es un "snapshot" del momento de la consulta, lo que la hace más predecible. `querySelectorAll` devuelve una lista estática, mientras que propiedades como `childNodes` devuelven una NodeList viva.

---

## Selección relativa a un elemento

Una vez que ya tenemos una referencia a un elemento, podemos realizar búsquedas dentro de su subárbol o navegar por sus nodos adyacentes:

- **Búsqueda interna:** `element.querySelector()` / `element.querySelectorAll()` / `element.getElementsBy...`
- **Propiedades de navegación:**
    - `parentNode` / `parentElement`
    - `children` / `childNodes`
    - `firstChild` / `lastChild`
    - `nextSibling` / `previousSibling`
    - `closest(selector)`: Recorre hacia arriba (ancestros) buscando la primera coincidencia con el selector. Es extremadamente útil para la **delegación de eventos**.

---

## Selección de elementos especiales

- **Directos:** `document.body`, `document.head`, `document.documentElement` (`<html>`).
- **Colecciones:** `document.forms`, `document.images`, `document.links`, etc.

---

## Buenas prácticas

- **Flexibilidad:** Prefiere `querySelector` para búsquedas complejas o basadas en selectores CSS.
- **Rendimiento:** Usa `getElementById` cuando solo necesites seleccionar un elemento por su ID único.
- **Funcionalidad:** Convierte las `NodeList` a array si necesitas usar métodos funcionales: `[...lista]` o `Array.from(lista)`.
- **Optimización:** Guarda referencias a elementos seleccionados frecuentemente en variables para evitar reconsultar el DOM innecesariamente.

---
[back](../index)
