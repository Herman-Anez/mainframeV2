# Prototipos en JavaScript

JavaScript es un lenguaje basado en **prototipos**. Cada objeto tiene un enlace interno a otro objeto llamado su prototipo, del cual hereda propiedades y métodos.

## Propiedad `__proto__` y `Object.getPrototypeOf()`

*   **`__proto__`**: Es un *accessor* heredado de `Object.prototype`. Aunque está expuesto en la mayoría de los navegadores, **no se recomienda su uso en producción**.
*   **Estándar**: La forma recomendada de interactuar con el prototipo es mediante `Object.getPrototypeOf(obj)` y `Object.setPrototypeOf(obj, proto)`.

## Cadena de Prototipos

Cuando accedemos a una propiedad, el motor de JavaScript la busca primero en el propio objeto. Si no existe, sube al prototipo, y continúa así sucesivamente hasta llegar a `Object.prototype` (cuyo prototipo es `null`). Este es el mecanismo fundamental de la **herencia** en JavaScript.

```javascript
const animal = { tipo: 'desconocido' };
const perro = Object.create(animal);
perro.ladrar = function() { return 'guau'; };

console.log(perro.tipo); // 'desconocido' (heredado)
console.log(perro.ladrar()); // 'guau'
console.log(perro.toString()); // Método heredado de Object.prototype
```

## Propiedad `constructor`

Las funciones (que pueden actuar como constructores) tienen una propiedad `prototype`. Este es un objeto con una propiedad `constructor` que apunta de vuelta a la función original.

> [!NOTE]
> Cuando creamos un objeto con `new`, su prototipo se establece automáticamente al `prototype` de la función constructora.

## Herencia Prototípica Clásica

Antes de la llegada de las clases en ES6, los desarrolladores manipulaban el `prototype` manualmente para simular herencia:

```javascript
function Animal(nombre) {
  this.nombre = nombre;
}
Animal.prototype.hablar = function() {
  return '...';
};

function Perro(nombre) {
  Animal.call(this, nombre); // Llamada al "super" constructor
}

// Establecer la herencia
Perro.prototype = Object.create(Animal.prototype);
Perro.prototype.constructor = Perro;

Perro.prototype.ladrar = function() {
  return 'guau';
};
```

> [!TIP]
> Este patrón es engorroso y ha sido reemplazado mayoritariamente por la sintaxis `class`, que es "azúcar sintáctico" sobre este mismo mecanismo de prototipos.

## Impacto en el Rendimiento

Recorrer la cadena de prototipos es una operación rápida. Sin embargo:

> [!WARNING]
> Modificar el prototipo de un objeto existente con `Object.setPrototypeOf` es una operación extremadamente lenta que debe evitarse en código de alto rendimiento. Lo recomendable es establecer el prototipo al momento de crear el objeto usando `Object.create()`.
---
[back](../index)
