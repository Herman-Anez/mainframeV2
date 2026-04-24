
# Métodos Funcionales de Arrays

A diferencia de los modificadores, estos métodos **no alteran el array original** (con la excepción parcial de `forEach`). Son pilares fundamentales de la programación funcional en JavaScript, permitiendo transformaciones de datos claras y declarativas.

## Iteración: `forEach()`

Ejecuta una función de callback para cada elemento del array.

*   **Callback:** Recibe `(elemento, indice, array)`.
*   **Comportamiento:** Ignora índices vacíos.
*   **Retorno:** No devuelve nada (`undefined`). Por lo tanto, no es encadenable.

```javascript
[1, 2, 3].forEach(n => console.log(n));
```

> [!WARNING]
> No se puede detener un `forEach` con `break` o `continue`. Si necesitas interrumpir la ejecución prematuramente, utiliza un bucle `for...of` o métodos como `some()` y `every()`.

---

## Transformación: `map()`

Crea un **nuevo array** aplicando una función de transformación a cada elemento.

```javascript
const numeros = [1, 2, 3];
const dobles = numeros.map(n => n * 2); // [2, 4, 6]
```

*   **Longitud:** El nuevo array siempre tendrá la misma longitud que el original.
*   **Agujeros:** Si el array original es disperso, el nuevo mantendrá los huecos en las mismas posiciones.

---

## Filtrado: `filter()`

Crea un **nuevo array** que contiene únicamente los elementos que cumplen con una condición (aquellos para los que el callback devuelve un valor *truthy*).

```javascript
const edades = [5, 10, 3, 15];
const mayores = edades.filter(n => n > 7); // [10, 15]
```

> [!NOTE]
> Si ningún elemento cumple la condición, el método devuelve un array vacío (`[]`).

---

## Acumulación: `reduce()` y `reduceRight()`

Reducen el array a un **único valor** acumulado.

```javascript
const suma = [1, 2, 3, 4].reduce((acc, n) => acc + n, 0); // 10
```

*   **Callback:** Recibe `(acumulador, elemento, indice, array)`.
*   **Valor inicial:** Si no se proporciona, el primer elemento del array se toma como acumulador inicial y la iteración comienza desde el segundo elemento.
*   **`reduceRight()`:** Realiza la misma operación pero iterando de derecha a izquierda.

---

## Búsqueda: `find()` y `findIndex()`

*   **`find(fn)`:** Devuelve el **primer elemento** que cumpla la condición. Si ninguno coincide, retorna `undefined`.
*   **`findIndex(fn)`:** Devuelve el **índice** del primer elemento que cumpla la condición. Si ninguno coincide, retorna `-1`.

---

## Comprobación: `some()` y `every()`

*   **`some(fn)`:** Devuelve `true` si **al menos un** elemento cumple la condición.
*   **`every(fn)`:** Devuelve `true` si **todos** los elementos cumplen la condición.

> [!TIP]
> Ambos métodos utilizan **cortocircuito**: la iteración se detiene en cuanto el resultado es definitivo (el primer `true` para `some` o el primer `false` para `every`).

---

## Aplanamiento: `flat()` y `flatMap()`

*   **`flat(depth?)`:** Crea un nuevo array aplanando sub-arrays hasta la profundidad indicada (por defecto 1).
*   **`flatMap(fn)`:** Combina un `map()` seguido de un `flat(1)`. Es ideal cuando el callback devuelve un array y queremos un resultado unidimensional.

```javascript
[1, [2, [3]]].flat(2); // [1, 2, 3]
```

---

## Encadenamiento (Pipelines)

Dado que la mayoría de estos métodos devuelven arrays nuevos, es posible crear flujos de procesamiento muy potentes y legibles:

```javascript
const resultado = usuarios
  .filter(u => u.activo)
  .map(u => u.nombre)
  .sort();
```
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