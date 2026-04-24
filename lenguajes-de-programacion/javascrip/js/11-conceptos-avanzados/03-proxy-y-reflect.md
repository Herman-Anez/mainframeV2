
## Archivo: `03-proxy-y-reflect.md`

Proxy

Permite interceptar y redefinir operaciones fundamentales sobre un objeto (get, set, delete, has, enumerate, construct, apply...). Se crea con new Proxy(target, handler).
```js
const persona = { nombre: 'Ana', edad: 28 };
const manejador = {
  get(target, prop) {
    if (prop === 'edad') return `${target.edad} años`;
    return Reflect.get(target, prop);
  },
  set(target, prop, valor) {
    if (prop === 'edad' && valor < 0) throw new Error('Edad no válida');
    target[prop] = valor;
    return true;
  }
};
const proxy = new Proxy(persona, manejador);
console.log(proxy.edad); // '28 años'
proxy.edad = -5; // lanza Error
```

### Métodos interceptables (trampas)

    get, set, deleteProperty, has (operador in), ownKeys, getOwnPropertyDescriptor, defineProperty, preventExtensions, isExtensible, apply (para funciones), construct (para new).

### Casos de uso

    Validación y saneamiento de datos.

    PropTypes en tiempo de ejecución.

    Observadores reactivos: frameworks como Vue 3 utilizan Proxy para la reactividad.

    Logging y profiling.

    APIs de objetos negativos (ej. valores por defecto: const cero = new Proxy({}, { get: (t,p) => p in t ? t[p] : 0 })).

    Virtualización de objetos (simular propiedades que no existen realmente).

### Reflect

Objeto incorporado con métodos estáticos que replican las operaciones internas del lenguaje (las mismas trampas de Proxy). Su propósito es normalizar la manipulación de objetos y proporcionar una forma segura de invocar la operación predeterminada dentro de un proxy.

    Reflect.get(obj, prop, receiver?) en lugar de obj[prop].

    Reflect.set(...), Reflect.deleteProperty, Reflect.apply, etc.

Dentro de un proxy, en lugar de target[prop] se recomienda Reflect.get(target, prop, receiver) para respetar la cadena de prototipos y posibles proxies anidados.
Relación Proxy y Reflect

Han sido diseñados para trabajar juntos; cada trampa de Proxy tiene un método correspondiente en Reflect que ejecuta el comportamiento por defecto.
```js
const manejador = {
  set(target, prop, value, receiver) {
    // alguna validación
    return Reflect.set(target, prop, value, receiver);
  }
};
```

### Precauciones

    Los proxies no son totalmente transparentes: proxy !== target, typeof, comparaciones pueden fallar.

    El rendimiento de proxies es inferior al acceso directo (aunque para la mayoría de aplicaciones es aceptable).

    No se pueden polifillar; requieren soporte nativo ES6.

---
