# Proxy y Reflect

JavaScript proporciona dos herramientas extremadamente potentes para la metaprogramación: **Proxy**, que permite interceptar operaciones, y **Reflect**, que permite ejecutarlas de forma controlada.

---

## Proxy

Un objeto `Proxy` permite envolver otro objeto (o función) e interceptar sus operaciones fundamentales, como la lectura/escritura de propiedades, la eliminación o incluso la invocación.

Se crea mediante: `new Proxy(target, handler)`

```js
const persona = { nombre: 'Ana', edad: 28 };

const manejador = {
  get(target, prop) {
    if (prop === 'edad') return `${target.edad} años`;
    return Reflect.get(target, prop);
  },
  set(target, prop, valor) {
    if (prop === 'edad' && valor < 0) {
      throw new Error('La edad no puede ser negativa');
    }
    target[prop] = valor;
    return true; // Indica que la asignación fue exitosa
  }
};

const proxy = new Proxy(persona, manejador);
console.log(proxy.edad); // "28 años"
proxy.edad = -5;         // Lanza Error
```

### Trampas (*Traps*) disponibles
Las "trampas" son los métodos del manejador que interceptan las operaciones:
- `get` / `set`: Lectura y escritura.
- `has`: Intercepta el operador `in`.
- `deleteProperty`: Intercepta `delete`.
- `apply`: Intercepta la llamada a una función.
- `construct`: Intercepta el uso de `new`.

---

## Reflect

Es un objeto incorporado que proporciona métodos estáticos para las mismas operaciones internas que intercepta un Proxy. Su propósito es facilitar la invocación del comportamiento predeterminado del lenguaje.

> [!TIP]
> Dentro de un Proxy, se recomienda usar siempre `Reflect` para realizar la operación original. Esto asegura que se respeten comportamientos complejos como la cadena de prototipos y el contexto de `this` (`receiver`).

```js
const manejador = {
  get(target, prop, receiver) {
    console.log(`Accediendo a: ${prop}`);
    return Reflect.get(target, prop, receiver);
  }
};
```

---

## Casos de uso comunes

1. **Validación de datos:** Asegurar que las propiedades de un objeto cumplan ciertos criterios antes de guardarlas.
2. **Reactividad:** Seguimiento automático de cambios en objetos (base de frameworks como **Vue 3**).
3. **Logging y Profiling:** Observar qué partes de un objeto se utilizan y con qué frecuencia.
4. **Valores por defecto:** Crear objetos que devuelven un valor predefinido en lugar de `undefined` para claves inexistentes.
5. **APIs de Solo Lectura:** Crear proxies que lancen errores al intentar modificar cualquier propiedad.

---

## Limitaciones y Precauciones

> [!WARNING]
> **Rendimiento:** El uso de Proxies añade una capa de indirección que es ligeramente más lenta que el acceso directo. Úsalos con sabiduría en secciones críticas de rendimiento.

> [!IMPORTANT]
> **Identidad:** Un Proxy es un objeto distinto al original (`proxy !== target`). Esto puede causar problemas si tu código depende de comparaciones de identidad o de referencias directas.

- **Polifills:** Los Proxies **no pueden** ser polifillados para navegadores antiguos de forma completa, ya que requieren soporte profundo a nivel de motor de JavaScript.
- **Transparencia:** Algunos objetos internos (como `Map`, `Set` o fechas) pueden fallar al ser envueltos en un Proxy si no se gestionan correctamente los enlaces internos (*internal slots*).

---
[back](../index)
