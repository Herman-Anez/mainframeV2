
# Métodos Modificadores de Arrays

Los métodos modificadores son aquellos que **mutan el array original**. Es fundamental identificarlos correctamente para evitar efectos laterales (side effects) no deseados en la lógica de nuestra aplicación.

## Gestión de Elementos en los Extremos

### Al Final del Array
*   **`push(...items)`:** Añade uno o más elementos al final del array. Devuelve la **nueva longitud**.
*   **`pop()`:** Elimina el último elemento y lo devuelve. Retorna `undefined` si el array está vacío.

### Al Inicio del Array
*   **`unshift(...items)`:** Añade uno o más elementos al inicio del array. Devuelve la **nueva longitud**.
*   **`shift()`:** Elimina el primer elemento y lo devuelve.

> [!NOTE]
> **Rendimiento:** `shift()` y `unshift()` son generalmente más lentos que `push()` y `pop()`, ya que requieren reindexar todos los elementos restantes del array tras la operación.

---

## El Método Multipropósito: `splice()`

`splice(indice, cantidadAEliminar, ...itemsAAgregar)` es la herramienta más versátil para modificar un array en cualquier posición.

1.  **Eliminación:** Borra `cantidadAEliminar` elementos desde el `indice` indicado.
2.  **Inserción:** Inserta `itemsAAgregar` en la posición especificada.
3.  **Retorno:** Devuelve un array con los elementos que fueron eliminados.

**Casos de uso comunes:**
*   **Inserción pura:** Pasar `cantidadAEliminar = 0`.
*   **Eliminación pura:** No pasar elementos adicionales para agregar.
*   **Índices negativos:** Permiten contar posiciones desde el final del array.

```javascript
const arr = [1, 2, 3, 4, 5];

// Elimina 2 elementos desde el índice 2 (3 y 4)
arr.splice(2, 2); 
// Resultado: arr = [1, 2, 5]

// Inserta 'a' y 'b' en el índice 1 sin eliminar nada
arr.splice(1, 0, 'a', 'b'); 
// Resultado: arr = [1, 'a', 'b', 2, 5]
```

---

## Relleno y Copia Interna

*   **`fill(valor, inicio?, fin?)`:** Rellena los índices desde `inicio` hasta `fin` (exclusivo) con un valor estático.
*   **`copyWithin(target, start, end?)`:** Copia una porción del propio array a otra posición dentro de sí mismo, sobrescribiendo el contenido existente.

```javascript
const data = [1, 2, 3, 4, 5];
data.copyWithin(0, 3); 
// Resultado: [4, 5, 3, 4, 5] (Copia desde el índice 3 al inicio)
```

---

## Ordenamiento y Reversa

*   **`sort(fnComparacion?)`:** Ordena los elementos *in-place*. 
    *   *Por defecto:* Convierte los elementos a strings y los compara según su valor UTF-16.
    *   *Orden numérico:* Requiere una función de comparación: `(a, b) => a - b`.
*   **`reverse()`:** Invierte el orden de los elementos del array *in-place*.

```javascript
const nums = [3, 1, 10];

nums.sort(); 
// Resultado: [1, 10, 3] (Orden léxico por defecto)

nums.sort((a, b) => a - b); 
// Resultado: [1, 3, 10] (Orden numérico correcto)
```

---

## Consideraciones sobre Inmutabilidad

> [!WARNING]
> Todos los métodos mencionados en este archivo modifican directamente el objeto original. Si tu arquitectura requiere inmutabilidad (muy común en frameworks como React), asegúrate de crear una copia del array antes de aplicar estos métodos utilizando técnicas como el operador spread (`[...]`) o el método `slice()`.