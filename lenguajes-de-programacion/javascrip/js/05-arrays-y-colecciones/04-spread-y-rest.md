# Operadores Spread y Rest en Arrays

El operador de propagación (`...`) es una de las herramientas más potentes introducidas en ES6. Aunque se utiliza tanto en arrays como en objetos, aquí nos enfocaremos en su aplicación específica para colecciones.

---

## Spread Operator (Expansión)

El **Spread Operator** permite convertir un iterable (como un array, string, Set o Map) en elementos individuales.

### 1. Creación de Copias Superficiales (Shallow Copies)
Permite duplicar un array sin mantener la referencia al original.

```javascript
const original = [1, 2, 3];
const copia = [...original];

copia.push(4); 
// Resultado: copia = [1, 2, 3, 4], original = [1, 2, 3]
```

> [!CAUTION]
> Solo realiza una copia de **un nivel de profundidad**. Si el array contiene objetos u otros arrays, las referencias internas seguirán siendo las mismas.

### 2. Combinación de Arrays
Es la forma más legible de concatenar múltiples colecciones.

```javascript
const a = [1, 2];
const b = [3, 4];
const combinado = [...a, ...b, 5]; // [1, 2, 3, 4, 5]
```

### 3. Inserción en Posiciones Arbitrarias
Permite insertar elementos en cualquier punto sin recurrir a `splice()`.

```javascript
const arr = [10, 50];
const nuevo = [0, ...arr, 100]; // [0, 10, 50, 100]
```

### 4. Paso de Argumentos a Funciones
Convierte un array de valores en argumentos individuales para una función.

```javascript
const notas = [1, 5, 3, 9, 2];
Math.max(...notas); // 9
```

---

## Rest Operator (Agrupación)

El **Rest Operator** realiza la función inversa al spread: recoge múltiples elementos y los agrupa en un único array.

### 1. Desestructuración de Arrays
Permite extraer los primeros elementos y agrupar el resto.

```javascript
const [primero, segundo, ...resto] = [10, 20, 30, 40, 50];
console.log(resto); // [30, 40, 50]
```

> [!IMPORTANT]
> El parámetro rest debe ser siempre el **último elemento** en la desestructuración.

### 2. Parámetros de Función (Rest Parameters)
Permite que una función acepte un número indefinido de argumentos como un array real, reemplazando al antiguo objeto `arguments`.

```javascript
function sumar(...numeros) {
  return numeros.reduce((a, b) => a + b, 0);
}
```

---

## Consideraciones de Rendimiento

> [!NOTE]
> El operador spread itera sobre el iterable completo. En la mayoría de los casos de uso cotidiano, el impacto es insignificante. Sin embargo, para operaciones con volúmenes de datos masivos en entornos críticos, considera alternativas como `push.apply()` o bucles tradicionales si el rendimiento es un cuello de botella.

----
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
-----