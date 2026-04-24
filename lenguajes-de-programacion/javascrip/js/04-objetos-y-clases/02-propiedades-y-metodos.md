
## Archivo: `02-propiedades-y-metodos.md`

Propiedades

Las propiedades de un objeto asocian una clave (nombre) con un valor. Además del valor, cada propiedad tiene atributos (descriptores):

    writable: si el valor puede cambiarse.

    enumerable: si aparece en bucles for...in y Object.keys().

    configurable: si la propiedad puede eliminarse o cambiar sus descriptores.

Por defecto, las propiedades definidas de forma literal son writable, enumerable y configurable.
Definición de propiedades con control preciso

Object.defineProperty(obj, prop, descriptor) permite establecer esos atributos.
```js
const obj = {};
Object.defineProperty(obj, 'id', {
  value: 123,
  writable: false,
  enumerable: true,
  configurable: false
});
obj.id = 456; // no tiene efecto (o lanza error en strict mode)
```

Object.defineProperties para múltiples propiedades.
Métodos

Son funciones almacenadas como propiedades del objeto. Pueden referirse al objeto a través de this. En métodos definidos con sintaxis abreviada, this apunta al objeto sobre el que se invoca el método.
Getters y Setters

Se definen con las palabras clave get y set, permitiendo ejecutar lógica al leer o escribir una propiedad.
```js
const persona = {
  nombre: 'Juan',
  apellido: 'Perez',
  get nombreCompleto() {
    return `${this.nombre} ${this.apellido}`;
  },
  set nombreCompleto(val) {
    const partes = val.split(' ');
    this.nombre = partes[0];
    this.apellido = partes[1];
  }
};
console.log(persona.nombreCompleto); // Juan Perez
persona.nombreCompleto = 'Ana Lopez';
console.log(persona.nombre); // Ana
```

### Método this en métodos

El valor de this depende de cómo se invoca la función:

    Llamada directa como método: obj.metodo() → this es obj.

    Función extraída: const fn = obj.metodo; fn() → this es objeto global (o undefined en estricto).

    Arrow functions: no tienen this propio, heredan el del contexto.

### Borrado de propiedades

El operador delete elimina la propiedad del objeto. Fallará si la propiedad es no configurable.
Verificación de existencia

    prop in obj (verifica cadena de prototipos).

    obj.hasOwnProperty(prop) (solo propiedades propias).

    obj[prop] !== undefined (puede fallar si el valor es undefined).

---
