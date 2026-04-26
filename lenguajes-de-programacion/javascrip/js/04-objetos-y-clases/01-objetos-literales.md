# Objetos Literales

En JavaScript, un objeto es una colección de pares clave-valor. La **notación literal** es la forma más común y sencilla de crearlos.

## Sintaxis Básica

```javascript
const persona = {
  nombre: 'Carlos',
  edad: 30,
  saludar: function() {
    return `Hola, soy ${this.nombre}`;
  }
};
```

## Nombres de Propiedades

*   Pueden ser **cadenas** (con comillas si contienen espacios o caracteres especiales) o **identificadores válidos**.
*   También pueden ser **números**, que se convierten a cadena automáticamente: `{ 0: 'valor' }` es válido.
*   Desde ES6, se pueden definir **propiedades computadas** con `[]`:

```javascript
const campo = 'edad';
const obj = { [campo]: 25 };
```

## Métodos Abreviados

ES6 permite definir métodos sin la palabra clave `function`:

```javascript
const obj = {
  saludar() { 
    console.log('hola'); 
  }
};
```

## Propiedades Shorthand

Si el nombre de la variable y la propiedad coinciden, se puede omitir el valor:

```javascript
const nombre = 'Ana', edad = 28;
const user = { nombre, edad }; // Equivale a { nombre: 'Ana', edad: 28 }
```

## Prototipo

> [!NOTE]
> Todo objeto literal tiene como prototipo `Object.prototype`, del que hereda métodos como `toString()`, `hasOwnProperty()`, etc.

Puede ser modificado con `Object.create()` o `Object.setPrototypeOf()` (aunque este último está desaconsejado por motivos de rendimiento).

## Acceso a Propiedades

Existen dos formas principales de acceder a las propiedades:

*   **Notación de punto:** `objeto.propiedad`
*   **Notación de corchetes:** `objeto['propiedad']` – Útil cuando el nombre es dinámico o contiene caracteres especiales.

## Comparación

> [!IMPORTANT]
> Dos objetos literales distintos **siempre son diferentes** aunque tengan el mismo contenido, ya que se comparan por **referencia**.

```javascript
const a = { x: 1 };
const b = { x: 1 };
console.log(a === b); // false
```

## Mutabilidad

Los objetos son **mutables**: se pueden añadir, modificar o eliminar propiedades en cualquier momento.
---
[back](../index)
