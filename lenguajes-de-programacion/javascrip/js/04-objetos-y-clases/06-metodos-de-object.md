
## Archivo: `06-metodos-de-object.md`


El objeto global Object proporciona métodos estáticos muy útiles para trabajar con objetos.
Métodos de iteración y conversión

    Object.keys(obj): devuelve un array con las claves propias enumerables.

    Object.values(obj): array con los valores propios enumerables.

    Object.entries(obj): array de pares [clave, valor].

```js
const obj = { a: 1, b: 2 };
Object.entries(obj); // [['a',1], ['b',2]]
```

Estos ignoran propiedades no enumerables y las heredadas.
Métodos para control de propiedades

    Object.defineProperty(obj, prop, descriptor) y Object.defineProperties: ya vistos.

    Object.getOwnPropertyDescriptor(obj, prop): devuelve el descriptor de una propiedad propia.

    Object.getOwnPropertyNames(obj): array de todas las claves propias (incluyendo no enumerables, excluyendo Symbols).

    Object.getOwnPropertySymbols(obj): array de símbolos propios.

    Object.hasOwn(obj, prop) (ES2022): método más seguro que obj.hasOwnProperty para verificar propiedad propia.

### Protección de objetos (inmutabilidad)

    Object.preventExtensions(obj): impide añadir nuevas propiedades.

    Object.seal(obj): preventExtensions + configura configurable: false para todas las propiedades existentes (no se pueden eliminar).

    Object.freeze(obj): seal + configura writable: false (objeto completamente inmutable de forma superficial). Las subpropiedades si son objetos pueden seguir modificándose.
    Para cada uno existen sus comprobadores: Object.isExtensible, Object.isSealed, Object.isFrozen.

```js
const config = Object.freeze({ api: 'https://...' });
config.api = 'otra'; // falla silenciosamente o lanza error en estricto
```

### Creación y manipulación de prototipos

    Object.create(proto, [descriptors]): crea un nuevo objeto con el prototipo especificado.

    Object.getPrototypeOf(obj) y Object.setPrototypeOf(obj, proto).

    Object.setPrototypeOf es lento; mejor usar Object.create.

### Métodos de copia y composición

    Object.assign(target, ...sources): copia las propiedades propias enumerables de los objetos fuente al objeto destino (copia superficial). Retorna el destino. Muy usado para combinar objetos.

```js
const base = { a: 1 };
const copia = Object.assign({}, base, { b: 2 }); // { a:1, b:2 }
```

    No copia getters/setters, sino sus valores evaluados.

### De objeto a otros formatos

    Object.fromEntries(iterable): inverso de Object.entries, construye un objeto a partir de pares clave-valor.

```js
Object.fromEntries([['nombre','Juan'], ['edad',30]]); // {nombre:'Juan', edad:30}
```

    JSON.stringify y JSON.parse para serialización, aunque no son métodos de Object, son indispensables.

---
