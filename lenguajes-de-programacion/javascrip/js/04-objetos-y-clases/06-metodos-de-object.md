# Métodos Estáticos de Object

El objeto global `Object` proporciona una amplia gama de métodos estáticos esenciales para manipular, proteger e inspeccionar objetos.

## Iteración y Conversión

Estos métodos permiten transformar objetos en arrays para facilitar su iteración:

*   **`Object.keys(obj)`**: Devuelve un array con las claves propias enumerables.
*   **`Object.values(obj)`**: Devuelve un array con los valores propios enumerables.
*   **`Object.entries(obj)`**: Devuelve un array de pares `[clave, valor]`.

```javascript
const obj = { a: 1, b: 2 };
Object.entries(obj); // [['a', 1], ['b', 2]]
```

> [!NOTE]
> Estos métodos ignoran las propiedades no enumerables y aquellas heredadas a través de la cadena de prototipos.

## Control de Propiedades

*   **`Object.getOwnPropertyDescriptor(obj, prop)`**: Devuelve los atributos (descriptores) de una propiedad específica.
*   **`Object.getOwnPropertyNames(obj)`**: Devuelve un array con todas las claves (incluyendo las no enumerables).
*   **`Object.hasOwn(obj, prop)`**: (ES2022) Forma segura y moderna de verificar si una propiedad es propia del objeto.

## Protección de Objetos (Inmutabilidad)

JavaScript ofrece tres niveles de protección para objetos:

1.  **`Object.preventExtensions(obj)`**: Impide añadir nuevas propiedades.
2.  **`Object.seal(obj)`**: Impide añadir/eliminar propiedades, pero permite modificar los valores de las existentes.
3.  **`Object.freeze(obj)`**: Hace que el objeto sea completamente inmutable (superficialmente).

```javascript
const config = Object.freeze({ api: 'https://api.com' });
config.api = 'otra'; // Fallará (en modo estricto lanza error)
```

> [!WARNING]
> La protección es **superficial**. Si una propiedad es a su vez un objeto, sus propiedades internas aún podrán ser modificadas a menos que también se congelen recursivamente.

## Manipulación de Prototipos

*   **`Object.create(proto)`**: Crea un nuevo objeto utilizando el objeto proporcionado como prototipo.
*   **`Object.getPrototypeOf(obj)`**: Obtiene el prototipo de un objeto.
*   **`Object.setPrototypeOf(obj, proto)`**: Cambia el prototipo (operación costosa en rendimiento).

## Copia y Composición

*   **`Object.assign(target, ...sources)`**: Copia las propiedades de uno o más objetos fuente a un objeto destino.

```javascript
const base = { a: 1 };
const extendido = Object.assign({}, base, { b: 2 }); // { a: 1, b: 2 }
```

> [!TIP]
> `Object.assign` realiza una **copia superficial**. Para copias profundas, se deben utilizar otros mecanismos como `structuredClone()`.

## Conversión a otros Formatos

*   **`Object.fromEntries(iterable)`**: El inverso de `entries()`. Crea un objeto a partir de una lista de pares clave-valor.
*   **`JSON.stringify()` / `JSON.parse()`**: Aunque pertenecen al objeto `JSON`, son herramientas fundamentales para la serialización de objetos.
```js
Object.fromEntries([['nombre','Juan'], ['edad',30]]); // {nombre:'Juan', edad:30}
```

    JSON.stringify y JSON.parse para serialización, aunque no son métodos de Object, son indispensables.

---
---
[back](../index)
