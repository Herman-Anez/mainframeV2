
## Archivo: `02-metodos-modificadores.md`


Estos métodos mutan el array original. Es importante reconocerlos para evitar efectos laterales no deseados.
Agregar y eliminar al final

    push(...items): añade uno o más elementos al final y devuelve la nueva longitud.

    pop(): elimina el último elemento y lo devuelve (o undefined si el array está vacío).

### Agregar y eliminar al inicio

    unshift(...items): añade al inicio, devuelve nueva longitud.

    shift(): elimina el primer elemento y lo devuelve.

Coste: shift y unshift deben reindexar todos los elementos, por lo que son más lentos que push/pop.
splice(indice, cantidadAEliminar, ...itemsAAgregar)

Método todoterreno para modificar un array en cualquier posición.

    Elimina cantidadAEliminar elementos desde indice.

    Inserta itemsAAgregar en esa misma posición.

    Devuelve un array con los elementos eliminados.

    Con cantidadAEliminar = 0 se usa como inserción pura.

    Con ...itemsAAgregar vacío se usa como eliminación pura.

    Los índices negativos cuentan desde el final.

```js
const arr = [1,2,3,4,5];
arr.splice(2, 2); // elimina 3,4 → arr = [1,2,5]
arr.splice(1, 0, 'a', 'b'); // arr = [1,'a','b',2,5]
```

### Relleno y copia dentro del array

    fill(valor, inicio?, fin?): rellena los índices de inicio a fin (exclusivo) con valor. Si no se pasan, rellena todo. Muta el array.

    copyWithin(target, start, end?): copia una porción del propio array a otra posición, sobrescribiendo. Útil para desplazamientos. Muta el array.

```js
[1,2,3,4,5].copyWithin(0, 3); // [4,5,3,4,5]
```

### Ordenamiento y reversa

    sort(fnComparacion?): ordena in-place y devuelve el array. Por defecto, convierte elementos a string y compara por código UTF-16. Para orden numérico pasar (a, b) => a - b.

    reverse(): invierte el orden in-place.

```js
const nums = [3,1,10];
nums.sort(); // [1, 10, 3] (orden léxico)
nums.sort((a,b) => a - b); // [1,3,10]
```

### Otros

    flat() y flatMap() no son mutadores (devuelven nuevo array, ver en otra sección), pero se pueden usar.

### Importante

Todos estos métodos modifican el array original. Si se necesita inmutabilidad, se deben hacer copias previas (con spread, slice, etc.).