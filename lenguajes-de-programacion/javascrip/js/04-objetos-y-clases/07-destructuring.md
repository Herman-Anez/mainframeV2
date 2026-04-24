## Archivo: `07-destructuring.md`


La desestructuración (destructuring) permite extraer valores de arrays u objetos y asignarlos a variables de forma concisa.
Desestructuración de objetos
```js
const persona = { nombre: 'Elena', edad: 28, ciudad: 'Madrid' };
const { nombre, edad } = persona;
console.log(nombre); // Elena
```

    Los nombres de las variables deben coincidir con las claves.

    Se pueden usar alias: { nombre: name, edad: age }.

    Se pueden asignar valores por defecto: { pais = 'España' }.

    También se puede extraer en parámetros de función:

```js
function presentar({ nombre, edad }) {
  return `${nombre} tiene ${edad} años`;
}
```

    Se puede anidar:

```js
const usuario = { datos: { email: 'a@b.com' } };
const { datos: { email } } = usuario;

    Se puede combinar con el operador rest para agrupar el resto de propiedades: const { nombre, ...resto } = obj;.
```

### Desestructuración de arrays
```js
const colores = ['rojo', 'verde', 'azul'];
const [primero, segundo] = colores;
console.log(primero); // rojo

    Se pueden omitir elementos con comas: const [,, tercero] = colores;.

    Rest en arrays: const [primero, ...demas] = colores;.

    Valores por defecto: const [a = 10] = [].

    Intercambio de variables: [a, b] = [b, a];.
```

### Casos de uso comunes

    Extraer propiedades de objetos de configuración.

    Múltiples valores de retorno emulados con arrays u objetos.

    Iteración con for...of y entries(): for (const [indice, valor] of arr.entries()).

### Desestructuración anidada y compleja

Se pueden mezclar objetos y arrays en una misma sentencia:
```js
const datos = { id: 1, items: ['a', 'b'] };
const { id, items: [x, y] } = datos;
console.log(x); // 'a'
```

### Errores comunes

    Intentar desestructurar null o undefined lanza TypeError; se puede proteger con valor por defecto: const { prop } = obj || {};.

    La desestructuración siempre crea nuevas variables, no modifica el original.

### 05-arrays-y-colecciones
---
