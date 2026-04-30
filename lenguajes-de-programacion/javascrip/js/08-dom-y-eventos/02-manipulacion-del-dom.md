# Manipulación del DOM

La manipulación del DOM consiste en crear, modificar o eliminar nodos, así como gestionar sus atributos, clases y estilos en tiempo de ejecución para crear interfaces interactivas.

---

## Creación de Elementos

*   **`document.createElement('etiqueta')`**: Crea un nuevo nodo de elemento.
*   **`document.createTextNode('texto')`**: Crea un nodo de texto puro.

```javascript
const nuevoParrafo = document.createElement('p');
nuevoParrafo.textContent = 'Este es un párrafo dinámico.';
```

---

## Inserción y Eliminación de Nodos

### Métodos Modernos (Recomendados)
Son más flexibles y permiten insertar múltiples elementos o cadenas de texto simultáneamente.

*   **`parent.append()`**: Inserta al final del contenedor.
*   **`parent.prepend()`**: Inserta al principio del contenedor.
*   **`element.before()` / `element.after()`**: Inserta como hermano anterior o posterior.
*   **`element.replaceWith()`**: Reemplaza el elemento actual por otro.
*   **`element.remove()`**: Elimina el propio elemento del DOM.

### Métodos Tradicionales
*   **`appendChild()`**: Inserta al final (solo un nodo).
*   **`insertBefore(nuevo, referencia)`**: Inserta antes de un hijo específico.
*   **`removeChild()`**: Elimina un hijo específico.

---

## Gestión de Contenido

| Propiedad | Descripción | Seguridad |
| :--- | :--- | :--- |
| **`textContent`** | Obtiene/establece el texto plano de un nodo y sus descendientes. | **Seguro** (no procesa HTML). |
| **`innerHTML`** | Obtiene/establece el contenido en formato HTML. | **Peligroso** (vulnerable a XSS). |
| **`innerText`** | Similar a `textContent` pero respeta estilos CSS (texto visible). | **Seguro**, pero más lento. |

> [!CAUTION]
> **Seguridad XSS:** Nunca utilices `innerHTML` con datos que provengan de un usuario. Prefiere siempre `textContent` o manipulación directa de nodos para evitar la ejecución de scripts maliciosos.

---

## Atributos y Clases

### Atributos
*   **`setAttribute('attr', 'valor')`** / **`getAttribute('attr')`**: Gestión de atributos HTML.
*   **`dataset`**: Acceso directo a atributos `data-*` (ej: `data-id` -> `el.dataset.id`).

### Gestión de Clases (`classList`)
Es la forma preferida de manipular estilos CSS mediante clases, evitando errores comunes al concatenar cadenas.

```javascript
const el = document.querySelector('.card');

el.classList.add('highlight');     // Añade clase
el.classList.remove('hidden');     // Elimina clase
el.classList.toggle('active');     // Alterna clase
el.classList.contains('active');   // Verifica si existe (devuelve booleano)
```

---

## Estilos CSS

Para modificar estilos directamente desde JavaScript:

1.  **Propiedad `.style`**: Modifica estilos en línea. Usa *camelCase* para propiedades con guiones (ej: `backgroundColor`).
2.  **`window.getComputedStyle(elemento)`**: Método de **solo lectura** para obtener el valor final de un estilo aplicado por CSS externo.

```javascript
el.style.fontSize = '20px';
el.style.cssText = 'color: blue; margin: 10px;'; // Asignación múltiple
```

---

## Rendimiento: `DocumentFragment`

Modificar el DOM de forma repetida es costoso porque obliga al navegador a recalcular el diseño (*reflow*).

> [!TIP]
> Si vas a insertar muchos elementos (ej: una lista de 100 items), utiliza un **`DocumentFragment`**. Es un contenedor ligero en memoria que se vuelca al DOM en una sola operación de renderizado.

```javascript
const fragmento = document.createDocumentFragment();

datos.forEach(d => {
  const li = document.createElement('li');
  li.textContent = d.texto;
  fragmento.append(li); // Inserción en memoria
});

listaUl.append(fragmento); // Una única inserción real en el DOM
```

---

## Clonación de Nodos

Usa `cloneNode(deep)` para duplicar elementos.
*   **`true`**: Clonación profunda (incluye hijos y contenido).
*   **`false`**: Clonación superficial (solo la etiqueta y sus atributos).

---
[Volver al Índice](../js-index.md)
