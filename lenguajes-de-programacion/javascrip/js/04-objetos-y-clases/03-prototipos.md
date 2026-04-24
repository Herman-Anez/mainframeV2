## Archivo: `03-prototipos.md`


js es un lenguaje basado en prototipos. Cada objeto tiene un enlace interno a otro objeto llamado su prototipo, y de él hereda propiedades.
Propiedad __proto__ y Object.getPrototypeOf()

    __proto__ es un accessor heredado de Object.prototype (no recomendado en producción, pero expuesto en la mayoría de navegadores).

    La forma estándar es Object.getPrototypeOf(obj) y Object.setPrototypeOf(obj, proto).

### Cadena de prototipos

Cuando accedemos a una propiedad, el motor la busca primero en el propio objeto. Si no existe, sube al prototipo, y así sucesivamente hasta llegar a Object.prototype (cuyo prototipo es null). Este es el mecanismo de herencia en js.
```js
const animal = { tipo: 'desconocido' };
const perro = Object.create(animal);
perro.ladrar = function() { return 'guau'; };
console.log(perro.tipo); // 'desconocido' (heredado)
console.log(perro.ladrar()); // 'guau'
console.log(perro.toString()); // método heredado de Object.prototype
```

### Propiedad constructor

Las funciones (que pueden actuar como constructor) tienen una propiedad prototype que es un objeto con una propiedad constructor que apunta de vuelta a la función. Cuando creamos un objeto con new, su prototipo se establece a ese prototype. Así, los objetos creados con new Func() heredan métodos definidos en Func.prototype.
Herencia prototípica clásica (antes de clases)

Los desarrolladores manipulaban prototype para simular herencia:
```js
function Animal(nombre) { this.nombre = nombre; }
Animal.prototype.hablar = function() { return '...'; };

function Perro(nombre) { Animal.call(this, nombre); }
Perro.prototype = Object.create(Animal.prototype);
Perro.prototype.constructor = Perro;
Perro.prototype.ladrar = function() { return 'guau'; };
```

Este patrón es engorroso y fue reemplazado por la sintaxis class (azúcar sintáctico sobre prototipos).
Impacto en el rendimiento

Recorrer la cadena de prototipos es rápido, pero modificar __proto__ o Object.setPrototypeOf es una operación lenta que debe evitarse en código de alto rendimiento. Lo recomendable es establecer el prototipo al crear el objeto con Object.create().