## Archivo: `01-objetos-literales.md`


En js, un objeto es una colección de pares clave-valor. La notación literal es la forma más común de crearlos.
Sintaxis básica
```js
const persona = {
  nombre: 'Carlos',
  edad: 30,
  saludar: function() {
    return `Hola, soy ${this.nombre}`;
  }
};
```

### Nombres de propiedades

    Pueden ser cadenas (con comillas si contienen espacios o caracteres especiales) o identificadores válidos.

    También pueden ser números, que se convierten a cadena automáticamente: { 0: 'valor' } es válido.

    Desde ES6, se pueden definir propiedades computadas con []:

```js
const campo = 'edad';
const obj = { [campo]: 25 };
```

### Métodos abreviados

ES6 permite definir métodos sin la palabra clave function:
```js
const obj = {
  saludar() { console.log('hola'); }
};
```

### Propiedades shorthand

Si el nombre de la variable y la propiedad coinciden, se omite el valor:
```js
const nombre = 'Ana', edad = 28;
const user = { nombre, edad }; // { nombre: 'Ana', edad: 28 }
```

### Prototipo

Todo objeto literal tiene como prototipo Object.prototype, del que hereda métodos como toString(), hasOwnProperty(), etc. Puede ser modificado con Object.create() o Object.setPrototypeOf() (desaconsejado por rendimiento).
Acceso a propiedades

### Notación punto: objeto.propiedad

    Notación corchetes: objeto['propiedad'] – útil cuando el nombre es dinámico o contiene caracteres especiales.

### Comparación

Dos objetos literales distintos siempre son diferentes aunque tengan el mismo contenido, porque se comparan por referencia.
```js
const a = {x:1};
const b = {x:1};
console.log(a === b); // false
```

### Mutabilidad

Los objetos son mutables: se pueden añadir, modificar o eliminar propiedades en cualquier momento.