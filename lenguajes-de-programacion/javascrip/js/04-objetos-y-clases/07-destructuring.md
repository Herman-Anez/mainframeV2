# Desestructuración (Destructuring)

La desestructuración es una expresión de JavaScript que permite extraer valores de arrays o propiedades de objetos y asignarlos a variables de forma concisa y legible.

## Desestructuración de Objetos

```javascript
const persona = { nombre: 'Elena', edad: 28, ciudad: 'Madrid' };
const { nombre, edad } = persona;

console.log(nombre); // Elena
```
``js
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
### Características principales:
*   **Alias**: Se pueden renombrar variables: `{ nombre: name, edad: age }`.
*   **Valores por defecto**: `{ pais = 'España' }` se usará si la propiedad no existe.
*   **Parámetros de función**: Muy útil para recibir objetos de configuración.
*   **Operador Rest**: Permite agrupar el resto de propiedades en un nuevo objeto: `const { nombre, ...resto } = obj;`.

## Desestructuración de Arrays

```javascript
const colores = ['rojo', 'verde', 'azul'];
const [primero, segundo] = colores;

console.log(primero); // rojo
```

*   **Omitir elementos**: Se pueden dejar espacios vacíos para saltar valores: `const [,, tercero] = colores;`.
*   **Operador Rest**: Agrupa los elementos restantes: `const [primero, ...demas] = colores;`.
*   **Intercambio de variables**:
    > [!TIP]
    > Puedes intercambiar los valores de dos variables sin necesidad de una variable temporal:
    > `[a, b] = [b, a];`

## Desestructuración Anidada

Es posible extraer valores de estructuras complejas mezclando objetos y arrays:

```javascript
const datos = { id: 1, items: ['a', 'b'] };
const { id, items: [x, y] } = datos;
console.log(x); // 'a'
```

## Casos de Uso Comunes

*   Extraer propiedades específicas de objetos de configuración.
*   Manejar múltiples valores de retorno desde una función.
*   Iterar sobre arrays de objetos usando `for...of` y `entries()`.

## Errores Comunes y Buenas Prácticas

> [!CAUTION]
> Intentar desestructurar `null` o `undefined` lanzará un `TypeError`. Siempre es recomendable proteger la operación con un valor por defecto:
> `const { prop } = obj || {};`

*   La desestructuración **siempre crea nuevas variables** y no modifica el objeto o array original.

---
### Siguiente tema: [05-arrays-y-colecciones](../05-arrays-y-colecciones/index.md)
