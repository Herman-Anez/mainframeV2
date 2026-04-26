# Propiedades y Métodos

## Propiedades

Las propiedades de un objeto asocian una clave (nombre) con un valor. Además del valor, cada propiedad tiene **atributos (descriptores)** que definen su comportamiento:

*   **`writable`**: Si el valor puede cambiarse.
*   **`enumerable`**: Si aparece en bucles `for...in` y `Object.keys()`.
*   **`configurable`**: Si la propiedad puede eliminarse o si sus descriptores pueden ser modificados.

> [!NOTE]
> Por defecto, las propiedades definidas de forma literal son `writable`, `enumerable` y `configurable`.

## Definición de Propiedades con Control Preciso

`Object.defineProperty(obj, prop, descriptor)` permite establecer estos atributos de forma explícita.

```javascript
const obj = {};
Object.defineProperty(obj, 'id', {
  value: 123,
  writable: false,
  enumerable: true,
  configurable: false
});

obj.id = 456; // No tiene efecto (o lanza error en strict mode)
```

También existe `Object.defineProperties` para definir múltiples propiedades a la vez.

## Métodos

Los métodos son funciones almacenadas como propiedades de un objeto. Pueden referirse al objeto a través de la palabra clave `this`.

> [!TIP]
> En métodos definidos con sintaxis abreviada, `this` apunta al objeto sobre el que se invoca el método.

## Getters y Setters

Se definen con las palabras clave `get` y `set`, permitiendo ejecutar lógica personalizada al leer o escribir una propiedad.

```javascript
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

## El valor de `this` en métodos

El valor de `this` depende de **cómo se invoca** la función:

*   **Llamada directa como método:** `obj.metodo()` → `this` es `obj`.
*   **Función extraída:** `const fn = obj.metodo; fn()` → `this` es el objeto global (o `undefined` en modo estricto).
*   **Arrow functions:** No tienen `this` propio; heredan el valor de `this` del contexto donde fueron creadas.

## Borrado de Propiedades

El operador `delete` elimina una propiedad del objeto. Fallará si la propiedad tiene el descriptor `configurable: false`.

```javascript
delete persona.edad;
```

## Verificación de Existencia

Existen varias formas de comprobar si una propiedad existe en un objeto:

*   **`prop in obj`**: Verifica la propiedad tanto en el objeto como en su cadena de prototipos.
*   **`obj.hasOwnProperty(prop)`**: Verifica solo las propiedades **propias** del objeto.
*   **`obj[prop] !== undefined`**: Puede fallar si la propiedad existe pero su valor es explícitamente `undefined`.

---
[back](../index)
