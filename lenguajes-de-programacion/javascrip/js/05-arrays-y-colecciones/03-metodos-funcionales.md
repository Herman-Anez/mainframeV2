
## Archivo: `03-metodos-funcionales.md`


Estos métodos no modifican el array original (a excepción de forEach que no devuelve nada, pero puede modificar elementos si el callback lo hace). Son la base de la programación funcional con arrays.
forEach(fn)

Ejecuta fn(elemento, indice, array) para cada elemento. Ignora índices vacíos. No devuelve nada, no se puede encadenar. Útil para efectos secundarios controlados.
```js
[1,2,3].forEach(n => console.log(n));
```

No se puede detener con break; si se necesita interrumpir, usar for...of o some/every.
map(fn)

Transforma cada elemento y devuelve un nuevo array con los resultados.
```js
const dobles = [1,2,3].map(n => n * 2); // [2,4,6]
```

La longitud del nuevo array siempre es igual a la original, aunque los índices vacíos permanecen vacíos.
filter(fn)

Devuelve un nuevo array con los elementos para los que fn devuelve un valor truthy.
```js
const mayores = [5, 10, 3, 15].filter(n => n > 7); // [10,15]
```

Si ningún elemento pasa, devuelve array vacío.
reduce(fn, valorInicial?) y reduceRight

Acumula los elementos en un solo valor. fn recibe (acumulador, elemento, indice, array).
```js
const suma = [1,2,3,4].reduce((acc, n) => acc + n, 0); // 10
```

    Si no se da valorInicial, el primer elemento se usa como acumulador inicial y la iteración empieza desde el segundo.

    reduceRight itera de derecha a izquierda.

### find(fn) y findIndex(fn)

    find devuelve el primer elemento que cumple la condición, o undefined.

    findIndex devuelve el índice de ese elemento, o -1.

### some(fn) y every(fn)

    some: ¿al menos un elemento cumple? → booleano.

    every: ¿todos cumplen? → booleano.

Ambos detienen la iteración tan pronto como se conoce el resultado.
flat(depth?) y flatMap(fn)

    flat(depth): "aplana" sub-arrays hasta la profundidad indicada (por defecto 1). Devuelve nuevo array.

```js
[1, [2, [3]]].flat(2); // [1,2,3]

    flatMap(fn): es un map() seguido de flat(1). Ideal cuando el callback devuelve un array y queremos un solo array como resultado.
```

### Encadenamiento

Debido a que estos métodos devuelven nuevos arrays (excepto forEach), se pueden encadenar para crear pipelines de procesamiento legibles:
```js
const resultado = usuarios
  .filter(u => u.activo)
  .map(u => u.nombre)
  .sort();

---

## Archivo: `04-spread-y-rest.md`

```

Se trata del operador ... usado tanto en arrays como en objetos (ya visto), pero aquí lo enfocamos en su uso con arrays y colecciones.
Spread en arrays (expansión)

Convierte los elementos de un iterable (array, string, Set, Map, etc.) en elementos individuales.
Creación de copias superficiales
```js
const original = [1,2,3];
const copia = [...original];
copia.push(4); // original sigue siendo [1,2,3]
```

Solo copia un nivel de profundidad (las referencias a objetos internos se comparten).
Combinar arrays
```js
const a = [1,2], b = [3,4];
const combinado = [...a, ...b, 5]; // [1,2,3,4,5]
```

### Insertar elementos en posición arbitraria sin splice
```js
const arr = [10, 50];
const nuevo = [0, ...arr, 100]; // [0,10,50,100]
```

### Pasar argumentos a funciones
```js
Math.max(...[1,5,3,9,2]); // 9
```

### Convertir NodeList u otros array-like a array
```js
const divs = document.querySelectorAll('div');
const arrDivs = [...divs];
```

Alternativa moderna: Array.from.
Rest en arrays (agrupación)

En desestructuración o en parámetros de función, ... recoge el resto de elementos en un array.
Destructuring rest
```js
const [primero, segundo, ...resto] = [10,20,30,40,50];
console.log(resto); // [30,40,50]
```

Debe ser el último elemento. Si no hay más elementos, resto será [].
Ignorar elementos

También se puede omitir la variable [a,,b] = [1,2,3] (a=1, b=3).
Rest en parámetros (ya visto en funciones)
```js
function sumar(...numeros) {
  return numeros.reduce((a,b) => a+b, 0);
}
```

Reemplaza a arguments.
Nota sobre rendimiento

El spread es una operación que itera el iterable completo; con grandes volúmenes puede ser costoso. Para operaciones pesadas considerar alternativas como push.apply o bucles, aunque normalmente no es un problema.