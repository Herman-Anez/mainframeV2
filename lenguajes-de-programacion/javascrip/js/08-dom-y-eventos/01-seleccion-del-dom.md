# Selección del DOM

El **DOM (Document Object Model)** es la representación estructural de un documento HTML en forma de árbol. Para interactuar con la página mediante JavaScript, el primer paso es obtener referencias a los nodos (elementos) que deseamos manipular.

---

## Métodos Tradicionales

Estos métodos son parte de las especificaciones más antiguas del DOM, pero siguen siendo extremadamente rápidos y útiles.

| Método | Descripción | Devuelve |
| :--- | :--- | :--- |
| `getElementById(id)` | Busca un elemento por su atributo `id`. | Un elemento o `null`. |
| `getElementsByClassName(class)` | Busca elementos por su clase CSS. | `HTMLCollection` (viva). |
| `getElementsByTagName(tag)` | Busca elementos por su etiqueta (ej. `div`).| `HTMLCollection` (viva). |
| `getElementsByName(name)` | Busca por el atributo `name`. | `NodeList` (viva). |

```javascript
const titulo = document.getElementById('main-title');
const items = document.getElementsByClassName('list-item');
```

---

## Métodos Modernos (Selectores CSS)

Introducidos para unificar la selección bajo la potente sintaxis de los selectores de CSS. Son los métodos más versátiles.

*   **`querySelector(selector)`**: Devuelve el **primer** elemento que coincida con el selector. Si no hay coincidencias, devuelve `null`.
*   **`querySelectorAll(selector)`**: Devuelve todos los elementos que coincidan con el selector.

```javascript
// Selección compleja
const linkActivo = document.querySelector('nav ul li.active > a');

// Selección múltiple
const todosLosBotones = document.querySelectorAll('.btn-primary');
```

---

## HTMLCollection vs NodeList

Es fundamental entender la diferencia entre los tipos de colecciones que devuelven los métodos de selección.

### HTMLCollection (Viva)
Es una colección dinámica. Si el DOM cambia (se añaden o eliminan elementos que coinciden con la búsqueda), la colección se actualiza automáticamente.
> [!WARNING]
> Las `HTMLCollection` no tienen el método `.forEach()`. Debes convertirlas a Array o usar un bucle `for...of`.

### NodeList (Estática)
Es un "snapshot" o captura del estado del DOM en el momento de la consulta. Si el DOM cambia después, la lista no se verá afectada.
> [!TIP]
> Las `NodeList` devueltas por `querySelectorAll` sí implementan el método `.forEach()` de forma nativa en navegadores modernos.

---

## Navegación y Selección Relativa

Una vez seleccionado un elemento, podemos movernos por el árbol del DOM sin necesidad de realizar nuevas búsquedas globales.

### Propiedades de Navegación
*   **Padre:** `parentElement` (más seguro que `parentNode`).
*   **Hijos:** `children` (solo elementos HTML) o `childNodes` (incluye nodos de texto y comentarios).
*   **Hermanos:** `nextElementSibling` / `previousElementSibling`.

### El método `.closest()`
Recorre el DOM hacia arriba (ancestros) hasta encontrar el primer elemento que coincida con el selector CSS proporcionado.
```javascript
const card = boton.closest('.card-container'); // Útil para delegación de eventos
```

---

## Buenas Prácticas

1.  **Cachear Selecciones:** Guardar el resultado de una selección en una variable si se va a usar varias veces. Consultar el DOM es una operación costosa.
2.  **ID vs Clase:** Usa `getElementById` para elementos únicos (rendimiento máximo) y `querySelector` para selecciones complejas o dinámicas.
3.  **Conversión a Array:** Usa el operador spread `[...]` o `Array.from()` cuando necesites usar métodos como `.map()`, `.filter()` o `.reduce()` sobre una colección de elementos.
4.  **Selección Específica:** Limita el ámbito de búsqueda. En lugar de `document.querySelectorAll`, usa `miElementoPadre.querySelectorAll` si sabes dónde están los elementos.

---
[Volver al Índice](../js-index.md)
