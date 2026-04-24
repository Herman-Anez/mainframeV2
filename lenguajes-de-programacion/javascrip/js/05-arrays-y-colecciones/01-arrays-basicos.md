
## Archivo: `01-arrays-basicos.md`


Los arrays en js son objetos de alto nivel que permiten almacenar colecciones ordenadas de elementos. Internamente son objetos con claves numéricas (índices) y una propiedad length especial.
Creación
```js
const arr1 = [1, 2, 3];          // literal
const arr2 = new Array(1, 2, 3); // constructor (no recomendado si se pasa un solo número, crea array con ese tamaño)
const arr3 = Array.of(5);        // crea [5] (soluciona ambigüedad)
const arr4 = Array.from('hola'); // convierte iterable/array-like en array: ['h','o','l','a']
```

### Índices y propiedad length

    Los índices son enteros no negativos. Se puede acceder con arr[indice].

    length es siempre uno más que el mayor índice existente (no es el número real de elementos si hay huecos).

    Modificar length directamente trunca o extiende el array. Si se asigna un valor más pequeño, se eliminan elementos sobrantes. Si se hace más grande, los huecos se llenan con empty (comportamiento de índice inexistente).

```js
const a = [10, 20, 30];
a.length = 2;      // ahora es [10, 20]
a.length = 5;      // [10, 20, , , ] -> los últimos tres son empty
console.log(a[3]); // undefined
```

### Arrays dispersos (sparse arrays)

Los arrays pueden tener "agujeros" si se asignan índices no consecutivos.
```js
const sparse = [];
sparse[100] = 'a';
console.log(sparse.length); // 101
```

Los métodos que iteran (forEach, map, etc.) ignoran los índices vacíos. Los bucles for tradicionales acceden a ellos devolviendo undefined. El operador in devuelve false para esos índices.
Detectar un array

Dado que typeof devuelve "object", la forma correcta es:

    Array.isArray(valor) (ES5) – recomendado.

    valor instanceof Array (falla entre iframes o dominios diferentes).

### Iteración básica

    for (let i = 0; i < arr.length; i++) – clásico, pero maneja índices manualmente.

    for...of – recorre valores (recomendado).

    for...in – recorre índices como strings (incluye propiedades no numéricas si las hay, no recomendado para arrays).

    Métodos funcionales como forEach.

### Comparación y mutabilidad

Los arrays son objetos, por lo que dos arrays con el mismo contenido son diferentes referencias. La comparación por valor requiere iterar manualmente o usar JSON.stringify (limitado).