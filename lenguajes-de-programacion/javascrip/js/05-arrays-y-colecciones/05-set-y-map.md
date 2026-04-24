
## Archivo: `05-set-y-map.md`


ES6 introdujo nuevas estructuras de datos eficientes para casos específicos.
Set

Colección de valores únicos, de cualquier tipo, sin claves. Permite inserción, búsqueda y eliminación rápidas (normalmente mejor rendimiento que con arrays para grandes colecciones).
Creación y métodos básicos
```js
const set = new Set([1,2,3,2,1]);
console.log(set); // Set(3) {1,2,3}
set.add(4);
set.has(2); // true
set.delete(3);
set.size; // 3
set.clear();

    add retorna el propio Set, permite encadenamiento.

    has es más rápido que indexOf en arrays cuando hay muchos elementos.

    Convierte a array: [...set] o Array.from(set).
```

### Iteración

### set.forEach(valor => ...)

### for (const valor of set)

    set.keys(), set.values(), set.entries() (estos dos últimos retornan el mismo iterador, con valor como clave y valor).

### Casos de uso

    Eliminar duplicados de un array: [...new Set(arr)].

    Conjuntos para operaciones de álgebra de conjuntos: unión, intersección, diferencia (usando spread y filter).

    Seguimiento de visitas únicas, IDs.

### WeakSet

Similar a Set pero solo acepta objetos y mantiene referencias débiles (si el objeto no tiene otras referencias, puede ser recolectado por el GC).

    No es iterable, no tiene propiedad size.

    Útil para marcar objetos sin prevenir su eliminación (ej. seguimiento de visitas DOM sin fugas de memoria).

### Map

Colección de pares clave-valor donde las claves pueden ser cualquier tipo (objetos, funciones, primitivos). A diferencia de objetos, mantiene el orden de inserción y tiene un mejor rendimiento en inserciones/eliminaciones frecuentes.
Creación y métodos
```js
const map = new Map();
map.set('nombre', 'Ana');
map.set(42, 'edad');
const objKey = { id: 1 };
map.set(objKey, 'datos');
```

### map.get('nombre'); // 'Ana'
map.has(42);       // true
map.size;          // 3
map.delete('edad');
map.clear();

### Iteración

### for (const [clave, valor] of map) (entries por defecto)

### map.forEach((valor, clave) => ...)

    map.keys(), map.values(), map.entries().

### Ventajas sobre objetos

    Las claves no se limitan a strings/symbols; pueden ser objetos.

    Propiedad size fácil de consultar.

    Mejor rendimiento en adiciones/eliminaciones frecuentes.

    No tiene claves heredadas por prototipo, es seguro iterar sin hasOwnProperty.

    Preserva el orden de inserción.

### Conversión con objetos y arrays

    De objeto a Map: new Map(Object.entries(obj)).

    De Map a objeto: Object.fromEntries(map).

    De array de pares a Map: new Map([['a',1], ['b',2]]).

### WeakMap

    Solo acepta objetos como claves y las referencias son débiles.

    No iterable, sin size.

    Ideal para almacenar datos asociados a objetos sin prevenir su recolección (metadatos privados, cachés).

    Uso común: cachear resultados de cálculo para objetos que pueden desaparecer.

---
