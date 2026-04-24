# Estructuras de Datos: Set y Map

ES6 introdujo nuevas estructuras de datos diseñadas para manejar colecciones de forma más eficiente y flexible que los objetos y arrays tradicionales en casos de uso específicos.

---

## Set

Un **Set** es una colección de **valores únicos** de cualquier tipo. A diferencia de un array, no permite elementos duplicados y optimiza las operaciones de búsqueda.

### Creación y Métodos Básicos
Permite realizar inserciones, búsquedas y eliminaciones rápidas.

```javascript
const miSet = new Set([1, 2, 3, 2, 1]);
console.log(miSet); // Set(3) {1, 2, 3}

miSet.add(4);       // Añade un elemento (retorna el Set, permite encadenamiento)
miSet.has(2);       // true (búsqueda eficiente)
miSet.delete(3);    // Elimina el elemento
miSet.size;         // 3 (propiedad para consultar el tamaño)
miSet.clear();      // Vacía el Set por completo
```

> [!TIP]
> **Eliminar duplicados:** La forma más rápida de limpiar un array de duplicados es: `[...new Set(arrayOriginal)]`.

### Iteración en Set
*   `for (const valor of miSet)`
*   `miSet.forEach(valor => ...)`
*   Métodos de iteradores: `miSet.keys()`, `miSet.values()`, `miSet.entries()`.

### Casos de Uso Comunes
*   **Álgebra de conjuntos:** Realizar uniones, intersecciones y diferencias de forma sencilla combinando spread y filtros.
*   **Seguimiento de IDs únicos:** Garantizar que no se procese dos veces el mismo identificador.

### WeakSet
Similar a `Set`, pero con restricciones importantes:
*   **Solo acepta objetos** como valores.
*   **Referencias débiles:** Si el objeto guardado no tiene otras referencias, puede ser recolectado por el Garbage Collector (GC).
*   **No iterable:** No tiene propiedad `size` ni se puede recorrer. Útil para "marcar" objetos sin generar fugas de memoria.

---

## Map

Un **Map** es una colección de pares **clave-valor** donde las claves pueden ser de cualquier tipo (objetos, funciones o primitivos). A diferencia de los objetos literales, mantiene el orden de inserción.

### Creación y Métodos
```javascript
const mapa = new Map();

mapa.set('nombre', 'Ana');
mapa.set(42, 'edad');

const objKey = { id: 1 };
mapa.set(objKey, 'metadatos');

mapa.get('nombre'); // 'Ana'
mapa.has(42);       // true
mapa.size;          // 3
mapa.delete(objKey);
```

### Ventajas sobre Objetos Literales
1.  **Claves flexibles:** Las claves no se limitan a Strings o Symbols.
2.  **Orden garantizado:** Preserva el orden cronológico de inserción durante la iteración.
3.  **Tamaño directo:** La propiedad `size` permite conocer el número de elementos instantáneamente.
4.  **Rendimiento:** Optimizado para escenarios de adiciones y eliminaciones frecuentes.
5.  **Seguridad:** No hereda claves del prototipo, evitando colisiones accidentales.

### Iteración en Map
*   `for (const [clave, valor] of mapa)`: Recorre los pares (comportamiento por defecto).
*   `mapa.forEach((valor, clave) => ...)`: Sigue el patrón estándar de callbacks.
*   `mapa.keys()`, `mapa.values()`, `mapa.entries()`.

### Conversión de Datos
*   **Objeto a Map:** `new Map(Object.entries(obj))`
*   **Map a Objeto:** `Object.fromEntries(mapa)`
*   **Array de pares a Map:** `new Map([['a', 1], ['b', 2]])`

### WeakMap
Versión del Map optimizada para la gestión de memoria:
*   **Claves únicamente objetos:** Solo se pueden usar objetos como claves.
*   **Referencias débiles:** No previene la recolección de basura de sus claves si estas no son accesibles desde otro lugar.
*   **No iterable:** Ideal para almacenar datos privados o cachés de resultados asociados a objetos cuyo ciclo de vida es incierto.
